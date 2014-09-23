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
DESCRIPTION_HEADER = 'DESCRIPTION'

def run(args):
    path = os.path.abspath(args.script)
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    script = __import__(os.path.basename(path)[:-3])       # assume script path ends in .py
    parser = vars(script)[args.method]()
    
    print get_table(parser, args.name_width, args.required_width, args.description_width)

def get_table(parser, nameWidth, reqWidth, descWidth):
    table = list()
    totalWidth = nameWidth + reqWidth + descWidth + 4      # 4 column separators
    append(table, '='*totalWidth, '\n')
    append(table, '|', NAME_HEADER, ' '*(nameWidth-len(NAME_HEADER)), '|')
    append(table, REQUIRED_HEADER, ' '*(reqWidth-len(REQUIRED_HEADER)), '|')
    append(table, DESCRIPTION_HEADER, ' '*(descWidth-len(DESCRIPTION_HEADER)), '|\n')
    append(table, '='*totalWidth, '\n')

    for arg in [a for a in set(vars(parser)['_option_string_actions'].values()) if a.default != '==SUPPRESS==']:
        print arg
        add_arg_row(table, arg, nameWidth, reqWidth, descWidth)

    return ''.join(table)

def add_arg_row(table, arg, nameWidth, reqWidth, descWidth):
    names = get_name_lines(arg, nameWidth)
    requireds = get_required_lines(arg, reqWidth)
    print requireds
    for i in xrange(len(max([names, requireds], key=lambda l: len(l)))):
        append(table, '|', names[i] if len(names) > i else ' '*nameWidth, '|')
        append(table, requireds[i] if len(requireds) > i else ' '*requiredWidth, '|\n')

def get_name_lines(arg, nameWidth):
    lines = list()

    namesRemaining = arg.option_strings
    currLine = ''
    while len(namesRemaining) > 0:
        if len(currLine) + len(namesRemaining[0]) + 1 < nameWidth:  # +1 is for slash separator
            currLine += ('/' if len(currLine) > 0 else '') + namesRemaining.pop(0)
        else:   # TODO: handle case where a single name is too long
            lines.append(currLine + ' '*(nameWidth-len(currLine)))
            currLine = ''
    lines.append(currLine + ' '*(nameWidth-len(currLine)))

    return lines

def get_required_lines(arg, reqWidth):
    # TODO: handle widths too great for single line
    line = ' REQUIRED' if arg.required else ' ' + str(arg.default)
    return [line + ' '*(reqWidth-len(line))]

def append(l, *args):
    for arg in args:
        l.append(arg)

if __name__ == '__main__':
    run(get_parser().parse_args(sys.argv[1:]))