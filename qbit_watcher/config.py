"""
Read config file
"""
from pathlib import Path
from qbit_watcher.logger import get_logger

import yaml

LOGGER = get_logger(__name__)


class ConfigError(Exception):
    """ Config Error
    """


class Config:
    def __init__(self, path):
        self.path = path

    def load(self):
        """
        Load and returns config file as yaml object
        """
        try:
            with open(self.path, 'r') as fd_config:
                conf = yaml.safe_load(fd_config)
        except yaml.YAMLError as exc:
            LOGGER.error(exc)
            raise
        except FileNotFoundError as fnfe:
            LOGGER.error(fnfe)
            raise
        return conf

    def validate(self):
        """ Validate config file
        """
        conf = self.load()
        if not Path(conf['folders']['src']).exists():
            LOGGER.error("Source folder does not exists: %s", conf['folders']['src'])
            raise ConfigError
        if not Path(conf['folders']['dest']).exists():
            LOGGER.error("Dest folder does not exists: %s", conf['folders']['dest'])
            raise ConfigError
