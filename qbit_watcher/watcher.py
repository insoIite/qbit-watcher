import os
import re
import time

from threading import Thread

from qbit_watcher.logger import get_logger
from qbit_watcher.qbittorrent import QBittorrent
from qbit_watcher.ftp import TorrentFTP
from qbit_watcher.sftp import TorrentSftp

from watchdog.events import FileSystemEventHandler

LOGGER = get_logger(__name__)


class TorrentHandler(FileSystemEventHandler):
    """
    Watcher class, Create a thread(manage) each time a new torrent is
    written on src folder
    """
    def __init__(self, config, toaster):
        self.conf = config
        self.torrent_folder = config['folders']['src']
        self.dest_folder = config['folders']['dest']

        if not os.path.exists(self.dest_folder):
            os.makedirs(self.dest_folder)
        self.toaster = toaster

    def manage(self, torrent_filename, torrent_name):
        """
        Connect to qbitorrent and add torrent
        Ensure the torrent has finished to be downloaded
        Download the torrent on local dest folder from FTP
        """
        LOGGER.info("new thread 'manage' for %s" % (torrent_filename))
        client = QBittorrent(self.conf['qbittorrent'], self.toaster)
        client.add_torrent(torrent_filename);

        while True:
            time.sleep(5)
            if client.torrent_complete(torrent_name):
                break

        if self.conf['ftp']:
            LOGGER.info("Using FTP")
            ftpCli = TorrentFTP(self.conf['ftp'], self.dest_folder, self.toaster)
            ftpCli.download(torrent_name)
        elif self.conf['sftp']:
            LOGGER.info("Using SFTP")
            sftpCli = TorrentSftp(self.conf['sftp'], self.dest_folder, self.toaster)
            sftpCli.download(torrent_name)
            sftpCli.close()

    def on_modified(self, event):
        """
        Listener on src folder,
        create a new thread for each torrent to download
        """
        for filename in os.listdir(self.torrent_folder):
            if not filename.endswith(".torrent"):
                continue
            LOGGER.info("New torrent %s detected" % (filename))
            src = '%s/%s' % (self.torrent_folder, filename)
            dest = '%s-processed' % (src)
            t_name = re.sub('\.torrent$', '', filename)
            t = Thread(target=self.manage, args=[dest, t_name])
            t.start()
            time.sleep(1)
            os.replace(src, dest)
