import logging
import sys

from .arguments import parse_arguments
from .config import load_config, get_config_path, get_root_dir
from .downloader import RfcDownloader
from .exception import RfcDLArgumentException, RfcDLConfigurationException

logger = logging.getLogger("rfcdl")


def setup_logger(logger):
    fmt = '%(asctime)s [%(levelname)s] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    level = logging.INFO

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(sh)


def main():
    setup_logger(logger)

    config_path = get_config_path()
    config = load_config(config_path)

    try:
        args = parse_arguments()
    except RfcDLArgumentException as e:
        msg = 'Failed to parse arguments: ' + str(e)
        logger.error(msg)
        exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)
        msg = "Application is running in debug mode."
        logger.debug(msg)
    elif args.quiet:
        logger.setLevel(logging.WARNING)

    logger.info("Starting RfcDL.")

    def load_parameter(required, conf_section, conf_name, arg_name):
        arg = getattr(args, arg_name, None)

        if arg is not None:
            return arg

        conf = config.get(conf_section, conf_name, fallback=None)

        if not required:
            return conf
        else:
            msg = "Required argument not provided: '{}'."
            logger.error(msg.format(arg_name))
            exit(1)

    directory = load_parameter(True, 'GENERAL', 'RootDir', 'directory')

    try:
        directory = get_root_dir(directory)
    except RfcDLConfigurationException as e:
        msg = "Initialization not successful: " + str(e)
        logger.error(msg)
        exit(1)

    dl = RfcDownloader(
        path=directory,
        samples=args.samples,
        limit=args.limit,
        retries=args.retries
    )
    dl.download()
