import os

from ftplib import FTP

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
        ftp = FTP()
        ftp.connect(host=self.conf['domain'], port=self.conf['port'])
        ftp.login(self.conf['user'], self.conf['password'])
        ftp.cwd( self.conf['remote_path'])
        return ftp

    def download(self, fname):
        """
        Download a file or a folder from remote FTP
        """
        res = self.ftp.nlst(fname)
        # This is a file
        if len(res) == 1:
            with open('%s/%s' % (self.dest, fname), 'wb') as fd_torrent:
                self.ftp.retrbinary('RETR %s' % fname, fd_torrent.write)
                print("FTP: ''%s' downloaded" % (fname))
                self.toaster.notif("%s is downloaded" % (fname))
        # this is a folder
        else:
            os.makedirs("%s/%s" % (self.dest, fname), exist_ok=True)
            for file in res:
                with open('%s/%s' % (self.dest, file), 'wb') as fd:
                    self.ftp.retrbinary('RETR %s' % (file), fd.write)
            self.toaster.notif("%s is downloaded" % (fname))
