# DeployGuard Risk Lab

DeployGuard Risk Lab is a deliberately realistic but non-production monorepo used to generate pull requests for AI-powered DevSecOps analysis. The `main` branch is a clean, secure baseline. Risky changes should be introduced later on feature branches so DeployGuard can evaluate meaningful diffs.

## Architecture

- `backend`: FastAPI service with JWT authentication, shared session validation, role permissions, SQLAlchemy models, configuration, and tests.
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

## Authentication flow

Login issues JWTs with a configured issuer and audience. Protected API requests first pass through
session middleware, which calls `validate_session_token()` and uses a short, expiry-bounded cache.
Route dependencies then resolve the active user, and `PermissionService` performs role checks for
the requested operation. Configure `SESSION_CACHE_TTL`, `TOKEN_ISSUER`, and `TOKEN_AUDIENCE`
alongside `JWT_SECRET_KEY` in each environment.

## Deploy

Terraform and Kubernetes files are examples for analysis and lab use. Review variables, image references, DNS names, and certificate handling before applying them in any real environment.

#TEST
Testing DeployGuard GitHub webhook integration.
