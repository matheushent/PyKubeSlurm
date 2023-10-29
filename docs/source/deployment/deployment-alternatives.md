## Deploy Alternatives

In cases where direct access to the Slurmrestd endpoint is not achievable, consider the following deployment alternatives:

- **VPN or Network Configuration**: Set up a Virtual Private Network (VPN) or configure network settings to ensure that the Kubernetes network can access the Slurmrestd endpoint securely.

- **Proxied Access**: Use a proxy server to route requests from the Kubernetes network to the Slurmrestd endpoint.

- **Kubernetes Pod Deployment**: Deploy PyKubeSlurm within a Kubernetes Pod that is part of the same network as the Slurmrestd endpoint. This can be achieved by carefully configuring your Kubernetes deployment.

It's important to adapt your deployment strategy to meet the accessibility requirements of the Slurmrestd endpoint.

Please ensure that your Kubernetes cluster meets the version requirements, and that the Slurmrestd endpoint accessibility is in place or alternatives are considered to fully utilize PyKubeSlurm for job scheduling and management.