"""Send an email

Filename: log2mail.py
Author: Tim Schlottmann
Copyright (c) 2021 Tim Schlottmann

License: `MIT`_ (Please look at license of surrounding project)

This file contains `log2mail`, a module that sends an email.

Functions:
    log2mail(str, str, str, str, str, str): sends an email

.. _MIT:
   https://github.com/TheTimmoth/logdog/blob/main/LICENSE
"""

from json.decoder import JSONDecodeError
import sys
import smtplib, ssl
import json
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import path


def log2mail(config_path: str,
             subject: str,
             message_text: str,
             sender: str,
             recipient: str,
             file_path: str = None):
  """Send an email

  Args:
      config_path (str): path to config file that contains login data
      subject (str): subject of the mail
      message_text (str): content of the mail
      sender (str): sender of the mail
      recipient (str): recipient of the mail
      file_path (str, optional): Path to a text file that gets
          attached. Defaults to None.
  """

  # Encoded password
  try:
    with open(config_path) as f:
      config = json.load(f)
  except FileNotFoundError as e:
    sys.stderr.write(f"Error: config file {config_path} is not present\n")
    sys.stderr.write(str(e) + "\n")
    sys.stderr.write("Exiting...\n")
    exit(1)
  except JSONDecodeError as e:
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
  secret = config["smtp"]["secret"].encode('UTF-8')
  password = config["smtp"]["password"].encode('UTF-8')
  cipher_suite = Fernet(secret)

  # SSL
  port = 465
  context = ssl.create_default_context()

  # Create message
  message = MIMEMultipart("mixed")
  message["Subject"] = subject
  message["From"] = sender
  message["To"] = recipient

  # Attach message text
  message.attach(MIMEText(message_text, "plain"))

  # Attach file
  if file_path:
    with open(file_path, "r", encoding="utf8") as f:
      attachment = MIMEText(f.read(), "plain")
    attachment.add_header("Content-Disposition",
                          "attachment",
                          filename=f"{path.basename(file_path)}")
    message.attach(attachment)

  message = message.as_bytes()

  # Send mail
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(username, cipher_suite.decrypt(password).decode())
    server.sendmail(username, receiver_mail, message)
