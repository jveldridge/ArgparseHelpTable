import argparse
import os.path
import sys

def get_parser():
    parser = argparse.ArgumentParser(description='Generates a text table listing information about\
                                                  arguments to a Python script using the argparse\
                                                  module.')
    parser.add_argument('-s', '--script', required=True,
                        help='Path to script for which argument table should be generated')
    parser.add_argument('-m', '--method', default='get_parser',
                        help='Name of (0-argument) method that returns argparse.ArgumentParser')
    parser.add_argument('-nw', '--name_width', type=int, default=25,
                        help='Number of characters for parameter name column')
    parser.add_argument('-rw', '--required_width', type=int, default=20,
                        help='Number of characters for required/default column')
    parser.add_argument('-dw', '--description_width', type=int, default=60,
                        help='Number of characters for description column')
    return parser

NAME_HEADER = ' PARAMETER NAME'
REQUIRED_HEADER = ' REQUIRED/DEFAULT'
DESCRIPTION_HEADER = ' DESCRIPTION'

def run(args):
    path = os.path.abspath(args.script)
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    script = __import__(os.path.basename(path)[:-3])       # assume script path ends in .py
    parser = vars(script)[args.method]()
    
    parser_args = get_parser_args(parser)
    if len(parser_args) > 0:
        print get_table(parser_args, args.name_width, args.required_width, args.description_width)

    # handle sub-parsers
    subparsers = vars(parser)['_subparsers']
    if subparsers:
        for name, subparser in subparsers.__dict__['_group_actions'][0].choices.iteritems():
            print subparsers.title + ": " + name
            print get_table(get_parser_args(subparser), args.name_width, args.required_width, args.description_width)


def get_parser_args(parser):
    usage = parser.format_usage()
    allArgs = vars(parser)['_option_string_actions'].values()
    args = [a for a in set(allArgs) if a.default != '==SUPPRESS==']
    args.sort(key=lambda a: usage.find(min(a.option_strings, key=lambda s: len(s))))
    return args

def get_table(args, nameWidth, reqWidth, descWidth):
    table = list()
    totalWidth = nameWidth + reqWidth + descWidth + 4      # 4 column separators
    append(table, '='*totalWidth, '\n')
    append(table, '|', NAME_HEADER, ' '*(nameWidth-len(NAME_HEADER)), '|')
    append(table, REQUIRED_HEADER, ' '*(reqWidth-len(REQUIRED_HEADER)), '|')
    append(table, DESCRIPTION_HEADER, ' '*(descWidth-len(DESCRIPTION_HEADER)), '|\n')
    append(table, '='*totalWidth, '\n')

    for arg in args:
        add_arg_row(table, arg, nameWidth, reqWidth, descWidth)
        append(table, '-'*totalWidth, '\n')

    return ''.join(table)

def add_arg_row(table, arg, nameWidth, reqWidth, descWidth):
    names = get_name_lines(arg, nameWidth)
    requireds = get_required_lines(arg, reqWidth)
    descriptions = get_description_lines(arg, descWidth)
    for i in xrange(len(max([names, requireds, descriptions], key=lambda l: len(l)))):
        append(table, '|', names[i] if len(names) > i else ' '*nameWidth, '|')
        append(table, requireds[i] if len(requireds) > i else ' '*reqWidth, '|')
        append(table, descriptions[i] if len(descriptions) > i else ' '*descWidth, '|\n')

def get_name_lines(arg, nameWidth):
    return get_lines(arg.option_strings, '/', nameWidth)

def get_required_lines(arg, reqWidth):
    # TODO: handle widths too great for single line
    line = ' REQUIRED' if arg.required else ' ' + str(arg.default)
    return [line + ' '*(reqWidth-len(line))]

def get_description_lines(arg, descWidth):
    return get_lines(arg.help.split(), ' ', descWidth)

def get_lines(tokens, separator, width):
    lines = list()

    tokensRemaining = list(tokens)
    currLine = ''
    while len(tokensRemaining) > 0:
        if len(currLine) + len(tokensRemaining[0]) + 1 < width:  # +1 is for separator
            currLine += (separator if len(currLine) > 0 else '') + tokensRemaining.pop(0)
        elif len(currLine) == 0 and len(tokensRemaining) > 0:
            currLine += tokensRemaining.pop(0)[:width]
        else:
            lines.append(currLine + ' '*(width-len(currLine)))
            currLine = ''
    lines.append(currLine + ' '*(width-len(currLine)))

    return lines

def append(l, *args):
    for arg in args:
        l.append(arg)

if __name__ == '__main__':
    run(get_parser().parse_args(sys.argv[1:]))