import logging
import shutil

from pysftp import Connection, CnOpts
from pathlib import Path

LOGGER = logging.getLogger(__name__)

dict_pgr = {}
percent_pgr = 10

def init_progress():
    for i in range(0, 101):
        if i % percent_pgr == 0:
            dict_pgr[str(i)] = ""

init_progress()

class TorrentSftp:
    def __init__(self, conf, dest_folder, toaster):
        self.conf = conf
        self.dest = dest_folder
        self.sftp = self.get_client()
        self.toaster = toaster


    def get_client(self):
        cnopts = CnOpts()
        cnopts.hostkeys = None
        sftp = Connection(
            self.conf['domain'],
            username=self.conf['user'],
            password=self.conf['password'],
            cnopts=cnopts,
            default_path=self.conf['remote_path']
        )
        LOGGER.info("Successfully connected to '%s' SFTP server", self.conf['domain'])
        return sftp

    def download(self, fname):
        """
        Download torrent to local workstation
        """
        LOGGER.info("Retrieving '%s'" % fname)
        if self.sftp.isfile(fname):
            self.sftp.get(
                fname,
                localpath="%s/%s" % (self.dest, fname),
                callback=lambda x,y: TorrentSftp.progress_cb(x, y)
            )
        elif self.sftp.isdir(fname):
            # Cannot get folder if its already exists on local.
            # Therefore remove it before downloading again
            path = Path("%s/%s" % (self.dest, fname))
            if path.exists():
                shutil.rmtree(path)
            self.sftp.get_r(fname, self.dest)
        else:
            LOGGER.info("No file to download found")
            return
        LOGGER.info("%s is downloaded", fname)
        self.toaster.notif("%s is downloaded" % (fname))

    @staticmethod
    def progress_cb(x, y):
        current_mb = x / 1024 / 1024
        total_mb = y / 1024 / 1024
        if int(100*(int(current_mb)/int(total_mb))) % percent_pgr == 0 and dict_pgr[str(int(100*(int(current_mb)/int(total_mb))))] == "":
            LOGGER.info("{}% ({} / {} MB)".format(str("%d" % (100*(int(x)/int(y)))), int(current_mb), int(total_mb)))
            dict_pgr[str(int(100*(int(current_mb)/int(total_mb))))] = "1"

    def close(self):
        self.sftp.close()
