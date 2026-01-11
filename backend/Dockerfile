FROM python:3.14-slim

WORKDIR /app
COPY ./backend /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
