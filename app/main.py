"""redis implementation"""

import argparse
import asyncio
import logging
import sys
from asyncio import StreamReader, StreamWriter

from app.classes.records import Record
from app.commands.executor import init
from app.commands.info import replication
from app.utils import parser

# import socket  # noqa: F401
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=FORMAT)
arguments = argparse.ArgumentParser()
# dictionary to store any data sent
datastore: dict[str, Record] = {}


async def start_server():
    """entrypoint for testing"""
    init(keystore=datastore, args={})
    server = await asyncio.start_server(
        lambda r, w: handler(r, w, datastore), "127.0.0.1", port=6379
    )
    return server


async def main(args):
    """main function to start our redis journey"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    logger.debug("Logs from your program will appear here!")
    init(keystore=datastore, args=vars(args))

    # create an asyncio server
    server = await asyncio.start_server(
        lambda r, w: handler(r, w, datastore), "127.0.0.1", port=args.port
    )
    logger.debug("Server is up: %s", server.is_serving())
    # return server

    replication_task = asyncio.create_task(replication(datastore))

    try:
        async with server:
            await server.serve_forever()
            logger.debug("Shutting down server")
    finally:
        replication_task.cancel()
        try:
            await replication_task
        except asyncio.CancelledError:
            print("Replication task failed to cancel")
    # report the details of the server


async def handler(reader: StreamReader, writer: StreamWriter, keystore: dict):
    """connection handler"""

    addr = writer.get_extra_info("peername")
    logger.debug("Connected with: %s", addr)

    while True:
        data = await reader.read(1024)
        if not data:
            logger.debug("Disconnected from: %s", addr)
            break

        message = data.decode()
        logger.debug("Received message: %s", message)

        resp = parser.parse(message, keystore)
        logger.debug("Sending responce: %s", resp)
        writer.write(resp)
        await writer.drain()

    logger.debug("Closing writer connection")
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    arguments.add_argument("--dir")
    arguments.add_argument("--dbfilename")
    arguments.add_argument("--port", default=6379)
    arguments.add_argument("--replicaof", default="")
    init_args = arguments.parse_args()
    asyncio.run(main(args=init_args))
