"""
Unit tests for workout modification and deletion endpoints.

This module tests the PUT /api/workouts/{workout_id} and DELETE /api/workouts/{workout_id}
endpoints for updating and deleting workout sessions.

Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from app.database import Base, get_db
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_workout_modification.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with database dependency override."""
    from app.routes.workouts import router
    from fastapi import FastAPI
    
    app = FastAPI()
    app.include_router(router)
    
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    return TestClient(app)


@pytest.fixture
def test_user(test_db):
    """Create a test user for workout operations."""
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def test_workout(test_db, test_user):
    """Create a test workout for modification and deletion tests."""
    workout = Workout(
        user_id=test_user.id,
        date=date(2024, 1, 15),
        duration_minutes=45,
        notes="Original workout notes"
    )
    test_db.add(workout)
    test_db.commit()
    test_db.refresh(workout)
    return workout


class TestWorkoutUpdate:
    """Test workout update endpoint."""
    
    def test_update_workout_all_fields(self, client, test_workout):
        """
        Test updating all workout fields returns updated data.
        
        Validates: Requirements 6.1, 6.2
        """
        update_data = {
            "date": "2024-01-20",
            "duration_minutes": 60,
            "notes": "Updated workout notes"
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all fields are updated (Requirements 6.1, 6.2)
        assert data["id"] == test_workout.id
        assert data["date"] == "2024-01-20"
        assert data["duration_minutes"] == 60
        assert data["notes"] == "Updated workout notes"
        assert data["user_id"] == test_workout.user_id
    
    def test_update_workout_partial_date_only(self, client, test_workout):
        """
        Test updating only the date field (partial update).
        
        Validates: Requirements 6.1, 6.2
        """
        update_data = {
            "date": "2024-01-25"
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify only date is updated, other fields remain unchanged
        assert data["date"] == "2024-01-25"
        assert data["duration_minutes"] == 45  # Original value
        assert data["notes"] == "Original workout notes"  # Original value
    
    def test_update_workout_partial_duration_only(self, client, test_workout):
        """
        Test updating only the duration_minutes field (partial update).
        
        Validates: Requirements 6.1, 6.2
        """
        update_data = {
            "duration_minutes": 90
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify only duration is updated
        assert data["duration_minutes"] == 90
        assert data["date"] == "2024-01-15"  # Original value
        assert data["notes"] == "Original workout notes"  # Original value
    
    def test_update_workout_partial_notes_only(self, client, test_workout):
        """
        Test updating only the notes field (partial update).
        
        Validates: Requirements 6.1, 6.2
        """
        update_data = {
            "notes": "New notes only"
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify only notes are updated
        assert data["notes"] == "New notes only"
        assert data["date"] == "2024-01-15"  # Original value
        assert data["duration_minutes"] == 45  # Original value
    
    def test_update_workout_clear_notes(self, client, test_workout):
        """
        Test clearing notes by setting to null.
        
        Validates: Requirements 6.1, 6.2
        """
        update_data = {
            "notes": None
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["notes"] is None
    
    def test_update_workout_nonexistent_id(self, client):
        """
        Test updating a non-existent workout returns 404.
        
        Validates: Requirement 6.3
        """
        update_data = {
            "duration_minutes": 60
        }
        
        response = client.put("/api/workouts/99999", json=update_data)
        
        assert response.status_code == 404
        data = response.json()
        
        assert "detail" in data
        assert "Workout with id 99999 not found" in data["detail"]
    
    def test_update_workout_invalid_duration_zero(self, client, test_workout):
        """
        Test updating workout with duration_minutes = 0 returns 422.
        
        Validates: Requirement 6.1 (validation)
        """
        update_data = {
            "duration_minutes": 0
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 422
    
    def test_update_workout_invalid_duration_negative(self, client, test_workout):
        """
        Test updating workout with negative duration_minutes returns 422.
        
        Validates: Requirement 6.1 (validation)
        """
        update_data = {
            "duration_minutes": -10
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 422
    
    def test_update_workout_invalid_date_format(self, client, test_workout):
        """
        Test updating workout with invalid date format returns 422.
        
        Validates: Requirement 6.1 (validation)
        """
        update_data = {
            "date": "15-01-2024"  # Wrong format
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 422
    
    def test_update_workout_persists_to_database(self, client, test_workout, test_db):
        """
        Test that workout updates are persisted to the database.
        
        Validates: Requirement 6.1
        """
        update_data = {
            "duration_minutes": 75,
            "notes": "Persisted update"
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        
        # Query database to verify persistence
        db_workout = test_db.query(Workout).filter(Workout.id == test_workout.id).first()
        
        assert db_workout is not None
        assert db_workout.duration_minutes == 75
        assert db_workout.notes == "Persisted update"
    
    def test_update_workout_with_exercises_included(self, client, test_workout, test_db):
        """
        Test that updating a workout returns exercises in response.
        
        Validates: Requirement 6.1 (response structure)
        """
        # Add an exercise to the workout
        exercise = Exercise(
            workout_id=test_workout.id,
            name="Bench Press",
            sets=3,
            reps=10,
            weight_kg=80.0
        )
        test_db.add(exercise)
        test_db.commit()
        
        update_data = {
            "duration_minutes": 50
        }
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify exercises are included in response
        assert "exercises" in data
        assert len(data["exercises"]) == 1
        assert data["exercises"][0]["name"] == "Bench Press"
    
    def test_update_workout_empty_body(self, client, test_workout):
        """
        Test updating workout with empty body (no changes).
        
        Validates: Requirement 6.1
        """
        update_data = {}
        
        response = client.put(f"/api/workouts/{test_workout.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify no fields changed
        assert data["date"] == "2024-01-15"
        assert data["duration_minutes"] == 45
        assert data["notes"] == "Original workout notes"


class TestWorkoutDeletion:
    """Test workout deletion endpoint."""
    
    def test_delete_workout_success(self, client, test_workout, test_db):
        """
        Test deleting a workout returns 204 and removes from database.
        
        Validates: Requirement 6.4
        """
        workout_id = test_workout.id
        
        response = client.delete(f"/api/workouts/{workout_id}")
        
        assert response.status_code == 204
        assert response.text == ""  # No content
        
        # Verify workout is deleted from database
        db_workout = test_db.query(Workout).filter(Workout.id == workout_id).first()
        assert db_workout is None
    
    def test_delete_workout_nonexistent_id(self, client):
        """
        Test deleting a non-existent workout returns 404.
        
        Validates: Requirement 6.6
        """
        response = client.delete("/api/workouts/99999")
        
        assert response.status_code == 404
        data = response.json()
        
        assert "detail" in data
        assert "Workout with id 99999 not found" in data["detail"]
    
    def test_delete_workout_cascade_deletes_exercises(self, client, test_workout, test_db):
        """
        Test deleting a workout also deletes all associated exercises.
        
        Validates: Requirement 6.5
        """
        # Add multiple exercises to the workout
        exercise1 = Exercise(
            workout_id=test_workout.id,
            name="Squats",
            sets=4,
            reps=12,
            weight_kg=100.0
        )
        exercise2 = Exercise(
            workout_id=test_workout.id,
            name="Deadlifts",
            sets=3,
            reps=8,
            weight_kg=120.0
        )
        exercise3 = Exercise(
            workout_id=test_workout.id,
            name="Running",
            duration_minutes=30
        )
        
        test_db.add_all([exercise1, exercise2, exercise3])
        test_db.commit()
        test_db.refresh(exercise1)
        test_db.refresh(exercise2)
        test_db.refresh(exercise3)
        
        exercise_ids = [exercise1.id, exercise2.id, exercise3.id]
        
        # Delete the workout
        response = client.delete(f"/api/workouts/{test_workout.id}")
        
        assert response.status_code == 204
        
        # Verify all exercises are deleted (cascade delete)
        for exercise_id in exercise_ids:
            db_exercise = test_db.query(Exercise).filter(Exercise.id == exercise_id).first()
            assert db_exercise is None, f"Exercise {exercise_id} should be deleted"
    
    def test_delete_workout_with_no_exercises(self, client, test_workout, test_db):
        """
        Test deleting a workout with no exercises.
        
        Validates: Requirement 6.4
        """
        workout_id = test_workout.id
        
        response = client.delete(f"/api/workouts/{workout_id}")
        
        assert response.status_code == 204
        
        # Verify workout is deleted
        db_workout = test_db.query(Workout).filter(Workout.id == workout_id).first()
        assert db_workout is None
    
    def test_delete_workout_does_not_affect_other_workouts(self, client, test_user, test_workout, test_db):
        """
        Test deleting a workout does not affect other workouts.
        
        Validates: Requirement 6.4
        """
        # Create another workout for the same user
        workout2 = Workout(
            user_id=test_user.id,
            date=date(2024, 1, 20),
            duration_minutes=60,
            notes="Second workout"
        )
        test_db.add(workout2)
        test_db.commit()
        test_db.refresh(workout2)
        
        # Delete the first workout
        response = client.delete(f"/api/workouts/{test_workout.id}")
        
        assert response.status_code == 204
        
        # Verify first workout is deleted
        db_workout1 = test_db.query(Workout).filter(Workout.id == test_workout.id).first()
        assert db_workout1 is None
        
        # Verify second workout still exists
        db_workout2 = test_db.query(Workout).filter(Workout.id == workout2.id).first()
        assert db_workout2 is not None
        assert db_workout2.notes == "Second workout"
    
    def test_delete_workout_twice_returns_404(self, client, test_workout):
        """
        Test deleting the same workout twice returns 404 on second attempt.
        
        Validates: Requirement 6.6
        """
        workout_id = test_workout.id
        
        # First deletion should succeed
        response1 = client.delete(f"/api/workouts/{workout_id}")
        assert response1.status_code == 204
        
        # Second deletion should return 404
        response2 = client.delete(f"/api/workouts/{workout_id}")
        assert response2.status_code == 404
        
        data = response2.json()
        assert "detail" in data
        assert f"Workout with id {workout_id} not found" in data["detail"]
    
    def test_delete_workout_cascade_only_deletes_own_exercises(self, client, test_user, test_workout, test_db):
        """
        Test that deleting a workout only deletes its own exercises, not exercises from other workouts.
        
        Validates: Requirement 6.5
        """
        # Create another workout
        workout2 = Workout(
            user_id=test_user.id,
            date=date(2024, 1, 20),
            duration_minutes=60
        )
        test_db.add(workout2)
        test_db.commit()
        test_db.refresh(workout2)
        
        # Add exercises to both workouts
        exercise1 = Exercise(
            workout_id=test_workout.id,
            name="Exercise for workout 1",
            sets=3,
            reps=10
        )
        exercise2 = Exercise(
            workout_id=workout2.id,
            name="Exercise for workout 2",
            sets=4,
            reps=12
        )
        
        test_db.add_all([exercise1, exercise2])
        test_db.commit()
        test_db.refresh(exercise1)
        test_db.refresh(exercise2)
        
        # Delete the first workout
        response = client.delete(f"/api/workouts/{test_workout.id}")
        
        assert response.status_code == 204
        
        # Verify exercise1 is deleted
        db_exercise1 = test_db.query(Exercise).filter(Exercise.id == exercise1.id).first()
        assert db_exercise1 is None
        
        # Verify exercise2 still exists
        db_exercise2 = test_db.query(Exercise).filter(Exercise.id == exercise2.id).first()
        assert db_exercise2 is not None
        assert db_exercise2.name == "Exercise for workout 2"
