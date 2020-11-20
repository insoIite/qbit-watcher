"""
Contains constants vars shared between module
"""
import os

from pathlib import Path

APPDATA = Path("%s\qbit-watcher" % os.getenv('APPDATA'))
CURRENT_DIR = Path().absolute()

APP_BARETAIL = CURRENT_DIR / "baretail.exe"
APP_ICON_SYSTRAY =  CURRENT_DIR / "icon" /"qbittorrent_systray.ico"
APP_ICON_TOAST =  CURRENT_DIR / "icon" / "qbittorrent_toast.ico"
APP_LOGFILE = APPDATA / "qbit-watcher.log"
APP_README = CURRENT_DIR / "README.md"

NOTEPAD = "notepad.exe"
