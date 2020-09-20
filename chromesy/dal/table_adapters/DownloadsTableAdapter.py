from chromesy.dal.models.Download import Download


class DownloadsTableAdapter(object):
    def __init__(self, db_connection):
        self._db_connection = db_connection

    def get_chrome_downloads(self, serializable=True):
        return self._db_connection.select(Download, serializable=serializable)
