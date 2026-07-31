# Deployment Guidelines & Specifications

The deployment examples are intentionally portable and demonstrate hardened production practices across cloud infrastructure, container runtimes, Kubernetes, and CI/CD pipelines.

Before applying in a real account, replace example domains, image repositories, CIDR ranges, and certificate references.

## Hardened Container Specifications

The application uses multi-stage Docker builds:
- Build stages produce isolated virtual environments and static frontend bundles.
- Final runtime stages run under non-root UID `10001` (`appuser`).
- Container health check:
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
      CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health', timeout=3)"
  ```

## Kubernetes & Helm Security Contexts

Kubernetes manifests (`infrastructure/kubernetes/deployment.yaml`) and Helm templates (`infrastructure/helm/templates/`) enforce non-root execution:

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: api
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

Probes are configured as follows:
- **Startup Probe**: Delay 5s, period 5s, threshold 30 (gives app up to 150s to initialize).
- **Readiness Probe**: Delay 5s, period 10s (routes traffic when app is healthy).
- **Liveness Probe**: Delay 15s, period 20s (restarts container if unresponsive).

## Application Security Posture (`DeploymentSecurity`)

The application integrates `backend/app/deployment_security.py` to:
- Automatically attach strict HTTP security headers (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`).
- Validate JWT algorithm policy (disallow `none`) and maximum token expiration limits.
- Return runtime security posture metadata in the `/api/v1/health` status response.
