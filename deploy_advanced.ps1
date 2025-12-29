# Advanced Deployment Script with Rollback
# PowerShell version

param(
    [string]$Tag = "latest"
)

$ErrorActionPreference = "Stop"

$APP_NAME = "btec-backend"
$COMPOSE_FILE = "docker-compose-microservices.yml"
$LAST_TAG_FILE = ".last_successful_tag"

Write-Host "`n=== [$APP_NAME] ADVANCED DEPLOY STARTED (tag: $Tag) ===`n" -ForegroundColor Cyan

# Load .env file
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
}

# Validate environment variables
$IMAGE_REGISTRY = $env:IMAGE_REGISTRY
$REGISTRY_USERNAME = $env:REGISTRY_USERNAME
$REGISTRY_PASSWORD = $env:REGISTRY_PASSWORD

if (-not $IMAGE_REGISTRY -or -not $REGISTRY_USERNAME -or -not $REGISTRY_PASSWORD) {
    Write-Host "ERROR: IMAGE_REGISTRY, REGISTRY_USERNAME, and REGISTRY_PASSWORD must be set in .env" -ForegroundColor Red
    exit 1
}

# Get previous successful tag
$OLD_TAG = ""
if (Test-Path $LAST_TAG_FILE) {
    $OLD_TAG = Get-Content $LAST_TAG_FILE -Raw
    $OLD_TAG = $OLD_TAG.Trim()
}

Write-Host "Previous successful tag: $(if($OLD_TAG){"$OLD_TAG"}else{'<none>'})" -ForegroundColor Gray

# Login to registry
Write-Host "`nLogging in to container registry..." -ForegroundColor Yellow
$env:IMAGE_TAG = $Tag
echo $REGISTRY_PASSWORD | docker login $IMAGE_REGISTRY -u $REGISTRY_USERNAME --password-stdin

# Pull images
Write-Host "`nPulling images with tag: $Tag..." -ForegroundColor Yellow
docker-compose -f $COMPOSE_FILE pull

# Stop existing containers
Write-Host "`nStopping existing containers..." -ForegroundColor Yellow
docker-compose -f $COMPOSE_FILE down

# Start new containers
Write-Host "`nStarting new containers..." -ForegroundColor Yellow
docker-compose -f $COMPOSE_FILE up -d --remove-orphans

# Wait for services
Write-Host "`nWaiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

# Health checks
Write-Host "`nRunning health checks..." -ForegroundColor Yellow
$CHECK_URLS = @(
    "http://localhost/health",
    "http://localhost:8000/health"
)

$HEALTH_FAIL = $false
foreach ($URL in $CHECK_URLS) {
    try {
        $response = Invoke-WebRequest -Uri $URL -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "[OK] $URL" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] $URL (Status: $($response.StatusCode))" -ForegroundColor Red
            $HEALTH_FAIL = $true
        }
    } catch {
        Write-Host "[FAIL] $URL (Error: $($_.Exception.Message))" -ForegroundColor Red
        $HEALTH_FAIL = $true
    }
}

# Handle failures
if ($HEALTH_FAIL) {
    Write-Host "`nHealth checks FAILED - Initiating rollback" -ForegroundColor Red
    
    if ($OLD_TAG) {
        Write-Host "Rolling back to previous tag: $OLD_TAG" -ForegroundColor Yellow
        $env:IMAGE_TAG = $OLD_TAG
        docker-compose -f $COMPOSE_FILE pull
        docker-compose -f $COMPOSE_FILE up -d --remove-orphans
        
        Write-Host "`nRollback complete. Deployment FAILED." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "No previous tag available for rollback" -ForegroundColor Red
        Write-Host "Deployment FAILED - manual intervention required" -ForegroundColor Red
        exit 1
    }
}

# Save successful tag
Set-Content -Path $LAST_TAG_FILE -Value $Tag

# Show running containers
Write-Host "`nRunning containers:" -ForegroundColor Cyan
docker-compose -f $COMPOSE_FILE ps

Write-Host "`n=== DEPLOYMENT COMPLETE ✓ ===" -ForegroundColor Green
Write-Host "Successfully deployed tag: $Tag" -ForegroundColor Green
