"""functions to handle configurations"""

configurations: dict[str, str] = {}


def _set_config_value(val: str) -> str:
    """removing - from strings"""
    if val.startswith("-"):
        return ""
    return val


def set_config(args: list[str]) -> str:
    """set config values"""
    for i in range(1, len(args) - 1):
        if not args[i].startswith("-"):
            continue
        configurations[args[i].strip("-")] = _set_config_value(args[i + 1])
    return "+OK"


def get_config(key: str) -> list[str]:
    """get config values"""
    return (
        [key, configurations[key]]
        if key in configurations
        else [key, "$-1"]  # "-ERR no matching key in configurations"]
    )
