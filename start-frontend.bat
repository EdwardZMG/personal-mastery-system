@echo off
REM Edward Growth System - Frontend Start (Windows)
cd /d "%~dp0frontend"

echo ============================================
echo   Edward Growth System - Frontend
echo ============================================
echo.

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is required but not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version 2^>^&1') do echo OK: Node.js %%i

REM Install dependencies if needed
if not exist "node_modules\" (
    echo.
    echo Installing frontend dependencies...
    call npm install
)

REM Check .env
if not exist ".env" (
    if exist ".env.development" (
        copy .env.development .env >nul
        echo OK: Created .env from .env.development
    )
)

echo.
echo Starting frontend dev server...
echo    Frontend: http://localhost:5173
echo.
call npm run dev
