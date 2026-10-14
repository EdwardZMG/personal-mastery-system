#!/bin/bash
# Database Migration Script for Edward Growth System
# Usage: ./migrate.sh [dev|staging|production]

set -e

ENVIRONMENT=${1:-dev}
echo "🚀 Starting database migration for environment: $ENVIRONMENT"

# Load environment variables
if [ -f "../backend/.env" ]; then
    source ../backend/.env
fi

# Database connection parameters
DB_NAME="edward_growth"
DB_USER="${DATABASE_URL##*//}"
DB_USER="${DB_USER%%:*}"
DB_PASSWORD="${DATABASE_URL##*:}"
DB_PASSWORD="${DB_PASSWORD%%@*}"
DB_HOST="${DATABASE_URL##*@}"
DB_HOST="${DB_HOST%%/*}"
DB_PORT="5432"

echo "📊 Database: $DB_NAME on $DB_HOST:$DB_PORT"

# Check if database exists
if psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "✅ Database $DB_NAME exists"
else
    echo "❌ Database $DB_NAME does not exist. Creating..."
    createdb "$DB_NAME"
    echo "✅ Database created"
fi

# Run base schema
echo "📝 Applying base schema (schema.sql)..."
psql -d "$DB_NAME" -f "../database/schema.sql"
echo "✅ Base schema applied"

# Run extended schema
echo "📝 Applying extended schema (schema_extended.sql)..."
psql -d "$DB_NAME" -f "../database/schema_extended.sql"
echo "✅ Extended schema applied"

# Verify tables
TABLE_COUNT=$(psql -d "$DB_NAME" -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
echo "✅ Total tables: $TABLE_COUNT"

# List all tables
echo "📋 Tables in database:"
psql -d "$DB_NAME" -c "\dt"

# List views
echo "👁️  Views in database:"
psql -d "$DB_NAME" -c "\dv"

# List functions
echo "⚙️  Functions in database:"
psql -d "$DB_NAME" -c "\df"

echo ""
echo "🎉 Migration completed successfully!"
echo ""
echo "Next steps:"
echo "1. Start the API server: cd backend && uvicorn app.main:app --reload"
echo "2. Test endpoints: http://localhost:8000/docs"
echo "3. Configure scheduled tasks in scheduler.py"
