"""unit tests for redis server"""

import asyncio
import logging
import sys
import time

import pytest

import app
import app.main

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=FORMAT)


@pytest.mark.asyncio
async def test_info(caplog):
    """testing server commands"""

    messages_to_send = [
        "*2\r\n$4\r\nINFO\r\n$11\r\nreplication\r\n",
    ]
    correct_returns = [
        "$89\r\nrole:master\r\nmaster_replid:8371b4fb1155b71f4a04d3e1bc3e18c4a990aeeb"
        + "\r\nmaster_repl_offset:0\r\n"
    ]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)

        messages = messages_to_send

        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        assert responses[0] == correct_returns[0]
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_ping(caplog):
    """testing server commands"""

    messages_to_send = [
        "*1\r\n$4\r\nPING\r\n",
    ]
    correct_returns = ["+PONG\r\n"]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)

        messages = messages_to_send

        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        assert responses[0] == correct_returns[0]
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_echo(caplog):
    """testing server commands"""

    messages_to_send = [
        "*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n",
    ]
    correct_returns = ["$3\r\nhey\r\n"]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)
        messages = messages_to_send

        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        assert responses[0] == correct_returns[0]
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_bad_get_commands(caplog):
    """testing server commands"""

    messages_to_send = [
        "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
    ]
    correct_returns = ["$-1\r\n"]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)

        messages = messages_to_send

        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        assert responses[0] == correct_returns[0]
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_set_get(caplog):
    """testing server commands"""

    messages_to_send = [
        "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
        "*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$3\r\nval\r\n",
        "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
    ]
    correct_returns = ["$-1\r\n", "+OK\r\n", "$3\r\nval\r\n"]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)
        messages = messages_to_send

        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        print(f"Recv: {responses[1]} | Expt: {correct_returns[1]}")
        print(f"Recv: {responses[2]} | Expt: {correct_returns[2]}")
        assert responses[0] == correct_returns[0]
        assert responses[1] == correct_returns[1]
        assert responses[2] == correct_returns[2]
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_set_get_px(caplog):
    """testing server commands"""

    messages_to_send = [
        "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
        "*5\r\n$3\r\nSET\r\n$3\r\nkey\r\n$3\r\nval\r\n$2\r\npx\r\n$3\r\n100\r\n",
        "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
        "*3\r\n$3\r\nSET\r\n$10\r\nstrawberry\r\n$4\r\npear\r\n",
        "*2\r\n$3\r\nGET\r\n$10\r\nstrawberry\r\n",
    ]
    correct_returns = [
        "$-1\r\n",
        "+OK\r\n",
        "$3\r\nval\r\n",
        "+OK\r\n",
        "$4\r\npear\r\n",
    ]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)
        messages = messages_to_send

        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        print(f"Recv: {responses[1]} | Expt: {correct_returns[1]}")
        print(f"Recv: {responses[2]} | Expt: {correct_returns[2]}")
        print(f"Recv: {responses[3]} | Expt: {correct_returns[3]}")
        print(f"Recv: {responses[4]} | Expt: {correct_returns[4]}")
        assert responses[0] == correct_returns[0]
        assert responses[1] == correct_returns[1]
        assert responses[2] == correct_returns[2]
        assert responses[3] == correct_returns[3]
        assert responses[4] == correct_returns[4]
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_set_get_configs(caplog):
    """testing server commands"""

    messages_to_send = [
        "*3\r\n$6\r\nCONFIG\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
        "*4\r\n$6\r\nCONFIG\r\n$3\r\nSET\r\n$3\r\nkey\r\n$3\r\nval\r\n",
        "*3\r\n$6\r\nCONFIG\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
        "*3\r\n$6\r\nCONFIG\r\n$3\r\nGET\r\n$1\r\n*\r\n",
    ]
    correct_returns = [
        "$-1\r\n",
        "+OK\r\n",
        "*2\r\n$3\r\nkey\r\n$3\r\nval\r\n",
        "$-1\r\n",  # "*2\r\n$3\r\nkey\r\n$3\r\nval\r\n",
    ]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)
        messages = messages_to_send

        for msg in messages:
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        print(f"Recv: {responses[1]} | Expt: {correct_returns[1]}")
        print(f"Recv: {responses[2]} | Expt: {correct_returns[2]}")
        print(f"Recv: {responses[3]} | Expt: {correct_returns[3]}")
        assert responses[0] == correct_returns[0]
        assert responses[1] == correct_returns[1]
        assert responses[2] == correct_returns[2]
        assert responses[3] == correct_returns[3]
    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_set_get_px_delay(caplog):
    """testing server commands"""

    messages_to_send = [
        "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
        "*5\r\n$3\r\nSET\r\n$3\r\nkey\r\n$3\r\nval\r\n$2\r\npx\r\n$3\r\n100\r\n",
        "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n",
    ]
    correct_returns = ["$-1\r\n", "+OK\r\n", "$-1\r\n"]

    caplog.set_level(logging.INFO)
    # Start server
    server = await app.main.start_server()
    host, port = server.sockets[0].getsockname()
    responses: list[str] = []

    async def client() -> list[str]:
        reader, writer = await asyncio.open_connection(host, port)

        messages = messages_to_send

        for msg in messages:
            time.sleep(1)
            writer.write(msg.encode())
            await writer.drain()

            data = await reader.read(1024)
            responses.append(data.decode())

        writer.close()
        await writer.wait_closed()
        return responses

    try:
        # Run client and get echoed messages
        responses = await asyncio.wait_for(client(), timeout=5.0)
        print(f"Recv: {responses[0]} | Expt: {correct_returns[0]}")
        print(f"Recv: {responses[1]} | Expt: {correct_returns[1]}")
        print(f"Recv: {responses[2]} | Expt: {correct_returns[2]}")
        assert responses[0] == correct_returns[0]
        assert responses[1] == correct_returns[1]
        assert responses[2] == correct_returns[2]
    finally:
        server.close()
        await server.wait_closed()
