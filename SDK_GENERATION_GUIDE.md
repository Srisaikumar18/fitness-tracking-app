# Python SDK Generation Guide for Fitness Tracking API

## Overview
This guide shows how to generate a Python SDK from your FastAPI application using OpenAPI Generator CLI.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Generate OpenAPI Spec](#generate-openapi-spec)
4. [Generate Python SDK](#generate-python-sdk)
5. [Install SDK](#install-sdk)
6. [Test Scripts](#test-scripts)
7. [SDK Usage Examples](#sdk-usage-examples)

---

## Prerequisites

- Java 8+ (required for OpenAPI Generator)
- Python 3.8+
- FastAPI backend running on http://localhost:8000

### Check Java Installation
```bash
java -version
```

If Java is not installed, download from: https://www.java.com/download/

---

## Installation

### Option 1: Using npm (Recommended for Windows)
```bash
npm install @openapitools/openapi-generator-cli -g
```

### Option 2: Using JAR file directly
```bash
# Download the latest JAR
curl -o openapi-generator-cli.jar https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.2.0/openapi-generator-cli-7.2.0.jar

# Or use wget
wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.2.0/openapi-generator-cli-7.2.0.jar
```

### Option 3: Using Chocolatey (Windows)
```bash
choco install openapi-generator-cli
```

### Verify Installation
```bash
# If installed via npm
openapi-generator-cli version

# If using JAR directly
java -jar openapi-generator-cli.jar version
```

---

## Generate OpenAPI Spec

### Step 1: Start Your FastAPI Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Step 2: Download OpenAPI Specification
Your FastAPI app automatically generates an OpenAPI spec at:
- **URL**: http://localhost:8000/openapi.json

Download it:
```bash
# Using curl
curl http://localhost:8000/openapi.json -o openapi.json

# Using PowerShell
Invoke-WebRequest -Uri "http://localhost:8000/openapi.json" -OutFile "openapi.json"
```

### Step 3: Verify OpenAPI Spec
```bash
# View the spec
cat openapi.json

# Or open in browser
start http://localhost:8000/docs
```

---

## Generate Python SDK

### Create SDK Generation Script

Create `generate_sdk.bat`:
```batch
@echo off
echo Generating Python SDK for Fitness Tracking API...

REM Download OpenAPI spec
echo Step 1: Downloading OpenAPI specification...
curl http://localhost:8000/openapi.json -o openapi.json

REM Generate SDK
echo Step 2: Generating Python SDK...
openapi-generator-cli generate ^
  -i openapi.json ^
  -g python ^
  -o fitness_tracker_sdk ^
  --package-name fitness_tracker_client ^
  --additional-properties=projectName=fitness-tracker-sdk,packageVersion=1.0.0

echo.
echo SDK generated successfully in 'fitness_tracker_sdk' folder!
echo.
echo Next steps:
echo 1. cd fitness_tracker_sdk
echo 2. pip install -e .
echo 3. Run test scripts
pause
```

### Alternative: Using JAR directly

Create `generate_sdk_jar.bat`:
```batch
@echo off
echo Generating Python SDK using JAR...

REM Download OpenAPI spec
curl http://localhost:8000/openapi.json -o openapi.json

REM Generate SDK using JAR
java -jar openapi-generator-cli.jar generate ^
  -i openapi.json ^
  -g python ^
  -o fitness_tracker_sdk ^
  --package-name fitness_tracker_client ^
  --additional-properties=projectName=fitness-tracker-sdk,packageVersion=1.0.0

echo SDK generated successfully!
pause
```

### Run the Generation Script
```bash
# Make sure backend is running first!
generate_sdk.bat
```

### SDK Generation Options Explained
- `-i openapi.json` - Input OpenAPI specification file
- `-g python` - Generate Python SDK
- `-o fitness_tracker_sdk` - Output directory
- `--package-name fitness_tracker_client` - Python package name
- `--additional-properties` - Additional configuration:
  - `projectName=fitness-tracker-sdk` - Project name
  - `packageVersion=1.0.0` - SDK version

---

## Install SDK

### Step 1: Navigate to SDK Directory
```bash
cd fitness_tracker_sdk
```

### Step 2: Install SDK in Development Mode
```bash
# Install in editable mode
pip install -e .

# Or install normally
pip install .
```

### Step 3: Verify Installation
```bash
pip list | grep fitness
```

You should see:
```
fitness-tracker-sdk    1.0.0
```

---

## Test Scripts

### Test Script 1: GET /api/workouts/

Create `test_get_workouts.py`:
```python
"""
Test script for GET /api/workouts/ endpoint
Retrieves all workouts from the API
"""

import fitness_tracker_client
from fitness_tracker_client.api import workouts_api
from fitness_tracker_client.rest import ApiException
from pprint import pprint

def test_get_workouts():
    """Test retrieving all workouts"""
    
    # Configure API client
    configuration = fitness_tracker_client.Configuration(
        host="http://localhost:8000"
    )
    
    # Create API client
    with fitness_tracker_client.ApiClient(configuration) as api_client:
        # Create API instance
        api_instance = workouts_api.WorkoutsApi(api_client)
        
        try:
            # Get all workouts
            print("📋 Fetching all workouts...")
            api_response = api_instance.get_workouts_api_workouts_get()
            
            print(f"\n✅ Success! Retrieved {len(api_response)} workouts\n")
            
            # Display workouts
            if api_response:
                print("=" * 80)
                print(f"{'ID':<5} {'User Name':<20} {'Activity':<15} {'Duration':<10} {'Calories':<10}")
                print("=" * 80)
                
                for workout in api_response:
                    print(f"{workout.id:<5} {workout.user_name:<20} {workout.activity:<15} {workout.duration:<10} {workout.calories:<10}")
                
                print("=" * 80)
                
                # Calculate statistics
                total_duration = sum(w.duration for w in api_response)
                total_calories = sum(w.calories for w in api_response)
                
                print(f"\n📊 Statistics:")
                print(f"   Total Workouts: {len(api_response)}")
                print(f"   Total Duration: {total_duration} minutes")
                print(f"   Total Calories: {total_calories} cal")
            else:
                print("ℹ️  No workouts found. Add some workouts first!")
                
        except ApiException as e:
            print(f"❌ Exception when calling WorkoutsApi->get_workouts: {e}")
            print(f"   Status: {e.status}")
            print(f"   Reason: {e.reason}")
            print(f"   Body: {e.body}")

if __name__ == "__main__":
    print("=" * 80)
    print("Fitness Tracker API - GET Workouts Test")
    print("=" * 80)
    print()
    
    test_get_workouts()
    
    print("\n" + "=" * 80)
    print("Test completed!")
    print("=" * 80)
```

### Test Script 2: POST /api/workouts/

Create `test_post_workout.py`:
```python
"""
Test script for POST /api/workouts/ endpoint
Creates a new workout in the API
"""

import fitness_tracker_client
from fitness_tracker_client.api import workouts_api
from fitness_tracker_client.model.workout_create import WorkoutCreate
from fitness_tracker_client.rest import ApiException
from pprint import pprint

def test_create_workout(user_name, activity, duration):
    """Test creating a new workout"""
    
    # Configure API client
    configuration = fitness_tracker_client.Configuration(
        host="http://localhost:8000"
    )
    
    # Create API client
    with fitness_tracker_client.ApiClient(configuration) as api_client:
        # Create API instance
        api_instance = workouts_api.WorkoutsApi(api_client)
        
        # Create workout data
        workout_data = WorkoutCreate(
            user_name=user_name,
            activity=activity,
            duration=duration
        )
        
        try:
            # Create workout
            print(f"➕ Creating workout...")
            print(f"   User: {user_name}")
            print(f"   Activity: {activity}")
            print(f"   Duration: {duration} minutes")
            print()
            
            api_response = api_instance.create_workout_api_workouts_post(workout_data)
            
            print("✅ Workout created successfully!\n")
            
            # Display created workout
            print("=" * 80)
            print("Created Workout Details:")
            print("=" * 80)
            print(f"ID:           {api_response.id}")
            print(f"User Name:    {api_response.user_name}")
            print(f"Activity:     {api_response.activity}")
            print(f"Duration:     {api_response.duration} minutes")
            print(f"Calories:     {api_response.calories} cal (calculated automatically)")
            print("=" * 80)
            
            return api_response
            
        except ApiException as e:
            print(f"❌ Exception when calling WorkoutsApi->create_workout: {e}")
            print(f"   Status: {e.status}")
            print(f"   Reason: {e.reason}")
            print(f"   Body: {e.body}")
            return None

def test_multiple_workouts():
    """Test creating multiple workouts"""
    
    workouts_to_create = [
        ("Alice Johnson", "running", 45),
        ("Bob Smith", "cycling", 60),
        ("Charlie Brown", "walking", 30),
        ("Diana Prince", "swimming", 40),
    ]
    
    print("=" * 80)
    print("Creating Multiple Workouts")
    print("=" * 80)
    print()
    
    created_workouts = []
    
    for user_name, activity, duration in workouts_to_create:
        workout = test_create_workout(user_name, activity, duration)
        if workout:
            created_workouts.append(workout)
        print()
    
    print("=" * 80)
    print(f"✅ Successfully created {len(created_workouts)} workouts!")
    print("=" * 80)

if __name__ == "__main__":
    print("=" * 80)
    print("Fitness Tracker API - POST Workout Test")
    print("=" * 80)
    print()
    
    # Test 1: Create a single workout
    print("Test 1: Create Single Workout")
    print("-" * 80)
    test_create_workout("John Doe", "running", 30)
    
    print("\n\n")
    
    # Test 2: Create multiple workouts
    print("Test 2: Create Multiple Workouts")
    print("-" * 80)
    test_multiple_workouts()
    
    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)
```

### Test Script 3: Combined Test Suite

Create `test_sdk_complete.py`:
```python
"""
Complete test suite for Fitness Tracker SDK
Tests all API endpoints with various scenarios
"""

import fitness_tracker_client
from fitness_tracker_client.api import workouts_api
from fitness_tracker_client.model.workout_create import WorkoutCreate
from fitness_tracker_client.rest import ApiException
import time

class FitnessTrackerTester:
    """Test suite for Fitness Tracker API"""
    
    def __init__(self, host="http://localhost:8000"):
        """Initialize the tester with API configuration"""
        self.configuration = fitness_tracker_client.Configuration(host=host)
        self.api_client = fitness_tracker_client.ApiClient(self.configuration)
        self.api_instance = workouts_api.WorkoutsApi(self.api_client)
        
    def test_health_check(self):
        """Test if API is accessible"""
        print("🏥 Testing API Health Check...")
        try:
            # Try to get workouts (simplest endpoint)
            self.api_instance.get_workouts_api_workouts_get()
            print("✅ API is healthy and accessible\n")
            return True
        except Exception as e:
            print(f"❌ API health check failed: {e}\n")
            return False
    
    def test_get_all_workouts(self):
        """Test GET /api/workouts/"""
        print("📋 Test: GET All Workouts")
        print("-" * 80)
        
        try:
            workouts = self.api_instance.get_workouts_api_workouts_get()
            print(f"✅ Retrieved {len(workouts)} workouts")
            
            if workouts:
                print(f"\nSample workout:")
                w = workouts[0]
                print(f"  ID: {w.id}, User: {w.user_name}, Activity: {w.activity}")
            
            print()
            return True
        except ApiException as e:
            print(f"❌ Failed: {e}\n")
            return False
    
    def test_create_workout(self, user_name, activity, duration):
        """Test POST /api/workouts/"""
        print(f"➕ Test: Create Workout ({activity} for {duration} min)")
        print("-" * 80)
        
        try:
            workout_data = WorkoutCreate(
                user_name=user_name,
                activity=activity,
                duration=duration
            )
            
            result = self.api_instance.create_workout_api_workouts_post(workout_data)
            
            print(f"✅ Created workout ID: {result.id}")
            print(f"   User: {result.user_name}")
            print(f"   Activity: {result.activity}")
            print(f"   Duration: {result.duration} min")
            print(f"   Calories: {result.calories} cal")
            print()
            return result
        except ApiException as e:
            print(f"❌ Failed: {e}\n")
            return None
    
    def test_calorie_calculation(self):
        """Test automatic calorie calculation for different activities"""
        print("🔥 Test: Calorie Calculation")
        print("-" * 80)
        
        test_cases = [
            ("running", 30, 300),   # 30 * 10
            ("cycling", 40, 320),   # 40 * 8
            ("walking", 50, 250),   # 50 * 5
            ("swimming", 25, 150),  # 25 * 6 (other)
        ]
        
        passed = 0
        failed = 0
        
        for activity, duration, expected_calories in test_cases:
            workout_data = WorkoutCreate(
                user_name="Test User",
                activity=activity,
                duration=duration
            )
            
            try:
                result = self.api_instance.create_workout_api_workouts_post(workout_data)
                
                if result.calories == expected_calories:
                    print(f"✅ {activity.capitalize()}: {duration} min = {result.calories} cal (expected {expected_calories})")
                    passed += 1
                else:
                    print(f"❌ {activity.capitalize()}: Got {result.calories} cal, expected {expected_calories}")
                    failed += 1
            except ApiException as e:
                print(f"❌ {activity.capitalize()}: API error - {e}")
                failed += 1
        
        print(f"\nResults: {passed} passed, {failed} failed")
        print()
        return failed == 0
    
    def test_activity_standardization(self):
        """Test activity name standardization (lowercase)"""
        print("🔤 Test: Activity Standardization")
        print("-" * 80)
        
        test_cases = [
            "RUNNING",
            "CyClInG",
            "  Walking  ",
            "SwImMiNg"
        ]
        
        passed = 0
        
        for activity_input in test_cases:
            workout_data = WorkoutCreate(
                user_name="Test User",
                activity=activity_input,
                duration=10
            )
            
            try:
                result = self.api_instance.create_workout_api_workouts_post(workout_data)
                expected = activity_input.strip().lower()
                
                if result.activity == expected:
                    print(f"✅ '{activity_input}' → '{result.activity}'")
                    passed += 1
                else:
                    print(f"❌ '{activity_input}' → '{result.activity}' (expected '{expected}')")
            except ApiException as e:
                print(f"❌ '{activity_input}': API error - {e}")
        
        print(f"\nResults: {passed}/{len(test_cases)} passed")
        print()
        return passed == len(test_cases)
    
    def test_validation(self):
        """Test input validation"""
        print("✔️  Test: Input Validation")
        print("-" * 80)
        
        # Test invalid duration (0)
        print("Testing duration = 0 (should fail)...")
        try:
            workout_data = WorkoutCreate(
                user_name="Test User",
                activity="running",
                duration=0
            )
            self.api_instance.create_workout_api_workouts_post(workout_data)
            print("❌ Should have rejected duration = 0")
        except ApiException as e:
            if e.status == 422:
                print("✅ Correctly rejected duration = 0")
            else:
                print(f"❌ Unexpected error: {e}")
        
        # Test negative duration
        print("Testing duration = -10 (should fail)...")
        try:
            workout_data = WorkoutCreate(
                user_name="Test User",
                activity="running",
                duration=-10
            )
            self.api_instance.create_workout_api_workouts_post(workout_data)
            print("❌ Should have rejected negative duration")
        except ApiException as e:
            if e.status == 422:
                print("✅ Correctly rejected negative duration")
            else:
                print(f"❌ Unexpected error: {e}")
        
        print()
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("=" * 80)
        print("Fitness Tracker SDK - Complete Test Suite")
        print("=" * 80)
        print()
        
        # Health check
        if not self.test_health_check():
            print("⚠️  API is not accessible. Make sure backend is running!")
            return
        
        # Run tests
        self.test_get_all_workouts()
        self.test_create_workout("SDK Test User", "running", 25)
        self.test_calorie_calculation()
        self.test_activity_standardization()
        self.test_validation()
        
        print("=" * 80)
        print("✅ All tests completed!")
        print("=" * 80)

if __name__ == "__main__":
    tester = FitnessTrackerTester()
    tester.run_all_tests()
```

---

## SDK Usage Examples

### Example 1: Simple Client

Create `simple_client.py`:
```python
"""
Simple client example using the generated SDK
"""

import fitness_tracker_client
from fitness_tracker_client.api import workouts_api
from fitness_tracker_client.model.workout_create import WorkoutCreate

# Configure API
configuration = fitness_tracker_client.Configuration(
    host="http://localhost:8000"
)

# Create client
with fitness_tracker_client.ApiClient(configuration) as api_client:
    api = workouts_api.WorkoutsApi(api_client)
    
    # Create a workout
    new_workout = WorkoutCreate(
        user_name="Jane Doe",
        activity="running",
        duration=45
    )
    
    result = api.create_workout_api_workouts_post(new_workout)
    print(f"Created workout ID: {result.id}")
    print(f"Calories burned: {result.calories}")
    
    # Get all workouts
    workouts = api.get_workouts_api_workouts_get()
    print(f"\nTotal workouts: {len(workouts)}")
```

### Example 2: Workout Manager Class

Create `workout_manager.py`:
```python
"""
Workout Manager - High-level wrapper around the SDK
"""

import fitness_tracker_client
from fitness_tracker_client.api import workouts_api
from fitness_tracker_client.model.workout_create import WorkoutCreate
from typing import List

class WorkoutManager:
    """High-level interface for managing workouts"""
    
    def __init__(self, host="http://localhost:8000"):
        """Initialize the workout manager"""
        self.configuration = fitness_tracker_client.Configuration(host=host)
        self.api_client = fitness_tracker_client.ApiClient(self.configuration)
        self.api = workouts_api.WorkoutsApi(self.api_client)
    
    def add_workout(self, user_name: str, activity: str, duration: int):
        """Add a new workout"""
        workout_data = WorkoutCreate(
            user_name=user_name,
            activity=activity,
            duration=duration
        )
        return self.api.create_workout_api_workouts_post(workout_data)
    
    def get_all_workouts(self):
        """Get all workouts"""
        return self.api.get_workouts_api_workouts_get()
    
    def get_workouts_by_user(self, user_name: str):
        """Get workouts for a specific user"""
        all_workouts = self.get_all_workouts()
        return [w for w in all_workouts if w.user_name == user_name]
    
    def get_workouts_by_activity(self, activity: str):
        """Get workouts for a specific activity"""
        all_workouts = self.get_all_workouts()
        return [w for w in all_workouts if w.activity == activity.lower()]
    
    def get_total_calories(self, user_name: str = None):
        """Calculate total calories burned"""
        if user_name:
            workouts = self.get_workouts_by_user(user_name)
        else:
            workouts = self.get_all_workouts()
        return sum(w.calories for w in workouts)
    
    def get_total_duration(self, user_name: str = None):
        """Calculate total workout duration"""
        if user_name:
            workouts = self.get_workouts_by_user(user_name)
        else:
            workouts = self.get_all_workouts()
        return sum(w.duration for w in workouts)
    
    def get_statistics(self):
        """Get workout statistics"""
        workouts = self.get_all_workouts()
        
        if not workouts:
            return {
                "total_workouts": 0,
                "total_duration": 0,
                "total_calories": 0,
                "unique_users": 0,
                "unique_activities": 0
            }
        
        return {
            "total_workouts": len(workouts),
            "total_duration": sum(w.duration for w in workouts),
            "total_calories": sum(w.calories for w in workouts),
            "unique_users": len(set(w.user_name for w in workouts)),
            "unique_activities": len(set(w.activity for w in workouts))
        }

# Example usage
if __name__ == "__main__":
    manager = WorkoutManager()
    
    # Add workouts
    print("Adding workouts...")
    manager.add_workout("Alice", "running", 30)
    manager.add_workout("Bob", "cycling", 45)
    manager.add_workout("Alice", "walking", 20)
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total Workouts: {stats['total_workouts']}")
    print(f"  Total Duration: {stats['total_duration']} min")
    print(f"  Total Calories: {stats['total_calories']} cal")
    print(f"  Unique Users: {stats['unique_users']}")
    print(f"  Unique Activities: {stats['unique_activities']}")
    
    # Get Alice's workouts
    alice_workouts = manager.get_workouts_by_user("Alice")
    print(f"\nAlice's workouts: {len(alice_workouts)}")
    print(f"Alice's total calories: {manager.get_total_calories('Alice')}")
```

---

## Running the Tests

### Step 1: Ensure Backend is Running
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Step 2: Run Test Scripts
```bash
# Test GET endpoint
python test_get_workouts.py

# Test POST endpoint
python test_post_workout.py

# Run complete test suite
python test_sdk_complete.py

# Test simple client
python simple_client.py

# Test workout manager
python workout_manager.py
```

---

## Troubleshooting

### Issue 1: "openapi-generator-cli: command not found"
**Solution**: Install using npm:
```bash
npm install @openapitools/openapi-generator-cli -g
```

### Issue 2: "Java not found"
**Solution**: Install Java 8 or higher from https://www.java.com/download/

### Issue 3: "Connection refused"
**Solution**: Make sure backend is running:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Issue 4: "Module not found: fitness_tracker_client"
**Solution**: Install the SDK:
```bash
cd fitness_tracker_sdk
pip install -e .
```

### Issue 5: SDK generation fails
**Solution**: Verify OpenAPI spec is valid:
```bash
# Download spec
curl http://localhost:8000/openapi.json -o openapi.json

# View spec
cat openapi.json
```

---

## SDK Structure

After generation, your SDK will have this structure:
```
fitness_tracker_sdk/
├── fitness_tracker_client/
│   ├── api/
│   │   └── workouts_api.py          # API methods
│   ├── model/
│   │   ├── workout_create.py        # WorkoutCreate model
│   │   └── workout_response.py      # WorkoutResponse model
│   ├── __init__.py
│   ├── configuration.py             # API configuration
│   ├── api_client.py                # HTTP client
│   └── rest.py                      # REST utilities
├── docs/                            # API documentation
├── test/                            # Generated tests
├── setup.py                         # Package setup
├── requirements.txt                 # Dependencies
└── README.md                        # SDK documentation
```

---

## Next Steps

1. ✅ Generate SDK using the guide above
2. ✅ Install SDK: `pip install -e fitness_tracker_sdk`
3. ✅ Run test scripts to verify functionality
4. ✅ Use SDK in your Python applications
5. ✅ Distribute SDK to other developers

---

## Benefits of Using SDK

1. **Type Safety**: Python type hints for all models
2. **Auto-completion**: IDE support for API methods
3. **Error Handling**: Built-in exception handling
4. **Documentation**: Generated docs for all endpoints
5. **Consistency**: Same interface across projects
6. **Maintainability**: Regenerate when API changes

---

**Last Updated**: April 2026  
**OpenAPI Generator Version**: 7.2.0  
**Python Version**: 3.8+
