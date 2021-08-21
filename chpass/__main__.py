import sys
from getpass import getuser

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
from chpass.services.package_version import check_latest_package_version
from chpass.services.path import get_chrome_logins_path, get_chrome_history_path, get_chrome_top_sites_path
from chpass.version import name as package_name


def create_file_adapter(file_adapter_type: str) -> file_adapter_interface:
    object_factory = ObjectFactory()
    object_factory.register_builder("json", JsonFileAdapter)
    object_factory.register_builder("csv", CsvFileAdapter)
    return object_factory.create(file_adapter_type, exception=FileAdapterNotSupportedException)


def create_chrome_db_adapter(protocol: str = "sqlite", os_user: str = getuser()) -> ChromeDBAdapter:
    logins_db_connection = DBConnection()
    history_db_connection = DBConnection()
    top_sites_db_connection = DBConnection()
    logins_db_connection.connect(protocol, get_chrome_logins_path(os_user))
    history_db_connection.connect(protocol, get_chrome_history_path(os_user))
    top_sites_db_connection.connect(protocol, get_chrome_top_sites_path(os_user))
    logins_db_adapter = LoginsDBAdapter(logins_db_connection)
    history_db_adapter = HistoryDBAdapter(history_db_connection)
    top_sites_db_adapter = TopSitesDBAdapter(top_sites_db_connection)
    return ChromeDBAdapter(logins_db_adapter, history_db_adapter, top_sites_db_adapter)


def start(args=None) -> None:
    if args:
        args = parse_args(args)
    else:
        args = parse_args(sys.argv[1:])
    check_latest_package_version(package_name)
    file_adapter = create_file_adapter(args.file_adapter)
    output_file_paths = OUTPUT_FILE_PATHS[args.file_adapter]
    chrome_db_adapter = create_chrome_db_adapter(DB_PROTOCOL, args.user)
    mode_actions = {
        "export": lambda: export_chrome_data(chrome_db_adapter, file_adapter,
                                             output_file_paths, args.output_file, args.user, args.export_kind),
        "import": lambda: import_chrome_passwords(chrome_db_adapter, args.file_path, file_adapter)
    }
    mode_actions[args.mode]()
    chrome_db_adapter.close()


if __name__ == "__main__":
    start()
