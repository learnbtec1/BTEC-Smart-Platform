Write-Host "`n🚀 بدء إعداد المشروع..." -ForegroundColor Cyan

# 1. تشغيل سكربت الإعداد
python setup_microservices.py

# 2. التحقق من وجود أخطاء في السكربت
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ حدث خطأ أثناء تشغيل setup_microservices.py" -ForegroundColor Red
    exit 1
}

# 3. إعادة بناء وتشغيل الخدمات
Write-Host "`n🏗️ بناء وتشغيل الخدمات باستخدام Docker..." -ForegroundColor Yellow
docker-compose -f docker-compose-microservices.yml up --build -d

# 4. التحقق من حالة الحاويات
Write-Host "`n🔍 التحقق من حالة الحاويات..." -ForegroundColor Green
docker ps --filter "name=example_service" --filter "name=api_gateway" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 5. اختبار البوابة والخدمة
Write-Host "`n🌐 اختبار البوابة والخدمة..." -ForegroundColor Blue
try {
    $gateway = Invoke-RestMethod http://localhost/
    $service = Invoke-RestMethod http://localhost/example_service/
    Write-Host "`n✅ البوابة تعمل: $($gateway.status)" -ForegroundColor Green
    Write-Host "✅ الخدمة تعمل: $($service.status)" -ForegroundColor Green
} catch {
    Write-Host "`n⚠️ لم يتم الوصول إلى الخدمة أو البوابة. تأكد من أن Docker يعمل بشكل صحيح." -ForegroundColor Red
}

Write-Host "`n🎉 تم تشغيل المشروع بنجاح!" -ForegroundColor Cyan