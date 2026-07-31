# DeployGuard Risk Lab

DeployGuard Risk Lab is a deliberately realistic but non-production monorepo used to generate pull requests for AI-powered DevSecOps analysis. The `main` branch is a clean, secure baseline. Risky changes should be introduced later on feature branches so DeployGuard can evaluate meaningful diffs.

## Architecture

- `backend`: FastAPI service with JWT authentication, SQLAlchemy models, Pydantic schemas, logging, modular `DeploymentSecurity` helper, configuration management, and pytest test suite.
- `frontend`: React and Vite single-page app with login, dashboard, routed views, and an API client.
- `infrastructure/terraform`: AWS examples for VPC, EC2, IAM, S3, KMS, and security groups.
- `infrastructure/kubernetes`: Hardened Kubernetes manifests featuring centralized pod security contexts (`runAsNonRoot: true`, `UID: 10001`), startup probes, and tuned resource limits.
- `infrastructure/helm`: Helm chart mirroring the Kubernetes workload utilizing reusable `_helpers.tpl` templates for security context and metadata labels.
- `docker`: Multi-stage Dockerfiles (`docker/Dockerfile` & `backend/Dockerfile`) with build layer caching, non-root user execution (`appuser: 10001`), and health checks.
- `.github/workflows`: Hardened CI/CD pipelines with dependency caching (`pip` & `npm`), explicit job permissions (`contents: read`), workflow concurrency limits, and artifact packaging.

## Run Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

## Run With Docker

```bash
export JWT_SECRET_KEY="$(openssl rand -hex 32)"
cd docker
docker compose up --build
```

## Platform Hardening & Deployment Specs

- **Non-Root Execution**: Runtime containers enforce user UID `10001` (`appuser`) with read-only root filesystems and dropped capabilities (`drop: ["ALL"]`).
- **Health Probes**: Probes include `startupProbe` (initialization buffer), `livenessProbe` (crash detection), and `readinessProbe` (traffic routing).
- **Application Security Baseline**: The shared `DeploymentSecurity` module (`backend/app/deployment_security.py`) dynamically injects security headers, validates token policies, and monitors environment posture.
- **CI Caching**: GitHub Actions workflows utilize `actions/setup-python` and `actions/setup-node` caching with explicit dependency lockfile hashes.

Terraform and Kubernetes files are examples for analysis and lab use. Review variables, image references, DNS names, and certificate handling before applying them in any real environment.
