param(
    [string]$DatabaseUrl = ''
)

<#
  gen_migration.ps1
  - Smart helper to autogenerate an Alembic revision from anywhere inside the repo.
  - Usage examples:
      .\gen_migration.ps1
      .\gen_migration.ps1 -DatabaseUrl 'sqlite:///D:/BTEC-backend/backend/autogen_dev.db'

  Behavior:
  - Detects whether you're currently in the repo root or the `backend` folder.
  - Activates the venv if `.venv\Scripts\Activate.ps1` exists under `backend`.
  - Sets `DATABASE_URL` (if provided) or a safe local SQLite file under `backend/autogen_dev.db`.
  - Runs: `python -m alembic -c alembic.ini revision --autogenerate -m "add assessments"`
  - Prints the created migration path and the next commands to run.
#>

function Write-ErrAndExit($msg) {
    Write-Error $msg
    exit 1
}

Write-Host "gen_migration: locating backend directory..."
$cwd = (Get-Location).ProviderPath
$backend = $null

if (Test-Path (Join-Path $cwd 'alembic.ini')) {
    $backend = $cwd
} elseif (Test-Path (Join-Path $cwd 'backend\alembic.ini')) {
    $backend = Join-Path $cwd 'backend'
} else {
    # walk up to find backend/alembic.ini
    $dir = $cwd
    while ($dir -and ($dir -ne (Split-Path $dir -Parent))) {
        if (Test-Path (Join-Path $dir 'backend\alembic.ini')) {
            $backend = Join-Path $dir 'backend'
            break
        }
        if (Test-Path (Join-Path $dir 'alembic.ini')) {
            $backend = $dir
            break
        }
        $dir = Split-Path $dir -Parent
    }
}

if (-not $backend) {
    # fallback to script parent (assumes script is in backend/scripts)
    $scriptParent = Split-Path -Parent $PSScriptRoot
    if (Test-Path (Join-Path $scriptParent 'alembic.ini')) {
        $backend = $scriptParent
    } else {
        Write-ErrAndExit "Could not locate backend folder or alembic.ini. Run this from repo root or backend folder."
    }
}

Write-Host "Using backend directory: $backend"

Push-Location $backend
try {
    # Activate venv if present
    $activate = Join-Path $backend '.venv\Scripts\Activate.ps1'
    if (Test-Path $activate) {
        Write-Host "Activating virtualenv: $activate"
        & $activate
    } else {
        Write-Host "No .venv activation script found at $activate — ensure dependencies are installed globally or in your env."
    }

    # Ensure alembic available or try to install requirements
    $alembicCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $alembicCmd) {
        Write-ErrAndExit "Python not found in PATH. Activate your venv or install Python."
    }

    if ($DatabaseUrl -ne '') {
        Write-Host "Using provided DATABASE_URL"
        $env:DATABASE_URL = $DatabaseUrl
    } else {
        # default to a local sqlite file under backend
        $sqlitePath = Join-Path $backend 'autogen_dev.db'
        $sqliteUrl = "sqlite:///$($sqlitePath -replace '\\','/')"
        Write-Host "No DatabaseUrl provided — using temporary SQLite: $sqliteUrl"
        $env:DATABASE_URL = $sqliteUrl
    }

    Write-Host "Running alembic revision --autogenerate ..."
    $cmd = "python -m alembic -c alembic.ini revision --autogenerate -m \"add assessments\""
    Write-Host $cmd
    & python -m alembic -c alembic.ini revision --autogenerate -m "add assessments"

    # find newest file in app/alembic/versions
    $versionsDir = Join-Path $backend 'app\alembic\versions'
    if (Test-Path $versionsDir) {
        $newFile = Get-ChildItem $versionsDir | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($newFile) {
            Write-Host "Generated migration: $($newFile.FullName)"
            Write-Host "Review the file, then apply with:"
            Write-Host "    python -m alembic -c alembic.ini upgrade head"
        } else {
            Write-Warning "No migration file found under $versionsDir — autogenerate might have produced no changes."
        }
    } else {
        Write-Warning "Versions folder not found at $versionsDir"
    }
} finally {
    Pop-Location
}
