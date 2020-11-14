"""
Main entry point
"""
import argparse
import time

from torrent_manager.config import Config
from torrent_manager.watcher import TorrentHandler

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
        help="Configuration file path"
    )
    return parser

def main():
    """
    Main function of the program
    """
    parser = get_parser()
    args = parser.parse_args()

    config = Config(args.config)
    conf = config.load()

    handler = TorrentHandler(conf)
    observer = Observer()
    observer.schedule(handler, conf['folders']['src'])
    observer.start()
    try:
        while(True):
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
