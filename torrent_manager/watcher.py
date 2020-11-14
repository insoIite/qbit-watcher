import os

from watchdog.events import FileSystemEventHandler

class TorrentHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.torrent_folder = config['local_folders']['torrent_folder']

    def on_modified(self, event):
        for filename in os.listdir(self.torrent_folder):
            if not filename.endswith(".torrent"):
                continue

            # thread
            # qbittorent upload
            src = '%s/%s' % (self.torrent_folder, filename)
            dest = '%s-processed' % (src)
            os.rename(src, dest)
            # qbittorent wait_for_complete
            # qbitorrent download on dest_folder
