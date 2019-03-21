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

### Dumping raw MIDI file contents

```bash
$ midihelper dump FILENAME [--format FORMAT] [--filter FILTER]
```

FORMAT determines the format for events.

* `%b` bytes in decimal
* `%x` bytes in hexadecimal
* `%T` delta time
* `%t` event type
* `%d` associated data

FILTER determines which events are shown.

### Playing a MIDI File

```bash
$ midihelper play FILENAME
```

### Convert

Converts notes to midi file.

```bash
$ midihelper convert FILENAME NOTES [--beat BEAT] [--velocity VELOCITY]
```

Example:

```text
$ midihelper convert test.mid "E8 Eb8 E8 Eb8 E8 b8 D8 C8 a"
```
