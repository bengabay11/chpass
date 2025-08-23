import getpass
import os
import sys
from typing import List

from chpass.config import (
    HISTORY_DB_FILE_NAME,
    LOGINS_DB_FILE_NAME,
    TOP_SITES_DB_FILE_NAME,
    GOOGLE_PICTURE_FILE_NAME,
    CHROME_FOLDER_OS_PATHS,
    DEFAULT_CHROME_PROFILE,
    GUEST_CHROME_PROFILE,
    SYSTEM_CHROME_PROFILE,
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


def get_chrome_profiles(user: str = getpass.getuser(), platform: str = sys.platform) -> List[str]:
    """Get all chrome profiles of the given user.

    Chrome profile directories typically use one of the following names:

    * ``Default`` – the first profile created when Chrome is installed.
    * ``Profile <number>`` – additional profiles created by the user.
    * ``Guest Profile`` – a temporary profile created for guest sessions.
    * ``System Profile`` – profile used internally by Chrome.

    :param user: Chrome user
    :param platform: Operating system
    :return: List of chrome profiles names
    :rtype: list[str]
    """
    chrome_user_folder = get_chrome_user_folder(user, platform)
    profiles = []
    for entry in os.listdir(chrome_user_folder):
        profile_path = os.path.join(chrome_user_folder, entry)
        if not os.path.isdir(profile_path):
            continue
        if entry in (DEFAULT_CHROME_PROFILE, GUEST_CHROME_PROFILE, SYSTEM_CHROME_PROFILE):
            profiles.append(entry)
        elif entry.startswith("Profile ") and entry[8:].isdigit():
            profiles.append(entry)
    return sorted(profiles)
