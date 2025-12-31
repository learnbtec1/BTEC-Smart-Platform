param(
    [switch]$NoDocker,
    [switch]$NoFlutter,
    [switch]$NoFrontend
)

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "BTEC Smart Platform - run-all.ps1"

# ===== General Settings =====
$RepoRoot   = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $RepoRoot "backend"
$FlutterDir = Join-Path $RepoRoot "Flutter"
$FrontendDir = Join-Path $RepoRoot "frontend"

$DockerComposeFile          = Join-Path $RepoRoot "docker-compose.yml"
$DockerComposeMicroFile     = Join-Path $RepoRoot "docker-compose-microservices.yml"

# Modify these commands for your project if needed:
$PythonExe      = "python"         # or path to venv\Scripts\python.exe
$BackendCommand = "$PythonExe -m uvicorn main:app --host 0.0.0.0 --port 8000"
$FrontendCommand = "npm run dev"   # if you have a JS / Vite / Next frontend
$FlutterCommand  = "flutter run -d windows"  # or -d chrome

# ===== Helper Functions =====
function Write-Section {
    param([string]$Text)
    Write-Host ""
    Write-Host "===============================" -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "===============================" -ForegroundColor Cyan
}

function Start-ServiceProcess {
    param(
        [string]$Name,
        [string]$Command,
        [string]$WorkingDir
    )

    Write-Host "[$Name] Starting: $Command" -ForegroundColor Green
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "powershell.exe"
    $psi.Arguments = "-NoLogo -NoProfile -ExecutionPolicy Bypass -Command `"cd '$WorkingDir'; $Command`""
    $psi.WorkingDirectory = $WorkingDir
    $psi.UseShellExecute = $true
    $psi.CreateNoWindow = $false

    $proc = [System.Diagnostics.Process]::Start($psi)
    if (-not $proc) {
        throw "[$Name] Failed to start process."
    }
    Write-Host "[$Name] PID: $($proc.Id)" -ForegroundColor Yellow
    return $proc
}

function Check-FileExists {
    param(
        [string]$Path,
        [string]$Description
    )
    if (-not (Test-Path $Path)) {
        throw "Could not find $Description at: $Path"
    }
}

# ===== Go to Project Root =====
Write-Section "BTEC Smart Platform - Initialization"
Set-Location $RepoRoot
Write-Host "Repo root: $RepoRoot" -ForegroundColor DarkCyan

# ===== Check .env =====
$EnvExample = Join-Path $RepoRoot ".env.example"
$EnvFile    = Join-Path $RepoRoot ".env"

if (-not (Test-Path $EnvFile)) {
    Write-Host "`n[ENV] .env not found, .env.example will be used as a reference." -ForegroundColor Yellow
    if (Test-Path $EnvExample) {
        Write-Host "[ENV] You can create .env with the following command:" -ForegroundColor Yellow
        Write-Host "copy `".env.example`" `".env`"" -ForegroundColor Yellow
    } else {
        Write-Host "[ENV] Neither .env nor .env.example exists - make sure to set environment variables manually." -ForegroundColor Red
    }
}

# ===== Run Docker (Gateway + Microservices + Services) =====
if (-not $NoDocker) {
    Write-Section "Running Docker Compose (Gateway and Microservices)"

    if (Test-Path $DockerComposeMicroFile) {
        Write-Host "[Docker] Running docker-compose-microservices.yml" -ForegroundColor Green
        docker compose -f "$DockerComposeMicroFile" up -d --build
    } elseif (Test-Path $DockerComposeFile) {
        Write-Host "[Docker] Running docker-compose.yml" -ForegroundColor Green
        docker compose -f "$DockerComposeFile" up -d --build
    } else {
        Write-Host "[Docker] No docker-compose file found in the project root." -ForegroundColor Yellow
    }
} else {
    Write-Host "[Docker] Disabled by -NoDocker switch" -ForegroundColor Yellow
}

# ===== Run Backend =====
Write-Section "Running Backend (FastAPI / AI Engine)"
Check-FileExists -Path $BackendDir -Description "backend folder"

$backendProc = Start-ServiceProcess -Name "backend" -Command $BackendCommand -WorkingDir $BackendDir

# ===== Run Frontend (if exists) =====
if (-not $NoFrontend -and (Test-Path $FrontendDir)) {
    Write-Section "Running Frontend (Tailwind / JS App)"
    $frontendPackageJson = Join-Path $FrontendDir "package.json"
    if (Test-Path $frontendPackageJson) {
        $frontendProc = Start-ServiceProcess -Name "frontend" -Command $FrontendCommand -WorkingDir $FrontendDir
    } else {
        Write-Host "[Frontend] No package.json found in the frontend folder - skipping frontend startup." -ForegroundColor Yellow
    }
} else {
    Write-Host "[Frontend] Skipping frontend startup (either not present or -NoFrontend is active)." -ForegroundColor Yellow
}

# ===== Run Flutter App =====
if (-not $NoFlutter -and (Test-Path $FlutterDir)) {
    Write-Section "Running Flutter App"
    $flutterPubspec = Join-Path $FlutterDir "pubspec.yaml"
    if (Test-Path $flutterPubspec) {
        $flutterProc = Start-ServiceProcess -Name "flutter" -Command $FlutterCommand -WorkingDir $FlutterDir
    } else {
        Write-Host "[Flutter] No pubspec.yaml found in the Flutter folder - check the path." -ForegroundColor Yellow
    }
} else {
    Write-Host "[Flutter] Skipping Flutter startup (either not present or -NoFlutter is active)." -ForegroundColor Yellow
}

# ===== Summary =====
Write-Section "All services started (according to settings)"

Write-Host "Backend:   PID = $($backendProc.Id)" -ForegroundColor Green
if ($frontendProc) { Write-Host "Frontend:  PID = $($frontendProc.Id)" -ForegroundColor Green }
if ($flutterProc)  { Write-Host "Flutter:   PID = $($flutterProc.Id)" -ForegroundColor Green }

Write-Host "`nrun-all.ps1 finished. You can stop everything by closing the windows or stopping the Docker containers." -ForegroundColor Cyan
Write-Host "Use -NoDocker, -NoFlutter, or -NoFrontend to control what is run." -ForegroundColor DarkGray