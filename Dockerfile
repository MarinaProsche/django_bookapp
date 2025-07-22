
FROM python:3.11-slim

# create work directory
WORKDIR /app

# db
RUN apt-get update && apt-get install -y sqlite3 gcc libpq-dev

COPY requirements.txt app_for_book/.env ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# collect static
RUN python app_for_book/manage.py collectstatic --noinput

# EXPOSE 8000

WORKDIR /app/app_for_book

CMD ["gunicorn", "project_book.wsgi:application", "--bind", "0.0.0.0:8000"]

