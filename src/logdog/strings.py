"""Parse strings and replace keywords

Filename: parsing.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

Functions:
    parse_string(str, str, str) -> str: Replaces keywords in a string
        with more useful information

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

import re
import subprocess as sp

# Supported keywords for parsing. Each keyword is a 2-tuple.
# The first element denotes the keyword as used in a string
# The second element denotes the keyword as regular expression
__keywords = [("hostname", "hostname"),
              ("detailed_information", "detailed\\_information"),
              ("brief_information", "brief\\_information"),
              ("stdout", "stdout")]


def parse_string(s: str,
                 detailed_information: str = "",
                 brief_information: str = "",
                 stdout: str = "") -> str:
  """Replaces keywords in `s`with more useful information

  Any occurrance of a keyword in `s` is replaced with information.
  A keyword can be provided with $KEYWORD or ${KEYWORD}. The second
  style is provided to give an option to definitely separate keywords
  from each other if necessary.

  Valid keywords:
      $HOSTNAME: the hostname of the system
      $DETAILED_INFORMATION: some detailed information
      $BRIEF_INFORMATION: some brief information
      $STDOUT: the output of the watcher (which contains the event)

  Please note that the `detailed_information` or `brief_information` strings gets also parsed for keywords.

  Example:
      handler: "Test string $HOSTNAME" gets converted to
          "Test string machine.example.com"

  Args:
      s (str): string to search for keywords
      detailed_information (str, optional): string that replaces
          keyword detailed_information. Defaults to "".
      brief_information (str, optional): string that replaces keyword
          brief_information. Defaults to "".

  Returns:
      str: the processed string
  """

  # Parse detailed_information for keywords
  # (The detailed_information keyword is not supported)
  if detailed_information:
    detailed_information = parse_string(detailed_information,
                                        brief_information=brief_information,
                                        stdout=stdout)

  # Parse brief_information for keywords
  # (The keywords brief_information, detailed_information and stdout
  # are not supported)
  if brief_information:
    brief_information = parse_string(brief_information)

  # Parse the search string
  for k in __keywords:
    p = re.compile(f"(\\$\\{{{k[1]}\\}})|(\\${k[1]})", re.IGNORECASE)
    m = p.search(s)

    if m:
      if k[0] == "hostname":
        f = sp.run(["hostname", "-f"], capture_output=True)
        s = s.replace(m.group(0), f.stdout.decode("UTF-8").strip())
      elif k[0] == "detailed_information":
        s = s.replace(m.group(0), detailed_information)
      elif k[0] == "brief_information":
        s = s.replace(m.group(0), brief_information)
      elif k[0] == "stdout" and stdout:
        s = s.replace(m.group(0), stdout)

  return s


def list_to_string(l: list, s: str = "\n") -> str:
  """Transforms a list into a string.

  The entries of the list are seperated by a seperator.

  Args:
      l (list): the list
      s (str, optional): the seperator. Defaults to "\\n".

  Returns:
      str: the list representation with seperator
  """

  r = ""
  for e in l:
    r += e + s
  return r
