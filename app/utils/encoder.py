"""encode data to adhere to redis return values"""

def encode(val: str | list[str]) -> str:
    """encode for redis protocol"""
    match (val):
        case str():
            return _simple_resp(val)
        case list():
            return _bulk_resp(val)
        case int():
            return _int_resp(val)
        case _:
            return _simple_resp(
                "-ERR Not all data types have been implemented"
            )

def _simple_resp(val: str) -> str:
    """simple resp"""
    size = len(val)
    if val.startswith("+") or val.startswith("$") or val.startswith("-"):
        return f"{val}\r\n"
    if size <= 0:
        return "$-1\r\n"
    return f"${size}\r\n{val}\r\n"


def _bulk_resp(val: list[str]) -> str:
    """simple resp"""
    array_size = len(val)
    output = "".join([f"${len(x)}\r\n{x}\r\n" for x in val])
    return f"*{array_size}\r\n{output}"


def _int_resp(val: int) -> str:
    return f":{val}\r\n"
