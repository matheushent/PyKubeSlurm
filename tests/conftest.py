"""
This module contains fixtures and configuration for Pytest testing.

Fixtures:
- server: A fixture that creates a TestServer and TestClient for testing web applications.
"""
import asyncio
from typing import Generator

import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from pykubeslurm.health_check import health_check


@pytest_asyncio.fixture
async def health_check_server(
    loop: asyncio.AbstractEventLoop,
) -> Generator[TestClient, None, None]:
    app = web.Application()
    app.router.add_get("/health", health_check)

    server = TestServer(app)
    client = TestClient(server)

    await server.start_server(loop=loop)
    await client.start_server()

    yield client

    await client.close()
    await server.close()
