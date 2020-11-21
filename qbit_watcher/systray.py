"""
Manage a systray (icon in taskbar) for windows
"""
import logging
import os
import time

from pathlib import Path
from subprocess import check_call, CalledProcessError

from qbit_watcher.settings import APP_LOGFILE, APP_README, APP_BARETAIL, NOTEPAD, APP_ICON_SYSTRAY
from infi.systray import SysTrayIcon

LOGGER = logging.getLogger(__name__)

class QbitTray:
    def __init__(self):
        self.icon_path = APP_ICON_SYSTRAY
        if not self.icon_path.is_file():
            self.icon_path = None
        self.icon = self.setup()

    def setup(self):
        menu_options = (
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

    @staticmethod
    def open_log_file(systray):
        prg = APP_BARETAIL if APP_BARETAIL.exists() else NOTEPAD
        cmd = [prg, APP_LOGFILE]
        _check_call(cmd)

    @staticmethod
    def open_readme(systray):
        cmd = [NOTEPAD, APP_README]
        _check_call(cmd)

    @staticmethod
    def on_quit_callback(systray):
        systray.visible = False

def _check_call(cmd):
    try:
        check_call(cmd)
    except CalledProcessError as cpe:
        LOGIN.error(cpe)
        raise
    return
