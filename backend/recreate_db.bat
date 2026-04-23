@echo off
REM Batch script to recreate the database after refactoring

echo ============================================================
echo DATABASE RECREATION SCRIPT
echo ============================================================
echo.
echo This will recreate the database with only the workouts table.
echo All existing data will be deleted.
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

REM Run the recreation script
echo.
python recreate_db.py

echo.
echo ============================================================
echo Done!
echo ============================================================
echo.
echo Next steps:
echo 1. Run: runapplication.bat (from the root directory)
echo 2. Visit: http://localhost:8000/docs
echo 3. Test the API with the 2 workout endpoints
echo.

pause
