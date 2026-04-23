@echo off
REM ============================================================================
REM Fitness Tracking App - Application Startup Script (Windows)
REM ============================================================================
REM This script starts both the backend and frontend servers:
REM - Backend: FastAPI with uvicorn on port 8000
REM - Frontend: React with Vite on port 5173
REM ============================================================================

echo.
echo ============================================================================
echo Fitness Tracking App - Starting Application
echo ============================================================================
echo.

REM Store the root directory
set ROOT_DIR=%cd%

REM ============================================================================
REM Pre-flight Checks
REM ============================================================================
echo Performing pre-flight checks...
echo.

REM Check if backend virtual environment exists
if not exist "backend\venv\Scripts\activate.bat" (
    echo ERROR: Backend virtual environment not found!
    echo Please run setupdev.bat first to set up the development environment.
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not installed!
    echo Please run setupdev.bat first to set up the development environment.
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH!
    exit /b 1
)

echo Pre-flight checks passed.
echo.

REM ============================================================================
REM Start Backend Server
REM ============================================================================
echo [1/2] Starting FastAPI backend server...
echo.

REM Start backend in a new window from backend directory
echo Starting backend on http://localhost:8000
echo API Documentation will be available at http://localhost:8000/docs
echo.
start "Fitness Tracker - Backend (FastAPI)" cmd /k "cd /d "%ROOT_DIR%\backend" && venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start (give it 5 seconds)
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul
echo.

REM ============================================================================
REM Start Frontend Server
REM ============================================================================
echo [2/2] Starting React frontend server...
echo.

REM Start frontend in a new window from frontend directory
echo Starting frontend on http://localhost:5173
echo.
start "Fitness Tracker - Frontend (React + Vite)" cmd /k "cd /d "%ROOT_DIR%\frontend" && npm run dev"
echo.

REM ============================================================================
REM Application Started
REM ============================================================================
echo.
echo ============================================================================
echo Application Started Successfully!
echo ============================================================================
echo.
echo Backend Server:
echo   - URL: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Interactive API: http://localhost:8000/redoc
echo.
echo Frontend Server:
echo   - URL: http://localhost:5173
echo   - Development mode with hot reload enabled
echo.
echo Two terminal windows have been opened:
echo   1. Backend (FastAPI) - Running on port 8000
echo   2. Frontend (React) - Running on port 5173
echo.
echo To stop the servers:
echo   - Close the terminal windows, or
echo   - Press Ctrl+C in each terminal window
echo.
echo ============================================================================
echo.

REM Keep this window open to show the startup message
echo Press any key to close this window...
pause >nul

exit /b 0
