#!/usr/bin/python
import sh
import re
import socket
import os.path
import argparse
import graphyte

HOSTNAME = socket.gethostname()
DEFAULT_URI = 'localhost'
DEFAULT_FILE = '/var/log/cpu-lat.log'
DEFAULT_METRIC = 'cpu-lat'


def main():
    print "Running graphite client... Hit Ctrl-C to end.\n"

    parser = get_parser()
    args = parser.parse_args()
    capture_and_ship(args)
    

def get_parser():
    """
    Specifies and handles input arguments.
    Supports argments specifiying:
        - Log filepath
        - Graphite URI
        - Metric type

    Returns: argparser
    """

    parser = argparse.ArgumentParser(description='Override default configuration for graphite client.')
    parser.add_argument('-f', '--file', default=DEFAULT_FILE, metavar='file',
                    help='log file to tail from')
    parser.add_argument('--uri', default=DEFAULT_URI,
                    help='URI to connect to graphite service')
    parser.add_argument('-m', '--metric', default=DEFAULT_METRIC,
                    help='metric type which makes up the key')

    return parser


def capture_and_ship(args):
    """
    Tails logs streaming into a specific file and
    ships data to graphite using the GraphiteClient.

    Parameters:
    args (object): contains the argment/defaults from the argparser
    """

    client = GraphiteClient(args.metric, args.uri)

    for line in sh.tail('-f', args.file, _iter=True):
        parsed_values = re.findall(r'[0-9+]', line) # regex finds all digits

        if len(parsed_values) > 0:
            client.send(parsed_values[0], parsed_values[-1]) # strips out the upper bound bucket


class GraphiteClient(object):
    """
    The GraphiteClient class interfaces with graphite service
    to connect and ship data.
    """

    def __init__(self, metric, uri):
        """
        Parameters:
        metric (str): metric type to form key
        uri (str): the uri for the graphit service
        """

        prefix = '.'.join([HOSTNAME, metric]) # generates prefix for key
        graphyte.init(uri, prefix=prefix)

    def send(self, bucket, value):
        """
        Parameters:
        bucket: the value should be the lower bound of each bucket
        value: numeric value
        """

        # TODO: Test with graphite
        # TODO: confirm ideal variable types:
        #       should be indifferent of str, unicode, int
        graphyte.send(bucket, value)


def is_valid_file(parser, filepath):
    """
    Verifies if a file path exists and is a file:
    returns the filename if True,
    raises a parser error if file does not exist.

    Parameters:
    parser: argparser
    filepath (str): the path to the log file

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

