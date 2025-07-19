"""Redis Record"""

from datetime import datetime, timedelta, timezone


class Record:
    """record to contain all data needed for a redis record"""

    def __init__(self, value: str, px: int = -1):
        """init record"""
        self.set(value=value, px=px)

    def get(self) -> str:
        """get the value if timeout has not expired"""
        print("Getting Value from record: " +
              f"{self.value}, {self.timeout}, " +
              f"{datetime.now(timezone.utc).timestamp()}")
        if self.px != -1:
            if self.timeout < datetime.now(timezone.utc).timestamp():
                print(f"Record timeout for {self.value}")
                return "$-1"
        return self.value

    def set(self, value: str, px: int = -1) -> None:
        """set value"""
        self.value = value
        self.px = px
        self.timeout = (
            datetime.now(timezone.utc).now() + timedelta(milliseconds=self.px)
        ).timestamp()

    def __str__(self) -> str:
        return f"{self.value}, px: {self.px}, timeout: {self.timeout}"

    def __repr__(self) -> str:
        return f"{self.value}, px: {self.px}, timeout: {self.timeout}"
