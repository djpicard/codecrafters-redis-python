"""encode data to adhere to redis return values"""

import logging
import sys

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


def encode(val: str | list[str]) -> str:
    """encode for redis protocol"""
    print(f"val to encode {val}")
    match (val):
        case str():
            return _simple_resp(val)
        case list():
            return _bulk_resp(val)
        case _:
            return _simple_resp("-ERR Not all data types have been implemented")


def _simple_resp(val: str) -> str:
    """simple resp"""
    size = len(val)
    if val.startswith("+") or val.startswith("$"):
        return f"{val}\r\n"
    if size <= 0:
        return "$-1\r\n"
    return f"${size}\r\n{val}\r\n"


def _bulk_resp(val: list[str]) -> str:
    """simple resp"""
    array_size = len(val)
    output = "".join([f"${len(x)}\r\n{x}\r\n" for x in val])
    print(f"output: {output}")
    return f"*{array_size}\r\n{output}"
