"""Core module for defining the health check server logic."""
import asyncio

from aiohttp import web

from pykubeslurm.settings import SETTINGS


async def health_check(request: web.Request) -> web.Response:
    """
    HTTP request handler to check the health of the server.

    Args:
        request: The HTTP request object.

    Returns:
        web.Response: A web response with "OK" to indicate the server is healthy.
    """
    return web.Response(text="OK")


async def main() -> None:
    """
    Start an aiohttp-based HTTP server to handle health checks.

    This function creates a simple HTTP server that responds to GET requests
    at the '/health' endpoint to indicate the server's health.
    """
    host = SETTINGS.HEALTH_CHECK_ADDRESS
    port = SETTINGS.HEALTH_CHECK_PORT

    app = web.Application()
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()


def init_health_check() -> None:
    """Initialize the health check server."""
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
