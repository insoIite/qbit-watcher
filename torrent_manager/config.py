"""
Read config file
"""
import yaml

class Config:
    def __init__(self, path):
        self.config = Config.load(path)

    def get_config(self):
        return {
            "seedbox": {
                "scheme": self.config['seedbox']['scheme'],
                "domain": self.config['seedbox']['domain'],
                "user": self.config['seedbox']['user'],
                "password": self.config['seedbox']['password'],
                "qbitorrent_port": self.config['seedbox']['qbitorrent_port']
            },
            "local_folders": {
                "torrent_folder": self.config['local_folders']['torrent_folder'],
                "dest_folder": self.config['local_folders']['dest_folder']
            }
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
