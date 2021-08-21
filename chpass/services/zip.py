from typing import List
from zipfile import ZipFile


def get_file_from_zip(zip_path: str, filename) -> None:
    zip_file = ZipFile(zip_path)
    return zip_file.read(filename)


def zip_files(zip_path: str, file_paths: List[str]) -> None:
    with ZipFile(zip_path, "w") as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path)
