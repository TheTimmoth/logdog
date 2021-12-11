"""log2mail action

Filename: log2mail.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

Functions:
    log2mail(str, str, str): Send mail according to given arguments

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

import sys

from log2mail import log2mail as l2m

import logdog.config as config
import logdog.strings as strings


def log2mail(detailed_information: str, brief_information: str, stdout: str):
  """Sends a mail according to the `config`

  Args:
      detailed_information (str): used as message text of the mail
      brief_information (str): used as subject of the mail
      stdout (str): may be included in the mail (keyword $STDOUT)
  """

  action_data = config.get_action_data(log2mail.__name__)

  print("Sending mail...")

  l2m(
      strings.parse_string(action_data["config"], detailed_information,
                           brief_information, stdout),
      strings.parse_string(action_data["subject"], detailed_information,
                           brief_information, stdout),
      strings.parse_string(action_data["message"], detailed_information,
                           brief_information, stdout),
      strings.parse_string(action_data["from"], detailed_information,
                           brief_information, stdout),
      strings.parse_string(action_data["to"], detailed_information,
                           brief_information, stdout),
  )
