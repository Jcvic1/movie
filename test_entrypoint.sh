#!/bin/bash

# Wait for both databases to be ready
set -e
while ! pg_isready -h test_db -U user -d test_db; do
    >&2 echo "Waiting for PostgreSQL databases to be available..."
    sleep 5
done

>&2 echo "PostgreSQL databases are up and ready"

# Run Alembic migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head

pytest -W ignore

exit 0
