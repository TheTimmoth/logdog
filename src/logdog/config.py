"""Load the config file and get config data

Filename: config.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

Initialize configuration and extract information.
Please look at the `configuration file reference`_ for further details
of the configuration file.

Functions:
    parse_config(str): Set up the configuration
    get_handler_names() -> list: get names of handlers
    get_handler_data(str) -> dict: get data for a handler
    get_action_names() -> list: get action names for handler
    get_action_data(str) -> dict: get data for action of handler
    get_event_names(str, str) -> list: get event names for action of
        handler
    get_event_data(str, str, str) -> dict: get data for event for
        action of handler
    get_default_action_names() -> list: get names of the default
        actions
    get_default_handler() -> dict: get default handler data
    get_default_event() -> dict: get default action data
    get_watcher_names() -> list: get watcher names
    get_watcher_data(str) -> dict: get data for a watcher

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE

.. _configuration file reference:
   https://example.com (TODO)
"""

import json

import logdog.handlers as handlers

__config = {}  # Config data

debug = False

def parse_config(config_file: str):
  """Set up the configuration

  Raises:
      FileNotFoundError: if `config_file` does not exist
      JSONDecodeError: if content of `config_file` has wrong format
  """

  global __config
  global debug

  with open(config_file, "r") as f:
    __config = json.load(f)

  try:
    debug = __config["logdog"]["debug"]
  except KeyError as e:
    pass

def get_handler_names() -> list:
  """Get the names of handlers

  Returns:
      list: a list of the handler names

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return list(__config["handlers"].keys())


def get_handler_data(handler: str) -> dict:
  """Get the config data for `handler`

  Args:
      handler (str): the `handler`

  Returns:
      dict: The data for the `handler`

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return __config["handlers"][handler]


def get_event_names(handler: str) -> list:
  """Get the names of events for handler

  Returns:
      list: a list of the events for handler

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return list(__config["handlers"][handler]["events"].keys())


def get_event_data(handler: str, event: str) -> dict:
  """Get the config data for `event` of `handler`

  Args:
      handler (str): the `handler`
      event (str): the `event`

  Returns:
      dict: The data for the `handler`

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return __config["handlers"][handler]["events"][event]


def get_action_names() -> list:
  """Get the names of actions for `event` of `handler`

  Args:
      handler (str): the `handler`
      event (str): the `event`

  Returns:
      list: The data for the `handler`

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return list(__config["actions"].keys())


def get_action_data(action: str) -> dict:
  """Get the config data for `action` of `event` of `handler`

  Args:
      action (str): the `action`

  Returns:
      dict: The data for the `handler`

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return __config["actions"][action]


def get_default_watcher_data() -> dict:
  """Get the config of the default handler

  Returns:
      dict: The data for the default handler

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return __config["logdog"]["default_watcher"]


def get_default_action_names() -> list:
  """Get the names of the default actions

  Returns:
      list: The names of the default actions

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return list(__config["logdog"]["default_actions"])


def get_watcher_names() -> list:
  """Get the names of watchers

  Returns:
      list: The names of the watchers

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return list(__config["watchers"].keys())


def get_watcher_data(watcher: str) -> dict:
  """Get the config data of `watcher`

  Returns:
      dict: The data for the default action

  Raises:
      KeyError: if config file violates `reference`_

  .. _reference:
     https://example.com (TODO)
  """

  return __config["watchers"][watcher]
