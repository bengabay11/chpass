import chpass.services.path as path


def test_get_chrome_profiles_recognizes_common_profiles(tmp_path, monkeypatch):
    """Ensure common Chrome profile names are detected."""
    profiles = [
        path.DEFAULT_CHROME_PROFILE,
        "Profile 1",
        path.GUEST_CHROME_PROFILE,
        path.SYSTEM_CHROME_PROFILE,
        "NotAProfile",
    ]
    for name in profiles:
        (tmp_path / name).mkdir()
    monkeypatch.setattr(path, "get_chrome_user_folder", lambda u, p: str(tmp_path))
    expected = [
        path.DEFAULT_CHROME_PROFILE,
        path.GUEST_CHROME_PROFILE,
        "Profile 1",
        path.SYSTEM_CHROME_PROFILE,
    ]
    assert path.get_chrome_profiles("user") == expected
