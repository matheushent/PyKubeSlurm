"""
This module contains tests for the health check server.

The health check server is responsible for checking the health status of the application.
These tests ensure that the server is functioning correctly by checking that the server returns a 200 status code
and the text 'OK' when the '/health' endpoint is accessed.

The tests use the pytest framework and the aiohttp library for making HTTP requests.
"""
from unittest import mock

import pytest
from aiohttp.test_utils import TestClient

from pykubeslurm.health_check import health_check, init_health_check, main
from pykubeslurm.settings import SETTINGS


@pytest.mark.asyncio
async def test_health_check_ok(health_check_server: TestClient):
    resp = await health_check_server.get("/health")
    assert resp.status == 200
    text = await resp.text()
    assert text == "OK"


@pytest.mark.asyncio
@mock.patch("pykubeslurm.health_check.web.TCPSite")
@mock.patch("pykubeslurm.health_check.web.Application")
@mock.patch("pykubeslurm.health_check.web.AppRunner")
async def test_health_check_server__test_main_logic(
    mocked_app_runner: mock.MagicMock,
    mocked_web_application: mock.MagicMock,
    mocked_tcp_site: mock.MagicMock,
):
    mocked_web_application.return_value.router.add_get = mock.MagicMock(return_value=None)
    mocked_app_runner.return_value.setup = mock.AsyncMock(return_value=None)
    mocked_tcp_site.return_value.start = mock.AsyncMock(return_value=None)

    await main()

    mocked_web_application.return_value.router.add_get.assert_called_once_with(
        "/health", health_check
    )
    mocked_web_application.assert_called_once_with()
    mocked_app_runner.assert_called_once_with(mocked_web_application.return_value)
    mocked_app_runner.return_value.setup.assert_awaited_once_with()
    mocked_tcp_site.return_value.start.assert_awaited_once_with()
    mocked_tcp_site.assert_called_once_with(
        mocked_app_runner.return_value,
        SETTINGS.HEALTH_CHECK_ADDRESS,
        SETTINGS.HEALTH_CHECK_PORT,
    )


@mock.patch("pykubeslurm.health_check.asyncio")
def test_health_check_server__test_init_health_check_logic(
    mocked_asyncio: mock.MagicMock,
):
    mocked_main = mock.MagicMock(return_value=None)
    mocked_asyncio.new_event_loop.return_value.create_task = mock.MagicMock(return_value=None)
    mocked_asyncio.new_event_loop.return_value.run_forever = mock.MagicMock(return_value=None)
    with mock.patch("pykubeslurm.health_check.main", mocked_main):
        init_health_check()

    mocked_main.assert_called_once_with()
    mocked_asyncio.new_event_loop.assert_called_once_with()
    mocked_asyncio.new_event_loop.return_value.create_task.assert_called_once_with(
        mocked_main.return_value
    )
    mocked_asyncio.new_event_loop.return_value.run_forever.assert_called_once_with()
