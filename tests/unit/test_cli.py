import pytest

from chpass.cli import parse_args
from chpass.config import DEFAULT_EXPORT_DESTINATION_FOLDER, DEFAULT_FILE_ADAPTER


@pytest.fixture(scope="module")
def export_mode() -> str:
    return "export"


@pytest.fixture(scope="module")
def import_mode() -> str:
    return "import"


@pytest.fixture(scope="module")
def from_file() -> str:
    return "passwords.csv"


def test_default_export(export_mode, connected_user):
    args = parse_args([export_mode])
    assert args.mode == export_mode
    assert args.user == connected_user
    assert args.destination_folder == DEFAULT_EXPORT_DESTINATION_FOLDER
    assert args.file_adapter == DEFAULT_FILE_ADAPTER
    assert args.profile == "Default"
    assert not hasattr(args, "from_file")


def test_default_import(import_mode, connected_user, from_file):
    args = parse_args([import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert args.user == connected_user
    assert not hasattr(args, "destination_folder")
    assert args.file_adapter == "csv"
    assert args.profile == "Default"
    assert args.from_file == from_file


def test_user_flag_export(export_mode, connected_user):
    user = connected_user
    args = parse_args(["-u", user, export_mode])
    assert args.mode == export_mode
    assert args.user == user
    assert args.profile == "Default"


def test_user_flag_import(import_mode, from_file, connected_user):
    user = connected_user
    args = parse_args(["-u", user, import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert args.user == user
    assert args.profile == "Default"


def test_file_adapter_flag_export(export_mode):
    file_adapter = export_mode
    args = parse_args(["-i", file_adapter, export_mode])
    assert args.mode == export_mode
    assert args.file_adapter == file_adapter
    assert args.profile == "Default"


@pytest.fixture
def correct_file_adapter() -> str:
    return "json"


def test_file_adapter_flag_import(import_mode, correct_file_adapter, from_file):
    args = parse_args(["-i", correct_file_adapter, import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert correct_file_adapter == correct_file_adapter
    assert args.profile == "Default"


@pytest.fixture
def correct_destination_folder() -> str:
    return "test"


def test_export_destination_folder_flag(export_mode, correct_destination_folder):
    args = parse_args([export_mode, "-d", correct_destination_folder])
    assert args.mode == export_mode
    assert args.destination_folder == correct_destination_folder
    assert args.profile == "Default"


def test_profile_flag_export(export_mode):
    profile = "Profile 1"
    args = parse_args(["-p", profile, export_mode])
    assert args.mode == export_mode
    assert args.profile == profile


def test_profile_flag_import(import_mode, from_file):
    profile = "Profile 1"
    args = parse_args(["-p", profile, import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert args.profile == profile


def test_profile_flag_no_value_export(export_mode, connected_user):
    args = parse_args(["-p", "-u", connected_user, export_mode])
    assert args.mode == export_mode
    assert args.profile == "Default"


def test_profile_flag_no_value_import(import_mode, from_file, connected_user):
    args = parse_args(["-p", "-u", connected_user, import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert args.profile == "Default"
