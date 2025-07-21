"""transactions """

from app.classes.Keystore import keystore
from app.classes.Registry import registry


@registry.register("INCR")
def incr(key:str) -> int | str:
    """increment int value"""
    return keystore.incr(key=key)

@registry.register("MULTI")
def multi() -> str:
    """set transaction capture"""
    transaction.active = True
    return "+OK"

class Transaction:
    """class to handle a transaction"""
    def __init__(self):
        self.cmds: list[str] = []
        self.active: bool    = False

    def queue(self, item: str) -> str:
        """queue commands"""
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

transaction = Transaction()
