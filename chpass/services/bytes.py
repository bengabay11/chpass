import ast
from typing import List, Callable


def convert_bytes_in_data(data: List[dict], convert_callback: Callable, byte_columns: list = None) -> List[dict]:
    if byte_columns is None:
        byte_columns = []
    for row in data:
        for byte_column in byte_columns:
            row[byte_column] = convert_callback(row[byte_column])
    return data


def str_bytes_to_bytes(str_bytes: str) -> bytes:
    return ast.literal_eval(str_bytes)
