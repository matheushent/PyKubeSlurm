"""Core module for defining Pydantic schemas."""
from enum import Enum
from typing import Any
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


class JobState(BaseModel):
    """
    Job state model.

    Used to indicate the state of a job, either if it is submitted or not.
    """


class JobState(str, Enum):
    """Slurm job state."""
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class Job(BaseModel):
    """Job CRD model."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Kubernetes stuff
    api_version: str = Field(..., alias="apiVersion")
    kind: str
    metadata: dict

    # Control stuff
    slurm_job_id: None | int = None
    get_user_environment: None | int = None
    state: None | JobState = None
    error: None | list[str] = None

    # Job stuff
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
    begin_time: None | int = None
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
    required_nodes: None | list[str] = None
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
    nodes: None | str = None
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

    def job_properties(self) -> dict:
        return self.model_dump(exclude=["api_version", "kind", "metadata", "slurm_job_id"], exclude_unset=True)
    
    @model_validator(mode="after")
    def check_user_environment(self) -> "Job":
        if self.environment is None:
            self.get_user_environment = 1
        return self
