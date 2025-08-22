import pytest

from chpass.cli import parse_args
from chpass.config import (
    DEFAULT_CHROME_PROFILE,
    DEFAULT_EXPORT_DESTINATION_FOLDER,
    DEFAULT_FILE_ADAPTER,
)


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
    assert args.profile == DEFAULT_CHROME_PROFILE
    assert not hasattr(args, "from_file")


def test_default_import(import_mode, connected_user, from_file):
    args = parse_args([import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert args.user == connected_user
    assert not hasattr(args, "destination_folder")
    assert args.file_adapter == "csv"
    assert args.from_file == from_file
    assert args.profile == DEFAULT_CHROME_PROFILE


def test_user_flag_export(export_mode, connected_user):
    user = connected_user
    args = parse_args(["-u", user, export_mode])
    assert args.mode == export_mode
    assert args.user == user
    assert args.profile == DEFAULT_CHROME_PROFILE


def test_user_flag_import(import_mode, from_file, connected_user):
    user = connected_user
    args = parse_args(["-u", user, import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert args.user == user
    assert args.profile == DEFAULT_CHROME_PROFILE


def test_file_adapter_flag_export(export_mode):
    file_adapter = export_mode
    args = parse_args(["-i", file_adapter, export_mode])
    assert args.mode == export_mode
    assert args.file_adapter == file_adapter
    assert args.profile == DEFAULT_CHROME_PROFILE


@pytest.fixture
def correct_file_adapter() -> str:
    return "json"


def test_file_adapter_flag_import(import_mode, correct_file_adapter, from_file):
    args = parse_args(["-i", correct_file_adapter, import_mode, "-f", from_file])
    assert args.mode == import_mode
    assert correct_file_adapter == correct_file_adapter
    assert args.profile == DEFAULT_CHROME_PROFILE


@pytest.fixture
def correct_destination_folder() -> str:
    return "test"


def test_export_destination_folder_flag(export_mode, correct_destination_folder):
    args = parse_args([export_mode, "-d", correct_destination_folder])
    assert args.mode == export_mode
    assert args.destination_folder == correct_destination_folder
    assert args.profile == DEFAULT_CHROME_PROFILE


def test_profile_flag(export_mode):
    profile = "Profile 1"
    args = parse_args(["-p", profile, export_mode])
    assert args.mode == export_mode
    assert args.profile == profile


def test_list_profiles(connected_user):
    args = parse_args(["list-profiles"])
    assert args.mode == "list-profiles"
    assert args.user == connected_user
    assert args.profile == DEFAULT_CHROME_PROFILE


@pytest.mark.parametrize(
    "export_kind",
    ["passwords", "history", "downloads", "top_sites", "profile_pic"],
)
def test_export_subcommands(export_kind):
    args = parse_args(["export", export_kind])
    assert args.mode == "export"
    assert args.export_kind == export_kind
    assert args.destination_folder == DEFAULT_EXPORT_DESTINATION_FOLDER
    assert args.profile == DEFAULT_CHROME_PROFILE
