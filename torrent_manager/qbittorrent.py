from qbittorrentapi import Client, TorrentStates

class QBittorrent:
    def __init__(self, conf):
        self.host='%s://%s' % (
            conf['seedbox']['scheme'],
            conf['seedbox']['domain']
        )
        self.port = conf['seedbox']['qbitorrent_port']
        self.user = conf['seedbox']['user']
        self.password = conf['seedbox']['password']
        self.client = self.get_client()

    def get_client(self):
        return Client(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password
        )

    def add_torrent(self, path):
        print(self.client.torrents.add(torrent_files=path))

    def torrent_complete(self, name):
        for torrent in self.client.torrents.info.all():
            if torrent.name != name:
                continue
            if torrent.state_enum.is_downloading:
                print("%s is downloading" % torrent.name)
            if torrent.state_enum.is_complete:
                return True
        return False

    def is_torrent_downloaded(self, hash):
        #print(self.client.torrents.info.all())
        print(self.client.torrents.info.stalled(hash))
        print(self.client.torrents.info.stalled_uploading(hash))
        print(self.client.torrents.info.downloading(hash))
        print(self.client.torrents.info.completed(hash))
