"""Core module for general helper functions."""
from datetime import datetime

from kubernetes import client
from loguru import logger

from pykubeslurm.schemas import KubernetesEvent, KubernetesEventType, Job, JobState
from pykubeslurm.vars import APP_STARTED_AT
from pykubeslurm.slurmrestd_interface import backend_client, inject_token


def handle_k8s_event(event: KubernetesEvent):
    """Handle kubernetes events."""
    if event.type == KubernetesEventType.ADDED:
        _add_slurm_job(Job(**event.object))
    if event.type == KubernetesEventType.MODIFIED:
        _update_slurm_job(Job(**event.object))
    if event.type == KubernetesEventType.DELETED:
        _delete_slurm_job(Job(**event.object))


def _update_job_crd(state: JobState, errors: None | list[str]):
    return


def _add_slurm_job(job_schema: Job):
    """
    Create a Slurm job by calling the Slurmrestd API.

    Args:
        job_schema: The job schema containing information from the applied manifest.
    """
    event_creation_timestamp: str = job_schema.metadata.get("creationTimestamp")
    event_creation_datetime = datetime.strptime(event_creation_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    with logger.focus("PyKubeSlurm - Event Added"):
        if event_creation_datetime > APP_STARTED_AT:
            job_properties = job_schema.job_properties()
            job_script = job_properties.pop("script")
            job_payload = {"script": job_script, "job": job_properties}
            response = backend_client.post("/slurm/v0.0.37/job/submit", json=job_payload, auth=lambda r: inject_token(r, "ubuntu"))
            response_json = response.json()
            errors = response_json.get("errors")
            if errors:
                logger.error(f"Error submitting job: {errors}")
                _update_job_crd(JobState.FAILED, errors=[err.get("error") for err in errors])
            else:
                _update_job_crd(JobState.SUBMITTED, errors=None)
        else:
            logger.warning("Event was created before PyKubeSlurm was started. Skipping.")


def _update_slurm_job(job_schema: Job):
    """
    Update a Slurm job by calling the Slurmrestd API.

    Args:
        job_schema: The job schema containing information from the applied manifest.
    """


def _delete_slurm_job(job_schema: Job):
    """
    Delete a Slurm job by calling the Slurmrestd API.

    Args:
        job_schema: The job schema containing information from the applied manifest.
    """
    # missing integration testing
