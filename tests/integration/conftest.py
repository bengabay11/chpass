import getpass

import pytest

from chpass.__main__ import create_chrome_db_adapter
from chpass.config import DB_PROTOCOL, DEFAULT_CHROME_PROFILE
from chpass.dal import chrome_db_adapter


@pytest.fixture(scope="session")
def connected_user() -> str:
    return getpass.getuser()


@pytest.fixture(scope="session")
def disconnected_user() -> str:
    return "Administrator"


@pytest.fixture(scope="session")
def chrome_db_adapter(request, connected_user) -> chrome_db_adapter:
    chrome_db_adapter = create_chrome_db_adapter(DB_PROTOCOL, connected_user, DEFAULT_CHROME_PROFILE)

    def fin():
        chrome_db_adapter.close()

    request.addfinalizer(fin)
    return chrome_db_adapter
