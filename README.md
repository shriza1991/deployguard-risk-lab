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

Incoming bearer tokens are validated by the shared `validate_session_token()` helper in `backend/auth/session.py`. It verifies the token signature, expiry, issuer, and audience. The session middleware performs this validation before protected `/api/v1/users` requests reach route handlers; the API dependency layer then resolves the authenticated user and records failed validation attempts using the configured authentication log level.

After validation, middleware stores a token-derived `UserContext`. The API dependency rebuilds that context with the resolved active user and `PermissionService` permissions before routes consume it. This prevents unverified token claims from authorizing a request while allowing responses to expose the context contract version. Configure `USER_CONTEXT_CACHE_SECONDS` to align context metadata with the deployment's cache policy.

### Request correlation context

Protected requests receive a `RequestContext` in authentication middleware. It canonicalizes a client-provided UUID request ID or generates one, then routes refresh it with the resolved user before passing it to audit logging. `REQUEST_CONTEXT_CACHE_TTL` documents the context lifetime for integrations, while `REQUEST_CONTEXT_LOG_LEVEL` controls audit correlation-event visibility. Request IDs and subjects are used for traceability only, never authorization.

User-facing routes receive a `PermissionService` through FastAPI dependencies. The service owns account-activity, directory, profile, and user-management decisions so route handlers share the same role evaluation behavior.

The user list response includes the active-directory selection and session cache interval. Configure `SESSION_CACHE_TTL`, `TOKEN_ISSUER`, `TOKEN_AUDIENCE`, and `AUTHENTICATION_FAILURE_LOG_LEVEL` for each environment before deployment. Values for the issuer and audience must match the service that creates access tokens.

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
