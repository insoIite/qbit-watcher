import time

from win10toast import ToastNotifier

class TorrentToaster:
    def __init__(self, conf):
        self.toaster = ToastNotifier()
        self.duration = conf['duration']
        self.title = conf['title']

    def notif(self, msg):
        """
        Perform a win notification
        """
        self.toaster.show_toast(
            self.title,
            msg,
            duration=self.duration,
            threaded=True
        )
        while self.toaster.notification_active(): time.sleep(0.1)
