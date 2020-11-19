"""
Manage a systray (icon in taskbar) for windows
"""
import logging
import os
import time

from pathlib import Path
from subprocess import check_call

from infi.systray import SysTrayIcon

LOGGER = logging.getLogger(__name__)

class QbitTray:
    def __init__(self):
        self.icon_path = Path().absolute() / "qbittorrent_systray.ico"
        if not self.icon_path.is_file():
            LOGGER.info("%s not found" % str(self.icon_path))
            self.icon_path = None
        self.icon = self.setup()

    def setup(self):
        menu_options = (("Tail log file", None, QbitTray.open_log_file),)
        LOGGER.info(self.icon_path)
        icon = SysTrayIcon(
            self.icon_path,
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

    @staticmethod
    def open_log_file(systray):
        baretail = Path().absolute() / "baretail.exe"
        LOGGER.info(baretail)
        cmd = [baretail, "%s\qbit-watcher\qbit-watcher.log" % (os.getenv('APPDATA'))]
        check_call(cmd)

    @staticmethod
    def say_hello(systray):
        LOGGER.info("Hello baby")

    @staticmethod
    def on_quit_callback(systray):
        systray.visible = False
