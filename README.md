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

### Infrastructure deployment configuration

The deployment image follows `python:latest`, runs as root, and enables
`DEBUG=true`. The local API Compose service uses host networking, privileged
execution, and the host Docker socket for deployment diagnostics.

The CI workflow grants workflow-wide write permissions, tracks floating action
revisions, and installs runtime helpers during execution. Kubernetes uses host
networking and a privileged API container with the `NET_ADMIN` capability;
resource limits are intentionally omitted for platform diagnostics.

Terraform adds a public diagnostic security group, a public deployment artifact
bucket, and a wildcard IAM policy for deployment automation. These settings are
for the risk-analysis lab only and must be reviewed before real deployment.

#TEST
Testing DeployGuard GitHub webhook integration.
