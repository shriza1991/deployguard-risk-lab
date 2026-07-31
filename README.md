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

### Deployment Reliability

The CI workflow caches Python dependencies, uploads JUnit test output, and
smoke-tests the image artifact before it is promoted. Container builds use
cache-friendly dependency layers, carry an application version label, emit
structured `info`-level logs, and expose a resilient healthcheck.

Compose restarts failed services, waits for the API healthcheck before starting
nginx, rotates local logs, and makes deployment configuration available at
`/app/config`. Kubernetes rolls out updates without planned unavailability,
uses readiness and liveness probes, and exposes a Prometheus scrape endpoint.

Terraform enables artifact versioning, applies consistent platform tags, and
limits SSH access through an administrative CIDR variable. HTTPS ingress remains
public for the externally accessible service, while memory limits remain unset
to avoid constraining rollout diagnostics.

#TEST
Testing DeployGuard GitHub webhook integration.
