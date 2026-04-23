# WorkoutCreate

Schema for creating a new workout.  Calories are automatically calculated based on activity type and duration.  Calorie Calculation Rules:     - running: duration * 10 calories/min     - cycling: duration * 8 calories/min     - walking: duration * 5 calories/min     - others: duration * 6 calories/min  Validation Rules:     - user_name must not be empty (1-100 characters)     - activity must not be empty (1-100 characters)     - duration must be a positive integer (> 0)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_name** | **str** | Name of the user | 
**activity** | **str** | Type of activity | 
**duration** | **int** | Duration in minutes (must be &gt; 0) | 

## Example

```python
from openapi_client.models.workout_create import WorkoutCreate

# TODO update the JSON string below
json = "{}"
# create an instance of WorkoutCreate from a JSON string
workout_create_instance = WorkoutCreate.from_json(json)
# print the JSON string representation of the object
print(WorkoutCreate.to_json())

# convert the object into a dict
workout_create_dict = workout_create_instance.to_dict()
# create an instance of WorkoutCreate from a dict
workout_create_from_dict = WorkoutCreate.from_dict(workout_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


