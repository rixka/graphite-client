import os.path
import argparse

DEFAULT_URI = 'localhost'
DEFAULT_FILE = '/var/log/cpu-lat.log'
DEFAULT_METRIC = 'cpu-lat'


def main():
    parser = get_parser()
    args = parser.parse_args()
    

def get_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--file', default=DEFAULT_FILE, metavar='file',
                    help='log file to tail from')
    parser.add_argument('--uri', default=DEFAULT_URI,
                    help='URI to connect to graphite service')
    parser.add_argument('-m', '--metric', default=DEFAULT_METRIC,
                    help='metric type which makes up the key')

    return parser


def is_valid_file(parser, arg):
    if os.path.isfile(arg):
        return arg
    else:
        parser.error("The file %s does not exist!" % arg)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

