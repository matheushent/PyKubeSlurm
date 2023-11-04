"""Core module for general helper functions."""
import asyncio
import json
from collections.abc import Coroutine
from datetime import datetime
from string import Template
from typing import Any

from kubernetes import client
from loguru import logger

from pykubeslurm.schemas import (
    Job,
    JobState,
    KubernetesEvent,
    KubernetesEventType,
    SlurmrestdJobSubmissionResponse,
    SlurmrestdResponse,
)
from pykubeslurm.settings import SETTINGS
from pykubeslurm.slurmrestd_interface import backend_client, inject_token
from pykubeslurm.vars import APP_STARTED_AT


def handle_k8s_event(event: KubernetesEvent) -> None:
    """Handle kubernetes events."""
    if event.type == KubernetesEventType.ADDED:
        _add_slurm_job(Job(**event.object))
    if event.type == KubernetesEventType.MODIFIED:
        _update_slurm_job(Job(**event.object))
    if event.type == KubernetesEventType.DELETED:
        _delete_slurm_job(Job(**event.object))


def _patch_object_status(name: str, body: dict[Any, Any]) -> None:
    """Update an object status."""
    client.CustomObjectsApi().patch_namespaced_custom_object_status(
        group=SETTINGS.CRD_GROUP,
        version=SETTINGS.CRD_VERSION,
        namespace=SETTINGS.NAMESPACE,
        plural=SETTINGS.JOB_CRD_PLURAL,
        name=name,
        body=body,
    )


def _build_job_status_body(
    slurm_job_id: None | int,
    state: JobState | str,
    errors: None | list[str],
    job_spec: dict[str, str | int | list[str | int] | bool | dict[str, Any]],
) -> dict[str, int | str | list[str] | None]:
    """Build the job status body."""
    return {
        "slurmJobId": slurm_job_id,
        "errors": errors,
        "state": str(state),
        "updatedAt": datetime_in_string(),
        "lastAppliedSpec": json.dumps(job_spec),
    }


def _update_job_crd(
    *,
    state: None | JobState = None,
    errors: None | list[str],
    name: str,
    slurm_job_id: None | int = None,
) -> None:
    """
    Update the status of the Job CRD and insert its spec as an annotation for internal control.

    Args:
        state: The Slurm job state indicating its submission status.
        errors: Errors occurred when submitting the job by Slurmrestd.
        name: Name of the Kubernetes resource.
    """
    object_body = client.CustomObjectsApi().get_namespaced_custom_object(
        group=SETTINGS.CRD_GROUP,
        version=SETTINGS.CRD_VERSION,
        namespace=SETTINGS.NAMESPACE,
        plural=SETTINGS.JOB_CRD_PLURAL,
        name=name,
    )
    object_body["status"] = _build_job_status_body(
        slurm_job_id=slurm_job_id
        if slurm_job_id is not None
        else object_body.get("status").get("slurmJobId"),
        state=state if state is not None else object_body.get("status").get("state"),
        errors=errors,
        job_spec=object_body["spec"],
    )
    _patch_object_status(name, object_body)


def _add_slurm_job(job_schema: Job) -> None:
    """
    Create a Slurm job by calling the Slurmrestd API.

    Args:
        job_schema: The job schema containing information from the applied manifest.
    """
    event_creation_timestamp = job_schema.metadata.creation_timestamp
    assert event_creation_timestamp is not None  # make mypy happy
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Event Added"):
        if event_creation_timestamp > APP_STARTED_AT:
            job_properties = job_schema.job_properties()
            job_script = job_properties.pop("script")
            job_payload = {"script": job_script, "job": job_properties}
            response = backend_client.post(
                "/slurm/v0.0.36/job/submit",
                json=job_payload,
                auth=lambda r: inject_token(r, "ubuntu"),
            )
            response_json = SlurmrestdJobSubmissionResponse(**response.json())  # type: ignore
            errors = response_json.get("errors")
            if errors:
                logger.error(f"Error submitting job: {errors}")
                _update_job_crd(
                    state=JobState.REJECTED,
                    errors=[err.get("error") for err in errors],
                    name=job_schema.metadata.name,
                    slurm_job_id=response_json.get("job_id"),
                )
            else:
                _update_job_crd(
                    state=JobState.SUBMITTED,
                    errors=None,
                    name=job_schema.metadata.name,
                    slurm_job_id=response_json.get("job_id"),
                )
            logger.success(f"SlurmJob {job_schema.metadata.name} submitted successfully.")
        else:
            logger.warning("Event was created before PyKubeSlurm was started. Skipping.")


def _update_slurm_job(job_schema: Job) -> None:
    """
    Update a Slurm job by calling the Slurmrestd API.

    Args:
        job_schema: The job schema containing information from the applied manifest.
    """
    assert job_schema.status is not None  # make mypy happy
    if job_schema.status.last_applied_spec is None:
        # simply skip since the resource was actually created
        return

    base_warning_message = Template("Unable to update SlurmJob $name because job state is $state")
    if job_schema.status.state not in [
        JobState.SUBMITTED,
        JobState.UNKNOWN,
        JobState.PENDING,
    ]:
        logger.warning(
            base_warning_message.substitute(
                name=job_schema.metadata.name, state=job_schema.status.state
            )
        )
        return

    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Event Updated"):
        managed_spec: dict[str, Any] = json.loads(job_schema.status.last_applied_spec)
        # managed_spec_set = set(managed_spec.items())

        desired_spec = job_schema.job_properties(exclude={"get_user_environment"})
        # desired_spec_set = set(desired_spec.items())

        # spec_diff_set = desired_spec_set - managed_spec_set
        # spec_diff_dict = dict(spec_diff_set)
        spec_diff_dict = {}
        # logger.debug(spec_diff_dict)

        for desired_key, desired_value in desired_spec.items():
            if desired_key not in managed_spec:
                spec_diff_dict[desired_key] = desired_value
            else:
                if desired_value != managed_spec[desired_key]:
                    spec_diff_dict[desired_key] = desired_value

        if spec_diff_dict == {}:
            # Reconcile updated the CRD status. Nothing to update
            return

        logger.debug(f"Updating SlurmJob {job_schema.metadata.name} with {spec_diff_dict}")

        response = backend_client.post(
            f"/slurm/v0.0.36/job/{job_schema.status.slurm_job_id}",
            json=spec_diff_dict,
            auth=lambda r: inject_token(r, "ubuntu"),
        )
        response_json = SlurmrestdResponse(**response.json())  # type: ignore
        if response_json.get("errors"):
            logger.error(f"Error when updating job: {response_json.get('errors')}")
        else:
            _update_job_crd(
                name=job_schema.metadata.name,
                slurm_job_id=job_schema.status.slurm_job_id,
                errors=None,
            )
            logger.success(f"SlurmJob {job_schema.metadata.name} updated successfully.")


def _delete_slurm_job(job_schema: Job) -> None:
    """
    Delete a Slurm job by calling the Slurmrestd API.

    Args:
        job_schema: The job schema containing information from the applied manifest.
    """
    # Jobs aren't being deleted by SLurmrestd at the moment
    # [Reference](https://bugs.schedmd.com/show_bug.cgi?id=18006)
    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus("PyKubeSlurm - Event Deleted"):
        logger.warning(f"Skipping SlurmJob {job_schema.metadata.name} deletion by Slurmrestd")


async def run_coroutines(*coros: Coroutine[Any, Any, Any]) -> None:
    """Run coroutines concurrently."""
    await asyncio.gather(*coros)


def datetime_in_string() -> str:
    """Return the current datetime in string format."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
