"""functions to handle configurations"""

configurations: dict[str, str] = {}


def reset_configs() -> str:
    """resetting configs"""
    configurations.clear()
    print(f"configuration reset {configurations}")
    return "+OK"


def _set_config_value(val: str) -> str:
    """removing - from strings"""
    if val.startswith("-"):
        return ""
    return val


def set_config_on_start(args: list[str]) -> str:
    """set config values"""
    for i in range(1, len(args) - 1):
        if not args[i].startswith("-"):
            continue
        configurations[args[i].strip("-")] = _set_config_value(args[i + 1])
    return "+OK"


def set_config(data: list[str]) -> list[str] | str:
    """get config values"""
    key = data[0]
    val = data[1]
    print(f"Configs: {configurations}, data: {key}, val: {val}")
    configurations[key] = val
    if key in configurations:
        return "+OK"
    return "$-1"


def get_config(key: str) -> list[str] | str:
    """get config values"""
    print(f"Configs: {configurations}, key: {key}")
    if key in configurations:
        return [key, configurations[key]]
    return "$-1"  # "-ERR no matching key in configurations"]
