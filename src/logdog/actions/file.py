"""file action

Filename: file.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

Functions:
    file(str, str, str): Send mail according to given arguments

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

import logdog.config as config
import logdog.strings as strings


def file(detailed_information: str, brief_information: str, stdout: str):
  """Sends a mail according to the `config`

  Args:
      detailed_information (str): used as message text of the mail
      brief_information (str): used as subject of the mail
      stdout (str): may be included in the mail (keyword $STDOUT)
  """

  action_data = config.get_action_data(file.__name__)

  print("Writing into file...")

  with open(action_data["path"], "a") as f:
    f.write(
        strings.parse_string(action_data["format"],
                             detailed_information=detailed_information,
                             brief_information=brief_information,
                             stdout=stdout))
