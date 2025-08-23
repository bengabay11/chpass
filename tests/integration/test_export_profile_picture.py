import os

import pytest

from chpass.exceptions.chrome_profile_not_found_exception import ChromeProfileNotFoundException
from chpass import export_profile_picture


@pytest.fixture(scope="module")
def correct_destination_path() -> str:
    return "test_profile_picture.jpg"


@pytest.fixture
def profile_not_exist() -> str:
    return "not_exist"


def test_export_profile_picture_profile_not_exist(
    monkeypatch, tmp_path, correct_destination_path, profile_not_exist
):
    monkeypatch.setattr(
        "chpass.services.path.get_chrome_user_folder", lambda user: str(tmp_path)
    )
    with pytest.raises(ChromeProfileNotFoundException):
        export_profile_picture(correct_destination_path, "user", profile_not_exist)
    assert not os.path.exists(correct_destination_path)

