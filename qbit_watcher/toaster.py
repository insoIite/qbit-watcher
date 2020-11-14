import time

from win10toast import ToastNotifier

class TorrentToaster:
    def __init__(self):
        self.toaster = ToastNotifier()

    def notif(self, title, msg):
        """
        Perform a win notification
        """
        self.toaster.show_toast(
            title,
            msg,
            duration=5,
            threaded=True
        )
        while self.toaster.notification_active(): time.sleep(0.1)
