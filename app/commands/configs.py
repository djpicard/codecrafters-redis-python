"""functions to handle configurations"""

from app.classes.records import Record  # pylint: disable=import-error


# configs
def configs(data: list[str], keystore: dict[str, Record]) -> list[str] | str:
    """config subcommands"""
    cmd = data[0]
    match cmd:
        case "GET":
            return get_config(data[1], keystore)
        case "SET":
            return set_config(data[1:], keystore)
        case _:
            return "-ERR Unimplemented config command"


def set_config(data: list[str], keystore: dict[str, Record]) -> list[str] | str:
    """get config values"""
    key = data[0]
    val = data[1]
    keystore[key] = Record(value=val)
    if key in keystore:
        return "+OK"
    return "$-1"


def get_config(key: str, keystore: dict[str, Record]) -> list[str] | str:
    """get config values"""
    if key in keystore:
        return [key, keystore[key].get()]
    return "$-1"  # "-ERR no matching key in configurations"]
