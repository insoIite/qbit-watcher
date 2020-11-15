"""
Logging definition for qbittorrent module
"""

import logging
import logging.handlers
import os

def create_logger(conf=None):
    """
    Create a logger instance
    :return: logger instance
    """
    logger = logging.getLogger()
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if conf and 'path' in conf:
        if not os.path.exists(os.path.dirname(conf['path'])):
            os.makedirs(conf['path'])
        file_handler = logging.handlers.RotatingFileHandler(
            conf['path'],
            maxBytes=(1048576*5),
            backupCount=7
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(logging.INFO)
    return logger
