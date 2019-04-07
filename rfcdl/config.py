import logging
import os

from configparser import ConfigParser
from pathlib import Path

from .exception import RfcDLConfigurationException

logger = logging.getLogger("rfcdl")


def load_config(path):
    config = ConfigParser(interpolation=None)
    config.read(path)

    return config


def _get_config_base():
    default = '~/.config'
    path = os.getenv('XDG_CONFIG_HOME', default)
    path = Path(path).expanduser().resolve()

    if not path.is_dir():
        msg = 'Could not find configuration file.'
        logger.error(msg)
        exit(1)

    return path


def get_config_path():
    config_directory = 'rfcdl'
    config_filename = 'config.ini'

    base = _get_config_base()
    directory = base / config_directory
    config = directory / config_filename

    return config


def get_root_dir(path):
    if path is None:
        msg = 'Invalid root directory.'
        raise RfcDLConfigurationException(msg)

    path = Path(path)
    path = path.expanduser().resolve()

    if not path.exists():
        path.mkdir(parents=True)

    if not path.is_dir():
        msg = 'Root directory path is not a directory.'
        raise RfcDLConfigurationException(msg)

    return path
