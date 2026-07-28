# DeployGuard Risk Lab

DeployGuard Risk Lab is a deliberately realistic but non-production monorepo used to generate pull requests for AI-powered DevSecOps analysis. The `main` branch is a clean, secure baseline. Risky changes should be introduced later on feature branches so DeployGuard can evaluate meaningful diffs.

## Architecture

- `backend`: FastAPI service with JWT authentication, SQLAlchemy models, Pydantic schemas, logging, configuration, and tests.
- `frontend`: React and Vite single-page app with login, dashboard, routed views, and an API client.
- `infrastructure/terraform`: AWS examples for VPC, EC2, IAM, S3, KMS, and security groups.
- `infrastructure/kubernetes`: Secure Kubernetes manifests with probes, resource limits, and restricted pod security posture.
- `infrastructure/helm`: Helm chart mirroring the Kubernetes workload.
- `docker`: Multi-stage application image, Compose stack, and Nginx reverse proxy.
- `.github/workflows`: CI and deployment workflows for linting, tests, builds, and artifacts.

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

## Deploy

Terraform and Kubernetes files are examples for analysis and lab use. Review variables, image references, DNS names, and certificate handling before applying them in any real environment.

### Deployment Reliability Improvements

The pipeline caches Python dependencies and validates the saved container image
through a deployment smoke test. Docker builds use cache-friendly dependency
layers, attach an application version label, run as a dedicated unprivileged
user, and expose a production healthcheck.

Compose automatically restarts services, rotates local logs, waits for API
health before starting nginx, and mounts local operational configuration
read-only at `/app/config`. Kubernetes rolls out updates without planned
unavailability and uses explicit readiness/liveness probe thresholds.

Terraform enables versioned, KMS-encrypted artifact storage, applies platform
ownership tags by default, and limits SSH administration to configured CIDRs.

#TEST
Testing DeployGuard GitHub webhook integration.
