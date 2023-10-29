# Requirements

PyKubeSlurm is a powerful Python package designed to simplify job scheduling in Kubernetes environments. To ensure successful installation and operation of PyKubeSlurm, please review the following requirements.

## System Requirements

- **Kubernetes Version**: PyKubeSlurm is compatible with Kubernetes versions >= 1.23. Ensure that your Kubernetes cluster meets this version requirement.

- **Slurmrestd Version**: PyKubeSlurm works with Slurmrestd version 0.0.36. Ensure that you have Slurmrestd version 0.0.36 installed in your Slurm cluster to ensure compatibility.

- **Federated Clusters**: Please note that PyKubeSlurm does not yet support federated clusters. Ensure that your Slurm cluster is not part of a federated setup when using PyKubeSlurm.

- **JWT Authentication**: PyKubeSlurm uses JWT (JSON Web Token) authentication for secure communication with Slurmrestd. Ensure that you have JWT authentication properly configured in your Slurmrestd setup.

- **Slurmrestd Accessibility**: Underlying PyKubeSlurm's mechanisms, it relies on Slurmrestd to submit and fetch resources against a Slurm cluster. To use PyKubeSlurm effectively, the Slurmrestd endpoint must be accessible by the Kubernetes network in which PyKubeSlurm runs. It is essential for PyKubeSlurm to establish a connection with Slurmrestd for job scheduling and management.

    If you are unable to meet this requirement or seek alternative deployment options, please refer to the [Deploy Alternatives](../deployment/deployment-alternatives.md) section for guidance.
