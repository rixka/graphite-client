import os.path
import argparse

DEFAULT_URI = 'localhost'
DEFAULT_FILE = '/var/log/cpu-lat.log'
DEFAULT_METRIC = 'cpu-lat'


def main():
    parser = get_parser()
    args = parser.parse_args()
    

def get_parser():
    """
    Specifies and handles input arguments.

    Returns: argparser
    """

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--file', default=DEFAULT_FILE, metavar='file',
                    help='log file to tail from')
    parser.add_argument('--uri', default=DEFAULT_URI,
                    help='URI to connect to graphite service')
    parser.add_argument('-m', '--metric', default=DEFAULT_METRIC,
                    help='metric type which makes up the key')

    return parser


def is_valid_file(parser, filepath):
    """
    Verifies if a file path exists and is a file:
    returns the filename if True,
    raises a parser error if file does not exist.

    Parameters:
    parser: argparser
    filepath: the path to the log file

    Returns:
    str: The filepath
    """

    if os.path.isfile(filepath):
        return filepath
    else:
        parser.error("The file %s does not exist!" % filepath)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

