"""info commands"""

import asyncio

from app.classes.Keystore import keystore
from app.classes.Registry import registry
from app.utils.encoder import encode  # pylint: disable=import-error

DEFAULT_MASTER_REPLID = "8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb"


def init_repl() -> None:
    """initialize replication store"""
    keystore.set(key="role", value="master")
    keystore.set(key="connected_slaves", value="0")
    keystore.set(key="master_replid", value=f"{DEFAULT_MASTER_REPLID}")
    keystore.set(key="master_repl_offset", value="0")

    if keystore.key_exists(key="replicaof"):
        if keystore.get(key="replicaof") != "":
            keystore.set(key="role", value="slave")

def info_repl() -> str:
    """retrieve replication info"""
    repl: list[str] = [
        "role",
        "master_replid",
        "master_repl_offset",
    ]
    output: list[str] = []
    for x in repl:  # pylint: disable=invalid-name
        if keystore.key_exists(key=x):
            output.append(f"{x}:{keystore.get(key=x)}")
    return "\r\n".join(output)

@registry.register("INFO")
def info(command: str) -> str | list[str]:
    """parse info commands"""
    match command.lower():
        case "replication":
            return info_repl()
    return "$-1"

@registry.register("PSYNC")
def psync(data:str, val:str) -> str:
    """psync return"""
    print(f"{data}")
    print(f"{val}")
    return f"FULLRESYNC {keystore.get("master_replid")} {keystore.get("master_repl_offset")}"


@registry.register("FULLRESYNC")
def fullresync(data: list[str]) -> str | list[str]:
    """parse fullresync response"""
    # data[0] replid
    # data[1] offset
    keystore.set(key="master_replid", value=data[0])
    keystore.set(key="master_repl_offset", value=data[1])
    return "OK"

@registry.register("REPLCONF")
def replconf(data: str, data2: str) -> str | list[str]:
    """handle replconf"""
    print(data)
    print(data2)
    print(keystore)
    return "OK" # just sending ok for now

async def replication():
    """replication loop"""
    if not keystore.key_exists("replicaof"):
        return
    host, port = keystore.get(key="replicaof").split()
    message = [
        ["PING"],
        ["REPLCONF", "listening-port", f"{keystore.get("port")}"],
        ["REPLCONF", "capa", "psync2"],
        ["PSYNC", "?", "-1"],
    ]
    try:
        while True:
            reader, writer = await asyncio.open_connection(host, port)
            for x in message:
                writer.write(encode(x).encode())
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
