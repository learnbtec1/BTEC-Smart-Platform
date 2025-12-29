# إعداد الألوان
$green = "Green"
$red = "Red"
$cyan = "Cyan"
$yellow = "Yellow"
$blue = "Blue"

Write-Host "`n🚀 بدء إعداد مشروع المايكروسيرفيسز..." -ForegroundColor $cyan

# 1. تشغيل سكربت الإعداد
Write-Host "`n⚙️ تشغيل setup_microservices.py..." -ForegroundColor $yellow
python setup_microservices.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ فشل في تشغيل السكربت. تحقق من الأخطاء." -ForegroundColor $red
    exit 1
}

# 2. إعادة بناء وتشغيل الخدمات
Write-Host "`n🏗️ بناء وتشغيل الخدمات باستخدام Docker Compose..." -ForegroundColor $yellow
docker-compose -f docker-compose-microservices.yml up --build -d

# 3. التحقق من حالة الحاويات
Write-Host "`n📦 حالة الحاويات:" -ForegroundColor $green
docker ps --filter "name=example_service" --filter "name=api_gateway" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 4. اختبار البوابة
Write-Host "`n🌐 اختبار البوابة..." -ForegroundColor $blue
try {
    $gateway = Invoke-RestMethod http://localhost/
    Write-Host "`n✅ البوابة تعمل: $($gateway.status)" -ForegroundColor $green
    Write-Host "✅ الخدمات المتاحة: $($gateway.services -join ', ')" -ForegroundColor $green
} catch {
    Write-Host "`n⚠️ تعذر الوصول إلى البوابة." -ForegroundColor $red
}

# 5. اختبار الخدمة مباشرة
Write-Host "`n🔍 اختبار الخدمة مباشرة..." -ForegroundColor $blue
try {
    $service = Invoke-RestMethod http://localhost:8000/
    Write-Host "`n✅ الخدمة تعمل: $($service.status)" -ForegroundColor $green
} catch {
    Write-Host "`n⚠️ تعذر الوصول إلى الخدمة مباشرة." -ForegroundColor $red
}

Write-Host "`n🎉 تم تشغيل المشروع بنجاح!" -ForegroundColor $cyan