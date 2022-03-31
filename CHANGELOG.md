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


# Release 1.0.0b1

First beta release (16.12.2021)

* New features
  - Install: check for `python3` as prerequisite
  - Logdog: Add `debug` option to config file for more verbose output (key is added to object `logdog`)
* Changes
  - Service: rename `logdog.service` to `logdog.service.template` to facilitate updates
* Fixes
  - Logdog: output does not appear in `journalctl` instantly


# Release 1.0.0b2

Second beta release (26.12.2021)

* New features
  - Logdog: add timestamp to internal events
  - Log2Mail: add supoort for multiple recipients
  - Log2Mail: add support for multiple attachments
  - Log2Mail: add option to ask for a password via stdin
* Changes
  - Logdog: update internal event descriptions
  - Log2Mail: simplify password storage
* Fixes
  - Logdog: change args of watcher `tail` from `-f` to `-F` to support rolling logs
  - Logdog: fix infinite recursion if a default action fails
  - Log2Mail: send simple EmailMessage (instead of MIMEMultipart message) when no attachments are present


# Release 1.0.0

Firt final release (16.01.2022)

* Rerelease of 1.0.0b2


# Release 1.1.0

Minor release (xx.xx.2022)

* New features
  - Log2Mail: allow multiple attachments for bin script
* Changes
* Fixes
  - Log2Mail: fix execution of bin script caused by attachment handling
