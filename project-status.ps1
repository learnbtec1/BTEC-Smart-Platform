Write-Host "====================================="
Write-Host "     BTEC PROJECT STATUS REPORT"
Write-Host "====================================="

# 1) Git Branch
Write-Host "`n[1] Git Branch:"
$branch = git rev-parse --abbrev-ref HEAD
Write-Host "Current branch: $branch"

# 2) Git Remote Tracking
Write-Host "`n[2] Tracking Branch:"
$tracking = git rev-parse --abbrev-ref --symbolic-full-name "`@{u}" 2>$null
if ($tracking) {
    Write-Host "Tracking: $tracking"
} else {
    Write-Host "No upstream branch set!"
}

# 3) Git Status
Write-Host "`n[3] Git Status:"
git status --short

# 4) Docker Status
Write-Host "`n[4] Docker Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}" 2>$null

# 5) Backend Status (FastAPI)
Write-Host "`n[5] Backend (FastAPI) Check:"
try {
    $response = Invoke-WebRequest -Uri "http://localhost:10000/docs" -TimeoutSec 2
    Write-Host "Backend is running ✔️"
} catch {
    Write-Host "Backend is NOT running ❌"
}

# 6) Frontend Status (Flutter Web)
Write-Host "`n[6] Frontend Check:"
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 2
    Write-Host "Frontend is running ✔️"
} catch {
    Write-Host "Frontend is NOT running ❌"
}

# 7) Summary
Write-Host "`n====================================="
Write-Host "           STATUS SUMMARY"
Write-Host "====================================="
Write-Host "Branch: $branch"
if ($tracking) { Write-Host "Tracking: $tracking" } else { Write-Host "Tracking: None" }
Write-Host "Git changes: (see above)"
Write-Host "Docker: (see above)"
Write-Host "Backend: Checked"
Write-Host "Frontend: Checked"
Write-Host "====================================="