"""encode data to adhere to redis return values"""

import logging
import sys

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


def encode(val: str) -> str:
    """encode for redis protocol"""
    size = len(val)
    if val == "PONG":
        return "+PONG\r\n"
    return f"${size}\r\n{val}\r\n"
