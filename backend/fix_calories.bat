@echo off
echo ======================================================================
echo Fixing Calorie Values in Database
echo ======================================================================
echo.
echo This script will recalculate calories for all existing workouts
echo based on the correct calorie calculation rules:
echo   - running: duration * 10 calories/min
echo   - cycling: duration * 8 calories/min
echo   - walking: duration * 5 calories/min
echo   - others: duration * 6 calories/min
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

REM Run the fix script
python fix_calories.py

REM Deactivate virtual environment
deactivate

echo.
pause
