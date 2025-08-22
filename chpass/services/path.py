import getpass
import os
import sys

from chpass.config import (
    HISTORY_DB_FILE_NAME,
    LOGINS_DB_FILE_NAME,
    TOP_SITES_DB_FILE_NAME,
    GOOGLE_PICTURE_FILE_NAME,
    CHROME_FOLDER_OS_PATHS,
    DEFAULT_CHROME_PROFILE
)
from chpass.exceptions.chrome_not_installed_exception import ChromeNotInstalledException
from chpass.exceptions.operating_system_not_supported import OperatingSystemNotSupported
from chpass.exceptions.user_not_found_exception import UserNotFoundException


def get_home_directory(user: str = getpass.getuser()) -> str:
    """Get home directory path of the given user
    :param user: OS user
    :return: Home directory
    :rtype: str
    """
    home_directory = os.path.expanduser("~" + user)
    if not os.path.exists(home_directory):
        raise UserNotFoundException(user)
    return home_directory


def get_chrome_user_folder(user: str = getpass.getuser(), platform=sys.platform) -> str:
    """Get chrome folder path of the given user
    :param user: Chrome user
    :param platform: Operating system
    :return: Chrome user folder
    :rtype: str
    """
    home_directory = get_home_directory(user)
    if platform not in CHROME_FOLDER_OS_PATHS.keys():
        raise OperatingSystemNotSupported(platform)
    chrome_folder_path = CHROME_FOLDER_OS_PATHS[platform]
    chrome_user_folder = os.path.join(home_directory, chrome_folder_path)
    if not os.path.exists(chrome_user_folder):
        raise ChromeNotInstalledException(user)
    return chrome_user_folder


def get_chrome_history_path(user: str = getpass.getuser(), profile: str = DEFAULT_CHROME_PROFILE) -> str:
    return os.path.join(get_chrome_user_folder(user), profile, HISTORY_DB_FILE_NAME)


def get_chrome_logins_path(user: str = getpass.getuser(), profile: str = DEFAULT_CHROME_PROFILE) -> str:
    return os.path.join(get_chrome_user_folder(user), profile, LOGINS_DB_FILE_NAME)


def get_chrome_top_sites_path(user: str = getpass.getuser(), profile: str = DEFAULT_CHROME_PROFILE) -> str:
    return os.path.join(get_chrome_user_folder(user), profile, TOP_SITES_DB_FILE_NAME)


def get_chrome_profile_picture_path(user: str = getpass.getuser(), profile: str = DEFAULT_CHROME_PROFILE) -> str:
    return os.path.join(get_chrome_user_folder(user), profile, GOOGLE_PICTURE_FILE_NAME)
