"""Core module for event based logic operations."""
import threading
import time

from kubernetes import client, watch
from loguru import logger

from pykubeslurm.helpers import handle_k8s_event
from pykubeslurm.schemas import KubernetesEvent
from pykubeslurm.settings import SETTINGS


def event_listener(
    thread_event: threading.Event,
) -> None:
    """Listen for kubernetes events."""
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Event listener logic"):
        logger.debug(f"Started thread. ID: {threading.get_ident()}")
        w = watch.Watch()
        while not thread_event.is_set():
            try:
                for event in w.stream(
                    client.CustomObjectsApi().list_namespaced_custom_object,
                    group=SETTINGS.CRD_GROUP,
                    version=SETTINGS.CRD_VERSION,
                    namespace=SETTINGS.NAMESPACE,
                    plural=SETTINGS.JOB_CRD_PLURAL,
                ):
                    handle_k8s_event(KubernetesEvent(**event))
            except Exception as err:
                # keep thread alive
                logger.exception(err)
                time.sleep(SETTINGS.EVENT_LISTENER_TIMEOUT)
        else:
            w.stop()
            logger.debug(f"Thread {threading.get_ident()} stopped")
