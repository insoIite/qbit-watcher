import logging
import shutil

from pysftp import Connection, CnOpts
from pathlib import Path

LOGGER = logging.getLogger(__name__)

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
            self.sftp.get(fname, localpath="%s/%s" %(self.dest, fname))
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
        self.toaster.notif("%s is downloaded" % (fname))

    def close(self):
        self.sftp.close()
