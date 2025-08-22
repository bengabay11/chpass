import sys

from chpass.cli import parse_args
from chpass.config import OUTPUT_FILE_PATHS, DB_PROTOCOL
from chpass.core.object_factory import ObjectFactory
from chpass.dal.chrome_db_adapter import ChromeDBAdapter
from chpass.dal.db_connection import DBConnection
from chpass.dal.db_adapters.history_db_adapter import HistoryDBAdapter
from chpass.dal.db_adapters.logins_db_adapter import LoginsDBAdapter
from chpass.dal.db_adapters.top_sites_db_adapter import TopSitesDBAdapter
from chpass.exceptions.file_adapter_not_supported_exception import FileAdapterNotSupportedException
from chpass.services.chrome import export_chrome_data, import_chrome_passwords
from chpass.services.file_adapters.csv_file_adapter import CsvFileAdapter
from chpass.services.file_adapters.json_file_adapter import JsonFileAdapter
from chpass.core.interfaces import file_adapter_interface
from chpass.services.path import get_chrome_logins_path, get_chrome_history_path, get_chrome_top_sites_path


def create_file_adapter(file_adapter_type: str) -> file_adapter_interface:
    object_factory = ObjectFactory()
    object_factory.register_builder("json", JsonFileAdapter)
    object_factory.register_builder("csv", CsvFileAdapter)
    return object_factory.create(file_adapter_type, exception=FileAdapterNotSupportedException)


def create_chrome_db_adapter(protocol: str, os_user: str, profile: str) -> ChromeDBAdapter:
    logins_db_connection = DBConnection()
    history_db_connection = DBConnection()
    top_sites_db_connection = DBConnection()
    logins_db_connection.connect(protocol, get_chrome_logins_path(os_user, profile))
    history_db_connection.connect(protocol, get_chrome_history_path(os_user, profile))
    top_sites_db_connection.connect(protocol, get_chrome_top_sites_path(os_user, profile))
    logins_db_adapter = LoginsDBAdapter(logins_db_connection)
    history_db_adapter = HistoryDBAdapter(history_db_connection)
    top_sites_db_adapter = TopSitesDBAdapter(top_sites_db_connection)
    return ChromeDBAdapter(logins_db_adapter, history_db_adapter, top_sites_db_adapter)


def start(args=None) -> None:
    if args:
        args = parse_args(args)
    else:
        args = parse_args(sys.argv[1:])
    file_adapter = create_file_adapter(args.file_adapter)
    output_file_paths = OUTPUT_FILE_PATHS[args.file_adapter]
    chrome_db_adapter = create_chrome_db_adapter(DB_PROTOCOL, args.user, args.profile)
    mode_actions = {
        "export": lambda: export_chrome_data(chrome_db_adapter, args.destination_folder, file_adapter,
                                             output_file_paths, args.user, args.export_kind, args.profile),
        "import": lambda: import_chrome_passwords(chrome_db_adapter, args.from_file, file_adapter)
    }
    mode_actions[args.mode]()
    chrome_db_adapter.close()


if __name__ == "__main__":
    start()
