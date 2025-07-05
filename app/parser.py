"""parsing redis protocol"""

import logging
import sys

import app.commands as cmd
import app.encoder as encoder

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


def parse(message: str) -> str:
    """parse full message received from client"""
    data = message.split("\r\n")
    logger.info(data)

    sym, val = data[0]
    if len(data[1:]) != (int(val) * 2 + 1):
        return "+Error\n\r"

    match sym:
        case "*":
            logger.info("Recieved array")
            return encoder.encode(parse_array(data[1:-1]))
        case _:
            logger.info("Bad command")

    return "Unknown command"


def _verify_size(size: str, data) -> bool:
    """checking the size of the data sent with the expected size"""
    sym, val = size
    if sym != "$":
        return False
    if int(val) != len(data):
        return False
    return True


def _get_commands(data: list[str]) -> list[str]:
    """splitting out each command and data pair"""
    if len(data) % 2 == 1:
        return []
    output = []
    for size, val in zip(data[::2], data[1::2]):
        if _verify_size(size, val):
            output.append(val)
    logger.info(output)
    return output


def parse_array(data: list[str]) -> str:
    """parse the command arrays"""
    logger.info(data)
    commands = _get_commands(data)
    results = ""
    match commands[0]:
        case "PING":
            results += cmd.ping()
        case "ECHO":
            results += cmd.echo(commands[1])
        case _:
            results += ""
    return results
