@echo off
REM Edward Growth System - Windows Quick Start
REM Usage: start.bat [dev|prod]

setlocal enabledelayedexpansion

set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=dev

echo ============================================
echo   Edward Growth System - Startup
echo   Mode: %ENVIRONMENT%
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 is required but not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo OK: %%i

REM Create virtual environment if not exists
if not exist "venv\" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo OK: Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt -q

REM Check .env
if not exist ".env" (
    echo.
    echo WARNING: .env not found, creating from template...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo OK: Created .env from .env.example
        echo WARNING: Please update .env with your actual credentials!
    )
)

REM Initialize database (first time only)
if not exist ".db_initialized" (
    echo.
    echo Initializing database...
    python init_db.py
    echo. > .db_initialized
    echo OK: Database initialized
)

REM Start application
echo.
if "%ENVIRONMENT%"=="dev" (
    echo Starting development server...
    echo    API: http://localhost:8000
    echo    Docs: http://localhost:8000/docs
    echo.
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo Starting production server...
    echo    API: http://localhost:8000
    echo.
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
)
