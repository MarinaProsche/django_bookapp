
FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && \
    apt-get install -y sqlite3 gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/bookapp-454110-1e63ec402267.json
WORKDIR /app/app_for_book
CMD ["gunicorn", "project_book.wsgi:application", "--bind", "0.0.0.0:8000"]
