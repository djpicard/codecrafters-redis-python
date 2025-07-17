"""functions for commands"""

from app.classes.records import Record
from app.commands import rdb
from app.commands.configs import configs  # get_config, set_config
from app.commands.info import info, init_repl


def cmds(commands: list[str], keystore: dict[str, Record]) -> str | list[str]:
    """handle commands"""
    match commands[0].upper():  # checking the instruction sent by the client
        case "PING":
            ret = ping()
        case "ECHO":
            ret = echo(key=commands[1])  # returning the same value sent by the client
        case "GET":
            ret = get_data(key=commands[1], keystore=keystore)
        case "SET":
            ret = set_data(data=commands[1:], keystore=keystore)
        case "CONFIG":
            ret = configs(data=commands[1:], keystore=keystore)
        case "INFO":
            ret = info(command=commands[1], keystore=keystore)
        case _:
            ret = ["-ERR Unimplemened command"]
    return ret


def ping() -> str:
    """return pong for ping command"""
    return "+PONG"


def echo(key: str) -> str:
    """return passed data to echo back to client"""
    return key


# data
def set_data(data: list[str], keystore: dict[str, Record]) -> str | list[str]:
    """setting data with key value pair"""
    key = data[0]
    val = data[1]
    px = -1  # pylint: disable=invalid-name
    if len(data) > 2:
        print(data)
        px = int(data[3])  # pylint: disable=invalid-name

    # set record and put it into the datastore
    record: Record = Record(value=val, px=int(px))
    keystore[key] = record
    if keystore[key] != record:
        return "$-1"  # "-ERR unable to set record into the datastore"
    return "+OK"


def get_data(key: str, keystore: dict[str, Record]) -> str:
    """getting data with specific key"""
    if not key in keystore:
        return "$-1"
    record: Record = keystore[key]
    return record.get()


def init(keystore: dict[str, Record], args: dict[str, str]) -> None:
    """initialize redis"""
    keystore.clear()
    init_args(keystore=keystore, args=args)
    init_repl(keystore)
    rdb.rdb_file_exists(keystore=keystore)


def init_args(keystore: dict[str, Record], args: dict[str, str]) -> None:
    """add args to keystore"""
    if not args:
        return
    for x, y in args.items():  # pylint: disable=invalid-name
        keystore[x] = Record(value=y)
