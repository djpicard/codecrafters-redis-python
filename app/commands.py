"""functions for commands"""

from datetime import datetime, timedelta, timezone

from app.configurations import get_config, reset_configs, set_config

# dictionary to store any data sent
datastore: dict[str, dict[str, str]] = {}


# utils
def reset_datastore() -> None:
    """reset the datastore on restart"""
    datastore.clear()


def ping() -> str:
    """return pong for ping command"""
    return "+PONG"


def echo(data: str) -> str:
    """return passed data to echo back to client"""
    return data


# data
def set_data(data: list[str]) -> str | list[str]:
    """setting data with key value pair"""
    key = data[0]
    options = data[1:]

    # set record and put it into the datastore
    record: dict[str, str] = _set_options(options=options)
    datastore[key] = record
    if datastore[key] != record:
        return "$-1"  # "-ERR unable to set record into the datastore"
    return "+OK"


def get_data(key: str) -> str:
    """getting data with specific key"""
    if not key in datastore:
        return "$-1"  # "-ERR Key not found in datastore"
    # data is stored in a dictionary
    # key is a str
    # data is stored as a dict[str, object])
    record = datastore[key]
    result = "-ERR No matching data found"
    for x, y in record.items():
        match x:
            case "px":
                currtime = datetime.now().timestamp()
                if currtime > float(y):
                    return "$-1"  # "-ERR record timed out"
            case "value":
                result = y
    return result


def _set_options(options: list[str]) -> dict[str, str]:
    """parse options given to the datastore"""
    it = iter(options)
    result: dict[str, str] = {}  # adding value for record
    for x in it:  # adding options for record
        match x.lower():
            case "px":
                px = datetime.now(timezone.utc).now() + timedelta(
                    milliseconds=int(next(it))
                )
                result["px"] = f"{px.timestamp()}"
            case _:
                result["value"] = x
    return result


# configs
def configs(data: list[str]) -> list[str] | str:
    """config subcommands"""
    cmd = data[0]
    match cmd:
        case "GET":
            return get_config(data[1])
        case "SET":
            return set_config(data[1:])
        case "RESET":
            return reset_configs()
        case _:
            return "-ERR Unimplemented config command"
