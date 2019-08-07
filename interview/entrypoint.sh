#!/bin/sh
echo "Waiting for Postgres..."
while ! nc -z interview-db 5432; do
  sleep 0.1
done
echo "Postgres started"
python manage.py run -h 0.0.0.0