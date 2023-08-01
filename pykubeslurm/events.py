"""Core module for event based logic operations."""
import threading
import time

from kubernetes import watch, client
from loguru import logger

from pykubeslurm.settings import SETTINGS
from pykubeslurm.schemas import KubernetesEvent
from pykubeslurm.helpers import handle_k8s_event

def event_listener(
    thread_event: threading.Event,
):
    """Listen for kubernetes events."""
    with logger.focus("PyKubeSlurm - Event listener logic"):
        logger.debug(f"Started thread. ID: {threading.get_ident()}")
        w = watch.Watch()
        while not thread_event.is_set():
            try:
                if SETTINGS.WATCH_ALL:
                    logger.warning("WATCH_ALL is set. Ignoring NAMESPACE setting then.")
                    for event in w.stream(
                        client.CustomObjectsApi().list_cluster_custom_object,
                        group=SETTINGS.CRD_GROUP,
                        version=SETTINGS.CRD_VERSION,
                        plural=SETTINGS.JOB_CRD_PLURAL,
                    ):
                        handle_k8s_event(KubernetesEvent(**event))
                else:
                    logger.warning("WATCH_ALL is not set. Using NAMESPACE setting.")
                    for event in w.stream(
                        client.CustomObjectsApi().list_namespaced_custom_object,
                        group=SETTINGS.CRD_GROUP,
                        version=SETTINGS.CRD_VERSION,
                        namespace=SETTINGS.NAMESPACE,
                        plural=SETTINGS.JOB_CRD_PLURAL
                    ):
                        handle_k8s_event(KubernetesEvent(**event))
            except Exception as err:
                # keep thread alive
                logger.exception(err)
                time.sleep(SETTINGS.EVENT_LISTENER_TIMEOUT)
        else:
            w.stop()
            logger.debug(f"Thread {threading.get_ident()} stopped")
