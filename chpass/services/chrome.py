import getpass
import os
from shutil import copyfile
from typing import List, Callable

from chpass.dal.chrome_db_adapter import ChromeDBAdapter
from chpass.core.interfaces import file_adapter_interface
from chpass.config import PASSWORDS_FILE_BYTES_COLUMNS, CREDENTIALS_ALREADY_EXIST_MESSAGE
from chpass.services.path import get_chrome_profile_picture_path
from chpass.services.zip import zip_files


def generic_export(
        get_data_func: Callable,
        file_adapter: file_adapter_interface,
        filename: str) -> None:
    data = get_data_func(serializable=True)
    file_adapter.write(data, filename)


def export_profile_picture(destination_path: str, user: str = getpass.getuser()) -> None:
    """Exports google profile picture
    :param destination_path: Destination path to export the picture
    :param user: Chrome user
    :return: None
    :rtype: None
    """
    source_path = get_chrome_profile_picture_path(user)
    copyfile(source_path, destination_path)


def export_history(
        chrome_db_adapter: ChromeDBAdapter,
        file_adapter: file_adapter_interface,
        filename: str) -> None:
    """Exports chrome history to a file
    :param chrome_db_adapter: Adapter for the chrome db
    :param file_adapter: Adapter for writing the history data to a file
    :param filename: Destination file name for the history
    :return: None
    :rtype: None
    """
    generic_export(chrome_db_adapter.history_db.history_table.get_chrome_history, file_adapter, filename)


def export_downloads(
        chrome_db_adapter: ChromeDBAdapter,
        file_adapter: file_adapter_interface,
        filename: str) -> None:
    """Exports chrome downloads to a file
    :param chrome_db_adapter: Adapter for the chrome db
    :param file_adapter: Adapter for writing the downloads data to a file
    :param filename: Destination file name for the downloads
    :return: None
    :rtype: None
    """
    generic_export(chrome_db_adapter.history_db.downloads_table.get_chrome_downloads, file_adapter, filename)


def export_top_sites(
        chrome_db_adapter: ChromeDBAdapter,
        file_adapter: file_adapter_interface,
        filename: str) -> None:
    """Exports chrome top sites to a file
    :param chrome_db_adapter: Adapter for the chrome db
    :param file_adapter: Adapter for writing the top sites data to a file
    :param filename: Destination file name for the top sites
    :return: None
    :rtype: None
    """
    generic_export(chrome_db_adapter.top_sites_db.top_sites_table.get_top_sites, file_adapter, filename)


def export_passwords(
        chrome_db_adapter: ChromeDBAdapter,
        file_adapter: file_adapter_interface,
        filename: str) -> None:
    """Exports chrome passwords to a file
    :param chrome_db_adapter: Adapter for the chrome db
    :param file_adapter: Adapter for writing the passwords data to a file
    :param filename: Destination file name for the passwords
    :return: None
    :rtype: None
    """
    logins = chrome_db_adapter.logins_db.logins_table.get_all_logins(serializable=True)
    file_adapter.write(logins, filename, byte_columns=PASSWORDS_FILE_BYTES_COLUMNS)


def export_chrome_data(
        chrome_db_adapter: ChromeDBAdapter,
        file_adapter: file_adapter_interface,
        output_file_paths: dict,
        compressed_file_path: str,
        user: str = getpass.getuser(),
        export_kind: str = None) -> None:
    """Exports chrome data to a file
    :param chrome_db_adapter: Adapter for the chrome db
    :param file_adapter: Adapter for writing the data to a file
    :param output_file_paths: Dictionary that maps between data type and its destination file path
    :param compressed_file_path: Path for the final compressed file
    :param user: Chrome user
    :param export_kind: Specific data type export instead of export all the data
    :return: None
    :rtype: None
    """
    export_functions = {
        "passwords": lambda: export_passwords(chrome_db_adapter, file_adapter, output_file_paths["passwords"]),
        "history": lambda: export_history(chrome_db_adapter, file_adapter, output_file_paths["history"]),
        "downloads": lambda: export_downloads(chrome_db_adapter, file_adapter, output_file_paths["downloads"]),
        "top_sites": lambda: export_top_sites(chrome_db_adapter, file_adapter, output_file_paths["top_sites"]),
        "profile_pic": lambda: export_profile_picture(output_file_paths['profile_picture'], user)
    }
    if export_kind:
        export_functions[export_kind]()
        zip_files(compressed_file_path, [output_file_paths[export_kind]])
        os.remove(output_file_paths[export_kind])
    else:
        for export_func in export_functions.values():
            export_func()
        zip_files(compressed_file_path, list(output_file_paths.values()))
        for file_path in output_file_paths.values():
            os.remove(file_path)


def filter_existed_logins(chrome_db_adapter: ChromeDBAdapter, logins_to_import: List[dict]) -> list:
    db_logins = chrome_db_adapter.logins_db.logins_table.get_all_logins(serializable=True)
    db_logins_signon_realms = [db_login["signon_realm"] for db_login in db_logins]
    unique_logins = []
    for login in logins_to_import:
        if login["signon_realm"] not in db_logins_signon_realms:
            unique_logins.append(login)
        else:
            print(CREDENTIALS_ALREADY_EXIST_MESSAGE.format(login["signon_realm"]))
    return unique_logins


def import_chrome_passwords(chrome_db_adapter: ChromeDBAdapter, source_file_path: str, file_adapter: file_adapter_interface) -> None:
    """Imports passwords to chrome db.
    :param chrome_db_adapter: Adapter for the chrome db
    :param source_file_path: Source file to import the passwords from
    :param file_adapter: Adapter to read the passwords from a file
    :return: None
    :rtype: None
    """
    if not os.path.exists(source_file_path):
        raise FileNotFoundError(source_file_path)
    logins_to_import = file_adapter.read(source_file_path, byte_columns=PASSWORDS_FILE_BYTES_COLUMNS)
    unique_logins_to_import = filter_existed_logins(chrome_db_adapter, logins_to_import)
    for login in unique_logins_to_import:
        chrome_db_adapter.logins_db.logins_table.insert_login(login)
