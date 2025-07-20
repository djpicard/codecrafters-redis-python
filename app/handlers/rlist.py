"""list functions"""

from ..Keystore import keystore
from ..Registry import registry


@registry.register("RPUSH")
def rpush(rlist: str, val: tuple[str, ...]) -> int:
    """handle rpush and return list size"""
    print(f"Val: {val}")
    return keystore.push_list(key=rlist, value=val)
