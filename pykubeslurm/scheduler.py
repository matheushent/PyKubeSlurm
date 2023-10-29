"""Core module for defining the reconciliation schedule logic."""
import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from kubernetes import client
from loguru import logger

from pykubeslurm.errors import ERROR_DICT
from pykubeslurm.helpers import datetime_in_string, run_coroutines
from pykubeslurm.schemas import JobState, JobStatus
from pykubeslurm.settings import SETTINGS
from pykubeslurm.slurmrestd_interface import backend_client


async def process_job_crd(job_status: JobStatus, name: str) -> None:
    """
    Process the Job CRD by fetching its data from slurmrestd and updating the SlurmJob CRD.

    Args:
        job_status: Job status instance model.
        name: Name of the Job CRD.
    """
    api = client.CustomObjectsApi()

    assert hasattr(logger, "focus")  # make mypy happy
    with logger.focus(f"PyKubeSlurm - SlurmJob {name} Reconciliation"):
        logger.info(f"Started reconciliation for SlurmJob {name}")
        slurmrestd_response = backend_client.get(f"/slurmdb/v0.0.36/job/{job_status.slurm_job_id}")

        slurmrestd_response_data = slurmrestd_response.json()
        errors = slurmrestd_response_data.get("errors")
        if errors:
            logger.error(
                f"Error fetching job from slurmrestd: {slurmrestd_response_data['errors']}"
            )
            api.patch_namespaced_custom_object_status(
                group=SETTINGS.CRD_GROUP,
                version=SETTINGS.CRD_VERSION,
                namespace=SETTINGS.NAMESPACE,
                plural=SETTINGS.JOB_CRD_PLURAL,
                name=name,
                body={
                    "status": {
                        "slurmJobId": job_status.slurm_job_id,
                        "state": JobState.UNKNOWN.value,
                        "errors": [ERROR_DICT.get(error.get("error_number")) for error in errors],
                        "updatedAt": datetime_in_string(),
                        "reason": None,
                        "lastAppliedSpec": job_status.last_applied_spec,
                    }
                },
            )
            return

        # In Slurm, the tuple (job_id, cluster) is unique. As PyKubeSlurm doesn't support
        # federated clusters yet, we take the first element of the job list.
        assert (
            len(slurmrestd_response_data["jobs"]) == 1
        ), "Federated clusters are not supported yet"
        job = slurmrestd_response_data["jobs"][0]
        job_state = JobState(job.get("state").get("current"))
        reason = job.get("state").get("reason")

        logger.info(f"Updating Job CRD {name} to state {job_state.value}, reason: {reason}")
        api.patch_namespaced_custom_object_status(
            group=SETTINGS.CRD_GROUP,
            version=SETTINGS.CRD_VERSION,
            namespace=SETTINGS.NAMESPACE,
            plural=SETTINGS.JOB_CRD_PLURAL,
            name=name,
            body={
                "status": {
                    "state": job_state.value,
                    "reason": reason,
                    "updatedAt": datetime_in_string(),
                    "slurmJobId": job_status.slurm_job_id,
                    "errors": [],
                    "lastAppliedSpec": job_status.last_applied_spec,
                }
            },
        )


def reconcile() -> None:
    """Reconcile jobs submitted to slurmrestd."""
    api = client.CustomObjectsApi()

    resources = api.list_namespaced_custom_object(
        group=SETTINGS.CRD_GROUP,
        version=SETTINGS.CRD_VERSION,
        namespace=SETTINGS.NAMESPACE,
        plural=SETTINGS.JOB_CRD_PLURAL,
    )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [
        process_job_crd(JobStatus(**resource.get("status")), resource.get("metadata").get("name"))
        for resource in resources.get("items")
        if resource.get("status").get("state")
        in [JobState.SUBMITTED, JobState.UNKNOWN, JobState.PENDING, JobState.RUNNING]
    ]
    if not tasks:
        logger.info("No jobs to reconcile")
    asyncio.run(run_coroutines(*tasks))


def init_scheduler() -> None:
    """Initialize the scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=reconcile,
        trigger="interval",
        seconds=SETTINGS.RECONCILIATION_TIME,
        id="reconcile_jobs",
    )
    scheduler.start()
