# -*- coding: utf-8 -*-
"""
    chpass
    ~~~~~
    chpass is a package for export and import chrome browser passwords.
    :copyright: 2020 Ben Gabay
    :license: MIT, see LICENSE for more details.
"""

import sys

from chpass import DBConnection, ChromeDBAdapter
from chpass.cli import create_arg_parser, parse_args
from chpass.config import OUTPUT_FILE_PATHS, DB_PROTOCOL
from chpass.core.ObjectFactory import ObjectFactory
from chpass.dal.ChromeDBAdapter import ChromeDBAdapter
from chpass.dal.DBConnection import DBConnection
from chpass.dal.db_adapters.HistoryDBAdapter import HistoryDBAdapter
from chpass.dal.db_adapters.LoginsDBAdapter import LoginsDBAdapter
from chpass.dal.db_adapters.TopSitesTableAdapter import TopSitesDBAdapter
from chpass.exceptions.FileAdapterNotSupportedException import FileAdapterNotSupportedException
from chpass.services.chrome import export_chrome_data, import_chrome_data
from chpass.services.file_adapters.CsvFileAdapter import CsvFileAdapter
from chpass.services.file_adapters.JsonFileAdapter import JsonFileAdapter
from chpass.core.interfaces import IFileAdapter

__version__ = '0.0.1'
__author__ = "Ben Gabay"
__license__ = "MIT"

from chpass.services.path import get_chrome_logins_path, get_chrome_history_path, get_chrome_top_sites_path


def create_file_adapter(file_adapter_type: str) -> IFileAdapter:
    object_factory = ObjectFactory()
    object_factory.register_builder("json", JsonFileAdapter)
    object_factory.register_builder("csv", CsvFileAdapter)
    return object_factory.create(file_adapter_type, FileAdapterNotSupportedException)


def create_chrome_db_adapter(protocol: str, os_user: str) -> ChromeDBAdapter:
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


def main(args=None) -> None:
    if args:
        args = parse_args(args)
    else:
        args = parse_args(sys.argv[1:])
    file_adapter = create_file_adapter(args.file_adapter)
    output_file_paths = OUTPUT_FILE_PATHS[args.file_adapter]
    chrome_db_adapter = create_chrome_db_adapter(DB_PROTOCOL, args.user)
    export_params = (chrome_db_adapter, args.user, args.destination_folder, args.all_data, file_adapter, output_file_paths)
    mode_actions = {
        "export": lambda: export_chrome_data(*export_params),
        "import": lambda: import_chrome_data(chrome_db_adapter, args.from_file, file_adapter)
    }
    mode_actions[args.mode]()
    chrome_db_adapter.close()
