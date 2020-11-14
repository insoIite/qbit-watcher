import os
import re
import time

from threading import Thread

from torrent_manager.qbittorrent import QBittorrent
from torrent_manager.ftp import TorrentFTP
from torrent_manager.toaster import TorrentToaster

from watchdog.events import FileSystemEventHandler


class TorrentHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.conf = config
        self.torrent_folder = config['folders']['src']
        self.dest_folder = config['folders']['dest']
        self.toaster = TorrentToaster()

    def manage(self, torrent_filename, torrent_name):

        client = QBittorrent(self.conf['qbitorrent'], self.toaster)
        client.add_torrent(torrent_filename);

        # transform to subthread
        while True:
            time.sleep(1)
            if client.torrent_complete(torrent_name):
                break

        ftpCli = TorrentFTP(self.conf['ftp'], self.dest_folder, self.toaster)
        ftpCli.download(torrent_name)


    def on_modified(self, event):
        for filename in os.listdir(self.torrent_folder):
            if not filename.endswith(".torrent"):
                continue
            src = '%s/%s' % (self.torrent_folder, filename)
            dest = '%s-processed' % (src)
            os.rename(src, dest)
            t_name = re.sub('\.torrent$', '', filename)
            time.sleep(1)
            t = Thread(target=self.manage, args=[dest, t_name])
            t.start()
