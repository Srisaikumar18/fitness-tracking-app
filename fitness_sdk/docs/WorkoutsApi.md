# openapi_client.WorkoutsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_workout_api_workouts_post**](WorkoutsApi.md#create_workout_api_workouts_post) | **POST** /api/workouts/ | Create Workout
[**get_workouts_api_workouts_get**](WorkoutsApi.md#get_workouts_api_workouts_get) | **GET** /api/workouts/ | Get Workouts


# **create_workout_api_workouts_post**
> WorkoutResponse create_workout_api_workouts_post(workout_create)

Create Workout

Create a new workout session.

This endpoint creates a new workout record with the provided user_name,
activity, and duration. Activity values are automatically standardized to 
lowercase for consistency, and calories are calculated based on activity type.

Calorie Calculation Rules:
    - running: duration * 10 calories/min
    - cycling: duration * 8 calories/min
    - walking: duration * 5 calories/min
    - others: duration * 6 calories/min

Args:
    workout: WorkoutCreate schema containing user_name, activity, and duration
    db: Database session (injected dependency)
    
Returns:
    WorkoutResponse: Created workout data with standardized activity and calculated calories
    
Raises:
    HTTPException 400: If input validation fails
    HTTPException 500: If database operation fails
    HTTPException 422: If Pydantic validation fails (automatic)
    
Example:
    POST /api/workouts/
    {
        "user_name": "John Doe",
        "activity": "Running",
        "duration": 45
    }
    
    Response 201:
    {
        "id": 1,
        "user_name": "John Doe",
        "activity": "running",
        "duration": 45,
        "calories": 450
    }

### Example


```python
import openapi_client
from openapi_client.models.workout_create import WorkoutCreate
from openapi_client.models.workout_response import WorkoutResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.WorkoutsApi(api_client)
    workout_create = openapi_client.WorkoutCreate() # WorkoutCreate | 

    try:
        # Create Workout
        api_response = api_instance.create_workout_api_workouts_post(workout_create)
        print("The response of WorkoutsApi->create_workout_api_workouts_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->create_workout_api_workouts_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workout_create** | [**WorkoutCreate**](WorkoutCreate.md)|  | 

### Return type

[**WorkoutResponse**](WorkoutResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workouts_api_workouts_get**
> List[WorkoutResponse] get_workouts_api_workouts_get()

Get Workouts

Retrieve all workouts.

This endpoint retrieves all workouts ordered by ID descending (most recent first).
Activities are returned in lowercase as stored in the database.

Args:
    db: Database session (injected dependency)
    
Returns:
    List[WorkoutResponse]: List of all workouts (may be empty)
    
Raises:
    HTTPException 500: If database operation fails
    
Example:
    GET /api/workouts/
    
    Response 200:
    [
        {
            "id": 2,
            "user_name": "Jane Smith",
            "activity": "cycling",
            "duration": 60,
            "calories": 480
        },
        {
            "id": 1,
            "user_name": "John Doe",
            "activity": "running",
            "duration": 45,
            "calories": 450
        }
    ]

### Example


```python
import openapi_client
from openapi_client.models.workout_response import WorkoutResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.WorkoutsApi(api_client)

    try:
        # Get Workouts
        api_response = api_instance.get_workouts_api_workouts_get()
        print("The response of WorkoutsApi->get_workouts_api_workouts_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkoutsApi->get_workouts_api_workouts_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[WorkoutResponse]**](WorkoutResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

