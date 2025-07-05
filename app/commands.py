"""functions for commands"""

import logging
import sys

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


def ping() -> str:
    """return pong for ping command"""
    return "PONG"


def echo(data: str) -> str:
    """return passed data to echo back to client"""
    return data
