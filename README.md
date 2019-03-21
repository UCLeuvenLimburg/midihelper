# MIDI Helper

## Installation

```bash
$ pip install --upgrade git+https://github.com/UCLeuvenLimburg/midihelper.git
```

Install local version in development mode (not meant for students):

```bash
$ git clone https://github.com/UCLeuvenLimburg/midihelper.git
$ cd midihelper
$ pip install -e .
```

## Usage

### Showing MIDI file contents

```bash
$ midihelper show FILENAME [--format FORMAT] [--filter FILTER]
```

FORMAT determines the format for events.

* `%b` bytes in decimal
* `%x` bytes in hexadecimal
* `%T` delta time
* `%t` event type
* `%d` associated data

FILTER determines which events are shown.