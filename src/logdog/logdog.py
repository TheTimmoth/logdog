"""Look for and handle events occuring in logfiles

Filename: logdog.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

This file contains `logdog`, a daemon that can spawn handlers to detect
events in the `stdout` output of watcher processes like `tail`.

Functions:
    logdog(str): the logdog daemon

Used terms:
    Handler: represents one watcher that is looking for events
    Watcher: process whose stdout is scanned for events
    Event: 1) A pattern that is discovered in stdout of a watcher
           2) An event that occurred in logdog itself

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

import atexit
import signal

import logdog.actions_ as actions
import logdog.config as config
import logdog.handlers as handlers
import logdog.strings as strings


def logdog(config_file: str):
  """The logdog: an event handling daemon mainly designed for logfiles

  The configuration is obtained from a config file. Please look at the
  `readme`_ file and the `example config`_ for further information on
  how to provide the correct settings.

  Args:
      config_file (str): The config file to configure the logdog daemon

  Raises:
      FileNotFoundError: if `config_file` does not exist
      JSONDecodeError: if content of `config_file` has wrong format

  .. _readme:
     https://github.com/TheTimmoth/logdog/blob/main/README.md

  .. _example config:
     https://example.com

  """

  # Handle termination signals
  # If a termination signal is received, call exit()
  # This ensures that atexit is executed
  try:
    signal.signal(signal.SIGHUP, lambda *args: exit(0))  # Signal: 1
    signal.signal(signal.SIGINT, lambda *args: exit(0))  # Signal: 2
    signal.signal(signal.SIGTERM, lambda *args: exit(0))  # Signal: 15
    no_exit_notify = False
  except Exception as e:
    # Signal registering failed
    handlers.handle_exception("Warning: there may be no exit notify")
    no_exit_notify = True

  # Parse config and discover actions
  try:
    config.parse_config(config_file)
    actions.discover_actions()
  except Exception as e:
    # Fatal error occurred -> no action handling possible
    handlers.handle_exception("Error: Watchdog cannot be executed")
    exit(0)

  # At this point internal events can be processed

  if no_exit_notify:
    # Event "no_exit_notify" -> inform user
    handlers.handle_event(
      "logdog",
      "no_exit_notify",
      brief_information="Logdog: warning - maybe no exit notify")

  # Spawn and monitor the handlers
  try:
    atexit.register(handlers.handle_exit)

    handlers.spawn_handlers()
    handlers.monitor_handlers()
  except Exception as e:
    # Uncovered exception occurred

    try:
      handlers.handle_event("watchdog",
                            "exception",
                            brief_information="Logdog: an error occurred",
                            detailed_information=handlers.handle_exception())
    except Exception as e:
      handlers.handle_exception()

    handlers.handle_exit(e)
