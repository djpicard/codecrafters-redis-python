"""utility functions"""
from ..classes.Keystore import keystore
from ..handlers.info import init_repl


def init(args: dict[str, str]) -> None:
    """initialize redis"""
    keystore.clear()
    init_args(args=args)
    init_repl()
    # rdb.rdb_file_exists()

def init_args(args: dict[str, str]) -> None:
    """add args to keystore"""
    if not args:
        return
    for x, y in args.items():  # pylint: disable=invalid-name
        keystore.set(key=x, value=y)
