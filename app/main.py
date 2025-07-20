"""redis implementation"""

import argparse
import asyncio
from asyncio import StreamReader, StreamWriter

from .handlers import configs, default, info, rlist  # pylint: disable=unused-import

# import app.handlers as handlers # pylint: disable=unused-import
from .Registry import registry
from .utils.utils import init

arguments = argparse.ArgumentParser()
# dictionary to store any data sent

async def start_server():
    """entrypoint for testing"""
    init(args={})

    server = await asyncio.start_server(handler, "127.0.0.1", port=6379)
    return server


async def main(args):
    """main function to start our redis journey"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Starting init and setting default values")
    init(args=vars(args))

    # create an asyncio server
    print("Setting server")
    server = await asyncio.start_server(handler, "127.0.0.1", port=args.port)
    # return server

    print("Setting replication task")
    replication_task = asyncio.create_task(info.replication())

    try:
        print("Starting server")
        async with server:
            await server.serve_forever()
    finally:
        print("Closing replication")
        replication_task.cancel()
        try:
            await replication_task
        except asyncio.CancelledError:
            print("Replication task failed to cancel")
    # report the details of the server


async def handler(reader: StreamReader, writer: StreamWriter):
    """connection handler"""

    # addr = writer.get_extra_info("peername")

    while True:
        data = await reader.read(1024)
        if not data:
            break

        message = data.decode()
        resp = registry.handle(message).encode()
        print(f"Resp: {resp}")

        writer.write(resp)
        await writer.drain()

    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    print("Started app")
    arguments.add_argument("--dir")
    arguments.add_argument("--dbfilename")
    arguments.add_argument("--port", default=6379)
    arguments.add_argument("--replicaof", default="")
    init_args = arguments.parse_args()
    print("Started asyncio process")
    asyncio.run(main(args=init_args))
