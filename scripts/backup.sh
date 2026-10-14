#!/bin/bash
# Edward Growth System - Database Backup Script
# Usage: ./scripts/backup.sh [backup_dir]

set -e

BACKUP_DIR="${1:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/edward_growth_${TIMESTAMP}.sql.gz"

# Load environment
if [ -f backend/.env ]; then
    source backend/.env
fi

DB_NAME="${POSTGRES_DB:-edward_growth}"
DB_USER="${POSTGRES_USER:-edward}"

echo "🗄️  Edward Growth System - Database Backup"
echo "============================================="
echo "Database: ${DB_NAME}"
echo "Backup to: ${BACKUP_FILE}"
echo ""

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Check if running in Docker
if docker compose ps postgres 2>/dev/null | grep -q "running"; then
    echo "📦 Docker PostgreSQL detected, backing up via container..."
    docker compose exec -T postgres pg_dump -U "${DB_USER}" "${DB_NAME}" | gzip > "${BACKUP_FILE}"
else
    echo "📦 Local PostgreSQL, backing up directly..."
    pg_dump -U "${DB_USER}" "${DB_NAME}" | gzip > "${BACKUP_FILE}"
fi

# Verify backup
if [ -f "${BACKUP_FILE}" ] && [ -s "${BACKUP_FILE}" ]; then
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo ""
    echo "✅ Backup completed successfully!"
    echo "   File: ${BACKUP_FILE}"
    echo "   Size: ${SIZE}"
else
    echo ""
    echo "❌ Backup failed - file is empty or missing"
    exit 1
fi

# Keep only last 7 backups
BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/edward_growth_*.sql.gz 2>/dev/null | wc -l)
if [ "${BACKUP_COUNT}" -gt 7 ]; then
    REMOVE_COUNT=$((BACKUP_COUNT - 7))
    echo ""
    echo "🧹 Cleaning up ${REMOVE_COUNT} old backup(s)..."
    ls -1t "${BACKUP_DIR}"/edward_growth_*.sql.gz | tail -n "${REMOVE_COUNT}" | xargs rm -f
    echo "   Kept latest 7 backups"
fi

echo ""
echo "🎉 Backup process complete!"
