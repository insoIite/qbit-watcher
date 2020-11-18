import logging
import time

from functools import partial

from infi.systray import SysTrayIcon

LOGGER = logging.getLogger(__name__)

class QbitTray:
    def __init__(self):
        self.icon = self.setup()

    def setup(self):
        menu_options = (("Say Hello", None, QbitTray.say_hello),)
        icon = SysTrayIcon(
            "icon.ico",
            "qbit-watcher",
             menu_options,
             on_quit=QbitTray.on_quit_callback
        )
        return icon

    def run(self, observer):
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
    def say_hello(systray):
        LOGGER.info("Hello baby")

    @staticmethod
    def on_quit_callback(systray):
        systray.visible = False
