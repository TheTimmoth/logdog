"""Look for and handle events occuring in logfiles

Package name: logdog
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

This package contains `logdog`, a daemon that can spawn handlers to detect
events in the `stdout` output of watcher processes like `tail`.

Functions:
    logdog(str): the logdog daemon

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

from .logdog import logdog

__all__ = [
    "logdog",
]
