"""
Read config file
"""
import yaml

class Config:
    def __init__(self, path):
        self.config = Config.load(path)

    def get_config(self):
        return {
            "url": self.config['seedbox']['url'],
            "qbitorrent_path": self.config['seedbox']['qbitorrent_path'],
            "user": self.config['seedbox']['user'],
            "password": self.config['seedbox']['password']
        }


    @staticmethod
    def load(config_path):
        """
        Load and returns config file as yaml object
        """
        with open(config_path, 'r') as fd_config:
            try:
                return yaml.safe_load(fd_config)
            except yaml.YAMLError as exc:
                print(exc)
