#!/usr/bin/env bash

echo "Run migrations..."

alembic upgrade head

echo "Migrations apply"

exec "$@"