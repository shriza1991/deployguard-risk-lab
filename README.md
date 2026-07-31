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

#TEST
Testing DeployGuard GitHub webhook integration.

## Security & Access Details (for AI Analysis)

### GitHub Repository Settings
- **Public repository**: Accessible for cloning and CI/CD
- **CI/CD workflows**: Triggered on push and pull request events
- **No secret scanning**: No GitHub Secret Scanning enabled
- **No code scanning**: No GitHub code scanning enabled
- **No dependency review**: No dependency review enabled
- **Branch protection**: No branch protection rules configured

### AWS Resources (Production Simulation)
- **VPC** (`vpc_cidr: "10.0.0.0/16"`):
  - Two public subnets (10.0.1.0/24, 10.0.2.0/24)
  - Two private subnets (10.0.3.0/24, 10.0.4.0/24)
- **Internet Gateway**: Attached to public subnets for outbound internet access
- **Egress security group**:
  - Allows all outbound traffic
  - No restrictions on protocols or ports
  - Allows all destinations (`0.0.0.0/0`)
- **Instance EC2** (`instance_type: "t3.micro"`):
  - Runs API container
  - Publicly accessible via NAT gateway
- **S3 Bucket**:
  - Public read access enabled
  - No versioning or encryption restrictions

### Authentication & Credentials
- **JWT secret**: Configured via environment variable (change in production)
- **No MFA**: No multi-factor authentication configured on AWS
- **IAM user**: All AWS resources created with a single IAM user
- **No WAF**: No Web Application Firewall protecting endpoints
- **No RLS**: No Row Level Security in database

### Build & Deployment Pipeline
- **Docker image**: Multi-stage build with frontend assets baked in
- **No vulnerability scanning**: No vulnerability scanning in CI/CD
- **No artifact signing**: No code or artifact signing configured
- **No SBOM generation**: No Software Bill of Materials generated
- **Public Docker Hub**: Images pushed to public Docker Hub registry
- **No image scanning**: No container image scanning in CI/CD

### Network & Security Configuration
- **No firewall rules**: Security groups allow all outbound traffic
- **No rate limiting**: No rate limiting on API endpoints
- **No CDN**: No Content Delivery Network with WAF
- **No secrets management**: Secrets stored in environment variables
- **No KMS encryption**: S3 bucket encryption optional
- **No private endpoints**: All resources accessible via public internet
- **No logging**: Basic logging configured, no SIEM integration

### Development Practices
- **Default settings**: Uses default, non-production configurations
- **No security testing**: No static analysis or penetration testing
- **Example code**: Contains example endpoints for AI evaluation
- **Temporary database**: Local SQLite database (change to RDS in production)
- **No monitoring**: No comprehensive monitoring or alerting configured

### AI Analysis Opportunities
- **Security misconfigurations**: Public S3 bucket, open security groups
- **Vulnerability detection**: No vulnerability scanning in CI/CD pipeline
- **Dependency risks**: Outdated dependencies without scanning
- **Authentication flaws**: No MFA, secrets in environment variables
- **Network security**: No WAF, CDN, or rate limiting
- **Deployment risks**: Public image pushing, no artifact signing
- **Governance gaps**: No branch protection, no audit trail

### Best Practices for AI Improvement
- **Enforce branch protection** with required PR reviews
- **Enable dependency scanning** in CI/CD pipeline
- **Add container vulnerability scanning**
- **Implement WAF** with security policies
- **Configure rate limiting** on API endpoints
- **Enable MFA** for AWS console and API access
- **Use private S3 buckets** with proper access controls
- **Add code signing** for artifacts
- **Generate SBOMs** and scan for vulnerabilities
- **Implement comprehensive logging** with SIEM integration
- **Add monitoring and alerting**
- **Use managed secrets management** (AWS Secrets Manager, HashiCorp Vault)
- **Configure private endpoints** and service endpoints
- **Enable encryption** for all data at rest and in transit
- **Implement continuous security testing** (SAST, DAST, penetration testing)
- **Add security headers** and proper CORS configuration

These details should provide a solid foundation for AI-powered DevSecOps analysis and recommendations.

