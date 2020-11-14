import qbittorrentapi

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
        print(self.host)
        return qbittorrentapi.Client(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password
        )
