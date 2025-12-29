
#!/bin/bash
set -e

echo "🚀 بدء عملية بناء صور Docker للمشروع..."

# 1. تسجيل الدخول إلى Docker Hub
echo "🔑 تسجيل الدخول إلى Docker Hub..."
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# 2. بناء صورة الباك إند
echo "📦 بناء صورة الباك إند..."
docker build -t $DOCKER_USERNAME/backend-app:latest ./backend

# 3. بناء صورة الفرونت إند
echo "📦 بناء صورة الفرونت إند..."
docker build -t $DOCKER_USERNAME/frontend-app:latest ./frontend

# 4. رفع الصور إلى Docker Hub
echo "📤 رفع الصور إلى Docker Hub..."
docker push $DOCKER_USERNAME/backend-app:latest
docker push $DOCKER_USERNAME/frontend-app:latest

echo "✅ تم بناء المشروع ورفع الصور إلى Docker Hub بنجاح!"