"""functions for commands"""

from app.classes.keystore import keystore
from app.classes.registry import registry


@registry.register("PING")
def ping() -> str:
    """return pong for ping command"""
    return "+PONG"

@registry.register("ECHO")
def echo(key: str) -> str:
    """return passed data to echo back to client"""
    return key

@registry.register("SET")
def set_key(key:str, value: str, args: str = "", px:int = -1):
    """setting data with specific key"""
    print(f"Setting key: {key}, value: {value}, px: {px}")
    return keystore.set(key, value, args, px)

@registry.register("GET")
def get_key(key: str | list[str]) -> str:
    """getting data with specific key"""
    print(f"Getting key: {key}")
    return keystore.get(key=key)
