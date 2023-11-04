"""
This module contains tests for `pykubeslurm/events.py` module.

The `events.py` module is responsibe for defining how the kubernetes events are
captured and handled in a high level overview.
"""
import threading
from typing import Any
from unittest import mock

from kubernetes import client

from pykubeslurm.events import event_listener
from pykubeslurm.schemas import KubernetesEvent, KubernetesEventType
from pykubeslurm.settings import SETTINGS


@mock.patch("pykubeslurm.events.watch")
@mock.patch("pykubeslurm.events.handle_k8s_event")
def test_events__test_k8s_event_stream(
    mocked_handle_k8s_event: mock.MagicMock,
    mocked_watch: mock.MagicMock,
    job_object: dict[str, Any],
    set_event,
    init_logging_in_testing,
):
    dummy_event = threading.Event()

    k8s_event = KubernetesEvent(
        raw_object={},
        type=KubernetesEventType.ADDED,
        object=job_object,
    )

    mocked_watch.Watch = mock.Mock()
    mocked_watch.Watch.return_value.stream = mock.Mock(return_value=[k8s_event.model_dump(mode="json")])
    mocked_watch.Watch.return_value.stop = mock.Mock(return_value=None)

    set_dummy_event_thread = threading.Thread(
        name="ControlThread", target=set_event, args=(dummy_event,)
    )
    set_dummy_event_thread.start()

    event_listener(dummy_event)

    set_dummy_event_thread.join()

    mocked_handle_k8s_event.assert_any_call(k8s_event)
    # mocked_watch.Watch.return_value.stream.assert_any_call(
    #     client.CustomObjectsApi().list_namespaced_custom_object,
    #     group=SETTINGS.CRD_GROUP,
    #     version=SETTINGS.CRD_VERSION,
    #     namespace=SETTINGS.NAMESPACE,
    #     plural=SETTINGS.JOB_CRD_PLURAL,
    # )
    mocked_watch.Watch.return_value.stop.assert_called_once_with()
    mocked_watch.Watch.assert_any_call()
