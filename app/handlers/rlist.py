"""list functions"""

from ..Keystore import keystore
from ..Registry import registry


@registry.register("RPUSH")
def rpush(rlist: str, *val: str) -> int:
    """handle rpush and return list size"""
    return _push(rlist, True, *val)

@registry.register("LPUSH")
def lpush(rlist: str, *val: str) -> int:
    """handle lpush and return list size"""
    return _push(rlist, False, *val)

def _push(rlist: str, right:bool, *val: str) -> int:
    """handle rpush and return list size"""
    print(f"Val: {val}")
    output:int = 0
    for x in val:
        output = keystore.push_list(key=rlist, value=x, right=right)
    return output

@registry.register("LRANGE")
def lrange(key:str, start: str, end:str) -> list[str]:
    """handle lrange and return list"""
    return keystore.lrange(key=key, start=start, end=end)

@registry.register("LLEN")
def length(key:str) -> int:
    """get length of list"""
    return keystore.length(key=key)

@registry.register("LPOP")
def lpop(key:str, val:str = "") -> str | list[str]:
    """popping first element from list"""
    return keystore.lpop(key=key, val=val)
