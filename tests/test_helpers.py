"""This module contains unit tests for the helpers.py module."""
from unittest import mock

from pykubeslurm.helpers import handle_k8s_event
from pykubeslurm.schemas import Job, KubernetesEvent, KubernetesEventType


@mock.patch("pykubeslurm.helpers._add_slurm_job")
def test_handle_k8s_event_added(mock_add_slurm_job: mock.Mock):
    event = KubernetesEvent(
        raw_object={},
        type=KubernetesEventType.ADDED,
        object={"script": "", "job_id": "123", "status": "RUNNING"},
    )

    handle_k8s_event(event)

    mock_add_slurm_job.assert_called_once_with(Job(job_id="123", status="RUNNING"))


@mock.patch("pykubeslurm.helpers._update_slurm_job")
def test_handle_k8s_event_modified(mock_update_slurm_job: mock.Mock):
    event = KubernetesEvent(
        raw_object={},
        type=KubernetesEventType.MODIFIED,
        object={"script": "", "job_id": "123", "status": "COMPLETED"},
    )

    handle_k8s_event(event)

    mock_update_slurm_job.assert_called_once_with(Job(job_id="123", status="COMPLETED"))


@mock.patch("pykubeslurm.helpers._delete_slurm_job")
def test_handle_k8s_event_deleted(mock_delete_slurm_job: mock.Mock):
    event = KubernetesEvent(
        raw_object={},
        type=KubernetesEventType.DELETED,
        object={"script": "", "job_id": "123", "status": "COMPLETED"},
    )

    handle_k8s_event(event)

    mock_delete_slurm_job.assert_called_once_with(Job(job_id="123", status="COMPLETED"))
