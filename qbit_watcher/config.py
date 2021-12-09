"""
Read config file
"""
from qbit_watcher.logger import get_logger

import yaml

LOGGER = get_logger(__name__)


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
