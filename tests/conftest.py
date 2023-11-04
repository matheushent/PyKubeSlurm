"""
This module contains fixtures and configuration for Pytest testing.

Fixtures:
- server: A fixture that creates a TestServer and TestClient for testing web applications.
"""
import asyncio
import sys
import threading
import time
from typing import Any, Generator

import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from focalize import attach_focalize

from pykubeslurm.health_check import health_check
from pykubeslurm.settings import SETTINGS


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


@pytest.fixture
def job_object() -> Generator[dict[str, Any], None, None]:
    object = {
        "apiVersion": "dummy",
        "kind": "SlurmJob",
        "metadata": {
            "name": "dummy",
            "namespace": "unittests",
            "creation_timestamp": "2023-10-30T12:00:00.000000000Z",
        },
        "spec": {
            "script": "#!/bin/bash\necho 'Testing is cool'",
            "standard_error": "/tmp/error.log",
            "standard_output": "/tmp/out.log",
            "current_working_directory": "/tmp",
            "time_limit": 1800,
            "tasks": 6,
            "name": "testing",
            "begin": "now+1hour",
        },
    }
    yield object


@pytest.fixture
def set_event():
    def _helper(event: threading.Event) -> None:
        time.sleep(5)  # give some time for things to happen before setting the event flag
        event.set()

    return _helper


@pytest.fixture
def init_logging_in_testing():
    attach_focalize(sys.stderr, level=SETTINGS.DEBUG_LEVEL)
    yield
