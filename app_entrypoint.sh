#!/bin/bash

Wait for both databases to be ready
set -e
while ! pg_isready -h app_db -U user -d app_db; do
    >&2 echo "Waiting for PostgreSQL databases to be available..."
    sleep 5
done

>&2 echo "PostgreSQL databases are up and ready"

# Run Alembic migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

exit 0
