from chromesy.dal.DBConnection import DBConnection
from chromesy.dal.models.TopSite import TopSite


class TopSitesTableAdapter(object):
    def __init__(self, db_connection: DBConnection) -> None:
        self._db_connection = db_connection

    def get_top_sites(self, serializable: bool = True) -> list:
        return self._db_connection.select(TopSite, serializable=serializable)
