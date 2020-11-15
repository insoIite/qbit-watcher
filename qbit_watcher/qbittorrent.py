import logging
import ntpath

from qbittorrentapi import Client, TorrentStates, exceptions

LOGGER = logging.getLogger(__name__)

class QBittorrent:
    def __init__(self, conf, toaster):
        self.host='%s://%s' % (conf['scheme'], conf['domain'])
        self.port = conf['port']
        self.user = conf['user']
        self.password = conf['password']
        self.client = self.get_client()
        self.toaster = toaster

    def get_client(self):
        """
        Returns a client to qbittorrent
        """
        client = Client(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password
        )
        try:
            client.auth_log_in()
            LOGGER.info("Successfully connected to qbittorrent")
        except exceptions.LoginFailed as login_exn:
            LOGGER.error("Failed to login to qbittorrent")
            raise
        except exceptions.Forbidden403Error as forbid_exn:
            LOGGER.error(forbid_exn)
            raise
        return client

    def add_torrent(self, path):
        """
        Add torrent to qbittorrent through API
        """
        self.toaster.notif("%s is on seedbox" % (ntpath.basename(path)))
        self.client.torrents.add(torrent_files=path)
        LOGGER.info("Torrent '%s' is added to qbittorrent", path)

    def torrent_complete(self, name):
        """
        Returns boolean depending on torrent state in qbittorrent
        """
        for torrent in self.client.torrents.info.all():
            if torrent.name != name:
                continue
            if torrent.state_enum.is_downloading:
                LOGGER.info("%s is downloading" % torrent.name)
            if torrent.state_enum.is_complete:
                LOGGER.info("%s is downloaded" % torrent.name)
                return True
        return False
