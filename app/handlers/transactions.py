"""transactions """

from app.classes.Keystore import keystore
from app.classes.Registry import registry


@registry.register("INCR")
def incr(key:str) -> int | str:
    """increment int value"""
    return keystore.incr(key=key)
