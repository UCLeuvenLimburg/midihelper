import argparse
import mido
import sys



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
    # Top level parser
    parser = argparse.ArgumentParser(prog='midi')
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(help='sub-command help')

    subparser = subparsers.add_parser('show', help='prints MIDI file contents')
    subparser.add_argument('filename', help='MIDI file name')
    subparser.add_argument('--format', help='Format', default='[%x] dt=%T %d')
    subparser.add_argument('--filter', help='Filter', default='*')
    subparser.set_defaults(func=_show)

    return parser


def shell_entry_point():
    '''
    Called from shell using 'midihelper' command
    '''
    parser = _create_command_line_arguments_parser()
    args = parser.parse_args()

    args.func(args)
