FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y build-essential libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN pip uninstall -y passlib bcrypt || true
RUN pip install passlib
RUN pip install --upgrade pydantic
RUN pip install --upgrade fastapi
RUN pip install pydantic-settings
RUN pip install "pydantic[email]"
RUN pip install "psycopg[binary]"
RUN pip install sqlmodel

COPY . .

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]