"""info commands"""

repl: list[str] = [
    "role"
]  # , "connected_slaves", "master_replid", "master_repl_offset"]


def init_repl(keystore: dict) -> None:
    """initialize replication store"""
    keystore["role"] = "master"
    keystore["connected_slaves"] = "0"
    keystore["master_replid"] = "masterreplid"
    keystore["master_repl_offset"] = "0"


def info(command: str, keystore: dict) -> str | list[str]:
    """parse info commands"""
    print(f"commands: {command}")
    match command.lower():
        case "replication":
            return replication(keystore=keystore)
    return "$-1"


def replication(keystore: dict) -> str | list[str]:
    """retrieve replication info"""
    output: list[str] = []
    print(f"keystore: {keystore}, repl: {repl}")
    for x in repl:
        if x in keystore:
            return f"{x}:{keystore[x]}"
    print(f"output: {output}")
    return output
