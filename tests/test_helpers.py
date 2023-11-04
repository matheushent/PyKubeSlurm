"""This module contains unit tests for the helpers.py module."""
from typing import Any
from unittest import mock

from pykubeslurm.helpers import handle_k8s_event
from pykubeslurm.schemas import Job, KubernetesEvent, KubernetesEventType


@mock.patch("pykubeslurm.helpers._add_slurm_job")
def test_handle_k8s_event_added(mock_add_slurm_job: mock.Mock, job_object: dict[str, Any]):
    event = KubernetesEvent(
        raw_object={},
        type=KubernetesEventType.ADDED,
        object=job_object,
    )

    handle_k8s_event(event)

    mock_add_slurm_job.assert_called_once_with(Job(**event.object))


@mock.patch("pykubeslurm.helpers._update_slurm_job")
def test_handle_k8s_event_modified(mock_update_slurm_job: mock.Mock, job_object: dict[str, Any]):
    event = KubernetesEvent(
        raw_object={},
        type=KubernetesEventType.MODIFIED,
        object=job_object,
    )

    handle_k8s_event(event)

    mock_update_slurm_job.assert_called_once_with(Job(**event.object))


@mock.patch("pykubeslurm.helpers._delete_slurm_job")
def test_handle_k8s_event_deleted(mock_delete_slurm_job: mock.Mock, job_object: dict[str, Any]):
    event = KubernetesEvent(
        raw_object={},
        type=KubernetesEventType.DELETED,
        object=job_object,
    )

    handle_k8s_event(event)

    mock_delete_slurm_job.assert_called_once_with(Job(**event.object))
