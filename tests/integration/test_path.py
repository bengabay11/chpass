import os

import pytest

from chpass.exceptions.operating_system_not_supported import OperatingSystemNotSupported
from chpass.exceptions.user_not_found_exception import UserNotFoundException
from chpass.services.path import get_home_directory, get_chrome_user_folder


@pytest.fixture(scope="module")
def invalid_os() -> int:
    return -1


@pytest.fixture(scope="module")
def os_not_exist() -> str:
    return "ChromeOS"


def test_get_home_directory(connected_user):
    home_directory = get_home_directory(connected_user)
    assert os.path.basename(home_directory) == connected_user
    assert os.path.exists(home_directory)


@pytest.fixture
def user_not_exist() -> str:
    return "not_exist"


def test_get_home_directory_user_not_exist(user_not_exist):
    with pytest.raises(UserNotFoundException):
        get_home_directory(user_not_exist)


@pytest.fixture
def invalid_user() -> int:
    return -1


def test_get_home_directory_invalid_user(invalid_user):
    with pytest.raises(TypeError):
        get_home_directory(invalid_user)


def test_get_chrome_user_folder(connected_user):
    chrome_user_folder = get_chrome_user_folder(connected_user)
    assert os.path.exists(chrome_user_folder)


def test_get_chrome_user_folder_os_not_exist(connected_user, os_not_exist):
    with pytest.raises(OperatingSystemNotSupported):
        get_chrome_user_folder(connected_user, platform=os_not_exist)


def test_get_chrome_user_folder_invalid_os(connected_user, invalid_os):
    with pytest.raises(OperatingSystemNotSupported):
        get_chrome_user_folder(connected_user, platform=invalid_os)
