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
    parser = script.__dict__[args.method]()
    
    print get_table(parser, args.name_width, args.required_width, args.description_width)

def get_table(parser, nameWidth, reqWidth, descWidth):
    table = list()
    totalWidth = nameWidth + reqWidth + descWidth + 4      # 4 column separators
    append(table, '='*totalWidth, '\n')
    append(table, '|', NAME_HEADER, ' '*(nameWidth-len(NAME_HEADER)), '|')
    append(table, REQUIRED_HEADER, ' '*(reqWidth-len(REQUIRED_HEADER)), '|')
    append(table, DESCRIPTION_HEADER, ' '*(descWidth-len(DESCRIPTION_HEADER)), '|\n')
    append(table, '='*totalWidth, '\n')

    return ''.join(table)

def append(l, *args):
    for arg in args:
        l.append(arg)

if __name__ == '__main__':
    run(get_parser().parse_args(sys.argv[1:]))