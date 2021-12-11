"""Spawn and surveil handler processes

Filename: handlers.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

Functions:
    handle_event(str, str, str, str, str): run actions for an event
    handle_exit(*args): handle exit signals
    handle_exception(str): handles an exception
    monitor_handlers(): serveil handler subprocesses
    spawn_handlers(): spawn handler subprocesses

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

import re
import subprocess as sp
import multiprocessing as mp
import sys
import time

import logdog.actions_ as actions
import logdog.config as config
import logdog.strings as strings

__processes = []  # Running watchers
__output_lock = mp.Lock()  # Lock for stdout/stderr


def handle_event(handler_name: str,
                 event_name: str,
                 brief_information: str = "",
                 detailed_information: str = "",
                 stdout: str = ""):
  """Runs actions for an event discovered by a handler

  A handler discovers an event. The handler provides brief and
  detailed event information, which is processed by the respective
  actions defined in the config file.

  Args:
      handler_name (str): the handler that discovers an event
      event (str): the discovered event
      brief_information (str, optional): brief event information.
          Defaults to "".
      detailed_information (str, optional): detailed event information.
          Defaults to "".
      stdout (str, optional): additional data from stdout.
          Defaults to "".
  """

  actions_to_perform = []
  try:
    # Look for specific actions
    actions_to_perform = config.get_event_data(handler_name,
                                               event_name)["actions"]
  except KeyError:
    try:
      # Use default actions if no specific actions exists
      actions_to_perform = config.get_default_action_names()
    except:
      # Event: No action defined -> inform user

      # Look for event "no_handler" of internal handler "logdog" to prevent
      # infinite recursion
      if handler_name == "logdog" and event_name == "no_handler":
        sys.stderr.write(
            f"No specific or default action for event {event_name} of handler {handler_name}. Cannot inform user.\n"
        )
        return

      sys.stderr.write(
          f"No specific or default action for event {event_name} of handler {handler_name}\n"
      )
      handle_event(
          "logdog",
          "no_handler",
          brief_information=f"Logdog: {handler_name}:{event_name} - no action",
          detailed_information=
          f"No specific or default action for event {event_name} of handler {handler_name}"
      ),
      return

  # Run defined actions of event
  for a in actions_to_perform:
    if actions.check_action_existence(a):
      __output_lock.acquire()
      try:
        actions.run_action(
            a,
            detailed_information,
            brief_information,
            stdout,
        )
      except Exception as e:
        __output_lock.release()
        s = handle_exception()
        handle_event("logdog", "action_failed", f"Action {a} failed",
                     f"Action {a} produced the following exception:\n{s}")
      else:
        __output_lock.release()


def handle_exit(*args):
  """Inform user if logdog exits

  If this functions gets called from `signal.signal()` the arguments
  are:
      signum (int): Number of the handled signal
      frame: a stack frame
  """

  handle_event("logdog",
               "handle_exit",
               detailed_information="",
               brief_information="Logdog exited")
  for p in __processes:
    p.kill()


def handle_exception(s: str = "") -> str:
  """Handle an exception of the logdog module itself

  Mainly used if no event handling is possible.

  Args:
      s (str, optional): information about the exception.
          Defaults to "".

  Returns:
      str: An error string for further processing
  """

  # Gather exception information
  exception_type, exception_object, exception_traceback = sys.exc_info()
  filename = exception_traceback.tb_frame.f_code.co_filename
  line_number = exception_traceback.tb_lineno

  # Output and return information
  s = f"Error in {filename}:{line_number} - {exception_type} - {exception_object}\n{s}\n"
  sys.stderr.write(s)
  return s


def __handler(handler_name: str):
  """Runs the watcher for `handler_name` to discover and process events

  Runs a watcher for a handler. Events that are disccovered from
  `stdout` of the watcher are getting processed.

  This is the main entrypoint for the spawning handler processes. For
  each handler this function gets called exactly once.

  Args:
      handler_name (str): the handler a watcher should be spawned for
  """

  # Initializations
  handler_data = config.get_handler_data(handler_name)
  events = []  # Events the handler handles
  history = []  # Recent output of stdout of the watcher
  max_prev_lines = 0  # Highest number of watcher output to store for all events

  # Initialize the events the handler should handle
  for e in handler_data["events"]:
    if handler_data["events"][e]["active"]:
      # Get next and previous lines to output for event `e`
      try:
        num_prev_lines = handler_data["events"][e]["prev_lines"]
      except KeyError:
        num_prev_lines = 0
      try:
        num_next_lines = handler_data["events"][e]["next_lines"]
      except KeyError:
        num_next_lines = 0

      # Add event to event list
      events.append((
          e,
          re.compile(handler_data["events"][e]["regexp"], re.IGNORECASE),
          num_prev_lines,
          num_next_lines,
      ))

    # Update max_prev_lines if necessary
    if num_prev_lines > max_prev_lines:
      max_prev_lines = num_prev_lines

  # Process command and cwd of watcher to run watcher (cwd: current working directory)
  try:
    # Get specific command for watcher
    watcher_data = config.get_watcher_data(handler_data["watcher"])
  except KeyError:
    # Use default command if nothing is specified for handler
    try:
      watcher_data = config.get_default_watcher_data()
    except KeyError as e:
      handle_exception(
          f"Please add section 'logdog' -> 'default_watcher' to the config file"
      )
  command = watcher_data["command"]
  try:
    cwd = watcher_data["cwd"]
  except KeyError:
    cwd = "./"

  # Parse command string and replace '$FILE' / '${FILE}' with given logfile of handler
  for i in range(len(command)):
    if command[i] == "$FILE" or command[i] == "${{FILE}}":
      command[i] = handler_data["file"]

  # Run watcher
  f = sp.Popen(command, cwd=cwd, stdout=sp.PIPE)

  # Event: Watcher has successfully started -> inform user
  handle_event(
      "logdog",
      "watcher_started",
      detailed_information=
      f"Watcher {command[0]} of handler {handler_name} started successfully\ncwd: {cwd}",
      brief_information=
      f"Watcher {handler_name}:{command[0]} started successfully")

  # Wait for events to occur
  current_line = 0  # Number of current line in history
  while True:
    # Get new line from log, only if all previous lines have been processed
    if current_line == len(history):
      # Check if handler is still alive
      if f.poll():
        return
      history.append(f.stdout.readline().decode("UTF-8").strip())

    # Check if an event has occurred
    for p in events:
      if p[1].search(history[current_line]):
        # Check if handler is still alive
        if f.poll():
          return

        # Append necessary number of next lines
        [
            history.append(f.stdout.readline().decode("UTF-8").strip())
            for _ in range(p[3])
        ]
        print(f"{handler_name} - {p[0]}: {history[current_line]}")

        # Print num_prev_lines + num_next_lines + 1 (current_line) lines
        handle_event(
            handler_name,
            p[0],
            brief_information=config.get_event_data(handler_name,
                                                    p[0])["brief_information"],
            detailed_information=config.get_event_data(
                handler_name, p[0])["detailed_information"],
            stdout=strings.list_to_string(history[(-p[2] - p[3] - 1):],
                                          "\n\n"),
        )

    if current_line >= max_prev_lines:
      # Cleanup history
      history.pop(0)
    else:
      # Build up history
      current_line += 1


def monitor_handlers():
  """Check if handlers are still alive and spawn event if not
  """

  while True:
    for p in __processes:
      if not p.is_alive():
        handle_event("logdog",
                     "worker_died",
                     detailed_information=f"{p.name} died",
                     brief_information="Logdog: worker died")
        __processes.remove(p)
        # TODO: add restart (for a defined number of retries) (maybe in action?)
      time.sleep(1)


def spawn_handlers():
  """Spawning one subprocess per handler defined in the config file
  """

  # Spawn a subprocess for each handler this is no internal one
  for handler in config.get_handler_names():
    __processes.append(
        mp.Process(target=__handler,
                   args=(handler, ),
                   name=f"Worker: {handler}"))
    __processes[-1].start()
