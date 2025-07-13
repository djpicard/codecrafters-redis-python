"""info commands"""

from app.classes.records import Record


def _init_repl(keystore: dict[str, Record]) -> None:
    """initialize replication store"""
    if keystore["replicaof"].get() == "":
        keystore["role"] = Record(value="master")
    else:
        keystore["role"] = Record(value="slave")
    keystore["connected_slaves"] = Record(value="0")
    keystore["master_replid"] = Record(value="8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb")
    keystore["master_repl_offset"] = Record(value="0")


def info(command: str, keystore: dict[str, Record]) -> str | list[str]:
    """parse info commands"""
    match command.lower():
        case "replication":
            return replication(keystore=keystore)
    return "$-1"


def replication(keystore: dict[str, Record]) -> str:
    """retrieve replication info"""
    repl: list[str] = [
        "role",
        "master_replid",
        "master_repl_offset",
    ]
    output: list[str] = []
    for x in repl:
        if x in keystore:
            output.append(f"{x}:{keystore[x].get()}")
    return "\r\n".join(output)
