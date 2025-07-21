"""functions to handle configurations"""

from app.classes.Keystore import keystore
from app.classes.Registry import registry


# configs
@registry.register("CONFIG")
def configs(cmd: str, key:str, val:str = "") -> list[str] | str:
    """config subcommands"""
    print(f"config command: {cmd}, val: {val}")
    match cmd:
        case "GET":
            return get_config(key=key)
        case "SET":
            return set_config(key=key, val=val)
        case _:
            return "-ERR Unimplemented config command"

def set_config(key: str, val: str) -> list[str] | str:
    """get config values"""
    keystore.set(key=key, value=val)
    if keystore.key_exists(key=key):
        return "+OK"
    return "$-1"


def get_config(key: str) -> list[str] | str:
    """get config values"""
    print(f"config get key: {key}")
    if keystore.key_exists(key=key):
        return [key, keystore.get(key=key)]
    return "$-1"  # "-ERR no matching key in configurations"]
