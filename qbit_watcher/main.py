"""
Main entry point
"""
import argparse
import os
import sys

from qbit_watcher.config import Config
from qbit_watcher.logger import create_logger
from qbit_watcher.systray import QbitTray
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
    logger = create_logger()

    parser = get_parser()
    args, _ = parser.parse_known_args()

    config = Config(args.config)
    conf = config.load()

    systray = QbitTray()
    systray.icon.start()

    handler = TorrentHandler(conf)
    observer = Observer()
    observer.schedule(handler, conf['folders']['src'])

    observer.start()
    logger.info("Watcher started")
    systray.run(observer)
