"""functions for commands"""

# dictionary to store any data sent
datastore: dict[str, str] = {}


def ping() -> str:
    """return pong for ping command"""
    return "+PONG"


def echo(data: str) -> str:
    """return passed data to echo back to client"""
    return data


def set_data(data: list[str]) -> str:
    """setting data with key value pair"""
    key, val = data[:2]
    # options = data[2:]
    datastore[key] = val
    return "+OK"


def get_data(data: str) -> str:
    """getting data with specific key"""
    return datastore[data] if data in datastore else ""
