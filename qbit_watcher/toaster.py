import logging
from pathlib import Path
import time

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
        icon_path = Path().absolute() / "qbittorrent_toast.ico"
        if not icon_path.is_file():
            icon_path = None

        try:
            self.toaster.show_toast(
                self.title,
                msg,
                duration=self.duration,
                icon_path=icon_path,
                threaded=True
            )
            while self.toaster.notification_active(): time.sleep(0.1)
        except Exception as exn:
            LOGGER.error(exn)
