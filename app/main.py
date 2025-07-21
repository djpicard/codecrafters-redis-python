"""redis implementation"""

import argparse
import asyncio
from asyncio import StreamReader, StreamWriter

from app.classes.Registry import registry
from app.handlers import (  # pylint: disable=unused-import
    configs,
    default,
    info,
    rlist,
    transactions,
)
from app.utils.encoder import encode
from app.utils.utils import init

arguments = argparse.ArgumentParser()

async def start_server():
    """entrypoint for testing"""
    init(args={})

    server = await asyncio.start_server(handler, "127.0.0.1", port=6379)
    return server


async def main(args):
    """main function to start our redis journey"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    init(args=vars(args))

    # create an asyncio server
    server = await asyncio.start_server(handler, "127.0.0.1", port=args.port)
    # return server

    replication_task = asyncio.create_task(info.replication())

    try:
        async with server:
            await server.serve_forever()
    finally:
        replication_task.cancel()
        try:
            await replication_task
        except asyncio.CancelledError:
            print("Replication task failed to cancel")
    # report the details of the server


async def handler(reader: StreamReader, writer: StreamWriter):
    """connection handler"""

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = data.decode()
        if not transactions.transaction.is_active():
            resp = await registry.handle(message)
        else:
            resp = transactions.transaction.queue(message)

        writer.write(encode(resp).encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    arguments.add_argument("--dir")
    arguments.add_argument("--dbfilename")
    arguments.add_argument("--port", default=6379)
    arguments.add_argument("--replicaof", default="")
    init_args = arguments.parse_args()
    asyncio.run(main(args=init_args))
