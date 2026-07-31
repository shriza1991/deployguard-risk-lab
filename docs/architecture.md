# Architecture

The repository models a small SaaS control plane. A FastAPI backend owns authentication, users, and audit events. A React frontend consumes the API through a typed service boundary. Infrastructure examples show how the workload could be deployed to AWS and Kubernetes with secure defaults.

The design intentionally spans application code, CI/CD, containers, cloud infrastructure, and orchestration so pull requests can exercise multiple DeployGuard agents.

## Deployment Architecture & Platform Hardening

### 1. Shared Deployment Security Helper (`DeploymentSecurity`)
The application uses a centralized security helper (`backend/app/deployment_security.py`) integrated into application setup (`app/main.py`), configuration management (`app/config.py`), security middleware (`app/security_headers.py`), authentication (`auth/jwt.py`), audit tracking (`services/audit_service.py`), and health probes (`api/v1_health.py`).

Key responsibilities:
- **Runtime Posture Check**: Verifies non-root container process execution (UID 10001) and security hardening status.
- **Security Headers Policy**: Generates standard HSTS, CSP, X-Frame-Options, X-Content-Type-Options, and Referrer-Policy headers.
- **Token Security Enforcement**: Enforces token lifespan caps and forbids weak cryptographic algorithms.
- **Health & Probe Status**: Exposes deployment metadata to Kubernetes liveness, readiness, and startup probes.

### 2. Multi-Stage Container Runtime
- Multi-stage Docker builds (`docker/Dockerfile` and `backend/Dockerfile`) separate build dependencies from runtime binaries.
- Dedicated non-root user `10001` (`appuser`) owns application assets.
- Dependency caching is optimized by separating `requirements.txt` / `package.json` copying from source code copy instructions.

### 3. Kubernetes & Helm Infrastructure
- Workloads deploy with centralized pod security context (`runAsNonRoot: true`, `runAsUser: 10001`, `seccompProfile: RuntimeDefault`) and container security context (`allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities: drop ALL`).
- Resource limits and requests are configured for predictable resource management (`requests: 250m / 256Mi`, `limits: 1000m / 512Mi`).
- Pod lifecycle management includes `startupProbe`, `livenessProbe`, and `readinessProbe`.
- Helm deployment utilizes reusable helper templates (`_helpers.tpl`) for common labels and security posture formatting.

### 4. CI/CD Pipeline Security
- GitHub Actions workflows (`.github/workflows/ci.yml` and `deploy.yml`) enforce minimal permissions (`contents: read`).
- Reusable pipeline environment variables (`PYTHON_VERSION`, `NODE_VERSION`, `IMAGE_NAME`) centralize workflow constants.
- Dependency caching (`pip` and `npm`) speeds up CI execution and avoids unneeded package index fetches.
- Workflow concurrency settings prevent overlapping execution on push events.
