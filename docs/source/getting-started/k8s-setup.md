# Configuring the Kubernetes Cluster for PyKubeSlurm Deployment

This document provides step-by-step instructions on how to configure your Kubernetes cluster for the deployment of PyKubeSlurm. To successfully set up PyKubeSlurm, ensure that you meet the following requirements:

## Requirements

1. **kubectl**: Ensure you have `kubectl` installed and configured to interact with your Kubernetes cluster.

2. **Kubernetes Cluster Access**: You should have access to your Kubernetes cluster to perform configuration tasks.

3. **JWT Key for Slurmrestd**: You need access to the JWT (JSON Web Token) key used to configure Slurmrestd for secure communication. Ensure you have the JWT key ready for the configuration steps.

## Creating a ConfigMap for the JWT Key

To configure PyKubeSlurm for secure communication with Slurmrestd, you need to create a ConfigMap containing the JWT key. This ConfigMap will be used by PyKubeSlurm for authentication.

Supposing the JWT key content is stored locally on your system at `/tmp/jwt.key`, follow these steps to create a ConfigMap with the JWT key:

1. Open your preferred terminal.

2. Use the following command to create a ConfigMap:

    ```bash
    kubectl create configmap pykubeslurm-jwt --from-file=jwt.key=/tmp/jwt.key
    ```

3. Verify that the ConfigMap has been created successfully by running:

    ```bash
    kubectl describe configmap pykubeslurm-jwt
    ```

    This command should display information about the newly created ConfigMap, including the JWT key.

4. You can now use the ConfigMap `pykubeslurm-jwt` in your PyKubeSlurm deployment configuration to ensure secure communication with Slurmrestd.

With the ConfigMap in place, PyKubeSlurm can securely access and communicate with Slurmrestd using the JWT key provided in the ConfigMap.

Please ensure that you have the necessary permissions and access to create ConfigMaps in your Kubernetes cluster. Additionally, use the actual JWT key for secure configuration.
