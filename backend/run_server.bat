@echo off
REM Script to run the FastAPI backend server correctly

echo ============================================================
echo Starting FastAPI Backend Server
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setupdev.bat first to create the virtual environment.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Run uvicorn from the backend directory
echo.
echo Starting server on http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run uvicorn with correct module path
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
