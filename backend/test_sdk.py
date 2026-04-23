"""
Test script for the Fitness Tracking App Python SDK.

This script demonstrates how to use the generated OpenAPI client to:
1. Create a new workout (POST /api/workouts/)
2. Retrieve all workouts (GET /api/workouts/)

Correct method names from WorkoutsApi:
- create_workout_api_workouts_post() - Create a new workout
- get_workouts_api_workouts_get() - Get all workouts
"""

import sys
import os

# Add the SDK to the Python path
sys.path.append(os.path.abspath("../fitness_sdk"))

from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from openapi_client.api.workouts_api import WorkoutsApi
from openapi_client.models.workout_create import WorkoutCreate

# Configure the API client
config = Configuration()
config.host = "http://localhost:8000"  # Backend API URL

# Create API client and WorkoutsApi instance
client = ApiClient(configuration=config)
api = WorkoutsApi(api_client=client)

print("=" * 60)
print("Fitness Tracking App - Python SDK Test")
print("=" * 60)

# Test 1: Get all workouts (GET /api/workouts/)
print("\n[TEST 1] Fetching all workouts...")
try:
    workouts = api.get_workouts_api_workouts_get()
    print(f"✅ Successfully retrieved {len(workouts)} workout(s)")
    
    if workouts:
        print("\nWorkouts:")
        for i, workout in enumerate(workouts, 1):
            print(f"  {i}. ID: {workout.id}")
            print(f"     User: {workout.user_name}")
            print(f"     Activity: {workout.activity}")
            print(f"     Duration: {workout.duration} minutes")
            print(f"     Calories: {workout.calories}")
            print()
    else:
        print("  No workouts found in the database.")
        
except Exception as e:
    print(f"❌ Error fetching workouts: {e}")

# Test 2: Create a new workout (POST /api/workouts/)
print("\n[TEST 2] Creating a new workout...")
try:
    # Create a WorkoutCreate object
    new_workout = WorkoutCreate(
        user_name="SDK Test User",
        activity="Running",
        duration=30
    )
    
    # Call the API to create the workout
    created_workout = api.create_workout_api_workouts_post(workout_create=new_workout)
    
    print(f"✅ Successfully created workout!")
    print(f"  ID: {created_workout.id}")
    print(f"  User: {created_workout.user_name}")
    print(f"  Activity: {created_workout.activity} (standardized to lowercase)")
    print(f"  Duration: {created_workout.duration} minutes")
    print(f"  Calories: {created_workout.calories} (automatically calculated)")
    
except Exception as e:
    print(f"❌ Error creating workout: {e}")

# Test 3: Verify the workout was created by fetching all workouts again
print("\n[TEST 3] Verifying workout creation...")
try:
    workouts = api.get_workouts_api_workouts_get()
    print(f"✅ Total workouts in database: {len(workouts)}")
    
    if workouts:
        latest_workout = workouts[0]  # Most recent workout (ordered by ID desc)
        print(f"\nLatest workout:")
        print(f"  ID: {latest_workout.id}")
        print(f"  User: {latest_workout.user_name}")
        print(f"  Activity: {latest_workout.activity}")
        print(f"  Duration: {latest_workout.duration} minutes")
        print(f"  Calories: {latest_workout.calories}")
        
except Exception as e:
    print(f"❌ Error verifying workout: {e}")

print("\n" + "=" * 60)
print("SDK Test Complete!")
print("=" * 60)