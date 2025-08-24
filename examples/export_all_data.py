"""Export all Chrome data to a folder using chpass."""

import getpass

from chpass.__main__ import create_chrome_db_adapter, create_file_adapter
from chpass.config import DB_PROTOCOL, OUTPUT_FILE_PATHS, DEFAULT_CHROME_PROFILE
from chpass.services.chrome import export_chrome_data

def main() -> None:
    """Export passwords, history, downloads, top sites and profile picture.

    Data is written for the current user into the "backup" folder using CSV
    format. Chrome must be closed while this runs.
    """
    file_adapter = create_file_adapter("csv")
    chrome_db_adapter = create_chrome_db_adapter(
        DB_PROTOCOL, getpass.getuser(), DEFAULT_CHROME_PROFILE
    )
    try:
        export_chrome_data(
            chrome_db_adapter,
            "backup",
            file_adapter,
            OUTPUT_FILE_PATHS["csv"],
        )
    finally:
        chrome_db_adapter.close()


if __name__ == "__main__":
    main()
