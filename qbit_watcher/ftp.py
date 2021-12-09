import os


from ftplib import FTP_TLS, FTP
from qbit_watcher.logger import get_logger
from qbit_watcher.ftp_util import parse_file

LOGGER = get_logger(__name__)


class TorrentFTP:
    def __init__(self, conf, dest_folder, toaster):
        self.conf = conf
        self.dest = dest_folder
        self.ftp = self.get_client()
        self.toaster = toaster

    def get_client(self):
        """
        Returns a ftp connection
        """
        if self.conf['tls']:
            ftp = FTP_TLS()
        else:
            ftp = FTP()

        ftp.connect(host=self.conf['domain'], port=self.conf['port'])
        ftp.login(self.conf['user'], self.conf['password'])

        if self.conf['tls']:
            ftp.prot_p()

        ftp.cwd( self.conf['remote_path'])
        LOGGER.info("Successfully connected to '%s' FTP server" % (self.conf['domain']))
        ftp.encoding = 'utf-8'
        return ftp

    def download(self, fname):
        """
        Download a file or a folder from remote FTP
        """
        remote_files = self.ftp.nlst(fname)
        # This is a file
        LOGGER.info('Retrieving %s' % (fname))
        if len(remote_files) == 1:
            with open('%s/%s' % (self.dest, fname), 'wb') as fd_torrent:
                self.ftp.retrbinary('RETR %s' % fname, fd_torrent.write)
        # this is a folder
        else:
            LOGGER.info("Folder detected, let's download each file")
            all_files = self.get_files_recurse(fname)
            for file_to_download in all_files:
                fpath, _fname = parse_file(file_to_download)
                abs_path = "%s/%s" % (self.dest, fpath)
                os.makedirs(abs_path, exist_ok=True)
                with open('%s/%s' % (abs_path, _fname), 'wb') as fd:
                    self.ftp.retrbinary('RETR %s' % (file_to_download), fd.write)
                    LOGGER.info("%s is downloaded", _fname)
        LOGGER.info('%s is retrieved', fname)
        self.toaster.notif("%s is downloaded" % (fname))

    def get_files_recurse(self, file_path):
        """
        Returns a list of all files to download with their parents directory
        e.g:
        ['folder1/folder2/file1', 'folder2/folder1/file1']
        ]
        """
        res = []
        remotes = self.ftp.nlst(file_path)
        if len(remotes) == 1:
            res.append(remotes[0])
        else:
            for remote in remotes:
                res += self.get_files_recurse(remote)
        return res
