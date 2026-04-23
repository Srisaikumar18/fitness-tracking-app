@echo off
echo ======================================================================
echo FITNESS TRACKING APP - FULL SYSTEM VERIFICATION
echo ======================================================================
echo.
echo This script will perform comprehensive end-to-end verification:
echo   - Backend API endpoints
echo   - Calorie calculation logic
echo   - Input validation
echo   - Frontend accessibility
echo   - Python SDK functionality
echo   - Integration tests
echo.
echo PREREQUISITES:
echo   1. Backend server must be running on port 8000
echo   2. Frontend server must be running on port 5173 (optional)
echo   3. Python SDK must be installed
echo.
echo ======================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run setupdev.bat first to create the virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Run the verification script
python verify_system.py

REM Deactivate virtual environment
deactivate

echo.
pause
