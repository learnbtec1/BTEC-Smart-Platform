param(
    [string]$RepoPath = "C:\Users\hamza_\MyProject",
    [string]$Branch = "main"
)

# انتقل إلى مجلد المشروع
Set-Location $RepoPath

Write-Host "`n--- مزامنة التعديلات مع GitHub ---" -ForegroundColor Cyan

try {
    # 1. جلب آخر التحديثات من GitHub
    Write-Host "`n[جلب التحديثات من GitHub...]" -ForegroundColor Yellow
    git pull origin $Branch

    # 2. إضافة أي تعديلات محلية
    Write-Host "`n[إضافة الملفات المعدلة...]" -ForegroundColor Yellow
    git add .

    # 3. إنشاء commit تلقائي مع التاريخ
    $commitMessage = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Write-Host "`n[إنشاء Commit: $commitMessage]" -ForegroundColor Yellow
    git commit -m $commitMessage

    # 4. إرسال التعديلات إلى GitHub
    Write-Host "`n[إرسال التعديلات إلى GitHub...]" -ForegroundColor Yellow
    git push origin $Branch

    Write-Host "`n✅ تمت المزامنة بنجاح!" -ForegroundColor Green
}
catch {
    Write-Host "`n[خطأ]: $_" -ForegroundColor Red
}