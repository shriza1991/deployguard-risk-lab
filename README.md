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

### Authentication architecture

Incoming bearer tokens are validated by `validate_access_token()` in `backend/auth/jwt.py`. The API dependency layer resolves the authenticated user and records failed validation attempts using the configured authentication log level.

User-facing routes receive a `UserPermissionService` through FastAPI dependencies. The service owns directory, profile, and user-management decisions so route handlers can share the same role evaluation behavior.

The user list response includes the active-directory selection and permission cache interval. Configure `PERMISSION_CACHE_SECONDS` and `AUTHENTICATION_FAILURE_LOG_LEVEL` for each environment before deployment.

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

#TEST
Testing DeployGuard GitHub webhook integration.

## Deployment Security

DeployGuard now performs automated AI-powered deployment risk analysis before production deployments.

webhook test!!!
