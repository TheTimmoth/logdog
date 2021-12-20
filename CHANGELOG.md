# Release 1.0.0a1

Initial release (11.12.2021)

* Features
  - A handler checks `stdout` of a watcher for events (provided as `regexp`)
  - If an event gets detected predefined actions can be performed
  - `logodog` gets configured using a `json` config file
  - Included actions:
    - file: Write configurable output into a file
    - log2mail: Send a mail with configurable content to a predefined receiver

* Remarks
  - A handler supports multiple events to look for
  - One handler checks `stdout` of exactly one watcher (e.g. `tail`)


# Release 1.0.0b2

First beta version (16.12.2021)

* New features
  - Install: check for `python3` as prerequisite
  - Logdog: Add `debug` option to config file for more verbose output (key is added to object `logdog`)
* Changes
  - Service: rename `logdog.service` to `logdog.service.template` to facilitate updates
* Fixes
  - Logdog: output does not appear in `journalctl` instantly


# Release 1.0.0b2

Second beta version (20.12.2021)

* New features
* Changes
* Fixes
  - Logdog: change args of watcher `tail` from `-f` to `-F` to support rolling logs
