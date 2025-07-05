"""unit tests for redis server"""

import asyncio
import logging
import sys

import pytest

import app
import app.main

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)

messages_to_send = [
    "*1\r\n$4\r\nPING\r\n",
    "*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n",
    "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
    "*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$3\r\nval\r\n",
    "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
]
correct_returns = ["+PONG\r\n", "$3\r\nhey\r\n", "$-1\r\n", "+OK\r\n", "$3\r\nval\r\n"]


@pytest.mark.asyncio
async def test_server_commands(caplog):
    """testing server commands"""
    caplog.set_level(logging.INFO)
    # Start server
    logger.debug("starting server")
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        logger.debug("connecting with server")
        reader, writer = await asyncio.open_connection(host, port)

        messages = messages_to_send

        for msg in messages:
            logger.debug("sending message: %s", msg)
            writer.write(msg.encode())
            await writer.drain()

            logger.debug("waiting on return message")
            data = await reader.read(1024)
            logger.debug("received: %s", data.decode())
            responses.append(data.decode())

            logger.debug("closing writer")

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        logger.debug("sending data")
        responses = await asyncio.wait_for(client(), timeout=5.0)
        assert len(responses) == len(correct_returns)
        assert responses == correct_returns
    finally:
        server.close()
        await server.wait_closed()
