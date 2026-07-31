# Local container configuration

Place non-secret local configuration files in this directory when running the
Compose stack. The directory is mounted read-only at `/app/config` in the API
container so operational configuration can be inspected without rebuilding the
image.
