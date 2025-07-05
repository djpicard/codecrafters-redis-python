"""unit tests for redis server"""

import asyncio
import logging
import sys

import pytest

import app
import app.main
import app.parser

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)

messages_to_send = ["*1\r\n$4\r\nPING\r\n", "*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n"]
correct_returns = ["+PONG\r\n", "$3\r\nhey\r\n"]


@pytest.mark.asyncio
async def test_server_commands(caplog):
    """testing server commands"""
    caplog.set_level(logging.INFO)
    # Start server
    logger.info("starting server")
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        logger.info("connecting with server")
        reader, writer = await asyncio.open_connection(host, port)

        messages = messages_to_send

        for msg in messages:
            logger.info(f"sending message {msg}")
            writer.write(msg.encode())
            await writer.drain()

            logger.info("waiting on return message")
            data = await reader.read(1024)
            logger.info(f"received {data.decode()}")
            responses.append(data.decode())

            logger.info("closing writer")

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        logger.info("sending data")
        responses = await asyncio.wait_for(client(), timeout=5.0)
        assert len(responses) == len(correct_returns)
        assert responses == correct_returns
    finally:
        server.close()
        await server.wait_closed()
