@echo off
echo ================================================================================
echo Fitness Tracker API - Python SDK Generator
echo ================================================================================
echo.

REM Check if backend is running
echo Step 1: Checking if backend is running...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Backend is not running!
    echo.
    echo Please start the backend first:
    echo   cd backend
    echo   python -m uvicorn app.main:app --reload
    echo.
    pause
    exit /b 1
)
echo [OK] Backend is running
echo.

REM Download OpenAPI spec
echo Step 2: Downloading OpenAPI specification...
curl -s http://localhost:8000/openapi.json -o openapi.json
if errorlevel 1 (
    echo [ERROR] Failed to download OpenAPI spec
    pause
    exit /b 1
)
echo [OK] OpenAPI spec downloaded
echo.

REM Check if openapi-generator-cli is installed
echo Step 3: Checking OpenAPI Generator installation...
where openapi-generator-cli >nul 2>&1
if errorlevel 1 (
    echo [WARNING] openapi-generator-cli not found
    echo.
    echo Please install it using one of these methods:
    echo   1. npm install @openapitools/openapi-generator-cli -g
    echo   2. Download JAR from: https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.2.0/openapi-generator-cli-7.2.0.jar
    echo.
    pause
    exit /b 1
)
echo [OK] OpenAPI Generator found
echo.

REM Generate SDK
echo Step 4: Generating Python SDK...
echo This may take a minute...
echo.

openapi-generator-cli generate ^
  -i openapi.json ^
  -g python ^
  -o fitness_tracker_sdk ^
  --package-name fitness_tracker_client ^
  --additional-properties=projectName=fitness-tracker-sdk,packageVersion=1.0.0

if errorlevel 1 (
    echo [ERROR] SDK generation failed
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo [SUCCESS] SDK generated successfully!
echo ================================================================================
echo.
echo SDK Location: fitness_tracker_sdk\
echo Package Name: fitness_tracker_client
echo.
echo Next steps:
echo   1. cd fitness_tracker_sdk
echo   2. pip install -e .
echo   3. python ..\test_get_workouts.py
echo   4. python ..\test_post_workout.py
echo.
echo ================================================================================
pause
