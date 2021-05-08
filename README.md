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
you can also clone the repo and install locally:
```bash
scripts/install.sh
```
## Usage
export the user passwords:
```bash
chpass export
```
the file will be saved under `dist/passwords.csv`

import the passwords:
```bash
chpass import -f passwords.csv
```

## File adapters
`chpass` support read/write functionality with `csv` and `json`.

the default export and import is done with `csv`.

you can change the file adapter with the flag:
```bash
chpass -i json export
```

## Requirements
- Python 3.6+
- Chrome 84.0+
- Windows 10/macOS/Linux

## Notes
> Chrome must be closed during the whole process, because its database is locked while running.

> In order to import the passwords successfully, Chrome must be restarted after the import to load the passwords from the database.

## License
This project is licensed under the terms of the MIT license.
