"""
Logging definition for qbittorrent module
"""

import logging
import logging.handlers
import os
import sys

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

    # No point to use configuration for this right now...
    log_file_path = "%s\qbit-watcher\qbit-watcher.log" % (os.getenv('APPDATA'))

    if not os.path.exists(os.path.dirname(log_file_path)):
        os.makedirs(os.path.dirname(log_file_path))

    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=(1048576*5),
        backupCount=7
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
