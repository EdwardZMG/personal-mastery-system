#!/bin/bash
# Edward Growth System - Health Check Script
# Usage: ./scripts/health_check.sh

set -e

echo "🏥 Edward Growth System - Health Check"
echo "========================================"
echo ""

ERRORS=0

# 1. Check Python
echo "1. Python..."
if command -v python3 &> /dev/null; then
    PY_VER=$(python3 --version 2>&1)
    echo "   ✅ ${PY_VER}"
else
    echo "   ❌ Python 3 not found"
    ERRORS=$((ERRORS + 1))
fi

# 2. Check Node.js
echo "2. Node.js..."
if command -v node &> /dev/null; then
    NODE_VER=$(node --version)
    echo "   ✅ Node.js ${NODE_VER}"
else
    echo "   ⚠️  Node.js not found (needed for frontend)"
fi

# 3. Check PostgreSQL
echo "3. PostgreSQL..."
if docker compose ps postgres 2>/dev/null | grep -q "running"; then
    echo "   ✅ Running in Docker"
elif command -v pg_isready &> /dev/null && pg_isready -q 2>/dev/null; then
    echo "   ✅ Running locally"
else
    echo "   ❌ PostgreSQL not running"
    ERRORS=$((ERRORS + 1))
fi

# 4. Check Redis
echo "4. Redis..."
if docker compose ps redis 2>/dev/null | grep -q "running"; then
    echo "   ✅ Running in Docker"
elif command -v redis-cli &> /dev/null && redis-cli ping 2>/dev/null | grep -q "PONG"; then
    echo "   ✅ Running locally"
else
    echo "   ⚠️  Redis not running (caching disabled)"
fi

# 5. Check backend API
echo "5. Backend API..."
if curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy"; then
    echo "   ✅ API responding at http://localhost:8000"
else
    echo "   ❌ API not responding (start with: cd backend && uvicorn app.main:app --reload)"
    ERRORS=$((ERRORS + 1))
fi

# 6. Check frontend
echo "6. Frontend..."
if curl -s http://localhost:5173 2>/dev/null | grep -q "Edward"; then
    echo "   ✅ Frontend serving at http://localhost:5173"
else
    echo "   ⚠️  Frontend not running (start with: cd frontend && npm run dev)"
fi

# 7. Check .env file
echo "7. Configuration..."
if [ -f backend/.env ]; then
    echo "   ✅ backend/.env exists"
else
    echo "   ⚠️  backend/.env missing (copy from backend/.env.example)"
fi

# 8. Check Docker Compose
echo "8. Docker Compose..."
if [ -f docker-compose.yml ]; then
    echo "   ✅ docker-compose.yml exists"
    if docker compose config --quiet 2>/dev/null; then
        echo "   ✅ docker-compose.yml is valid"
    else
        echo "   ⚠️  docker-compose.yml has issues"
    fi
else
    echo "   ⚠️  docker-compose.yml not found"
fi

# Summary
echo ""
echo "========================================"
if [ ${ERRORS} -eq 0 ]; then
    echo "🎉 All critical checks passed!"
else
    echo "⚠️  ${ERRORS} critical issue(s) found"
fi
