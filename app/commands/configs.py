"""functions to handle configurations"""


# configs
def configs(data: list[str], keystore: dict) -> list[str] | str:
    """config subcommands"""
    cmd = data[0]
    print(data)
    match cmd:
        case "GET":
            return get_config(data[1], keystore)
        case "SET":
            return set_config(data[1:], keystore)
        case _:
            return "-ERR Unimplemented config command"


def set_config(data: list[str], keystore: dict) -> list[str] | str:
    """get config values"""
    key = data[0]
    val = data[1]
    keystore[key] = val
    if key in keystore:
        return "+OK"
    return "$-1"


def get_config(key: str, keystore: dict) -> list[str] | str:
    """get config values"""
    if key in keystore:
        return [key, keystore[key]]
    return "$-1"  # "-ERR no matching key in configurations"]
