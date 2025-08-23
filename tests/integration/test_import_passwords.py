import pytest
from chpass.config import DEFAULT_EXPORT_DESTINATION_FOLDER


@pytest.fixture(scope="module")
def import_mode() -> str:
    return "import"


@pytest.fixture(scope="module")
def from_file():
    return DEFAULT_EXPORT_DESTINATION_FOLDER / "passwords.csv"


@pytest.fixture(scope="module")
def file_adapter_type() -> str:
    return "json"


def test_default_import(import_mode, from_file):
    pass


def test_import_with_connected_user(import_mode, from_file, connected_user):
    pass


def test_import_with_disconnected_user(import_mode, from_file, disconnected_user):
    pass


def test_export_file_adapter(import_mode, from_file, file_adapter_type):
    pass
