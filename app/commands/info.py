"""info commands"""

import asyncio

from app.classes.records import Record


def init_repl(keystore: dict[str, Record]) -> None:
    """initialize replication store"""
    if "replicaof" in keystore:
        if keystore["replicaof"].get() != "":
            keystore["role"] = Record(value="slave")
    else:
        keystore["role"] = Record(value="master")
    keystore["connected_slaves"] = Record(value="0")
    keystore["master_replid"] = Record(value="8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb")
    keystore["master_repl_offset"] = Record(value="0")


def info(command: str, keystore: dict[str, Record]) -> str | list[str]:
    """parse info commands"""
    match command.lower():
        case "replication":
            return info_repl(keystore=keystore)
    return "$-1"


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
    message = "*1\r\n$4\r\nPING\r\n"
    try:
        while True:
            reader, writer = await asyncio.open_connection(host, port)
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(1024)
            if not data:
                break

            message = data.decode()

            # resp = parser.parse(message, keystore)
    except (  # pylint: disable=invalid-name,unused-variable
        Exception  # pylint: disable=broad-exception-caught
    ) as e:  # pylint: disable=invalid-name,unused-variable
        await asyncio.sleep(10)
