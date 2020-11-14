import os
import re
import time

from threading import Thread

from qbit_watcher.qbittorrent import QBittorrent
from qbit_watcher.ftp import TorrentFTP
from qbit_watcher.toaster import TorrentToaster

from watchdog.events import FileSystemEventHandler


class TorrentHandler(FileSystemEventHandler):
    """
    Watcher class, Create a thread(manage) each time a new torrent is
    written on src folder
    """
    def __init__(self, config):
        self.conf = config
        self.torrent_folder = config['folders']['src']
        self.dest_folder = config['folders']['dest']
        if not os.path.exists(self.dest_folder):
            os.makedirs(self.dest_folder)
        self.toaster = TorrentToaster(config['toaster'])

    def manage(self, torrent_filename, torrent_name):
        """
        Connect to qbitorrent and add torrent
        Ensure the torrent has finished to be downloaded
        Download the torrent on local dest folder from FTP
        """
        client = QBittorrent(self.conf['qbitorrent'], self.toaster)
        client.add_torrent(torrent_filename);

        while True:
            time.sleep(1)
            if client.torrent_complete(torrent_name):
                break

        ftpCli = TorrentFTP(self.conf['ftp'], self.dest_folder, self.toaster)
        ftpCli.download(torrent_name)

    def on_modified(self, event):
        """
        Listener on src folder,
        create a new thread for each torrent to download
        """
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
