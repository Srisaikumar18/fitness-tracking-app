@echo off
echo ================================================================================
echo Fitness Tracker API - SDK Quick Start
echo ================================================================================
echo.
echo This script will:
echo   1. Generate Python SDK from your FastAPI app
echo   2. Install the SDK
echo   3. Run test scripts
echo.
echo Prerequisites:
echo   - Backend must be running on http://localhost:8000
echo   - openapi-generator-cli must be installed
echo   - Python 3.8+ with pip
echo.
pause
echo.

REM Step 1: Generate SDK
echo ================================================================================
echo Step 1: Generating SDK
echo ================================================================================
call generate_sdk.bat
if errorlevel 1 (
    echo [ERROR] SDK generation failed
    pause
    exit /b 1
)
echo.

REM Step 2: Install SDK
echo ================================================================================
echo Step 2: Installing SDK
echo ================================================================================
cd fitness_tracker_sdk
pip install -e .
if errorlevel 1 (
    echo [ERROR] SDK installation failed
    pause
    exit /b 1
)
cd ..
echo [OK] SDK installed successfully
echo.

REM Step 3: Run tests
echo ================================================================================
echo Step 3: Running Tests
echo ================================================================================
echo.

echo Test 1: GET /api/workouts/
echo --------------------------------------------------------------------------------
python test_get_workouts.py
echo.
echo.

echo Test 2: POST /api/workouts/
echo --------------------------------------------------------------------------------
python test_post_workout.py
echo.
echo.

echo ================================================================================
echo [SUCCESS] SDK Quick Start Completed!
echo ================================================================================
echo.
echo SDK is ready to use!
echo.
echo Example usage:
echo   import fitness_tracker_client
echo   from fitness_tracker_client.api import workouts_api
echo.
echo Documentation:
echo   - SDK Guide: SDK_GENERATION_GUIDE.md
echo   - API Docs: http://localhost:8000/docs
echo.
pause
