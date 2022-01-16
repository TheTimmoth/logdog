"""Send an email

Filename: log2mail.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

This file contains `log2mail`, a module that sends an email.

Functions:
    log2mail(str, str, str, str, list, list): sends an email

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

import base64
import json
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass


def log2mail(config_path: str,
             subject: str,
             message_text: str,
             sender: str,
             recipients: list,
             file_paths: list = None,
             askpass: bool = False):
  """Send an email

  Args:
      config_path (str): path to config file that contains login data
      subject (str): subject of the mail
      message_text (str): content of the mail
      sender (str): sender of the mail
      recipients (list): recipient of the mail
      file_paths (list, optional): Path to a text file that gets
          attached. Defaults to None.
  """

  if file_paths == None:
    file_paths = []

  # Read config data
  try:
    with open(config_path) as f:
      config = json.load(f)
  except FileNotFoundError as e:
    sys.stderr.write(f"Error: config file {config_path} is not present\n")
    sys.stderr.write(str(e) + "\n")
    sys.stderr.write("Exiting...\n")
    exit(1)
  except json.decoder.JSONDecodeError as e:
    sys.stderr.write(
        f"Error: config file {config_path} contains invalid json\n")
    sys.stderr.write(str(e) + "\n")
    sys.stderr.write("Exiting...\n")
    exit(2)

  # Get SMTP data
  smtp_server = config["smtp"]["server"]
  receiver_mail = config["smtp"]["receiver"]

  # Get SMTP login data
  username = config["smtp"]["username"]
  password = getpass() if askpass else str(
      base64.b64decode(config["smtp"]["password"]), "utf-8")

  # SSL
  port = 465
  context = ssl.create_default_context()

  # Create message
  if file_paths:
    message = MIMEMultipart()
  else:
    message = EmailMessage()
  message["Subject"] = subject
  message["From"] = sender
  message["To"] = ", ".join(recipients)

  if file_paths:
    # Attach message text
    message.attach(MIMEText(message_text))

    # Attach file
    for fp in file_paths:
      try:
        with open(fp, "rb") as f:
          attachment = MIMEApplication(f.read())
      except FileNotFoundError:
        pass
      else:
        attachment.add_header("Content-Disposition",
                              "attachment",
                              filename=f"{os.path.basename(fp)}")
        message.attach(attachment)
  else:
    message.set_content(message_text)

  message = message.as_bytes()

  # Send mail
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(username, password)
    server.sendmail(username, receiver_mail, message)
