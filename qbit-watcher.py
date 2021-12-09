import os
import logging
import sys

from qbit_watcher.main import main


def create_emergency_logger():
    """
    Application will run without I/O available
    We need to write in a emergency file if something goes wrong
    Emergency file will be in APPDATA
    """
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_file_path = "%s\qbit-watcher\emergency.log" % (os.getenv('APPDATA'))

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


if __name__ == '__main__':
    try:
        main()
    # Catch all wanted worst case scenario
    except Exception as exn:
        logger = create_emergency_logger()
        logger.error(exn)
        sys.exit(1)
