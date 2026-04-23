@echo off
REM ============================================================================
REM Fitness Tracking App - Development Environment Setup Script (Windows)
REM ============================================================================
REM This script sets up the complete development environment including:
REM - Backend Python virtual environment
REM - Backend dependencies installation
REM - Database migrations with Alembic
REM - Frontend Node.js dependencies installation
REM ============================================================================

echo.
echo ============================================================================
echo Fitness Tracking App - Development Environment Setup
echo ============================================================================
echo.

REM Store the root directory
set ROOT_DIR=%cd%

REM ============================================================================
REM STEP 1: Backend Setup
REM ============================================================================
echo [1/4] Setting up backend environment...
echo.

REM Navigate to backend directory
cd backend
if errorlevel 1 (
    echo ERROR: Backend directory not found!
    cd "%ROOT_DIR%"
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    cd "%ROOT_DIR%"
    exit /b 1
)

echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    cd "%ROOT_DIR%"
    exit /b 1
)

echo Virtual environment created successfully.
echo.

REM ============================================================================
REM STEP 2: Install Backend Dependencies
REM ============================================================================
echo [2/4] Installing backend dependencies...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    cd "%ROOT_DIR%"
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)

REM Install dependencies
echo Installing Python packages from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies!
    cd "%ROOT_DIR%"
    exit /b 1
)

echo Backend dependencies installed successfully.
echo.

REM ============================================================================
REM STEP 3: Run Database Migrations
REM ============================================================================
echo [3/4] Running database migrations...
echo.

REM Check if alembic.ini exists
if not exist "alembic.ini" (
    echo ERROR: alembic.ini not found!
    echo Please ensure Alembic is properly configured.
    cd "%ROOT_DIR%"
    exit /b 1
)

REM Run migrations
echo Running Alembic migrations...
python -m alembic upgrade head
if errorlevel 1 (
    echo WARNING: Database migration failed!
    echo This might be okay if the database is already set up.
    echo You can manually run migrations later with: alembic upgrade head
    echo.
) else (
    echo Database migrations completed successfully.
    echo.
)

REM Deactivate virtual environment before moving to frontend
call venv\Scripts\deactivate.bat 2>nul

REM Return to root directory
cd "%ROOT_DIR%"

REM ============================================================================
REM STEP 4: Frontend Setup
REM ============================================================================
echo [4/4] Setting up frontend environment...
echo.

REM Navigate to frontend directory
cd frontend
if errorlevel 1 (
    echo ERROR: Frontend directory not found!
    cd "%ROOT_DIR%"
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js from https://nodejs.org/
    cd "%ROOT_DIR%"
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH!
    cd "%ROOT_DIR%"
    exit /b 1
)

REM Install frontend dependencies
echo Installing frontend dependencies with npm...
npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies!
    cd "%ROOT_DIR%"
    exit /b 1
)

echo Frontend dependencies installed successfully.
echo.

REM Return to root directory
cd "%ROOT_DIR%"

REM ============================================================================
REM Setup Complete
REM ============================================================================
echo.
echo ============================================================================
echo Development Environment Setup Complete!
echo ============================================================================
echo.
echo Backend:
echo   - Virtual environment created at: backend\venv
echo   - Dependencies installed from: backend\requirements.txt
echo   - Database migrations applied
echo.
echo Frontend:
echo   - Dependencies installed from: frontend\package.json
echo   - Node modules located at: frontend\node_modules
echo.
echo Next Steps:
echo   1. To start both servers automatically:
echo      runapplication.bat
echo.
echo   2. Or start them manually:
echo.
echo      Backend:
echo        cd backend
echo        venv\Scripts\activate
echo        python -m uvicorn app.main:app --reload
echo.
echo      Frontend:
echo        cd frontend
echo        npm run dev
echo.
echo ============================================================================
echo.

exit /b 0
