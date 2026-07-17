Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Push-Location backend
ruff check .
Pop-Location
Push-Location frontend
npm run lint
Pop-Location

