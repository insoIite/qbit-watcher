import logging
from pathlib import Path
import time

from qbit_watcher.settings import APP_ICON_TOAST

from win10toast import ToastNotifier

LOGGER = logging.getLogger(__name__)

class TorrentToaster:
    def __init__(self, conf):
        self.toaster = ToastNotifier()
        self.duration = conf['duration']
        self.title = conf['title']

    def notif(self, msg):
        """
        Perform a win notification
        """
        if not APP_ICON_TOAST.is_file():
            icon_path = None

        try:
            self.toaster.show_toast(
                self.title,
                msg,
                duration=self.duration,
                icon_path=str(APP_ICON_TOAST),
                threaded=True
            )
            while self.toaster.notification_active(): time.sleep(0.1)
        except Exception as exn:
            LOGGER.error(exn)
