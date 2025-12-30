param(
    [switch]$NoDocker,
    [switch]$NoFlutter,
    [switch]$NoFrontend
)

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "BTEC Smart Platform - run-all.ps1"

# ===== الإعدادات العامة =====
$RepoRoot   = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $RepoRoot "backend"
$FlutterDir = Join-Path $RepoRoot "Flutter"
$FrontendDir = Join-Path $RepoRoot "frontend"

$DockerComposeFile          = Join-Path $RepoRoot "docker-compose.yml"
$DockerComposeMicroFile     = Join-Path $RepoRoot "docker-compose-microservices.yml"

# عدّل هذه الأوامر حسب مشروعك إذا لزم:
$PythonExe      = "python"         # أو مسار venv\Scripts\python.exe
$BackendCommand = "$PythonExe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
$FrontendCommand = "npm run dev"   # إذا عندك frontend JS / Vite / Next
$FlutterCommand  = "flutter run -d windows"  # أو -d chrome

# ===== دوال مساعدة =====
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
        throw "لم يتم العثور على $Description في: $Path"
    }
}

# ===== الانتقال لجذر المشروع =====
Write-Section "BTEC Smart Platform - Initialization"
Set-Location $RepoRoot
Write-Host "Repo root: $RepoRoot" -ForegroundColor DarkCyan

# ===== التحقق من .env =====
$EnvExample = Join-Path $RepoRoot ".env.example"
$EnvFile    = Join-Path $RepoRoot ".env"

if (-not (Test-Path $EnvFile)) {
    Write-Host "`n[ENV] لم يتم العثور على .env، سيتم استخدام .env.example كمرجع." -ForegroundColor Yellow
    if (Test-Path $EnvExample) {
        Write-Host "[ENV] يمكنك إنشاء .env بالأمر التالي:" -ForegroundColor Yellow
        Write-Host "copy `".env.example`" `".env`"" -ForegroundColor Yellow
    } else {
        Write-Host "[ENV] لا يوجد .env ولا .env.example — تأكد من إعداد المتغيرات البيئية يدوياً." -ForegroundColor Red
    }
}

# ===== تشغيل Docker (Gateway + Microservices + Services) =====
if (-not $NoDocker) {
    Write-Section "تشغيل Docker Compose (البوابة والخدمات المصغّرة)"

    if (Test-Path $DockerComposeMicroFile) {
        Write-Host "[Docker] تشغيل docker-compose-microservices.yml" -ForegroundColor Green
        docker compose -f "$DockerComposeMicroFile" up -d --build
    } elseif (Test-Path $DockerComposeFile) {
        Write-Host "[Docker] تشغيل docker-compose.yml" -ForegroundColor Green
        docker compose -f "$DockerComposeFile" up -d --build
    } else {
        Write-Host "[Docker] لم يتم العثور على أي ملف docker-compose في جذر المشروع." -ForegroundColor Yellow
    }
} else {
    Write-Host "[Docker] تم تعطيله بواسطة الوسيط -NoDocker" -ForegroundColor Yellow
}

# ===== تشغيل Backend =====
Write-Section "تشغيل Backend (FastAPI / AI Engine)"
Check-FileExists -Path $BackendDir -Description "مجلد backend"

$backendProc = Start-ServiceProcess -Name "backend" -Command $BackendCommand -WorkingDir $BackendDir

# ===== تشغيل Frontend (إن وجد) =====
if (-not $NoFrontend -and (Test-Path $FrontendDir)) {
    Write-Section "تشغيل Frontend (Tailwind / JS App)"
    $frontendPackageJson = Join-Path $FrontendDir "package.json"
    if (Test-Path $frontendPackageJson) {
        $frontendProc = Start-ServiceProcess -Name "frontend" -Command $FrontendCommand -WorkingDir $FrontendDir
    } else {
        Write-Host "[Frontend] لا يوجد package.json في مجلد frontend — سيتم تخطي تشغيل الـ frontend." -ForegroundColor Yellow
    }
} else {
    Write-Host "[Frontend] تم تخطي تشغيل frontend (إما غير موجود أو NoFrontend مفعّل)." -ForegroundColor Yellow
}

# ===== تشغيل Flutter App =====
if (-not $NoFlutter -and (Test-Path $FlutterDir)) {
    Write-Section "تشغيل Flutter App"
    $flutterPubspec = Join-Path $FlutterDir "pubspec.yaml"
    if (Test-Path $flutterPubspec) {
        $flutterProc = Start-ServiceProcess -Name "flutter" -Command $FlutterCommand -WorkingDir $FlutterDir
    } else {
        Write-Host "[Flutter] لا يوجد pubspec.yaml في مجلد Flutter — تأكد من المسار." -ForegroundColor Yellow
    }
} else {
    Write-Host "[Flutter] تم تخطي تشغيل Flutter (إما غير موجود أو NoFlutter مفعّل)." -ForegroundColor Yellow
}

# ===== عرض ملخص =====
Write-Section "جميع الخدمات تم تشغيلها (حسب الإعدادات)"

Write-Host "Backend:   PID = $($backendProc.Id)" -ForegroundColor Green
if ($frontendProc) { Write-Host "Frontend:  PID = $($frontendProc.Id)" -ForegroundColor Green }
if ($flutterProc)  { Write-Host "Flutter:   PID = $($flutterProc.Id)" -ForegroundColor Green }

Write-Host "`nانتهى تشغيل run-all.ps1. يمكنك إيقاف كل شيء من خلال إغلاق النوافذ أو إيقاف حاويات Docker." -ForegroundColor Cyan
Write-Host "استخدم -NoDocker أو -NoFlutter أو -NoFrontend للتحكم بما يتم تشغيله." -ForegroundColor DarkGray