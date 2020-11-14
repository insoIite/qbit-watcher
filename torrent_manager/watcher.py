import os
import re
import time

from torrent_manager.qbittorrent import QBittorrent

from watchdog.events import FileSystemEventHandler

class TorrentHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.conf = config
        self.torrent_folder = config['local_folders']['torrent_folder']

    def on_modified(self, event):

        for filename in os.listdir(self.torrent_folder):
            if not filename.endswith(".torrent"):
                continue
            src = '%s/%s' % (self.torrent_folder, filename)
            t_name = re.sub('\.torrent$', '', filename)
            dest = '%s-processed' % (src)
            client = QBittorrent(self.conf)
            client.add_torrent(src);
            os.rename(src, dest)
            # transform to subthread
            while True:
                time.sleep(1)
                if client.torrent_complete(t_name):
                    break
            print("Download is complete")



            # qbittorent wait_for_complete
            # qbitorrent download on dest_folder
