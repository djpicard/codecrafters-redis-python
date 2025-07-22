"""functions for commands"""

from app.classes.Keystore import keystore
from app.classes.Registry import registry


@registry.register("PING")
def ping() -> str:
    """return pong for ping command"""
    return "PONG"

@registry.register("ECHO")
def echo(key: str) -> bytes:
    """return passed data to echo back to client"""
    return key.encode()

@registry.register("SET")
def set_key(key:str, value: str, args: str = "", px:int = -1):
    """setting data with specific key"""
    return keystore.set(key, value, args, px)

@registry.register("GET")
def get_key(key: str | list[str]) -> bytes | None:
    """getting data with specific key"""
    return keystore.get(key=key)

@registry.register("TYPE")
def get_type(key: str) -> str:
    """getting type for the specific key"""
    return keystore.get_type(key=key)
