Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
python -m venv backend/.venv
backend/.venv/Scripts/pip install -r backend/requirements.txt

