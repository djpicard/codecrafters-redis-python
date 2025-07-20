"""Redis Record"""

from datetime import datetime, timedelta, timezone
from enum import Enum


class Mode(Enum):
    """enum for mode types"""
    STRING     = "string"
    LIST    = "list"

class Record:
    """record to contain all data needed for a redis record"""

    def __init__(self, mode: Mode = Mode.STRING):
        """init record"""
        # sets mode for the key
        self.mode: Mode = mode
        match(self.mode):
            case Mode.STRING:
                self.value: str = ""
                self.px: int = -1
                self.timeout: float = 0
            case Mode.LIST:
                self.rlist: list[str] = []

    def clear_list(self) -> None:
        """clears the rlist if it exists"""
        if self.rlist:
            self.rlist.clear()

    def get(self) -> str:
        """default get data"""
        match(self.mode):
            case Mode.STRING:
                return self._get_key()
            case Mode.LIST:
                return self._get_list()

    def _get_list(self) -> str:
        """getting list data"""
        return f"{self.rlist}"

    def _get_key(self) -> str:
        """get the value if timeout has not expired"""
        if int(self.px) > 0:
            if self.timeout < datetime.now(timezone.utc).timestamp():
                return "$-1"
        return self.value

    def set(self, value:str, px: int = -1) -> None:
        """set command for all types that the record could contain"""
        self.set_key(value=value, px=px)

    def set_key(self, value: str, px: int = -1) -> None:
        """set value"""
        self.value: str     = value
        self.px: int        = px
        if int(self.px) > 0:
            self.timeout: float = (
                datetime.now(timezone.utc).now() + timedelta(milliseconds=int(self.px))
            ).timestamp()

    def push(self, value: str, right:bool) -> int:
        """push data into list"""
        if right:
            self.rlist.append(value)
        else:
            self.rlist.insert(0, value)
        return len(self.rlist)

    def __str__(self) -> str:
        return f"{self.value}, px: {self.px}, timeout: {self.timeout}"

    def __repr__(self) -> str:
        return f"{self.value}, px: {self.px}, timeout: {self.timeout}"

    def type(self) -> str:
        """getting data type for the record"""
        return self.mode.value

    def get_records(self, start:str, end:str) -> list[str]:
        """get a set of records"""
        if end == "-1":
            return self.rlist[int(start):]
        return self.rlist[int(start):int(end) + 1]
