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


def _show(args):
    filename = args.filename
    format = args.format
    filter = args.filter
    mid = mido.MidiFile(filename)

    def should_be_printed(message):
        if filter == '*':
            return True
        else:
            return message.type in filter.split(',')

    for track in mid.tracks:
        for message in track:
            if should_be_printed(message):
                result = format
                result = result.replace('%b', " ".join(map(str, message.bytes())))
                result = result.replace('%x', message.hex())
                result = result.replace('%T', str(message.time))
                result = result.replace('%t', message.type)
                result = result.replace('%d', ' '.join(f'{key}={value}' for key, value in message.dict().items()))

                print(result)


def _create_command_line_arguments_parser():
    '''
    Creates parsers and subparsers
    '''
    parser = argparse.ArgumentParser(prog='midi')
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(help='sub-command help')

    subparser = subparsers.add_parser('show', help='prints MIDI file contents')
    subparser.add_argument('filename', help='MIDI file name')
    subparser.add_argument('--format', help='Format', default='[%x] dt=%T %d')
    subparser.add_argument('--filter', help='Filter', default='*')
    subparser.set_defaults(func=_show)

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
