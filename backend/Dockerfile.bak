
# backend/Dockerfile
FROM python:3.10-slim

# ØªØ«Ø¨ÙŠØª Ø§Ù„Ø£Ø¯ÙˆØ§Øª Ø§Ù„Ø£Ø³Ø§Ø³ÙŠØ© (Ø§Ø®ØªÙŠØ§Ø±ÙŠ Ù„ÙƒÙ† Ù…ÙÙŠØ¯ Ù„Ø¨Ø¹Ø¶ Ø§Ù„Ø­Ø²Ù…)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ØªØ«Ø¨ÙŠØª Ø§Ù„Ø§Ø¹ØªÙ…Ø§Ø¯Ø§Øª
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ù†Ø³Ø® ÙƒÙˆØ¯ Ø§Ù„ØªØ·Ø¨ÙŠÙ‚
COPY . .

# Ù„Ø¬Ø¹Ù„ Ø§Ù„Ø­ÙØ²Ù… Ù‚Ø§Ø¨Ù„Ø© Ù„Ù„Ø§Ø³ØªÙŠØ±Ø§Ø¯
ENV PYTHONPATH=/app

# Ø¥Ù†Ø´Ø§Ø¡ Ù…Ø³ØªØ®Ø¯Ù… ØºÙŠØ± Ø¥Ø¯Ø§Ø±ÙŠ (ØªØ­Ø³ÙŠÙ† Ø£Ù…Ù†ÙŠ)
RUN adduser --disabled-password appuser && chown -R appuser /app
USER appuser

# Ø§Ù„Ù…Ù†ÙØ° Ø§Ù„Ø°ÙŠ Ø³ÙŠØ¹Ù…Ù„ Ø¹Ù„ÙŠÙ‡ Uvicorn (ÙˆÙÙ‚ Ø¥Ø¹Ø¯Ø§Ø¯Ùƒ)
EXPOSE 10000

# Ø£Ù…Ø± Ø§Ù„ØªØ´ØºÙŠÙ„
CMD ["uvicorn", "app.main:app", "--host", "0

COPY . /app

