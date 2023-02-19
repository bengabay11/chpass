import os
from typing import List

import pytest

from chpass.services.file_adapters.csv_file_adapter import CsvFileAdapter
from chpass.services.file_adapters.json_file_adapter import JsonFileAdapter


@pytest.fixture(scope="module")
def correct_data_list() -> List[dict]:
    return [{
        "column1": "value1",
        "column2": "value2",
        "column3": "value3"
    }]


@pytest.fixture(scope="module")
def invalid_data_list() -> str:
    return "invalid data list"


@pytest.fixture(scope="module")
def not_exist_output_file_path() -> str:
    return "not_exist/test"


@pytest.fixture(scope="module")
def invalid_output_file_path() -> int:
    return -1


@pytest.mark.parametrize("file_adapter, output_file_path", [(CsvFileAdapter(), "test.csv"), (JsonFileAdapter(), "test.json")])
def test_csv_write(file_adapter, output_file_path, correct_data_list):
    file_adapter.write(correct_data_list, output_file_path)
    assert os.path.exists(output_file_path)


@pytest.mark.parametrize("file_adapter, output_file_path", [(CsvFileAdapter(), "test.csv"), (JsonFileAdapter(), "test.json")])
def test_csv_read(file_adapter, output_file_path, correct_data_list):
    result_correct_data_list = file_adapter.read(output_file_path)
    assert result_correct_data_list == correct_data_list
    os.remove(output_file_path)


@pytest.mark.parametrize("file_adapter", [CsvFileAdapter(), JsonFileAdapter()])
def test_csv_write_output_file_path_not_exist(file_adapter, not_exist_output_file_path, correct_data_list):
    with pytest.raises(OSError):
        file_adapter.write(correct_data_list, not_exist_output_file_path)
    assert not os.path.exists(not_exist_output_file_path)


@pytest.mark.parametrize("file_adapter", [CsvFileAdapter(), JsonFileAdapter()])
def test_csv_write_invalid_output_file_path(file_adapter, invalid_output_file_path, correct_data_list):
    with pytest.raises(ValueError):
        file_adapter.write(correct_data_list, invalid_output_file_path)
    assert not os.path.exists(invalid_output_file_path)


@pytest.mark.parametrize("file_adapter, output_file_path", [(CsvFileAdapter(), "test.csv"), (JsonFileAdapter(), "test.json")])
def test_csv_write_invalid_data_list(file_adapter, output_file_path, invalid_data_list):
    with pytest.raises(ValueError):
        file_adapter.write(invalid_data_list, output_file_path)
    assert not os.path.exists(output_file_path)
