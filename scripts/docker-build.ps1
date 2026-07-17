Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
docker build -f docker/Dockerfile -t deployguard-risk-lab:local .

