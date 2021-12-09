"""
Main entry point
"""

from qbit_watcher.logger import get_logger
from qbit_watcher.config import Config
from qbit_watcher.settings import APP_CONFIG_FILE
from qbit_watcher.systray import QbitTray
from qbit_watcher.toaster import TorrentToaster
from qbit_watcher.watcher import TorrentHandler

from watchdog.observers import Observer

log_cfg = {
    "stream_handler": True
}


def main():
    """
    Main function of the program
    """
    logger = get_logger("qbit", log_cfg)

    config = Config(APP_CONFIG_FILE)
    conf = config.load()

    toaster = TorrentToaster(conf['toaster'])

    systray = QbitTray(conf['qbittorrent'], toaster)
    systray.icon.start()

    handler = TorrentHandler(conf, toaster)
    observer = Observer()
    observer.schedule(handler, conf['folders']['src'])

    observer.start()
    logger.info("Watcher started")
    systray.run(observer)
