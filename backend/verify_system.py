"""
Full End-to-End System Verification Script

This script performs comprehensive verification of the Fitness Tracking App:
- Backend API endpoints
- Calorie calculation logic
- Input validation
- Frontend integration
- Python SDK functionality
- Error handling

Usage:
    python verify_system.py
"""

import sys
import os
import time
import requests
from typing import Dict, List, Tuple

# Add SDK to path
sys.path.append(os.path.abspath("../fitness_sdk"))

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Test results tracking
test_results = {
    'passed': 0,
    'failed': 0,
    'warnings': 0,
    'issues': []
}

def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")

def print_test(test_name: str):
    """Print test name."""
    print(f"{Colors.BOLD}[TEST]{Colors.END} {test_name}...", end=" ")

def print_pass(message: str = "PASS"):
    """Print pass message."""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    test_results['passed'] += 1

def print_fail(message: str):
    """Print fail message."""
    print(f"{Colors.RED}❌ FAIL: {message}{Colors.END}")
    test_results['failed'] += 1
    test_results['issues'].append(message)

def print_warning(message: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  WARNING: {message}{Colors.END}")
    test_results['warnings'] += 1

def print_info(message: str):
    """Print info message."""
    print(f"   {message}")

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

# ============================================================================
# 1. BACKEND VERIFICATION
# ============================================================================

def verify_backend_health():
    """Verify backend server is running and healthy."""
    print_header("1. BACKEND VERIFICATION")
    
    # Test 1.1: Backend server is running
    print_test("Backend server is running")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy' and data.get('database') == 'connected':
                print_pass()
                print_info(f"Status: {data.get('status')}")
                print_info(f"Database: {data.get('database')}")
            else:
                print_fail(f"Health check returned unexpected data: {data}")
        else:
            print_fail(f"Health check returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print_fail("Cannot connect to backend server. Is it running on port 8000?")
        return False
    except Exception as e:
        print_fail(f"Error checking backend health: {e}")
        return False
    
    # Test 1.2: API documentation is accessible
    print_test("API documentation is accessible")
    try:
        response = requests.get(f"{BACKEND_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_pass()
        else:
            print_fail(f"API docs returned status {response.status_code}")
    except Exception as e:
        print_fail(f"Error accessing API docs: {e}")
    
    # Test 1.3: OpenAPI schema is accessible
    print_test("OpenAPI schema is accessible")
    try:
        response = requests.get(f"{BACKEND_URL}/openapi.json", timeout=5)
        if response.status_code == 200:
            schema = response.json()
            if 'paths' in schema and '/api/workouts/' in schema['paths']:
                print_pass()
            else:
                print_fail("OpenAPI schema missing expected paths")
        else:
            print_fail(f"OpenAPI schema returned status {response.status_code}")
    except Exception as e:
        print_fail(f"Error accessing OpenAPI schema: {e}")
    
    return True

def verify_workout_creation():
    """Verify workout creation endpoint."""
    print_header("2. WORKOUT CREATION VERIFICATION")
    
    test_cases = [
        {
            'name': 'Create workout with running',
            'data': {'user_name': 'Test User', 'activity': 'Running', 'duration': 45},
            'expected_activity': 'running',
            'expected_calories': 450
        },
        {
            'name': 'Create workout with cycling',
            'data': {'user_name': 'Test User', 'activity': 'Cycling', 'duration': 60},
            'expected_activity': 'cycling',
            'expected_calories': 480
        },
        {
            'name': 'Create workout with walking',
            'data': {'user_name': 'Test User', 'activity': 'Walking', 'duration': 30},
            'expected_activity': 'walking',
            'expected_calories': 150
        },
        {
            'name': 'Create workout with other activity',
            'data': {'user_name': 'Test User', 'activity': 'Swimming', 'duration': 40},
            'expected_activity': 'swimming',
            'expected_calories': 240
        },
    ]
    
    for test_case in test_cases:
        print_test(test_case['name'])
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/workouts/",
                json=test_case['data'],
                timeout=5
            )
            
            if response.status_code == 201:
                workout = response.json()
                
                # Verify activity standardization
                if workout['activity'] != test_case['expected_activity']:
                    print_fail(f"Activity not standardized. Expected '{test_case['expected_activity']}', got '{workout['activity']}'")
                    continue
                
                # Verify calorie calculation
                if workout['calories'] != test_case['expected_calories']:
                    print_fail(f"Incorrect calories. Expected {test_case['expected_calories']}, got {workout['calories']}")
                    continue
                
                print_pass()
                print_info(f"Activity: {workout['activity']} (standardized)")
                print_info(f"Calories: {workout['calories']} (calculated)")
            else:
                print_fail(f"Expected status 201, got {response.status_code}")
        except Exception as e:
            print_fail(f"Error: {e}")

def verify_input_validation():
    """Verify input validation."""
    print_header("3. INPUT VALIDATION VERIFICATION")
    
    validation_tests = [
        {
            'name': 'Empty user_name',
            'data': {'user_name': '', 'activity': 'Running', 'duration': 30},
            'expected_status': 400,
            'expected_error': 'User name cannot be empty'
        },
        {
            'name': 'Empty activity',
            'data': {'user_name': 'Test User', 'activity': '', 'duration': 30},
            'expected_status': 400,
            'expected_error': 'Activity cannot be empty'
        },
        {
            'name': 'Duration = 0',
            'data': {'user_name': 'Test User', 'activity': 'Running', 'duration': 0},
            'expected_status': 400,
            'expected_error': 'Duration must be greater than 0'
        },
        {
            'name': 'Negative duration',
            'data': {'user_name': 'Test User', 'activity': 'Running', 'duration': -10},
            'expected_status': 400,
            'expected_error': 'Duration must be greater than 0'
        },
        {
            'name': 'Duration > 1440',
            'data': {'user_name': 'Test User', 'activity': 'Running', 'duration': 1500},
            'expected_status': 400,
            'expected_error': 'Duration cannot exceed 1440 minutes'
        },
        {
            'name': 'Missing user_name',
            'data': {'activity': 'Running', 'duration': 30},
            'expected_status': 422,
            'expected_error': None  # Pydantic validation error
        },
        {
            'name': 'Missing activity',
            'data': {'user_name': 'Test User', 'duration': 30},
            'expected_status': 422,
            'expected_error': None  # Pydantic validation error
        },
        {
            'name': 'Missing duration',
            'data': {'user_name': 'Test User', 'activity': 'Running'},
            'expected_status': 422,
            'expected_error': None  # Pydantic validation error
        },
    ]
    
    for test in validation_tests:
        print_test(test['name'])
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/workouts/",
                json=test['data'],
                timeout=5
            )
            
            if response.status_code == test['expected_status']:
                if test['expected_error']:
                    error_data = response.json()
                    # Check if error message is in the response
                    error_str = str(error_data).lower()
                    if test['expected_error'].lower() in error_str:
                        print_pass()
                    else:
                        print_fail(f"Expected error message containing '{test['expected_error']}', got: {error_data}")
                else:
                    print_pass()
            else:
                print_fail(f"Expected status {test['expected_status']}, got {response.status_code}")
        except Exception as e:
            print_fail(f"Error: {e}")

def verify_workout_retrieval():
    """Verify workout retrieval endpoint."""
    print_header("4. WORKOUT RETRIEVAL VERIFICATION")
    
    print_test("Get all workouts")
    try:
        response = requests.get(f"{BACKEND_URL}/api/workouts/", timeout=5)
        
        if response.status_code == 200:
            workouts = response.json()
            print_pass()
            print_info(f"Retrieved {len(workouts)} workout(s)")
            
            if workouts:
                # Verify ordering (most recent first)
                print_test("Workouts ordered by ID descending")
                if len(workouts) > 1:
                    is_ordered = all(workouts[i]['id'] >= workouts[i+1]['id'] for i in range(len(workouts)-1))
                    if is_ordered:
                        print_pass()
                    else:
                        print_fail("Workouts not ordered by ID descending")
                else:
                    print_pass("(only 1 workout, ordering N/A)")
        else:
            print_fail(f"Expected status 200, got {response.status_code}")
    except Exception as e:
        print_fail(f"Error: {e}")

# ============================================================================
# 2. FRONTEND VERIFICATION
# ============================================================================

def verify_frontend():
    """Verify frontend is accessible."""
    print_header("5. FRONTEND VERIFICATION")
    
    print_test("Frontend server is running")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_pass()
            print_info(f"Frontend accessible at {FRONTEND_URL}")
        else:
            print_fail(f"Frontend returned status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print_warning("Cannot connect to frontend server. Is it running on port 5173?")
        print_info("Frontend verification skipped")
        return False
    except Exception as e:
        print_fail(f"Error checking frontend: {e}")
        return False
    
    return True

# ============================================================================
# 3. SDK VERIFICATION
# ============================================================================

def verify_sdk():
    """Verify Python SDK functionality."""
    print_header("6. PYTHON SDK VERIFICATION")
    
    # Test 6.1: SDK imports
    print_test("SDK imports successfully")
    try:
        from openapi_client.api_client import ApiClient
        from openapi_client.configuration import Configuration
        from openapi_client.api.workouts_api import WorkoutsApi
        from openapi_client.models.workout_create import WorkoutCreate
        print_pass()
    except ImportError as e:
        print_fail(f"SDK import error: {e}")
        print_info("Run: cd fitness_sdk && pip install -e .")
        return False
    
    # Test 6.2: SDK configuration
    print_test("SDK configuration")
    try:
        config = Configuration()
        config.host = BACKEND_URL
        client = ApiClient(configuration=config)
        api = WorkoutsApi(api_client=client)
        print_pass()
    except Exception as e:
        print_fail(f"SDK configuration error: {e}")
        return False
    
    # Test 6.3: SDK can fetch workouts
    print_test("SDK can fetch workouts")
    try:
        workouts = api.get_workouts_api_workouts_get()
        print_pass()
        print_info(f"Fetched {len(workouts)} workout(s)")
    except Exception as e:
        print_fail(f"SDK fetch error: {e}")
    
    # Test 6.4: SDK can create workouts
    print_test("SDK can create workouts")
    try:
        new_workout = WorkoutCreate(
            user_name="SDK Test User",
            activity="Running",
            duration=25
        )
        created = api.create_workout_api_workouts_post(workout_create=new_workout)
        
        # Verify response
        if created.activity == 'running' and created.calories == 250:
            print_pass()
            print_info(f"Created workout ID: {created.id}")
            print_info(f"Activity: {created.activity} (standardized)")
            print_info(f"Calories: {created.calories} (calculated)")
        else:
            print_fail(f"Unexpected workout data: activity={created.activity}, calories={created.calories}")
    except Exception as e:
        print_fail(f"SDK create error: {e}")
    
    return True

# ============================================================================
# 4. INTEGRATION TESTS
# ============================================================================

def verify_integration():
    """Verify end-to-end integration."""
    print_header("7. INTEGRATION TESTS")
    
    # Test 7.1: Create via API, verify via SDK
    print_test("Create workout via API, verify via SDK")
    try:
        # Create via API
        api_data = {
            'user_name': 'Integration Test User',
            'activity': 'Cycling',
            'duration': 50
        }
        api_response = requests.post(
            f"{BACKEND_URL}/api/workouts/",
            json=api_data,
            timeout=5
        )
        
        if api_response.status_code != 201:
            print_fail(f"API creation failed with status {api_response.status_code}")
        else:
            created_workout = api_response.json()
            workout_id = created_workout['id']
            
            # Verify via SDK
            from openapi_client.api_client import ApiClient
            from openapi_client.configuration import Configuration
            from openapi_client.api.workouts_api import WorkoutsApi
            
            config = Configuration()
            config.host = BACKEND_URL
            client = ApiClient(configuration=config)
            api = WorkoutsApi(api_client=client)
            
            workouts = api.get_workouts_api_workouts_get()
            found = any(w.id == workout_id for w in workouts)
            
            if found:
                print_pass()
                print_info(f"Workout ID {workout_id} verified via SDK")
            else:
                print_fail(f"Workout ID {workout_id} not found via SDK")
    except Exception as e:
        print_fail(f"Integration test error: {e}")
    
    # Test 7.2: Create via SDK, verify via API
    print_test("Create workout via SDK, verify via API")
    try:
        from openapi_client.api_client import ApiClient
        from openapi_client.configuration import Configuration
        from openapi_client.api.workouts_api import WorkoutsApi
        from openapi_client.models.workout_create import WorkoutCreate
        
        config = Configuration()
        config.host = BACKEND_URL
        client = ApiClient(configuration=config)
        api = WorkoutsApi(api_client=client)
        
        # Create via SDK
        new_workout = WorkoutCreate(
            user_name="SDK Integration Test",
            activity="Walking",
            duration=35
        )
        created = api.create_workout_api_workouts_post(workout_create=new_workout)
        workout_id = created.id
        
        # Verify via API
        api_response = requests.get(f"{BACKEND_URL}/api/workouts/", timeout=5)
        if api_response.status_code == 200:
            workouts = api_response.json()
            found = any(w['id'] == workout_id for w in workouts)
            
            if found:
                print_pass()
                print_info(f"Workout ID {workout_id} verified via API")
            else:
                print_fail(f"Workout ID {workout_id} not found via API")
        else:
            print_fail(f"API verification failed with status {api_response.status_code}")
    except Exception as e:
        print_fail(f"Integration test error: {e}")

# ============================================================================
# 5. CALORIE CALCULATION VERIFICATION
# ============================================================================

def verify_calorie_calculations():
    """Verify calorie calculation accuracy."""
    print_header("8. CALORIE CALCULATION VERIFICATION")
    
    test_cases = [
        ('running', 1, 10),
        ('running', 45, 450),
        ('running', 100, 1000),
        ('cycling', 1, 8),
        ('cycling', 60, 480),
        ('cycling', 75, 600),
        ('walking', 1, 5),
        ('walking', 30, 150),
        ('walking', 120, 600),
        ('swimming', 1, 6),
        ('swimming', 40, 240),
        ('yoga', 50, 300),
    ]
    
    for activity, duration, expected_calories in test_cases:
        print_test(f"Calorie calculation: {activity} {duration}min = {expected_calories}cal")
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/workouts/",
                json={
                    'user_name': 'Calorie Test User',
                    'activity': activity,
                    'duration': duration
                },
                timeout=5
            )
            
            if response.status_code == 201:
                workout = response.json()
                if workout['calories'] == expected_calories:
                    print_pass()
                else:
                    print_fail(f"Expected {expected_calories}, got {workout['calories']}")
            else:
                print_fail(f"Request failed with status {response.status_code}")
        except Exception as e:
            print_fail(f"Error: {e}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def print_summary():
    """Print test summary."""
    print_header("VERIFICATION SUMMARY")
    
    total_tests = test_results['passed'] + test_results['failed']
    pass_rate = (test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"{Colors.GREEN}Passed: {test_results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed: {test_results['failed']}{Colors.END}")
    print(f"{Colors.YELLOW}Warnings: {test_results['warnings']}{Colors.END}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if test_results['issues']:
        print(f"\n{Colors.RED}{Colors.BOLD}Issues Found:{Colors.END}")
        for i, issue in enumerate(test_results['issues'], 1):
            print(f"  {i}. {issue}")
    
    print("\n" + "=" * 70)
    
    if test_results['failed'] == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED! System is fully working.{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED. Please review issues above.{Colors.END}")
    
    print("=" * 70 + "\n")

def main():
    """Main verification function."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("=" * 70)
    print("  FITNESS TRACKING APP - FULL SYSTEM VERIFICATION")
    print("=" * 70)
    print(f"{Colors.END}")
    print(f"\nBackend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"\nStarting verification...\n")
    
    time.sleep(1)
    
    # Run all verification tests
    backend_ok = verify_backend_health()
    
    if backend_ok:
        verify_workout_creation()
        verify_input_validation()
        verify_workout_retrieval()
        verify_calorie_calculations()
    
    verify_frontend()
    
    sdk_ok = verify_sdk()
    
    if backend_ok and sdk_ok:
        verify_integration()
    
    # Print summary
    print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if test_results['failed'] == 0 else 1)

if __name__ == "__main__":
    main()
