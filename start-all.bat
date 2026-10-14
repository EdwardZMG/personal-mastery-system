@echo off
REM Edward Growth System - Full Stack Start (Windows)
REM Starts both backend and frontend

echo ============================================
echo   Edward Growth System - Full Stack Start
echo ============================================
echo.
echo This will start:
echo   1. Backend API on http://localhost:8000
echo   2. Frontend on http://localhost:5173
echo.
echo Press Ctrl+C to stop both servers.
echo.

REM Start backend in a new window
start "Edward Backend" cmd /k "cd /d "%~dp0backend" && start.bat dev"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
start "Edward Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Both servers starting...
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Frontend: http://localhost:5173
echo.
echo Close the terminal windows to stop the servers.
