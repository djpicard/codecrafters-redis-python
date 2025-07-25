"""Stream Support"""

from app.classes.Keystore import keystore
from app.classes.Registry import registry


@registry.register("XADD")
def cmd_xadd(key: str, entry_id: str, *args:str):
    """handle xadd commands"""
    print(f"key: {key}, entry: {entry_id}, args: {args}")
    return keystore.xadd(key, entry_id, args)
