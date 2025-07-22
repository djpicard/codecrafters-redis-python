"""encode data to adhere to redis return values"""

def encode(val) -> str: # pylint: disable=too-many-return-statements,line-too-long
    """encode for redis protocol"""
    match (val):
        case bytes():
            return _bulk_resp(val)
        case str():
            return _simple_resp(val)
        case list():
            return _array_resp(val)
        case int():
            return _int_resp(val)
        case Exception():
            return _exception_resp(val)
        case None:
            return _null_resp()
        case _:
            return _exception_resp(Exception("-ERR Not all data types have been implemented"))

def _exception_resp(val: Exception):
    """exception resp"""
    print(val)
    print(val.args)
    return f"{val.args}\r\n"

def _null_resp() -> str:
    """null value"""
    return "$-1\r\n"


def _simple_resp(val: str) -> str:
    """simple string"""
    return f"+{val}\r\n"


def _bulk_resp(val: bytes) -> str:
    """simple resp"""
    value = val.decode()
    size = len(value)
    return f"${size}\r\n{value}\r\n"


def _array_resp(val: list[str]) -> str:
    """simple resp"""
    array_size = len(val)
    output = "".join([f"${len(x)}\r\n{x}\r\n" for x in val])
    return f"*{array_size}\r\n{output}"


def _int_resp(val: int) -> str:
    return f":{val}\r\n"
