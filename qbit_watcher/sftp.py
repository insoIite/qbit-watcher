
import os
import shutil

from pathlib import Path
from qbit_watcher.logger import get_logger
from qbit_watcher.ftp_util import parse_file, get_size_format

from pysftp import Connection, CnOpts


LOGGER = get_logger(__name__)


class SftpGetProgress:
    def __init__(self):
        self.percent_pgr = 10
        self.dict_pgr = {}
        self._init()

    def _init(self):
        for i in range(0, 101):
            if i % self.percent_pgr == 0:
                self.dict_pgr[str(i)] = ""

    def progress_cb(self, x, y):
        current, total, fsize = get_size_format(x, y)
        if int(100*(int(x)/int(y))) % self.percent_pgr == 0 and self.dict_pgr[str(int(100*(int(x)/int(y))))] == "":
            LOGGER.info("{}% ({} / {} {})".format(str("%d" % (100*(int(x)/int(y)))), int(current), int(total), fsize))
            self.dict_pgr[str(int(100*(int(x)/int(y))))] = "1"


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
            port=self.conf["port"],
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
            pgr = SftpGetProgress()
            self.sftp.get(
                fname,
                localpath="%s/%s" % (self.dest, fname),
                callback=lambda x,y: pgr.progress_cb(x, y)
            )
        elif self.sftp.isdir(fname):
            # Cannot get folder if its already exists on local.
            # Therefore remove it before downloading again
            files = self.get_files_recurse(fname)
            path = Path("%s/%s" % (self.dest, fname))
            if path.exists():
                shutil.rmtree(path)
            for file_to_download in files:
                fpath, _fname = parse_file(file_to_download)
                abs_path = "%s/%s" % (self.dest, fpath)
                os.makedirs(abs_path, exist_ok=True)
                LOGGER.info("Retrieving: %s", file_to_download)
                pgr = SftpGetProgress()
                self.sftp.get(
                    file_to_download,
                    "%s/%s" % (abs_path, _fname),
                    callback=lambda x,y: pgr.progress_cb(x, y)
                )
        else:
            LOGGER.info("No file to download found")
            return
        LOGGER.info("%s is downloaded", fname)
        self.toaster.notif("%s is downloaded" % (fname))

    def get_files_recurse(self, f_path):
        """
        get_r method on pysftp have issues on windows, let's implement
        our own
        """
        res = []
        if self.sftp.isfile(f_path):
            res.append(f_path)
        else:
            current_dir = self.sftp.listdir(f_path)
            for remote_f in current_dir:
                res += self.get_files_recurse('%s/%s' % (f_path, remote_f))
        return res

    def close(self):
        self.sftp.close()
