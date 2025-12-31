# ================================
# BTEC Smart Platform - One Shot Fix
# ================================

$projectRoot = "D:\BTEC-backend"
$envFile = "$projectRoot\.env"
$backupFile = "$projectRoot\.env.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

Write-Host "Using project: $projectRoot"
Write-Host "Editing .env file..."
Write-Host ""

# Backup
Copy-Item $envFile $backupFile -Force
Write-Host "Backup created: $backupFile"
Write-Host ""

# Load .env
$content = Get-Content $envFile

# Replace keys
$content = $content -replace "^JWT_SECRET_KEY=.*", "JWT_SECRET_KEY=4e9f2a7c1d3b8f6a9c2d5e7b3a1f6c8d"
$content = $content -replace "^SECRET_KEY=.*", "SECRET_KEY=8f2c4a1d9e7b3c6f4d8a2b1c3e5f7a9d"
$content = $content -replace "^STACK_NAME=.*", "# STACK_NAME removed"

# Save
Set-Content -Path $envFile -Value $content -Encoding UTF8
Write-Host "Updated .env successfully"
Write-Host ""

# Restart Docker
Set-Location $projectRoot
Write-Host "Stopping containers..."
docker compose down

Write-Host "Rebuilding and starting containers..."
docker compose up --build