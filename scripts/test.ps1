Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Push-Location backend
pytest
Pop-Location

