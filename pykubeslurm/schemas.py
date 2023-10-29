"""Core module for defining Pydantic schemas or typed dictionaries."""
import datetime
from enum import Enum
from typing import Any, TypedDict

from pydantic import BaseModel, ConfigDict, Field, model_validator


class KubernetesEventType(str, Enum):
    """Kubernetes event type."""

    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"
    ERROR = "ERROR"


class KubernetesEvent(BaseModel):
    """Kubernetes event model."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    object: dict[str, Any]
    raw_object: dict[str, Any]
    type: KubernetesEventType


class JobState(str, Enum):
    """Slurm job state."""

    UNKNOWN = "UNKNOWN"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"

    def __str__(self) -> str:
        return self.value


class KubernetesObjectMeta(BaseModel):
    """Kubernetes object metadata."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    name: str
    generate_name: None | str = Field(None, alias="generateName")
    namespace: str
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)
    creation_timestamp: None | datetime.datetime = Field(None, alias="creationTimestamp")


class KubernetesResource(BaseModel):
    """Common Kubernetes fields."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    api_version: str = Field(..., alias="apiVersion")
    kind: str
    metadata: KubernetesObjectMeta
    spec: dict[Any, Any]


class JobProperties(BaseModel):
    """Job properties model."""

    script: str
    account: None | str = None
    cpus_per_task: None | int = None
    name: None | str = None
    partition: None | str = None
    admin_comment: None | str = None
    allocation_node_list: None | str = None
    allocation_node_port: None | int = None
    argv: None | list[str] = None
    batch_features: None | str = None
    begin_time: None | str = None
    flags: None | list[str] = None
    burst_buffer: None | str = None
    clusters: None | str = None
    cluster_constraint: None | str = None
    comment: None | str = None
    contiguous: None | bool = None
    container: None | str = None
    container_id: None | str = None
    core_specification: None | int = None
    thread_specification: None | int = None
    cpu_binding: None | str = None
    cpu_binding_flags: None | list[str] = None
    cpu_frequency: None | str = None
    cpus_per_tres: None | str = None
    crontab: None | str = None
    deadline: None | int = None
    delay_boot: None | int = None
    dependency: None | str = None
    end_time: None | int = None
    environment: None | dict[str, Any] = None
    excluded_nodes: None | list[str] = None
    extra: None | str = None
    constraints: None | str = None
    group_id: None | str = None
    hetjob_group: None | int = None
    immediate: None | bool = None
    job_id: None | int = None
    kill_on_node_fail: None | bool = None
    licenses: None | str = None
    mail_type: None | list[str] = None
    mcs_label: None | str = None
    memory_binding: None | str = None
    memory_binding_type: None | list[str] = None
    memory_per_tres: None | str = None
    network: None | str = None
    nice: None | int = None
    tasks: None | int = None
    open_mode: None | list[str] = None
    reserve_ports: None | int = None
    overcommit: None | bool = None
    distribution_plane_size: None | int = None
    power_flags: None | list[str] = None
    prefer: None | str = None
    hold: None | bool = None
    priority: None | int = None
    profile: None | list[str] = None
    qos: None | str = None
    reboot: None | bool = None
    requeue: None | bool = None
    reservation: None | str = None
    shared: None | list[str] = None
    exclusive: None | list[str] = None
    oversubscribe: None | bool = None
    site_factor: None | int = None
    spank_environment: None | list[str] = None
    distribution: None | str = None
    time_limit: None | int = None
    time_minimum: None | int = None
    tres_bind: None | str = None
    tres_freq: None | str = None
    tres_per_job: None | str = None
    tres_per_node: None | str = None
    tres_per_socket: None | str = None
    tres_per_task: None | str = None
    user_id: None | str = None
    wait_all_nodes: None | bool = None
    kill_warning_flags: None | list[str] = None
    kill_warning_signal: None | str = None
    kill_warning_delay: None | int = None
    current_working_directory: None | str = None
    minimum_cpus: None | int = None
    maximum_cpus: None | int = None
    nodes: None | list[int] = None
    minimum_nodes: None | int = None
    maximum_nodes: None | int = None
    minimum_boards_per_node: None | int = None
    minimum_sockets_per_board: None | int = None
    sockets_per_node: None | int = None
    threads_per_core: None | int = None
    tasks_per_node: None | int = None
    tasks_per_socket: None | int = None
    tasks_per_core: None | int = None
    tasks_per_board: None | int = None
    ntasks_per_tres: None | int = None
    minimum_cpus_per_node: None | int = None
    memory_per_cpu: None | int = None
    memory_per_node: None | int = None
    temporary_disk_per_node: None | int = None
    selinux_context: None | str = None
    required_switches: None | int = None
    standard_error: None | str = None
    standard_input: None | str = None
    standard_output: None | str = None
    wait_for_switch: None | int = None
    wckey: None | str = None
    x11: None | list[str] = None
    x11_magic_cookie: None | str = None
    x11_target_host: None | str = None
    x11_target_port: None | int = None

    # undocumented fields
    get_user_environment: None | int = None

    @model_validator(mode="after")
    def check_user_environment(self) -> "JobProperties":
        if self.environment is None:
            self.get_user_environment = 1
        return self


class JobStatus(BaseModel):
    """Job status model."""

    slurm_job_id: None | int = Field(None, alias="slurmJobId")
    errors: None | list[str] = Field(None)
    state: None | JobState = Field(None)
    updated_at: None | str = Field(None, alias="updatedAt")
    reason: None | str = Field(None)
    last_applied_spec: None | str = Field(None, alias="lastAppliedSpec")


class Job(KubernetesResource):
    """Job CRD model."""

    spec: JobProperties  # type: ignore
    status: None | JobStatus = None

    def job_properties(
        self, exclude: set[int] | set[str] | dict[int, Any] | dict[str, Any] | None = None
    ) -> dict[str, str | int | list[str | int] | bool | dict[str, Any]]:
        """Dump the job properties into a dict."""
        return self.spec.model_dump(exclude_unset=True, exclude=exclude)


class SlurmrestdPluginInfo(TypedDict):
    """Slurmrestd plugin info."""

    type: str
    name: str


class SlurmVersion(TypedDict):
    """Slurm semantic version."""

    major: int
    macro: int
    minor: int


class SlurmrestdSlurmInfo(TypedDict):
    """
    Provide detailed information about the Slurm version retrieved from Slurmrestd.

    Usually, the `release` field is composed as:
    .. code-block:: python
        f"{SlurmVersion.major}.{SlurmVersion.macro}.{SlurmVersion.minor}"
    """

    version: SlurmVersion
    release: str


class SlurmrestdMeta(TypedDict):
    """Slurmrestd meta info."""

    plugin: SlurmrestdPluginInfo
    slurm: SlurmrestdSlurmInfo


class SlurmrestdErrorPayload(TypedDict):
    """Slurmrestd error type in the response payload."""

    description: None | str
    error_number: int
    error: str
    source: str


class SlurmrestdResponse(TypedDict):
    """Base slurmrestd response model."""

    meta: SlurmrestdMeta
    errors: list[SlurmrestdErrorPayload]


class SlurmrestdJobSubmissionResponse(SlurmrestdResponse):
    """Slurmrestd response for the endpoint `POST /slurm/v0.0.36/job/submit`."""

    job_id: None | int
    step_id: None | str
    job_submit_user_msg: None | str
