# WorkoutResponse

Schema for workout API responses.  Extends WorkoutBase with database fields. Used for serializing Workout model instances in API responses.  Attributes:     id: Unique workout identifier

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_name** | **str** | Name of the user | 
**activity** | **str** | Type of activity | 
**duration** | **int** | Duration in minutes (must be &gt; 0) | 
**calories** | **int** | Calories burned (must be &gt; 0) | 
**id** | **int** | Unique workout identifier | 

## Example

```python
from openapi_client.models.workout_response import WorkoutResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WorkoutResponse from a JSON string
workout_response_instance = WorkoutResponse.from_json(json)
# print the JSON string representation of the object
print(WorkoutResponse.to_json())

# convert the object into a dict
workout_response_dict = workout_response_instance.to_dict()
# create an instance of WorkoutResponse from a dict
workout_response_from_dict = WorkoutResponse.from_dict(workout_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


