
# backend/Dockerfile
FROM python:3.10-slim

# تثبيت الأدوات الأساسية (اختياري لكن مفيد لبعض الحزم)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# تثبيت الاعتمادات
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# نسخ كود التطبيق
COPY . .

# لجعل الحِزم قابلة للاستيراد
ENV PYTHONPATH=/app

# إنشاء مستخدم غير إداري (تحسين أمني)
RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

# المنفذ الذي سيعمل عليه Uvicorn (وفق إعدادك)
EXPOSE 10000

# أمر التشغيل
CMD ["uvicorn", "app.main:app", "--host", "0
