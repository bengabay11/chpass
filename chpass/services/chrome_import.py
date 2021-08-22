import os
from typing import List


from chpass.dal.chrome_db_adapter import ChromeDBAdapter
from chpass.core.interfaces import file_adapter_interface
from chpass.config import PASSWORDS_FILE_BYTES_COLUMNS, CREDENTIALS_ALREADY_EXIST_MESSAGE
from chpass.services.encryption import get_master_key, decrypt_password
from chpass.services.zip import extract_file_from_zip


def import_chrome_passwords(
        chrome_user_folder: str,
        chrome_db_adapter: ChromeDBAdapter,
        source_file_path: str,
        file_adapter: file_adapter_interface) -> None:
    """Imports passwords to chrome db.
    :param chrome_user_folder: Local Chrome folder of the user
    :param chrome_db_adapter: Adapter for the chrome db
    :param source_file_path: Source file to import the passwords from
    :param file_adapter: Adapter to read the passwords from a file
    :return: None
    :rtype: None
    """
    if not os.path.exists(source_file_path):
        raise FileNotFoundError(source_file_path)
    extract_file_from_zip(source_file_path, "passwords.csv")
    logins = file_adapter.read("passwords.csv", byte_columns=PASSWORDS_FILE_BYTES_COLUMNS)
    os.remove("passwords.csv")
    unique_logins = filter_existed_logins(chrome_db_adapter, logins)
    master_key = get_master_key(chrome_user_folder)
    for login in unique_logins:
        login["password_value"] = decrypt_password(login["password_value"], master_key)
        chrome_db_adapter.logins_db.logins_table.insert_login(login)


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
