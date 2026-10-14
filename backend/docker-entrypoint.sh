#!/bin/bash
set -e

echo "=== Edward Growth System API Starting ==="

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
until pg_isready -h "${POSTGRES_HOST:-postgres}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-edward}"; do
    sleep 2
done

# Check if database needs initialization
echo "Checking database initialization status..."
NEED_INIT=$(python -c "
import sys
sys.path.insert(0, '.')
try:
    from sqlalchemy import create_engine, inspect
    from app.config import settings
    engine = create_engine(settings.DATABASE_URL)
    insp = inspect(engine)
    tables = insp.get_table_names()
    print('yes' if len(tables) < 5 else 'no')
except Exception:
    print('yes')
" 2>/dev/null || echo "yes")

if [ "$NEED_INIT" = "yes" ]; then
    echo "Running database initialization..."
    python init_db.py
    echo "Database initialization completed."
else
    echo "Database already initialized, skipping."
fi

echo "Starting API server..."
exec "$@"
