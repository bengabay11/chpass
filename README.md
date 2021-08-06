[![Unit Tests](https://github.com/bengabay11/chpass/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/bengabay11/chpass/actions/workflows/unit-tests.yml)
[![Integration Tests](https://github.com/bengabay11/chpass/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/bengabay11/chpass/actions/workflows/integration-tests.yml)
[![python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/chpass/)
[![platform](https://img.shields.io/badge/platform-windows%20%7C%20ubuntu%20%7C%20macos-lightgrey)](https://pypi.org/project/chpass/)

# chpass
Gather information from Chrome 🔑

## Features
- import/export passwords
- history
- google account profile picture
- downloads
- top visited sites

## Installing
```bash
$ pip install chpass
```

## Usage
```bash
usage: chpass [-h] [-u USER] [-i FILE_ADAPTER] {import,export} ...
```
#### Export
```bash
usage: chpass export [-h] [-d DESTINATION_FOLDER] {passwords,history,downloads,top_sites,profile_pic} ...
```
#### Import
```bash
usage: chpass import [-h] -f FROM_FILE
```

## File adapters
`chpass` support read/write functionality with `csv` and `json`.

the default export and import is done with `csv`.

you can change the file adapter with the flag:
```bash
chpass -i json export
```

## Notes
> Chrome must be closed during the whole process, because its database is locked while running.

> In order to import the passwords successfully, Chrome must be restarted after the import to load the passwords from the database.

## License
This project is licensed under the terms of the MIT license.
