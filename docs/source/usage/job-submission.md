# Submitting Jobs to Slurm using PyKubeSlurm

To submit jobs to Slurm using PyKubeSlurm, ensure that PyKubeSlurm is up and running within your Kubernetes cluster. You should also have `kubectl` available for job submission. Below is an example of a Kubernetes CRD to create a Slurm job.

```yaml
apiVersion: mhtosta.engineering/v1alpha1
kind: SlurmJob
metadata:
  name: example-slurm-job--1hour
spec:
  script: |
    #!/bin/bash
    echo "I'm an example"
  cpus_per_task: 1
  standard_error: "/tmp/err.log"
  standard_output: "/tmp/out.log"
  current_working_directory: "/tmp"
  time_limit: 90
  name: now-job-1hour
  begin_time: now+1hour
```

# Submitting the Job

To submit the job, you can use `kubectl` and apply the YAML configuration file:

```bash
kubectl apply -f your-job-config.yaml
```

Replace `your-job-config.yaml` with the actual file containing your Slurm job configuration. You can also apply using `stdin`:

```bash
kubectl apply -f - <<EOF
apiVersion: mhtosta.engineering/v1alpha1
kind: SlurmJob
metadata:
  name: example-slurm-job--1hour
spec:
  script: |
    #!/bin/bash
    echo "I'm an example"
  cpus_per_task: 1
  standard_error: "/tmp/err.log"
  standard_output: "/tmp/out.log"
  current_working_directory: "/tmp"
  time_limit: 90
  name: now-job-1hour
  begin_time: now+1hour
EOF
```

By following these steps, you can easily submit jobs to Slurm using PyKubeSlurm, leveraging the flexibility and power of Kubernetes Custom Resource Definitions (CRDs) to define your job configurations.

# Available Parameters for Slurm Job

PyKubeSlurm provides a wide range of parameters to customize Slurm job configurations. Below is a comprehensive list of available parameters, along with their respective data types:

- `script`: (Type: string) The job script to execute.
- `account`: (Type: string) The account associated with the job.
- `cpus_per_task`: (Type: integer) The number of CPUs per task (format: int32).
- `name`: (Type: string) The name of the job.
- `partition`: (Type: string) The Slurm partition where the job should run.
- `admin_comment`: (Type: string) An administrator comment for the job.
- `allocation_node_list`: (Type: string) The list of allocation nodes.
- `allocation_node_port`: (Type: integer) Port number for allocation nodes (format: int32).
- `argv`: (Type: array of strings) An array of arguments for the job.
- `batch_features`: (Type: string) Features associated with the batch.
- `begin_time`: (Type: string) The job's start time, supporting various time formats.
- `flags`: (Type: array of strings) An array of job flags.
- `burst_buffer`: (Type: string) Burst buffer settings for the job.
- `clusters`: (Type: string) Cluster-specific settings.
- `cluster_constraint`: (Type: string) Cluster constraint settings.
- `comment`: (Type: string) Comments related to the job.
- `contiguous`: (Type: boolean) Flag indicating job continuity.
- `container`: (Type: string) The container to use for the job.
- `container_id`: (Type: string) The ID of the container.
- `core_specification`: (Type: integer) Specification for CPU cores (format: int32).
- `thread_specification`: (Type: integer) Specification for CPU threads (format: int32).
- `cpu_binding`: (Type: string) CPU binding settings.
- `cpu_binding_flags`: (Type: array of strings) Flags for CPU binding.
- `cpu_frequency`: (Type: string) CPU frequency settings.
- `cpus_per_tres`: (Type: string) CPUs per TRES settings.
- `crontab`: (Type: string) Crontab settings.
- `deadline`: (Type: integer) Job deadline (format: int64).
- `delay_boot`: (Type: integer) Boot delay (format: int32).
- `dependency`: (Type: string) Job dependencies.
- `end_time`: (Type: integer) Job end time (format: int64).
- `environment`: (Type: object) Environment variable settings.
- `excluded_nodes`: (Type: array of strings) Excluded nodes for the job.
- `extra`: (Type: string) Extra job settings.
- `constraints`: (Type: string) Job constraints.
- `group_id`: (Type: string) Group ID for the job.
- `hetjob_group`: (Type: integer) HETJob group (format: int32).
- `immediate`: (Type: boolean) Flag for immediate job execution.
- `job_id`: (Type: integer) Job ID (format: int32).
- `kill_on_node_fail`: (Type: boolean) Flag to kill the job on node failure.
- `licenses`: (Type: string) License requirements.
- `mail_type`: (Type: array of strings) Types of email notifications.
- `mcs_label`: (Type: string) MCS label for the job.
- `memory_binding`: (Type: string) Memory binding settings.
- `memory_binding_type`: (Type: array of strings) Types of memory binding.
- `memory_per_tres`: (Type: string) Memory per TRES settings.
- `network`: (Type: string) Network settings.
- `nice`: (Type: integer) Nice value (format: int32).
- `tasks`: (Type: integer) Number of tasks (format: int32).
- `open_mode`: (Type: array of strings) Open mode settings.
- `reserve_ports`: (Type: integer) Number of ports to reserve (format: int32).
- `overcommit`: (Type: boolean) Flag for overcommitting resources.
- `distribution_plane_size`: (Type: integer) Distribution plane size (format: int32).
- `power_flags`: (Type: array of strings) Power-related flags.
- `prefer`: (Type: string) Preferred resources.
- `hold`: (Type: boolean) Flag to hold the job.
- `priority`: (Type: integer) Job priority (format: int32).
- `profile`: (Type: array of strings) Job profiles.
- `qos`: (Type: string) Quality of Service settings.
- `reboot`: (Type: boolean) Flag to reboot nodes.
- `requeue`: (Type: boolean) Flag to allow requeuing.
- `reservation`: (Type: string) Reservation settings.
- `shared`: (Type: array of strings) Shared resource settings.
- `exclusive`: (Type: array of strings) Exclusive resource settings.
- `oversubscribe`: (Type: boolean) Flag to allow oversubscription.
- `site_factor`: (Type: integer) Site factor (format: int32).
- `spank_environment`: (Type: array of strings) SPANK environment settings.
- `distribution`: (Type: string) Distribution settings.
- `time_limit`: (Type: integer) Time limit for the job (format: int32).
- `time_minimum`: (Type: integer) Minimum time limit (format: int32).
- `tres_bind`: (Type: string) TRES binding settings.
- `tres_freq`: (Type: string) TRES frequency settings.
- `tres_per_job`: (Type: string) TRES per job settings.
- `tres_per_node`: (Type: string) TRES per node settings.
- `tres_per_socket`: (Type: string) TRES per socket settings.
- `tres_per_task`: (Type: string) TRES per task settings.
- `user_id`: (Type: string) User ID associated with the job.
- `wait_all_nodes`: (Type: boolean) Flag to wait for all nodes.
- `kill_warning_flags`: (Type: array of strings) Flags for kill warnings.
- `kill_warning_signal`: (Type: string) Signal for kill warnings.
- `kill_warning_delay`: (Type: integer) Kill warning delay (format: int16).
- `current_working_directory`: (Type: string) Working directory for the job.
- `minimum_cpus`: (Type: integer) Minimum CPUs required (format: int32).
- `maximum_cpus`: (Type: integer) Maximum CPUs allowed (format: int32).
- `nodes`: (Type: array of integers) List of node IDs (format: int32).
- `minimum_nodes`: (Type: integer) Minimum number of nodes (format: int32).
- `maximum_nodes`: (Type: integer) Maximum number of nodes (format: int32).
- `minimum_boards_per_node`: (Type: integer) Minimum boards per node (format: int32).
- `minimum_sockets_per_board`: (Type: integer) Minimum sockets per board (format: int32).
- `sockets_per_node`: (Type: integer) Number of sockets per node (format: int32).
- `threads_per_core`: (Type: integer) Number of threads per core (format: int32).
- `tasks_per_node`: (Type: integer) Number of tasks per node (format: int32).
- `tasks_per_socket`: (Type: integer) Number of tasks per socket (format: int32).
- `tasks_per_core`: (Type: integer) Number of tasks per core (format: int32).
- `tasks_per_board`: (Type: integer) Number of tasks per board (format: int32).
- `ntasks_per_tres`: (Type: integer) Number of tasks per TRES (format: int32).
- `minimum_cpus_per_node`: (Type: integer) Minimum CPUs per node (format: int32).
- `memory_per_cpu`: (Type: integer) Memory per CPU (format: uint64).
- `memory_per_node`: (Type: integer) Memory per node (format: uint64).
- `temporary_disk_per_node`: (Type: integer) Temporary disk per node (format: int32).
- `selinux_context`: (Type: string) SELinux context settings.
- `required_switches`: (Type: integer) Required switches (format: uint32).
- `standard_error`: (Type: string) Path to the standard error file.
- `standard_input`: (Type: string) Path to the standard input file.
- `standard_output`: (Type: string) Path to the standard output file.
- `wait_for_switch`: (Type: integer) Time to wait for switches (format: int32).
- `wckey`: (Type: string) Workload Characterization (WCKey) for the job.
- `x11`: (Type: array of strings) X11 settings.
- `x11_magic_cookie`: (Type: string) X11 magic cookie for authentication.
- `x11_target_host`: (Type: string) X11 target host settings.
- `x11_target_port`: (Type: integer) X11 target port number (format: int32).

Please note that this list covers all available parameters for customizing Slurm job configurations. Customize these parameters based on your specific job requirements to leverage the full power of PyKubeSlurm and Slurm job management.

!!! warning

    PyKubeSlurm was built on top of Slurmrestd 0.0.36. If you find any error related to these parameters, let us know by opening an issue on [GitHub](https://github.com/matheushent/PyKubeSlurm).