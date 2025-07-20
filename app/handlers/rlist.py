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

@registry.register("LRANGE")
def lrange(key:str, start: str, end:str) -> list[str]:
    """handle lrange and return list"""
    return keystore.lrange(key=key, start=start, end=end)
