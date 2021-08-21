import pytest

from chpass.cli import parse_args
from chpass.config import DEFAULT_FILE_ADAPTER


@pytest.fixture(scope="module")
def export_mode() -> str:
    return "export"


@pytest.fixture(scope="module")
def import_mode() -> str:
    return "import"


@pytest.fixture(scope="module")
def input_file_path() -> str:
    return "passwords.csv"


@pytest.fixture(scope="module")
def output_file() -> str:
    return "import"


@pytest.fixture
def correct_file_adapter() -> str:
    return "json"


def test_default_export(export_mode, connected_user, output_file):
    args = parse_args([export_mode, "-o", output_file])
    assert args.mode == export_mode
    assert args.user == connected_user
    assert args.output_file == output_file
    assert args.file_adapter == DEFAULT_FILE_ADAPTER
    assert not hasattr(args, "file_path")


def test_default_import(import_mode, connected_user, input_file_path):
    args = parse_args([import_mode, "-i", input_file_path])
    assert args.mode == import_mode
    assert args.user == connected_user
    assert not hasattr(args, "output_file")
    assert args.file_adapter == DEFAULT_FILE_ADAPTER
    assert args.input_file_path == input_file_path


def test_user_flag_export(export_mode, connected_user, output_file):
    user = connected_user
    args = parse_args(["-u", user, export_mode, "-o", output_file])
    assert args.mode == export_mode
    assert args.user == user


def test_mode_failed(connected_user):
    user = connected_user
    with pytest.raises(SystemExit):
        parse_args(["-u", user])


def test_export_output_flag_failed(export_mode, connected_user):
    user = connected_user
    with pytest.raises(SystemExit):
        parse_args(["-u", user, export_mode])


def test_import_input_flag_failed(import_mode, connected_user):
    user = connected_user
    with pytest.raises(SystemExit):
        parse_args(["-u", user, import_mode])


def test_user_flag_import(import_mode, connected_user, input_file_path):
    user = connected_user
    args = parse_args(["-u", user, import_mode, "-i", input_file_path])
    assert args.mode == import_mode
    assert args.user == user
    assert args.input_file_path == input_file_path


def test_file_adapter_flag_export(export_mode, correct_file_adapter, output_file):
    args = parse_args(["-f", correct_file_adapter, export_mode, "-o", output_file])
    assert args.mode == export_mode
    assert args.file_adapter == correct_file_adapter


def test_file_adapter_flag_import(import_mode, correct_file_adapter, input_file_path):
    args = parse_args(["-f", correct_file_adapter, import_mode, "-i", input_file_path])
    assert args.mode == import_mode
    assert correct_file_adapter == correct_file_adapter
    assert args.input_file_path == input_file_path
