"""logdog actions

Package name: actions
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

To add an action to logdog create a function inside this module and add
it to the `__init__.py` file. The logdog imports all modules from this
file and calls them automatically, if they are mentioned in the config
file. Note that the action has to be mentioned by the function name in
the config file. For example the function `log2mail` can be referenced
by writing 'log2mail' in the config file.

An action gets calles with the following parameters:
    detailed_information (str): detailed event information
    brief_information (str): brief event information
    stdout (str): captured watcher output (which contains the event)

The action can deal with this information as it like. It may also
access configuration data stored in the config file via calling
`logdog.config.get_action_data(action_name)`. `action_name` has to be
the same as the function name the action gets called.

Functions:
    log2mail(str, str, str): Send mail

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

from .file import file
from .log2mail import log2mail

__all__ = [
    "file"
    "log2mail",
]
