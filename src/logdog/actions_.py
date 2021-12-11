"""Discover actions from package actions

Filename: actions.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

Functions:
    discover_actions(): get all callable action names
    check_action_existence(str): check if action is callable
    run_action(str, *args): run action

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

import re

import logdog.actions as actions

__action_names = []  # Names of actions


def discover_actions():
  """Dynamically discovers callable actions from actions module

  These actions can be used by the handlers to handle events
  """

  global __action_names

  # Get actions
  p = re.compile("__")
  for a in dir(actions):
    if not p.search(a):
      __action_names.append(a)


def check_action_existence(action: str) -> bool:
  """Check if an action is a valid callable module

  Args:
      action (str): the name of the action to check

  Returns:
      bool: `True` if action exitsts, `False` otherwise
  """

  return (True if action in __action_names else False)


def run_action(action: str, *args):
  """Runs action with arguments `*args`

  Args:
      action (str): name of the action
      *args: paramters that are passed to the action
  """

  getattr(actions, action)(*args)
