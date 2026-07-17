# Architecture

The repository models a small SaaS control plane. A FastAPI backend owns authentication, users, and audit events. A React frontend consumes the API through a typed service boundary. Infrastructure examples show how the workload could be deployed to AWS and Kubernetes with secure defaults.

The design intentionally spans application code, CI/CD, containers, cloud infrastructure, and orchestration so pull requests can exercise multiple DeployGuard agents.

