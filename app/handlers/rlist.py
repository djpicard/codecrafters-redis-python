"""list functions"""

from app.classes.Keystore import keystore
from app.classes.Registry import registry


@registry.register("RPUSH")
def rpush(rlist: str, val: str) -> int:
    """handle rpush and return list size"""
    return keystore.push_list(key=rlist, value=val)
