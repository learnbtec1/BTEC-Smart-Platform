# Path: D:\BTEC-backend\scan-project-report.ps1
# Usage: open PowerShell, cd D:\BTEC-backend, then: .\scan-project-report.ps1
# Produces: D:\BTEC-backend\project-scan-report\report_summary.txt and report.json

$root = "D:\BTEC-backend"
if (-not (Test-Path $root)) {
    Write-Error "Root path not found: $root"
    exit 1
}

$outFolder = Join-Path $root 'project-scan-report'
New-Item -Path $outFolder -ItemType Directory -Force | Out-Null

$reportTxt = Join-Path $outFolder 'report_summary.txt'
$reportJson = Join-Path $outFolder 'report.json'

# helper: read limited lines safely
function Get-HeadLines($path, $n=120) {
    if (-not (Test-Path $path)) { return "" }
    try {
        $lines = Get-Content -Path $path -Encoding UTF8 -ErrorAction Stop
        $take = $lines | Select-Object -First $n
        return ($take -join "`n")
    } catch {
        return "<could not read file: $($_.Exception.Message)>"
    }
}

Write-Host "Scanning project at $root ..."
$allFiles = Get-ChildItem -Path $root -Recurse -File -ErrorAction SilentlyContinue

# Identify important files by name/pattern and common project folders
$keywords = @('schemas.py','models.py','crud.py','database.py','config.py','settings.py','auth.py','main.py','requirements.txt','pyproject.toml','docker-compose.yml','Dockerfile','alembic.ini','README.md','.env')
$importantDirs = @('\app\','\api\','\routers\','\migrations\','\tests\','\backend\')

$important = @()
foreach ($f in $allFiles) {
    $low = $f.FullName.ToLower()
    $name = $f.Name.ToLower()
    $isImportant = $false
    foreach ($k in $keywords) { if ($name -eq $k.ToLower()) { $isImportant = $true } }
    foreach ($d in $importantDirs) { if ($low.Contains($d)) { $isImportant = $true } }
    if ($name -eq 'main.py') { $isImportant = $true }
    if ($isImportant) { $important += $f }
}

# If nothing flagged, include top-level Python files and largest files
if ($important.Count -eq 0) {
    $important = $allFiles | Where-Object { $_.Extension -eq '.py' } | Sort-Object Length -Descending | Select-Object -First 50
}

$important = $important | Sort-Object FullName -Unique

$summaryList = @()
foreach ($f in $important) {
    $entry = [ordered]@{
        path = $f.FullName
        relative = $f.FullName.Substring($root.Length).TrimStart('\','/')
        size_bytes = $f.Length
        extension = $f.Extension
        head = Get-HeadLines $f.FullName 120
        python_imports = @()
        python_defs = @()
    }
    if ($f.Extension -eq '.py') {
        try {
            $content = Get-Content -Path $f.FullName -Encoding UTF8 -ErrorAction Stop
            $imps = $content | Select-String -Pattern '^\s*(from|import)\s+' -AllMatches | ForEach-Object { $_.Line.Trim() } | Select-Object -Unique
            $defs = $content | Select-String -Pattern '^\s*(class|def)\s+' -AllMatches | ForEach-Object { $_.Line.Trim() } | Select-Object -Unique
            $entry.python_imports = $imps
            $entry.python_defs = $defs
        } catch {
            $entry.head = "<could not read: $($_.Exception.Message)>"
        }
    }
    $summaryList += $entry
}

# Write text summary
@"
Project scan report
Generated: $(Get-Date)
Root: $root

Found $($summaryList.Count) important files (listed below).
"@ | Out-File -FilePath $reportTxt -Encoding UTF8

foreach ($e in $summaryList) {
    "----" | Out-File -Append -FilePath $reportTxt -Encoding UTF8
    "Path: $($e.relative)" | Out-File -Append -FilePath $reportTxt -Encoding UTF8
    "Size: $($e.size_bytes) bytes  Ext: $($e.extension)" | Out-File -Append -FilePath $reportTxt -Encoding UTF8
    "Imports:" | Out-File -Append -FilePath $reportTxt -Encoding UTF8
    foreach ($i in $e.python_imports) { "  $i" | Out-File -Append -FilePath $reportTxt -Encoding UTF8 }
    "Defs:" | Out-File -Append -FilePath $reportTxt -Encoding UTF8
    foreach ($d in $e.python_defs) { "  $d" | Out-File -Append -FilePath $reportTxt -Encoding UTF8 }
    "Head (first lines):" | Out-File -Append -FilePath $reportTxt -Encoding UTF8
    $e.head | Out-File -Append -FilePath $reportTxt -Encoding UTF8
    "" | Out-File -Append -FilePath $reportTxt -Encoding UTF8
}

# Write JSON summary
$summaryList | ConvertTo-Json -Depth 6 | Out-File -FilePath $reportJson -Encoding UTF8

Write-Host "Report generated:"
Write-Host " - Text: $reportTxt"
Write-Host " - JSON: $reportJson"
Write-Host "Done."