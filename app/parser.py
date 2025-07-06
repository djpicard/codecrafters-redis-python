"""parsing redis protocol"""

import logging
import sys

from app import commands as cmd
from app import encoder

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


def parse(message: str) -> str:
    """parse full message received from client"""
    data = message.split("\r\n")
    #
    # data 0 - type of message and how many words + word length
    # data 1::2 - the length of each word denoted as $<int>
    # data 2::2 - actual data with data[2] being the command sent
    #
    logger.debug(data)

    sym, val = data[0]
    res, err = _check_data(
        data=data[1:-1], length=val
    )  # verify that the sent command is properly formated
    if not res:
        return err

    match sym:
        case "*":
            return encoder.encode(
                parse_cmd(data[2::2])
            )  # we only need the command and arguments which are every odd number in the array
        case _:
            logger.debug("Bad command")
            return "-ERR Command Not Impemented"

    return "-ERR Unknown command"


def parse_cmd(data: list[str]) -> str:
    """parse the command arrays"""
    logger.debug("Command data: %s", data)
    results = ""
    match data[0]:  # checking the instruction sent by the client
        case "PING":
            results += cmd.ping()
        case "ECHO":
            results += cmd.echo(data[1])  # returning the same value sent by the client
        case "GET":
            results += cmd.get_data(data[1])
        case "SET":
            results += cmd.set_data(data[1:])
        case _:
            results += ""
    return results


def _check_data(data: list[str], length: str) -> tuple[bool, str]:
    """verify that the incoming data is valid"""
    if len(data) != (int(length) * 2):
        return False, "-ERR command doesn't match given size"
    if len(data) % 2 == 1:
        return False, "-ERR bad format or missing data"
    for size, val in zip(data[::2], data[1::2]):
        if not _verify_size(size, val):
            return False, "-ERR data does not match given size"
    return True, ""


def _verify_size(size: str, data) -> bool:
    """checking the size of the data sent with the expected size"""
    if size == "":
        return False
    sym, val = size
    if sym != "$":
        return False
    if int(val) != len(data):
        return False
    return True
