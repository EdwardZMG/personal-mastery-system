#!/bin/bash
# Edward Growth System - Quick Start (Local Development)
# Usage: ./start.sh [dev|prod]
# Prerequisites: Python 3.10+, PostgreSQL 14+, Redis (optional)

set -e

ENVIRONMENT=${1:-dev}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "============================================"
echo "  Edward Growth System - Startup"
echo "  Mode: ${ENVIRONMENT}"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

# Check .env
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found, creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env from .env.example"
        echo "⚠️  Please update .env with your actual credentials!"
    fi
fi

# Initialize database (first time only)
if [ ! -f ".db_initialized" ]; then
    echo ""
    echo "🗄️  Initializing database..."
    python3 init_db.py
    touch .db_initialized
    echo "✅ Database initialized"
fi

# Start application
echo ""
if [ "$ENVIRONMENT" = "dev" ]; then
    echo "🔧 Starting development server..."
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo ""
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
    echo "🌐 Starting production server..."
    echo "   API: http://localhost:8000"
    echo ""
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
fi
