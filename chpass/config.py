import os

CHROME_FOLDER_OS_PATHS = {
    "win32": r"AppData\Local\Google\Chrome\User Data",
    "linux": ".config/google-chrome",
    "linux2": ".config/google-chrome",
    "darwin": "Library/Application Support/Google/Chrome"
}

LOGINS_DB_FILE_PATH = "Login Data"
HISTORY_DB_FILE_PATH = "History"
TOP_SITES_DB_FILE_PATH = "Top Sites"
GOOGLE_PICTURE_FILE_PATH = "Google Profile Picture.png"

DEFAULT_EXPORT_DESTINATION_FOLDER = "dist"
OUTPUT_FILE_PATHS = {
    "csv": {
        "passwords": "passwords.csv",
        "history": "history.csv",
        "downloads": "downloads.csv",
        "top_sites": "top_sites.csv",
        "profile_picture": "profile.jpg"
    },
    "json": {
        "passwords": "passwords.json",
        "history": "history.json",
        "downloads": "downloads.json",
        "top_sites": "top_sites.json",
        "profile_picture": "profile.jpg"
    }
}
DB_PROTOCOL = "sqlite"

DEFAULT_FILE_ADAPTER = "csv"
CSV_ADAPTER_ENCODING = "utf-8"
DEFAULT_USER = "~"
WRITE_FILE_MODE = "w"

PASSWORDS_FILE_BYTES_COLUMNS = ["form_data", "password_value", "possible_username_pairs"]

CREDENTIALS_ALREADY_EXIST_MESSAGE = "Warning: credentials already exist on chrome for this user. url: {}"
