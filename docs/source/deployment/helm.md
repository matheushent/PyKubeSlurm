# Deploying PyKubeSlurm with Helm Chart

This guide provides step-by-step instructions on how to deploy PyKubeSlurm using a Helm chart. Helm simplifies the installation and management of PyKubeSlurm in your Kubernetes cluster.

## Prerequisites

Before you begin, ensure you have the following prerequisites in place:

- **Kubernetes Cluster**: You should have a Kubernetes cluster up and running. PyKubeSlurm is designed to work with Kubernetes versions >= 1.23.

- **kubectl**: Ensure that you have `kubectl` installed and configured to interact with your Kubernetes cluster.

- **Helm 3**: You need Helm 3 installed on your local machine. If you don't have Helm 3, follow the official Helm 3 installation instructions: [Helm 3 Installation Guide](https://helm.sh/docs/intro/install/).

## Deploy PyKubeSlurm with Helm

Follow these steps to deploy PyKubeSlurm using a Helm chart:

1. Open your terminal.

2. Clone the PyKubeSlurm repository from the upstream GitHub repo:

    ```bash
    git clone https://github.com/matheus/PyKubeSlurm.git
    ```

3. Change to the cloned directory:

    ```bash
    cd PyKubeSlurm/chart
    ```

4. Create a `values.yaml` file to customize your PyKubeSlurm deployment. You can use Helm's default `values.yaml` as a starting point:

    ```bash
    helm show values .
    ```

    You can edit `values.yaml` to configure PyKubeSlurm according to your specific requirements. For detailed information on what needs to be configured and how, please refer to the [Appendix](#appendix-helm-chart-values) section to gain a comprehensive understanding of each configuration option.

5. Deploy PyKubeSlurm with Helm, specifying a release name (e.g., pykubeslurm-release) and the path to your `values.yaml` file:

    ```bash
    helm install pykubeslurm-release . -f values.yaml
    ```

6. PyKubeSlurm will be deployed in your Kubernetes cluster. You can monitor the deployment progress by running:

    ```bash
    kubectl get pods
    ```

    Wait for all the pods to be in a running state.

7. Once the deployment is complete, you can create custom CRDs and use PyKubeSlurm for efficient job scheduling in your Kubernetes environment.

## Unstalling PyKubeSlurm

To uninstall PyKubeSlurm, you can use Helm to delete the release:

```bash
helm uninstall pykubeslurm-release
```

This command will remove the PyKubeSlurm deployment and associated resources. Note that no job will actually be deleted on Slurm by taking this action.

## Appendix: Helm Chart Values

The following is an explanation of Helm chart values that you can customize in the `values.yaml` file when deploying PyKubeSlurm:

| Value                                | Description                                      | Default                          |
| ------------------------------------ | ------------------------------------------------ | -------------------------------- |
| replicaCount                         | Number of pod replicas                          | 1                                |
| image.repository                     | Container image repository                       | matheushent/pykubeslurm           |
| image.pullPolicy                     | Container image pull policy                      | IfNotPresent                     |
| image.tag                            | Container image tag                             | "0.1.0-a1"                       |
| rbac.create                          | Whether or not to create RBAC resources         | true                             |
| imagePullSecrets                     | List of image pull secrets                      | [] (empty list)                  |
| nameOverride                         | Override for Helm chart name                    | "" (empty string)                |
| fullnameOverride                     | Override for Helm chart full name               | "" (empty string)                |
| serviceAccount.create                | Create a service account                        | true                             |
| serviceAccount.annotations            | Annotations for the service account             | {} (empty map)                   |
| serviceAccount.name                  | Name of the service account                     | "pykubeslurm"                    |
| pykubeslurm.jwtKeyResourceName        | Name of the JWT key resource on Kubernetes      | pykubeslurm-jwt-key              |
| pykubeslurm.jwtKeyFromSecret          | Use Secret for JWT key                          | true                             |
| pykubeslurm.config.debugLevel         | Debug level for the PyKubeSlurm app             | DEBUG                            |
| pykubeslurm.config.eventListenerTimeout | Timeout for event listener in seconds           | 10                               |
| pykubeslurm.config.slurmrestdUserToken | User to call Slurmrestd resources on behalf of | ubuntu                           |
| pykubeslurm.config.slurmrestdTimeout   | Timeout for Slurm REST API in seconds           | 10                               |
| pykubeslurm.config.slurmrestdUrl       | URL of the Slurm REST API                       | http://slurmrestd:6820           |
| pykubeslurm.config.slurmrestdJwtKeyPath | Path to the JWT key file                       | /etc/pykubeslurm/jwt.key         |
| pykubeslurm.config.slurmrestdExpTime   | Token expiration time in seconds                | 3600                             |
| pykubeslurm.config.reconciliationInterval | Reconciliation interval in seconds             | 60                               |
| pykubeslurm.config.healthCheckPort     | Health check port                               | 8080                             |
| podAnnotations                       | Annotations for the pod                         | {} (empty map)                   |
| podSecurityContext                   | Pod security context                            | {} (empty map)                   |
| securityContext                      | Container security context                      | {} (empty map)                   |
| resources                            | Resource limits and requests                    | {} (empty map)                   |
| nodeSelector                         | Node selector for pod placement                 | {} (empty map)                   |
| tolerations                          | Tolerations for pod scheduling                  | [] (empty list)                  |
| affinity                             | Node affinity for pod placement                 | {} (empty map)                   |
