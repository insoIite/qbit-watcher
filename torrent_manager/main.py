"""
Main entry point
"""
import argparse

from torrent_manager.config import Config

class DefaultParser(argparse.ArgumentParser):
    """ Print the helper on any error"""
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
    parser = get_parser()
    args = parser.parse_args()
    config = Config(args.config)
    print(config.get_config())

if __name__ == "__main__":
    main()
