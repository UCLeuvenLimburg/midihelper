import argparse
import pygame
import time
import mido
import sys


def _play(args):
    filename = args.filename

    pygame.mixer.init(44100, -16, 2, 1024)
    pygame.mixer.music.load(filename)

    try:
        print(f'Playing {filename}... Press CTRL+C to interrupt')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.25)
    finally:
        pygame.mixer.music.stop()


def _dump(args):
    filename = args.filename
    format = args.format
    filter = args.filter
    mid = mido.MidiFile(filename)

    def should_be_printed(message):
        if filter == '*':
            return True
        else:
            return message.type in filter.split(',')

    print(f'MIDI file contains {len(mid.tracks)} track(s)')

    for track_index, track in enumerate(mid.tracks):
        print(f"Track {track_index + 1} contains {len(track)} events")

        for message in track:
            if should_be_printed(message):
                result = format
                result = result.replace('%b', " ".join(map(str, message.bytes())))
                result = result.replace('%x', message.hex())
                result = result.replace('%T', str(message.time))
                result = result.replace('%t', message.type)
                result = result.replace('%d', ' '.join(f'{key}={value}' for key, value in message.dict().items()))

                print(result)



def _notes(args):
    class Note:
        def __init__(self, start, duration, channel, note_index, instrument):
            self.start = start
            self.duration = duration
            self.channel = channel
            self.note_index = note_index
            self.instrument = instrument

        def format(self, format):
            format = format.replace('%c', str(self.channel))
            format = format.replace('%n', str(self.note_index))
            format = format.replace('%s', str(self.start))
            format = format.replace('%e', str(self.start + self.duration))
            format = format.replace('%d', str(self.duration))
            format = format.replace('%i', str(self.instrument))

            return format

    filename = args.filename
    format = args.format
    midi = mido.MidiFile(filename)
    notes = []

    for track in midi.tracks:
        time = 0
        note_starts = [ -1 ] * 128
        channel_instruments = [ 0 ] * 16

        def process_note_on(channel, dt, note_index, velocity):
            nonlocal time, note_starts
            if velocity == 0:
                process_note_off(channel, dt, note_index, velocity)
            elif note_starts[note_index] != -1:
                process_note_off(channel, dt, note_index, 0)
                process_note_on(channel, 0, note_index, velocity)
            else:
                time += dt
                note_starts[note_index] = time

        def process_note_off(channel, dt, note_index, velocity):
            nonlocal time, channel_instruments, note_starts
            time += dt
            start = note_starts[note_index]
            duration = time-start
            instrument = channel_instruments[channel]
            note = Note(start=start, duration=duration, note_index=note_index, instrument=instrument, channel=channel)
            notes.append(note)
            note_starts[note_index] = -1


        def process_program_change(channel, dt, instrument):
            nonlocal time, channel_instruments
            channel_instruments[channel] = instrument
            time += dt

        for message in track:
            if message.type == 'note_on':
                process_note_on(message.channel, message.time, message.note, message.velocity)
            elif message.type == 'note_off':
                process_note_off(message.channel, message.time, message.note, message.velocity)
            elif message.type == 'program_change':
                process_program_change(message.channel, message.time, message.program)
            else:
                time += message.time

    notes.sort(key=lambda n: n.start)

    for note in notes:
        print(note.format(format))



def _create_command_line_arguments_parser():
    '''
    Creates parsers and subparsers
    '''
    parser = argparse.ArgumentParser(prog='midi')
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(help='sub-command help')

    subparser = subparsers.add_parser('dump', help='prints MIDI file contents')
    subparser.add_argument('filename', help='MIDI file name')
    subparser.add_argument('--format', help='Format', default='[%x] dt=%T %d')
    subparser.add_argument('--filter', help='Filter', default='*')
    subparser.add_argument('--no-events', help="Don't print events", action='store_const', const='', dest='filter')
    subparser.set_defaults(func=_dump)

    subparser = subparsers.add_parser('notes', help='prints notes')
    subparser.add_argument('filename', help='MIDI file name')
    subparser.add_argument('--format', help='Format', default='channel=%c note=%n start=%s duration=%d instrument=%i')
    subparser.set_defaults(func=_notes)

    subparser = subparsers.add_parser('play', help='plays MIDI file')
    subparser.add_argument('filename', help='MIDI file name')
    subparser.set_defaults(func=_play)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'midihelper' command
    '''
    parser = _create_command_line_arguments_parser()
    args = parser.parse_args()

    args.func(args)
