"""redis implementation"""

import asyncio
import logging
import sys

from app import parser

# import socket  # noqa: F401
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


async def start_server():
    """entrypoint for pytests"""
    server = await asyncio.start_server(handler, "127.0.0.1", port=6379)
    return server


async def main():
    """main function to start our redis journey"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    logger.info("Logs from your program will appear here!")
    # create an asyncio server
    server = await asyncio.start_server(handler, "127.0.0.1", port=6379)
    logger.info(f"Server is up: {server.is_serving()}")
    # return server

    async with server:
        await server.serve_forever()
        logger.info("Shutting down server")
    # report the details of the server


async def handler(reader, writer):
    """connection handler"""

    addr = writer.get_extra_info("peername")
    logger.info(f"Connected with {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            logger.info(f"Disconnected from {addr}")
            break

        message = data.decode()
        logger.info(f"Received message: {message}")

        resp = parser.parse(message)
        logger.info(f"Sending responce: {resp}")
        writer.write(resp.encode())
        await writer.drain()

    logger.info("Closing writer connection")
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
