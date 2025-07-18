"""info commands"""

import asyncio

from app.classes.records import Record  # pylint: disable=import-error
from app.utils.encoder import encode  # pylint: disable=import-error

DEFAULT_MASTER_REPLID = "8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb"


def init_repl(keystore: dict[str, Record]) -> None:
    """initialize replication store"""
    keystore["role"] = Record(value="master")
    keystore["connected_slaves"] = Record(value="0")
    keystore["master_replid"] = Record(value=f"{DEFAULT_MASTER_REPLID}")
    keystore["master_repl_offset"] = Record(value="0")

    if "replicaof" in keystore:
        if keystore["replicaof"].get() != "":
            keystore["role"] = Record(value="slave")


def info(command: str, keystore: dict[str, Record]) -> str | list[str]:
    """parse info commands"""
    match command.lower():
        case "replication":
            return info_repl(keystore=keystore)
    return "$-1"

def fullresync(data: list[str], keystore: dict[str, Record]) -> str | list[str]:
    """parse fullresync response"""
    # data[0] replid
    # data[1] offset
    keystore["master_replid"] = Record(value=data[0])
    keystore["master_repl_offset"] = Record(value=data[1])
    return "OK"


def info_repl(keystore: dict[str, Record]) -> str:
    """retrieve replication info"""
    repl: list[str] = [
        "role",
        "master_replid",
        "master_repl_offset",
    ]
    output: list[str] = []
    for x in repl:  # pylint: disable=invalid-name
        if x in keystore:
            output.append(f"{x}:{keystore[x].get()}")
    return "\r\n".join(output)


async def replication(keystore: dict[str, Record]):
    """replication loop"""
    if not keystore["replicaof"]:
        return
    host, port = keystore["replicaof"].get().split()
    message = [
        ["PING"],
        ["REPLCONF", "listening-port", f"{keystore["port"].get()}"],
        ["REPLCONF", "capa", "psync2"],
        ["PSYNC", "?", "-1"],
    ]
    try:
        while True:
            reader, writer = await asyncio.open_connection(host, port)
            for x in message:
                writer.write(encode(x))
                await writer.drain()

                data = await reader.read(1024)
                if not data:
                    break

                resp = data.decode()
                print(resp)
            writer.close()
            await writer.wait_closed()

            # resp = parser.parse(message, keystore)
    except (  # pylint: disable=invalid-name,unused-variable
        Exception  # pylint: disable=broad-exception-caught
    ) as e:  # pylint: disable=invalid-name,unused-variable
        await asyncio.sleep(10)
