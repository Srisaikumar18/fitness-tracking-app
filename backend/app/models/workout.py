"""
Workout SQLAlchemy model for the Fitness Tracking App.

This module defines the Workout model representing fitness sessions.
"""

from sqlalchemy import Column, Integer, String
from app.database import Base


class Workout(Base):
    """
    Workout model representing a fitness session in the tracking system.
    
    Attributes:
        id: Unique identifier for the workout (primary key)
        user_name: Name of the user performing the workout
        activity: Type of activity/exercise performed
        duration: Duration of the workout session in minutes
        calories: Calories burned during the workout
    
    Validation Rules:
        - user_name must not be empty
        - activity must not be empty
        - duration must be a positive integer
        - calories must be a positive integer
    """
    
    __tablename__ = "workouts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Workout information
    user_name = Column(String(100), nullable=False)
    activity = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of Workout for debugging."""
        return f"<Workout(id={self.id}, user='{self.user_name}', activity='{self.activity}', duration={self.duration}min, calories={self.calories})>"
