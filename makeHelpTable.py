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
    return parser

def run(args):
    path = os.path.abspath(args.script)
    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    script = __import__(os.path.basename(path)[:-3])       # assume script path ends in .py
    parser = script.__dict__[args.method]()
    print parser


if __name__ == '__main__':
    run(get_parser().parse_args(sys.argv[1:]))