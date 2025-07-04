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
    print("Logs from your program will appear here!")

    # switching from sockets to asyncio server
    # server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    # create an asyncio server
    server = await asyncio.start_server(handler, "127.0.0.1", port=6379)
    print(f"Server is up: {server.is_serving()}")

    async with server:
        await server.serve_forever()
        print("Shutting down server")
    # report the details of the server

    print(f"Server is up: {server.is_serving()}")


async def handler(reader, writer):
    """connection handler"""
    data = await reader.read(1024)
    message = data.decode()
    print(f"Received message: {message}")

    resp = "+PONG\r\n"
    print(f"Sending responce: {resp}")
    writer.write(resp.encode())
    await writer.drain()

    print("Closing writer connection")
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
