import pytest

from chpass.dal.db_connection import DBConnection


def test_connect_missing_database(tmp_path):
    db_conn = DBConnection()
    missing_db = tmp_path / "missing.db"
    with pytest.raises(FileNotFoundError):
        db_conn.connect("sqlite", str(missing_db))
