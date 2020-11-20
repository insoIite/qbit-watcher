"""
Logging definition for qbittorrent module
"""

import logging
import logging.handlers
import os
import sys

from qbit_watcher.settings import APP_LOGFILE

def create_logger():
    """
    Create a logger instance
    :return: logger instance
    """
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    if sys.stdout.isatty() and sys.stderr.isatty():
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        APP_LOGFILE,
        maxBytes=(1048576*5),
        backupCount=7
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
