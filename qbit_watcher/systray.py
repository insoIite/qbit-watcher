"""
Manage a systray (icon in taskbar) for windows
"""
import logging
import os
import time

from functools import partial
from pathlib import Path
from subprocess import Popen, CalledProcessError

from qbit_watcher.qbittorrent import QBittorrent
from qbit_watcher.settings import APP_LOGFILE, APP_README, APP_BARETAIL, NOTEPAD, APP_ICON_SYSTRAY

from infi.systray import SysTrayIcon

LOGGER = logging.getLogger(__name__)

class QbitTray:
    def __init__(self, conf, toaster):
        self.conf = conf
        self.toaster = toaster
        self.icon_path = APP_ICON_SYSTRAY
        if not self.icon_path.is_file():
            self.icon_path = None
        self.icon = self.setup()

    def setup(self):
        menu_options = (
            ("Clean torrents older than %d days" % (self.conf["clean_older_than"]), None, lambda x: self.clean_torrents()),
            ("Open log file", None, QbitTray.open_log_file),
            ("Open README", None, QbitTray.open_readme),
        )
        icon = SysTrayIcon(
            str(self.icon_path),
            "qbit-watcher",
             menu_options,
             on_quit=QbitTray.on_quit_callback
        )
        return icon

    def run(self, observer):
        """
        Observer will run until you quit from the systray icon
        """
        try:
            self.icon.visible = True
            while(self.icon.visible):
                time.sleep(10)
            observer.stop()
        except KeyboardInterrupt:
            observer.stop()
        # Let's finish running thread before stopping
        observer.join()

    def clean_torrents(self):
        client = QBittorrent(self.conf, self.toaster)
        infos = client.get_torrents_info_added()
        filtered = QbitTray.filter_older_than(self.conf['clean_older_than'], infos)
        filtered_list = list(filtered.keys())
        if filtered_list:
            client.delete_torrents(filtered_list)
        else:
            LOGGER.info("No torrents to remove")

    @staticmethod
    def open_log_file(systray):
        prg = APP_BARETAIL if APP_BARETAIL.exists() else NOTEPAD
        cmd = [prg, APP_LOGFILE]
        _run(cmd)

    @staticmethod
    def open_readme(systray):
        cmd = [NOTEPAD, APP_README]
        _run(cmd)

    @staticmethod
    def on_quit_callback(systray):
        systray.visible = False

    @staticmethod
    def filter_older_than(timing, torrents):
        """
        Return torrents older than timing
        """
        res = {}
        for hash, timestamp in torrents.items():
            if not timestamp > int(time.time()) - timing * 86400:
                res[hash] = timestamp
        return res

def _run(cmd):
    try:
        Popen(cmd)
    except CalledProcessError as cpe:
        LOGIN.error(cpe)
        raise
    return
