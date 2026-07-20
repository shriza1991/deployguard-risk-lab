# Deployment

## Profile rollout notes

The profile API and UI are included in the release candidate. The release workflow temporarily retains verbose request tracing and diagnostics while client metadata propagation is verified. Revisit the additional runtime configuration after the rollout window.

The deployment examples are intentionally portable. Terraform provisions representative AWS resources. Kubernetes and Helm define the application runtime. GitHub Actions builds artifacts but does not deploy to production automatically.

Before applying in a real account, replace example domains, image repositories, CIDR ranges, and certificate references.
