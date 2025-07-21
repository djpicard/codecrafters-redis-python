"""transactions """

from app.classes.Keystore import keystore
from app.classes.Registry import registry


@registry.register("INCR")
def cmd_incr(key:str) -> int | str:
    """increment int value"""
    return keystore.incr(key=key)

@registry.register("MULTI")
def cmd_multi() -> str:
    """set transaction capture"""
    transaction.active = True
    return "+OK"

@registry.register("EXEC")
def cmd_exec() -> str :
    """handles bad exec command"""
    return "-ERR EXEC without MULTI"

class Transaction:
    """class to handle a transaction"""
    def __init__(self):
        self.cmds: list[str] = []
        self.active: bool    = False

    async def queue(self, item: str) -> str | list[str]:
        """queue commands"""
        if "EXEC" in item.split("\r\n"):
            self.unset_active()
            return await self.__run__()
        self.cmds.append(item)
        return "QUEUED"

    def exec(self) -> str:
        """exec the transaction"""
        return ""

    def set_active(self) -> None:
        """setting transactions to actively capture"""
        self.active = True

    def unset_active(self) -> None:
        """unset transactions"""
        self.active = False

    def is_active(self) -> bool:
        """returns if the transaction is actively capturing records"""
        return self.active

    async def __run__(self) -> list[str]:
        """runs the saved commands"""
        output: list[str] = []
        for x in self.cmds:
            output.append(await registry.handle(x))
        return output

transaction = Transaction()
