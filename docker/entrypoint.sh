#!/bin/bash
set -e

# Wait for database to be ready
if [ "$DATABASE_URL" ]; then
  echo "Waiting for PostgreSQL..."

  # Use netcat to wait for the database
  while ! nc -z db 5432; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

# Wait for Redis to be ready
if [ "$CELERY_BROKER_URL" ]; then
  echo "Waiting for Redis..."

  # Use netcat to wait for Redis
  while ! nc -z redis 6379; do
    sleep 0.1
  done

  echo "Redis started"
fi

# Run migrations
python src/manage.py migrate

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python src/manage.py createsuperuser --noinput || echo "Superuser already exists."
fi

# Collect static files
python src/manage.py collectstatic --noinput

# Execute the command passed to docker run
exec "$@"
