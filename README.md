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

The deployment artifacts support a container image, Helm release, and Terraform environment. Build the image from the repository root so the frontend bundle is included:

```bash
docker build -f docker/Dockerfile -t deployguard-risk-lab:local .
```

Configure the chart values for the target environment before rendering manifests:

```bash
helm template deployguard-risk-lab infrastructure/helm \
  --set image.tag="$IMAGE_TAG" \
  --set application.environment=staging
```

Use Terraform plans to review infrastructure changes before applying them:

```bash
cd infrastructure/terraform
terraform init
terraform plan -var="environment=staging"
```

The API exposes `/api/v1/health` for platform checks. The container health check uses the same endpoint and honors the `APP_PORT` environment variable.

Review image references, DNS names, certificates, and environment-specific Helm values before applying any deployment configuration.

#TEST
Testing DeployGuard GitHub webhook integration.

## Deployment Security

DeployGuard now performs automated AI-powered deployment risk analysis before production deployments.

webhook test!!!
