"""
Read config file
"""
import logging

import yaml

LOGGER = logging.getLogger(__name__)

class Config:
    def __init__(self, path):
        self.path = path

    def load(self):
        """
        Load and returns config file as yaml object
        """
        with open(self.path, 'r') as fd_config:
            try:
                conf = yaml.safe_load(fd_config)
                LOGGER.info("%s is loaded", self.path)
            except yaml.YAMLError as exc:
                LOGGER.info(exc)
                raise
            return conf
