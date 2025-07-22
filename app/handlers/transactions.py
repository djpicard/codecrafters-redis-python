"""transactions """

from app.classes.Keystore import keystore
from app.classes.Registry import registry
from app.utils.encoder import encode


@registry.register("INCR")
def cmd_incr(key:str) -> int | str | Exception:
    """increment int value"""
    return keystore.incr(key=key)

@registry.register("MULTI")
def cmd_multi() -> str:
    """set transaction capture"""
    return "OK"

@registry.register("EXEC")
def cmd_exec() -> Exception :
    """handles bad exec command"""
    return Exception("-ERR EXEC without MULTI")

class Transaction:
    """class to handle a transaction"""
    def __init__(self):
        self._cmds: list[str] = []
        self._active: bool    = False

    async def queue(self, item: str) -> str | list[str]:
        """queue commands"""
        if "EXEC" in item.split("\r\n"):
            self.unset_active()
            return await self.__run__()
        self._cmds.append(item)
        return "QUEUED"

    def exec(self) -> str:
        """exec the transaction"""
        return ""

    def set_active(self) -> None:
        """setting transactions to actively capture"""
        self._active = True

    def unset_active(self) -> None:
        """unset transactions"""
        self._active = False

    def is_active(self) -> bool:
        """returns if the transaction is actively capturing records"""
        return self._active

    def _to_str(self, x, encoding='utf-8', errors='strict') -> str:
        """convert all values to string"""
        if isinstance(x, bytes):
            return x.decode(encoding, errors)
        return str(x)

    async def __run__(self) -> list[str]:
        """runs the saved commands"""
        output: list[str] = []
        for x in self._cmds:
            tmp = await registry.handle(x)
            output.append(encode(tmp))
        return output
