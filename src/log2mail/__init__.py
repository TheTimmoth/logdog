"""Send an email

Package name: log2mail
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

This package contains `log2mail`, a module that sends an email.

Functions:
    log2mail(str, str, str, str, str, str): sends an email

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

from .log2mail import log2mail

__all__ = [
    "log2mail",
]
