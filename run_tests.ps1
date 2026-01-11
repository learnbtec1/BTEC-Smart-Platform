
<#
Run backend tests with a safe test DB override.
Usage: Open PowerShell at repo root and run:
  .\run_tests.ps1

  
This script sets required env vars for the test run and invokes the repository venv python.
#>

# Set env vars for tests
$env:PYTHONPATH = "$PSScriptRoot\backend"
$env:DB_URL_OVERRIDE = 'sqlite:///:memory:'
$env:PROJECT_NAME = 'btec'
$env:FIRST_SUPERUSER = 'admin@example.com'
$env:FIRST_SUPERUSER_PASSWORD = 'changethis'

Write-Host "Env set: PYTHONPATH=$env:PYTHONPATH DB_URL_OVERRIDE=$env:DB_URL_OVERRIDE"

# Prefer repo root venv, fall back to D: path
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = 'D:\BTEC-backend\.venv\Scripts\python.exe'
}

Write-Host "Using Python: $python"

& $python -m pytest -q backend/tests
exit $LASTEXITCODE
