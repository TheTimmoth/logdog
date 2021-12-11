# Logdog - a stdout event sniffer and handler

Logdog is a small program that spawns handler that able to scan the output of so called watchers (e.g. `tail`) for predefined events. If an event occurs it is handled by logdog by performing predefined actions.

## Installation
1) Please clone this repository via
    ```bash
    git clone https://github.com/TheTimmoth/logdog.git
    ```

2) `cd` into the newly created directory `logdog`

3) *Optional: If you want to change the path to the config file please run*
    ```bash
    editor ./service/logdog.service
    ```
    *and change `-c %%LOGDOG_PATH%%/logdog.json` to the new config file location.*

4) Please run
    ```
    ./install.sh
    ```

## Usage
1) Create a settings file that contains the handlers, watchers and events. Please look at section [Configuration](#Configuration) to write a config.

2) Optional: to check your configuration you can run Logdog in foreground with the following command:
    ```
    logdog -c /path/to/config.json
    ```

3) If you have followed the section [Installation](#Installation) you can now simply run:
    ```bash
    systemctl start logdog
    ```

## Configuration with `logdog.json`
To configure logdog a configuration file needs to be created. By default this file is stored inside the repository folder:
```bash
./logdog.json
```

### Ready-to-start-example
A ready-to-start-example is provided in the file `logdog.json.example`. You can use this file as a starting point. By default the log `/var/log/auth` gets monitored for events like `ssh` login and `su` usage. Any captured events gets written into a file `captured_events.log` within the project folder.


### Overall structure
The configuration file has the following structure:
```
{
  "logdog": { ... },
  "actions": { ... },
  "watchers": { ... },
  "handlers": { ... }
}
```

### The `logdog` object
The `logdog` object contains general settings that are used if no specific setting applies. It has to be structured as follows:
```
{
  "logdog": {
    "default_actions": ["log2mail"],
    "default_watcher": "tail"
  }
}
```
* `"default_actions": ["some_action", "another_action", ...]` - the default actions that are performed if no specific ones are available.
* `"default_watcher": "some_watcher"` - the default watcher that is used if no specific ones is available

### The `actions` object
The `actions` object contains all possible actions with their configuration data. These actions can be executed if an event occurs. Which action will be run at a certain event is defined in the [`handlers` object](#the-handlers-object). It has to be structured as follows:
```
{
  "actions": {
    "log2mail": { ... },
    "write_file": { ... }
  }
}
```
Please note that every action has its own unique key-value pairs. You can find some examples in the section [Actions](#Actions).

### The `watchers` object
The `watchers` object contains all possible watchers. A watcher is an program like the command `tail -F` which does produce continuous `stdout` output that gets than monitored by Logdog. The structure of the object is the following:
```
  "watchers": {
    "tail": {
      "cwd": "../",
      "command": ["tail", "-f", "$FILE"]
    }
    "program_01": {
      "cwd": "/tmp/",
      "command": ["program_01", "arg1", "arg2]
    }
  }
```
A watcher is a key-value pair with a unique identifier as key and an object as value. Each watcher need to have the following key-value pairs:
* `"cwd": "/path/to/working/directory"` - The working directory of the watcher
* `"command": ["/path/to/exec", "arg1, "arg2", ...]` - The command and its arguments that is executed by the watcher. The `stdout` of this program gets monitored. The keyword `$FILE` can be used as an argument and is replaced by the filename that is defined for the handler in the [`handlers` object](#the-handlers-object).

### The `handlers` object
The handlers object contains the handlers that can handle events. Each handler represents one command whose output gets monitored. Per handler multiple events can be defined that the handler reacts to. The structure of the handler object is the following:
```
  "handlers": {
    "auth": {
      "file": "/var/log/auth",
      "watcher": "tail",
      "events": { ... },
    },
    "another_handler": {
      "file": "/path/to/file",
      "watcher": "some_watcher",
      "events": { ... },
    }
  }
```
Each handler has to contain the following key-value-pairs:
* `"file": "/path/to/file" (Optional)`: a path to a file. If the watcher defines `$FILE` as one of his arguments it gets replaced by the string given here.
* `"watcher": "some_watcher"`: the watcher to use. The watcher needs to be a key from the [`watchers` object](#the-watchers-object).
* `"events": { ... }`: defines the events that need to be handled. Please look at the [`events` object](#the-events-object).

### The `events` object
The `events` object defines the events that occur during monitoring the output of the watcher. An event fires if the given regex matches a output line. For each event a defined number of previous and next lines of the output can be captured. Each event has some information that describes the event in a brief and in a detailed manner. These descriptions can be used by the actions that can be defined per event. These actions are performed if an event fires.
```
      "events": {
        "login": {
          "active": true,
          "next_lines": 2,
          "prev_lines": 0,
          "regexp": "sshd\\[[0-9]*\\]\\: Accepted publickey",
          "brief_information": "SSH: successfull login",
          "detailed_information": "$STDOUT",
          "actions": [
            "log2mail"
          ]
        },
        "event_name": { ... }
      }
```
The following key-value pairs has to be present within an event:
* `"event_name": {} ` - An unique identifier for the event
* `"active": bool` - Predicts if the event gets considered or not
* `"next_lines": int` - Number of following lines to capture
* `"prev_lines": int` - Number of previous lines to capture
* `"regexp": "some regular expression"` - Regular expression against which each output line gets evaluated
* `"brief_information": ` - Brief event description.
* `"detailed_information": ` - Detailed event description. Use keyword `$STDOUT` to include captured output
* `"actions": ["some_action", "another_action", ...]` - Actions that are executed if the event is detected. Each action has to be a key in the [`actions` object](#the-actions-object).

## Actions
Note that the keywords `${BRIEF_INFORMATION}` and `${DETAILED_INFORMATION}` corresponds to the keys `brief_information` and `detailed_information` in the [`events` object](#the-events-object).

### `file`
The `file` action writes any event to a file. It gets configured in the with the [`actions` object](#the-actions-object) following key-value pairs:
```
    "file": {
      "path": "/path/to/output/file",
      "format": "${BRIEF_INFORMATION}\n${DETAILED_INFORMATION}\n\n"
    },
```
* `"path": "/path/to/output/file"` - defines the path of the output file
* `"format": ""` - defines the output format for each event.

### `log2mail`
The `log2mail` action sends an email to a defined receiver. It gets configured in the with the [`actions` object](#the-actions-object) following key-value pairs:
```
    "log2mail": {
      "from": "noreply@example.com <noreply@example.com>",
      "to": "Important Receiver <admin@example.com>",
      "subject": "${BRIEF_INFORMATION}",
      "message": "${DETAILED_INFORMATION}",
      "config": "../log2mail.json"
    }
```

`log2mail` requires a config file that contains login data to a mailserver that is used to send the mail.
An example configuration is provided in the file `log2mail.json.example`. The file contains an encrypted version of the password for a mailserver together with a key to encrypt the password. **Please make sure that the file can only be accessed by yourself (and the script of course).**

To generate the values needed for `secret` and `password` run the following script:
```python
#! /usr/bin/python3

from cryptography.fernet import Fernet
from getpass import getpass

key = Fernet.generate_key()
print(f"\"secret\": \"{key.decode('UTF-8')}\" ")
fernet = Fernet(key)

password = fernet.encrypt(getpass().encode())
print(f"\"password\": \"{password.decode('UTF-8')}\" ")

```

## Known limitations
* Events that need multiple lines of the output to get recognized are not supported.
* `log2mail` supports only one receiver.
