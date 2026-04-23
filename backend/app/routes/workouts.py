"""
Workout management routes for the Fitness Tracking App.

This module provides API endpoints for workout session management including
creation and retrieval with comprehensive error handling.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from typing import List
import logging

from app.database import get_db
from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate, WorkoutResponse

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/workouts", tags=["Workouts"])


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)) -> WorkoutResponse:
    """
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
    """
    try:
        # Validate duration
        if workout.duration <= 0:
            logger.warning(f"Invalid duration provided: {workout.duration}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid input",
                    "message": "Duration must be greater than 0",
                    "field": "duration",
                    "value": workout.duration
                }
            )
        
        # Validate user_name is not empty after stripping
        if not workout.user_name or not workout.user_name.strip():
            logger.warning("Empty user_name provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid input",
                    "message": "User name cannot be empty",
                    "field": "user_name"
                }
            )
        
        # Validate activity is not empty after stripping
        if not workout.activity or not workout.activity.strip():
            logger.warning("Empty activity provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid input",
                    "message": "Activity cannot be empty",
                    "field": "activity"
                }
            )
        
        # Validate duration is reasonable (not too large)
        if workout.duration > 1440:  # 24 hours in minutes
            logger.warning(f"Unreasonably large duration provided: {workout.duration}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid input",
                    "message": "Duration cannot exceed 1440 minutes (24 hours)",
                    "field": "duration",
                    "value": workout.duration
                }
            )
        
        # Standardize activity to lowercase for consistency
        standardized_activity = workout.activity.strip().lower()
        
        # Validate activity length after standardization
        if len(standardized_activity) > 100:
            logger.warning(f"Activity name too long: {len(standardized_activity)} characters")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Invalid input",
                    "message": "Activity name cannot exceed 100 characters",
                    "field": "activity",
                    "length": len(standardized_activity)
                }
            )
        
        # Calculate calories based on activity type
        calorie_rates = {
            "running": 10,
            "cycling": 8,
            "walking": 5
        }
        
        # Get calorie rate for activity (default to 6 for others)
        calorie_rate = calorie_rates.get(standardized_activity, 6)
        calculated_calories = workout.duration * calorie_rate
        
        # Create workout record with standardized activity and calculated calories
        db_workout = Workout(
            user_name=workout.user_name.strip(),
            activity=standardized_activity,
            duration=workout.duration,
            calories=calculated_calories
        )
        
        # Persist to database with error handling
        try:
            db.add(db_workout)
            db.commit()
            db.refresh(db_workout)
            
            logger.info(f"Workout created successfully: ID={db_workout.id}, User={db_workout.user_name}, Activity={db_workout.activity}")
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Database integrity error",
                    "message": "Failed to create workout due to data constraint violation",
                    "hint": "Please check your input data"
                }
            )
        
        except OperationalError as e:
            db.rollback()
            logger.error(f"Database operational error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Database connection error",
                    "message": "Failed to connect to the database",
                    "hint": "Please try again later or contact support"
                }
            )
        
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error during workout creation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Database error",
                    "message": "An unexpected database error occurred while creating the workout",
                    "hint": "Please try again later"
                }
            )
        
        # Return workout response
        return WorkoutResponse.model_validate(db_workout)
    
    except HTTPException:
        # Re-raise HTTP exceptions (already handled)
        raise
    
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error during workout creation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred while processing your request",
                "hint": "Please try again later or contact support"
            }
        )


@router.get("/", response_model=List[WorkoutResponse])
async def get_workouts(db: Session = Depends(get_db)) -> List[WorkoutResponse]:
    """
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
    """
    try:
        # Query all workouts ordered by ID descending (most recent first)
        workouts = db.query(Workout).order_by(Workout.id.desc()).all()
        
        logger.info(f"Retrieved {len(workouts)} workouts successfully")
        
        # Convert to response models and return
        return [WorkoutResponse.model_validate(workout) for workout in workouts]
    
    except OperationalError as e:
        logger.error(f"Database operational error while retrieving workouts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Database connection error",
                "message": "Failed to connect to the database",
                "hint": "Please try again later or contact support"
            }
        )
    
    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving workouts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Database error",
                "message": "An unexpected database error occurred while retrieving workouts",
                "hint": "Please try again later"
            }
        )
    
    except Exception as e:
        logger.error(f"Unexpected error while retrieving workouts: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred while processing your request",
                "hint": "Please try again later or contact support"
            }
        )
