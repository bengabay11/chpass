from chromesy.dal.table_adapters.LoginsTableAdapter import LoginsTableAdapter
from chromesy.utils.singleton_meta import SingletonMeta


class LoginsDBAdapter(metaclass=SingletonMeta):
    def __init__(self, db_connection):
        self._db_connection = db_connection
        self._logins_table_adapter = LoginsTableAdapter(self._db_connection)

    @property
    def logins(self):
        return self._logins_table_adapter
