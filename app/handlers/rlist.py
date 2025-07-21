"""list functions"""

from app.classes.Keystore import keystore
from app.classes.Registry import registry


@registry.register("RPUSH")
async def rpush(rlist: str, *val: str) -> int:
    """handle rpush and return list size"""
    return await _push(rlist, True, *val)

@registry.register("LPUSH")
async def lpush(rlist: str, *val: str) -> int:
    """handle lpush and return list size"""
    return await _push(rlist, False, *val)

async def _push(rlist: str, right:bool, *val: str) -> int:
    """handle *push and return list size"""
    print(f"Val: {val}")
    output:int = 0
    for x in val:
        output = await keystore.push_list(key=rlist, value=x, right=right)
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
async def lpop(key:str, val:str = "") -> str | list[str]:
    """popping first element from list"""
    return await keystore.lpop(key=key, val=val)

@registry.register("BLPOP")
async def blpop(key:str, timeout:str = "") -> str | list[str]:
    """popping first element from list"""
    return await keystore.blpop(key=key, timeout=float(timeout))
