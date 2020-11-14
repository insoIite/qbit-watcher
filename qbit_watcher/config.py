"""
Read config file
"""
import yaml

class Config:
    def __init__(self, path):
        self.path = path

    def load(self):
        """
        Load and returns config file as yaml object
        """
        with open(self.path, 'r') as fd_config:
            try:
                return yaml.safe_load(fd_config)
            except yaml.YAMLError as exc:
                print(exc)
