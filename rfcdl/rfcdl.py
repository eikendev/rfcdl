import logging

from .arguments import parse_arguments
from .config import load_config, get_default_config_file, get_root_dir
from .downloader import RfcDownloader
from .exception import RfcDLArgumentException, RfcDLConfigurationException
from .logging import setup_logger

logger = logging.getLogger("rfcdl")


def main():
    setup_logger(logger)

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

    config_file = args.config_file

    if config_file is None:
        config_file = get_default_config_file()

    config = load_config(config_file)

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
