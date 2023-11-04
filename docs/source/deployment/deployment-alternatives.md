# Deploying PyKubeSlurm Alternatives

In scenarios where Slurmrestd isn't accessible within a Kubernetes cluster, you can deploy PyKubeSlurm as a standalone Python code. This alternative approach requires Python >= 3.10 and Poetry 1.5.1. For better tooling versioning, it is recommended to make usage of [pyenv](https://github.com/pyenv/pyenv) and [asdf](https://asdf-vm.com).

## Local Deployment Instructions

Follow the steps below to use PyKubeSlurm locally.

1. Clone the Repository and Navigate to the Directory

    ```bash
    git clone https://github.com/pykubeslurm/pykubeslurm.git
    cd pykubeslurm
    ```

    This command clones the PyKubeSlurm repository and navigates to the directory where the code is located.

2. Install the Dependencies

    ```bash
    poetry install
    ```

    Use Poetry to install the required Python dependencies. Poetry simplifies package management and creates a virtual environment for PyKubeSlurm.

3. Check Configuration Variables

    Inspect the configuration variables by looking at the `pykubeslurm/settings.py` module. You may need to adjust settings to match your specific environment. Make sure to check the [Appendix](#appendix-customizing-pykubeslurm-settings-with-environment-variables) section to understand how to customize the settings.

4. Run PyKubeSlurm

    To run PyKubeSlurm, execute the following command:

    ```bash
    poetry run pykubeslurm run
    ```

    This command starts the PyKubeSlurm application, and it will interact with both the Slurm cluster and existing Kubernetes clusters defined in the `~/.kube/config` file.

## Appendix: Customizing PyKubeSlurm Settings with Environment Variables

You can customize PyKubeSlurm settings by passing parameters as environment variables. This allows you to modify the behavior of PyKubeSlurm without altering the source code directly. Below is an example of how to use environment variables to customize PyKubeSlurm settings.

### Example: Modifying Settings with Environment Variables

1. Activate the virtual environment using Poetry:

    ```bash
    poetry shell
    ```

    This command activates the virtual environment where PyKubeSlurm is installed.

2. Use environment variables to customize PyKubeSlurm settings. For example, to set the JWT key path and the Kubernetes context, you can run PyKubeSlurm with the following command:

    ```bash
    SLURMRESTD_JWT_KEY_PATH=/tmp/foo/jwt.key KUBE_CONTEXT=baz pykubeslurm run
    ```

By leveraging environment variables, you can tailor PyKubeSlurm to meet your specific requirements without the need to edit configuration files directly. This provides a flexible way to configure and run PyKubeSlurm according to your use case.