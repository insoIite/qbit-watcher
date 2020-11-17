"""
Main entry point
"""
import argparse
import os
import sys
import time

from qbit_watcher.config import Config
from qbit_watcher.logger import create_logger
from qbit_watcher.watcher import TorrentHandler

from watchdog.observers import Observer


class DefaultParser(argparse.ArgumentParser):
    """
     Print the helper on any error
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def get_parser():
    """
    Create argument parser for entry point
    """
    parser = DefaultParser()
    parser.add_argument(
        '-c', '--config',
        default=os.getenv("QBIT_WATCHER_CONF", ""),
        help="Configuration file path"
    )
    return parser

def main():
    """
    Main function of the program
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()
    config = Config(args.config)
    try:
        conf = config.load()
    except:
        sys.exit(1)

    if 'log' in conf:
        logger = create_logger(conf['log'])
    else:
        logger = create_logger()

    handler = TorrentHandler(conf)
    observer = Observer()
    observer.schedule(handler, conf['folders']['src'])
    observer.start()
    logger.info("Watcher started")
    try:
        while(True):
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
