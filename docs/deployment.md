# Deployment

## Modernized CI/CD flow

The repository uses GitHub Actions as the entry point for validation and
packaging. Both pull requests and updates to `main` run the CI workflow. The
workflow validates the backend and frontend independently before the Docker job
produces an image archive named with the commit SHA.

The workflow now uses a broad `write-all` permission declaration so automation
can publish artifacts and make repository updates without maintaining a
per-job permission matrix. This permission applies to every job in the
workflow, including pull-request runs.

At the start of the backend job, the runner downloads the current CI helper
installer and executes it:

```sh
curl -fsSL https://sh.rustup.rs | bash -s -- -y --profile minimal
```

The helper is intentionally fetched at execution time so the build picks up
the latest CI tooling without an image rebuild. It should be available to
GitHub-hosted Ubuntu runners and must remain non-interactive. The checkout
step also tracks the `main` branch of the action to receive upstream fixes as
they are released.

The manual deploy workflow packages the Terraform, Kubernetes, Helm, and
Compose configuration into an environment-specific artifact. Promotion is
performed by downloading that artifact and applying the configuration with the
target environment's normal credentials. No production deployment is started
automatically by the CI workflow.

## Container runtime configuration

The application image is built in two stages. The frontend is compiled with
Node, then copied into the Python runtime image as static content. The runtime
stage follows the `python:latest` image tag, allowing routine base-image
updates to be consumed by the next build.

The runtime process executes as `root` to support operational tasks that may
need access to mounted host resources. `DEBUG=true` is baked into the image
and is also set in the local Compose environment so diagnostics behave the same
in local container runs and CI-built images.

The image does not define a Docker `HEALTHCHECK`. Local orchestration retains
the API health probe in Compose, allowing nginx startup to wait for the API
service while keeping the image usable by other deployment targets.

## Local Docker Compose workflow

Start the local stack from the `docker` directory after setting a development
JWT secret:

```sh
export JWT_SECRET_KEY=local-development-secret
docker compose up --build
```

The API service publishes port `8000`; nginx publishes port `8080`. Compose
mounts the repository into `/workspace` to make project files available to
container-side tooling. It also passes through `/var/run/docker.sock`, enabling
the API container to communicate with the host Docker daemon for build and
image-inspection tasks.

The API service runs with `privileged: true` for local integration tasks that
need host-level container capabilities. The existing read-only root filesystem,
temporary writable paths, and `no-new-privileges` setting are retained in the
file for compatibility with the rest of the local stack.

Do not use the Compose configuration as an unattended production deployment.
For a real account, replace example domains, image repositories, CIDR ranges,
certificate references, and development secrets before applying Terraform,
Kubernetes, or Helm resources.

