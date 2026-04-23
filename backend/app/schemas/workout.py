"""
Workout Pydantic schemas for the Fitness Tracking App.

This module defines Pydantic schemas for Workout data validation and serialization.
These schemas are used by FastAPI routes to validate incoming requests and
serialize responses.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class WorkoutBase(BaseModel):
    """
    Base Workout schema with common fields.
    
    Attributes:
        user_name: Name of the user performing the workout
        activity: Type of activity/exercise performed
        duration: Duration of the workout session in minutes (must be positive)
        calories: Calories burned during the workout (must be positive)
    """
    user_name: str = Field(..., min_length=1, max_length=100, description="Name of the user")
    activity: str = Field(..., min_length=1, max_length=100, description="Type of activity")
    duration: int = Field(..., gt=0, description="Duration in minutes (must be > 0)")
    calories: int = Field(..., gt=0, description="Calories burned (must be > 0)")


class WorkoutCreate(BaseModel):
    """
    Schema for creating a new workout.
    
    Calories are automatically calculated based on activity type and duration.
    
    Calorie Calculation Rules:
        - running: duration * 10 calories/min
        - cycling: duration * 8 calories/min
        - walking: duration * 5 calories/min
        - others: duration * 6 calories/min
    
    Validation Rules:
        - user_name must not be empty (1-100 characters)
        - activity must not be empty (1-100 characters)
        - duration must be a positive integer (> 0)
    """
    user_name: str = Field(..., min_length=1, max_length=100, description="Name of the user")
    activity: str = Field(..., min_length=1, max_length=100, description="Type of activity")
    duration: int = Field(..., gt=0, description="Duration in minutes (must be > 0)")


class WorkoutUpdate(BaseModel):
    """
    Schema for updating an existing workout.
    
    All fields are optional to allow partial updates.
    
    Attributes:
        user_name: Updated user name (optional)
        activity: Updated activity (optional)
        duration: Updated duration in minutes (optional, must be > 0 if provided)
        calories: Updated calories (optional, must be > 0 if provided)
    
    Validation Rules:
        - If user_name provided, must be 1-100 characters
        - If activity provided, must be 1-100 characters
        - If duration provided, must be a positive integer (> 0)
        - If calories provided, must be a positive integer (> 0)
        - All fields are optional for partial updates
    """
    user_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated user name")
    activity: Optional[str] = Field(None, min_length=1, max_length=100, description="Updated activity")
    duration: Optional[int] = Field(None, gt=0, description="Updated duration in minutes (must be > 0 if provided)")
    calories: Optional[int] = Field(None, gt=0, description="Updated calories (must be > 0 if provided)")


class WorkoutResponse(WorkoutBase):
    """
    Schema for workout API responses.
    
    Extends WorkoutBase with database fields. Used for serializing
    Workout model instances in API responses.
    
    Attributes:
        id: Unique workout identifier
    """
    id: int = Field(..., description="Unique workout identifier")
    
    model_config = ConfigDict(from_attributes=True)
