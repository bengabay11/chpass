import pytest
from chpass.config import DEFAULT_EXPORT_DESTINATION_FOLDER


@pytest.fixture(scope="module")
def export_mode() -> str:
    return "export"


@pytest.fixture(scope="module")
def file_adapter_type() -> str:
    return "json"


@pytest.fixture(scope="module")
def destination_folder():
    return DEFAULT_EXPORT_DESTINATION_FOLDER


def test_default_export(export_mode):
    pass


def test_export_with_connected_user(export_mode, connected_user):
    pass


def test_export_with_disconnected_user(export_mode, disconnected_user):
    pass


def test_export_file_adapter(export_mode, file_adapter_type):
    pass


def test_export_destination_folder(export_mode, destination_folder):
    pass
