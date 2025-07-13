"""parsing redis protocol"""

import logging
import sys

from app.classes.records import Record
from app.commands.executor import cmds
from app.utils import encoder

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=FORMAT)


def parse(message: str, keystore: dict[str, Record]) -> bytes:
    """parse full message received from client"""
    # getting tokens
    commands = [x for x in message.split("\r\n")[1:-1] if not x.startswith("$")]

    logger.debug(commands)
    return encoder.encode(cmds(commands=commands, keystore=keystore))
