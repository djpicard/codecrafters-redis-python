"""list functions"""

from ..Keystore import keystore
from ..Registry import registry


@registry.register("RPUSH")
def rpush(rlist: str, *val: str) -> int:
    """handle rpush and return list size"""
    print(f"Val: {val}")
    output:int = 0
    for x in val:
        output = keystore.push_list(key=rlist, value=x)
    return output
