"""Main module for the Operator app."""
import sys
import threading
import time

import typer
from focalize import attach_focalize
from kubernetes import config
from loguru import logger

from pykubeslurm.events import event_listener
from pykubeslurm.health_check import init_health_check
from pykubeslurm.scheduler import init_scheduler
from pykubeslurm.settings import SETTINGS
from pykubeslurm.vars import APP_STARTED_AT  # noqa: F401

app = typer.Typer(name="PyKubeSlurm")

attach_focalize(sys.stderr, level=SETTINGS.DEBUG_LEVEL)


@app.callback()
def callback():  # type: ignore
    """PyKubeSlurm - A Kubernetes Operator for scheduling jobs on Slurm."""
    init_scheduler()


@app.command(name="run")
def run():  # type: ignore
    """Run the Operator app."""
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Run app"):
        try:
            logger.info("Trying to load in cluster config")
            config.load_incluster_config()
            logger.info("Successfully loaded in cluster config")
        except config.ConfigException as err:
            logger.error(f"Could not load in cluster config: {err}")
            try:
                logger.info(f"Trying to load kubernetes config from `{SETTINGS.KUBE_CONFIG}`")
                config.load_kube_config(
                    config_file=SETTINGS.KUBE_CONFIG, context=SETTINGS.KUBE_CONTEXT
                )
                logger.info(
                    f"Successfully loaded the context `{SETTINGS.KUBE_CONTEXT}` from `{SETTINGS.KUBE_CONFIG}`"
                )
            except config.ConfigException as err:
                logger.error(f"Could not load kubernetes config: {err}")
                raise err
        except Exception as err:
            logger.error(f"Could not load kubernetes config: {err}")
            raise err

        event = threading.Event()

        event_listener_thread = threading.Thread(
            name="EventListener", target=event_listener, args=(event,)
        )
        health_check_thread = threading.Thread(name="HealthCheck", target=init_health_check)

        try:
            health_check_thread.start()
            while True:
                if not event_listener_thread.is_alive():
                    logger.debug("Starting the event listener...")
                    event_listener_thread.start()
                time.sleep(5)
        except KeyboardInterrupt:
            logger.debug("Exiting by keyboard interruption...")
            event.set()
            event_listener_thread.join()
            health_check_thread.join()
        except config.config_exception.ConfigException as err:
            logger.error(f"Could not load kubernetes config: {err}")
            raise SystemExit(1)
        except Exception as err:
            event.set()
            event_listener_thread.join()
            health_check_thread.join()
            raise err


if __name__ == "__main__":
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Start app"):
        try:
            app()
        except Exception as err:
            logger.error(f"Unexpected error: {err}")
            raise SystemExit(1)
