"""redis implementation"""

import asyncio
import logging
import sys

# import socket  # noqa: F401

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


async def main():
    """main function to start our redis journey"""
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    logger.info("Logs from your program will appear here!")

    # switching from sockets to asyncio server
    # server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    # create an asyncio server
    server = await asyncio.start_server(handler, "127.0.0.1", port=6379)
    async with server:
        await server.serve_forever()
        await logger.info("Shutting down server")
    # report the details of the server
    logger.info(f"Server is up: {server.is_serving()}")


async def handler(reader, writer):
    """connection handler"""
    data = await reader.read(1024)
    message = data.decode()
    logger.info(f"Received message: {message}")

    writer.write(b"+PONG\r\n")
    await writer.drain()

    logger.info("Sent data back")
    writer.close()


if __name__ == "__main__":
    asyncio.run(main())
