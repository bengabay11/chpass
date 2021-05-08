import getpass

import pytest

from chpass.__main__ import create_chrome_db_adapter
from chpass.config import DB_PROTOCOL

from chpass.dal import ChromeDBAdapter


@pytest.fixture(scope="session")
def connected_user() -> str:
    return getpass.getuser()


@pytest.fixture(scope="session")
def chrome_db_adapter(request, connected_user) -> ChromeDBAdapter:
    chrome_db_adapter = create_chrome_db_adapter(DB_PROTOCOL, connected_user)

    def fin():
        chrome_db_adapter.close()

    request.addfinalizer(fin)
    return chrome_db_adapter
