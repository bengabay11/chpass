# -*- coding: utf-8 -*-
"""
    chpass
    ~~~~~
    chpass is a package for gather information from Chrome.
    :copyright: 2020 Ben Gabay
    :license: MIT, see LICENSE for more details.
"""
__version__ = "0.4.2"

from .__main__ import start

from .services.chrome import (
    import_chrome_passwords,
    export_chrome_data,
    export_profile_picture,
    export_downloads,
    export_top_sites,
    export_history,
    export_passwords
)
from .services.path import get_chrome_user_folder, get_home_directory


def main():
    start()
