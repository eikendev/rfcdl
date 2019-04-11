import logging

from argparse import ArgumentParser

from .exception import RfcDLArgumentException

logger = logging.getLogger("rfcdl")


def parse_arguments():
    parser = ArgumentParser(
        prog="rfcdl",
        description="A tool for downloading RFCs in high-speed."
    )
    parser.add_argument("-v", "--debug", action="store_true",
                        help="Print debug information.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Print errors and warnings only.")
    parser.add_argument("-c", "--config-file", type=str,
                        help="File to read configuration from.")
    parser.add_argument("-d", "--directory", type=str,
                        help="Directory to store documents in.")
    parser.add_argument("-n", "--samples", type=int, default=0,
                        help="Only load this many random documents in total.")
    parser.add_argument("--limit", type=int, default=200,
                        help="Only load this many documents at once.")
    parser.add_argument("--retries", type=int, default=10,
                        help="How often a document is tried to be received on"
                        " failure.")

    args = parser.parse_args()

    if args.debug and args.quiet:
        msg = 'Cannot be quiet in debug mode.'
        raise RfcDLArgumentException(msg)

    return args
