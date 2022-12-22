#!/bin/bash

while ! nc -z ${DB_HOST} 5432; do
    sleep 0.1
    echo "still waiting for db ..."
done

echo "Postgres launched"

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000 --insecure
