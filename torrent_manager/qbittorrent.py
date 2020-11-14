import ntpath
from qbittorrentapi import Client, TorrentStates

class QBittorrent:
    def __init__(self, conf, toaster):
        self.host='%s://%s' % (conf['scheme'], conf['domain'])
        self.port = conf['port']
        self.user = conf['user']
        self.password = conf['password']
        self.client = self.get_client()
        self.toaster = toaster

    def get_client(self):
        return Client(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password
        )

    def add_torrent(self, path):
        self.toaster.notif("Torrent-Manager", "%s is on seedbox" % (ntpath.basename(path)))
        self.client.torrents.add(torrent_files=path)
        import time


    def torrent_complete(self, name):
        for torrent in self.client.torrents.info.all():
            if torrent.name != name:
                continue
            if torrent.state_enum.is_downloading:
                print("%s is downloading" % torrent.name)
            if torrent.state_enum.is_complete:
                return True
        return False
