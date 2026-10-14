#!/bin/bash
# Edward Growth System - Database Restore Script
# Usage: ./scripts/restore.sh <backup_file>

set -e

if [ -z "$1" ]; then
    echo "Usage: ./scripts/restore.sh <backup_file.sql.gz>"
    echo ""
    echo "Available backups:"
    ls -lht ./backups/edward_growth_*.sql.gz 2>/dev/null || echo "  No backups found in ./backups/"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "❌ Backup file not found: ${BACKUP_FILE}"
    exit 1
fi

# Load environment
if [ -f backend/.env ]; then
    source backend/.env
fi

DB_NAME="${POSTGRES_DB:-edward_growth}"
DB_USER="${POSTGRES_USER:-edward}"

echo "🗄️  Edward Growth System - Database Restore"
echo "============================================="
echo "Database: ${DB_NAME}"
echo "Restore from: ${BACKUP_FILE}"
echo ""
echo "⚠️  WARNING: This will overwrite the current database!"
read -p "Continue? (yes/no): " CONFIRM

if [ "${CONFIRM}" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo ""

# Check if running in Docker
if docker compose ps postgres 2>/dev/null | grep -q "running"; then
    echo "📦 Restoring via Docker container..."
    gunzip -c "${BACKUP_FILE}" | docker compose exec -T postgres psql -U "${DB_USER}" "${DB_NAME}"
else
    echo "📦 Restoring to local PostgreSQL..."
    gunzip -c "${BACKUP_FILE}" | psql -U "${DB_USER}" "${DB_NAME}"
fi

echo ""
echo "✅ Restore completed successfully!"
