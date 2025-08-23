from unittest.mock import MagicMock

from chpass.services.chrome import export_chrome_data, import_chrome_passwords


def test_export_passwords_message(tmp_path, capsys):
    chrome_db_adapter = MagicMock()
    chrome_db_adapter.logins_db.logins_table.get_all_logins.return_value = []
    file_adapter = MagicMock()
    output_file_paths = {
        "passwords": "passwords.csv",
        "history": "history.csv",
        "downloads": "downloads.csv",
        "top_sites": "top.csv",
        "profile_picture": "profile.png",
    }
    export_chrome_data(chrome_db_adapter, str(tmp_path), file_adapter, output_file_paths, export_kind="passwords")
    captured = capsys.readouterr()
    assert "[+] Exported 'passwords' to" in captured.out
    assert str(tmp_path) in captured.out


def test_import_passwords_message(tmp_path, capsys):
    chrome_db_adapter = MagicMock()
    chrome_db_adapter.logins_db.logins_table.get_all_logins.return_value = []
    file_adapter = MagicMock()
    file_adapter.read.return_value = []
    source_file = tmp_path / "passwords.csv"
    source_file.write_text("")
    import_chrome_passwords(chrome_db_adapter, str(source_file), file_adapter)
    captured = capsys.readouterr()
    assert "[+] Imported 0 credentials from" in captured.out
    assert str(source_file) in captured.out
