"""Redis Record"""

import asyncio
from collections import deque
from datetime import datetime, timedelta, timezone
from enum import Enum


class Mode(Enum):
    """enum for mode types"""
    STRING  = "string"
    LIST    = "list"
    INT     = "int"

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
                self.rlist: deque[str] = deque()
                self._waiters: deque[asyncio.Future[str]] = deque()
            case Mode.INT:
                self.int_val: int = 0

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
            case Mode.INT:
                return self._get_int()

    def _get_int(self) -> str:
        """getting int data"""
        return f"{self.int_val}"

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

    async def push(self, value: str, right:bool) -> int:
        """push data into list"""
        if right:
            self.rlist.append(value)
        else:
            self.rlist.appendleft(value)
        output = len(self.rlist)

        while self._waiters:
            future = self._waiters.popleft()
            if not future.done():
                future.set_result(self.rlist.popleft())
                return output

        return output

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
            return list(self.rlist)[int(start):]
        return list(self.rlist)[int(start):int(end) + 1]

    def length(self) -> int:
        """get length of list"""
        return len(self.rlist)

    def mpop(self, val:int) -> list[str]:
        """pop multiple values"""
        output: list[str] = []
        for _ in range(val):
            output.append(self.rlist.popleft())
        return output

    def pop(self) -> str:
        """popping first element from list"""
        return self.rlist.popleft()

    async def blpop(self, timeout:float = 0.0) -> str:
        """blocking pop"""
        if self.rlist:
            return self.rlist.popleft()

        loop = asyncio.get_event_loop()
        future: asyncio.Future[str] = loop.create_future()
        self._waiters.append(future)

        try:
            print(f"timeout: {timeout}")
            if timeout and timeout > 0:
                return await asyncio.wait_for(future, float(timeout))
            return await future # pylint: disable=line-too-long
        except asyncio.TimeoutError:
            self._waiters.remove(future)
            return "$-1"

    def incr(self) -> int:
        """increment int value"""
        print(self.mode)
        self.int_val += 1
        return self.int_val
