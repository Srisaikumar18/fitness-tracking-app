"""
Pydantic schemas package for the Fitness Tracking App.

This package contains all Pydantic schemas used for data validation
and serialization in the FastAPI application.
"""

from app.schemas.workout import (
    WorkoutBase,
    WorkoutCreate,
    WorkoutUpdate,
    WorkoutResponse
)

__all__ = [
    "WorkoutBase",
    "WorkoutCreate",
    "WorkoutUpdate",
    "WorkoutResponse",
]
