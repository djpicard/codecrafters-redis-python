"""functions for commands"""

from datetime import datetime, timedelta, timezone

from app.commands import rdb
from app.commands.configs import configs  # get_config, set_config
from app.commands.info import info, init_repl


def cmds(commands: list[str], keystore: dict) -> str | list[str]:
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
def set_data(data: list[str], keystore: dict) -> str | list[str]:
    """setting data with key value pair"""
    key = data[0]
    options = data[1:]

    # set record and put it into the datastore
    record: dict[str, str] = _set_options(options=options)
    keystore[key] = record
    if keystore[key] != record:
        return "$-1"  # "-ERR unable to set record into the datastore"
    return "+OK"


def get_data(key: str, keystore: dict[str, dict[str, str]]) -> str:
    """getting data with specific key"""
    if not key in keystore:
        return "$-1"  # "-ERR Key not found in datastore"
    # data is stored in a dictionary
    # key is a str
    # data is stored as a dict[str, object])
    record: dict[str, str] = keystore[key]
    result = "-ERR No matching data found"

    for x in record:
        match x:
            case "px":
                currtime = datetime.now().timestamp()
                if currtime > float(record[x]):
                    return "$-1"  # "-ERR record timed out"
            case "value":
                result = record[x]
    return result


def _set_options(options: list[str]) -> dict[str, str]:
    """parse options given to the datastore"""
    it = iter(options)
    result: dict[str, str] = {}  # adding value for record
    for x in it:  # adding options for record
        match x.lower():
            case "px":
                px = datetime.now(timezone.utc).now() + timedelta(
                    milliseconds=int(next(it))
                )
                result["px"] = f"{px.timestamp()}"
            case _:
                result["value"] = x
    return result


def init(keystore: dict, args: dict) -> None:
    """initialize redis"""
    keystore.clear()
    keystore.update(args)
    init_repl(keystore)
    rdb.rdb_file_exists(keystore=keystore)
