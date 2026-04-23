"""
Unit tests for workout creation endpoint.

This module tests the POST /api/workouts endpoint for creating new workout sessions.

Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from app.database import Base, get_db
from app.models.user import User
from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_workout_creation.db"

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
    """Create a test user for workout creation."""
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


class TestWorkoutCreation:
    """Test workout creation endpoint."""
    
    def test_create_workout_with_valid_data(self, client, test_user):
        """
        Test creating a workout with valid data returns 201 and workout data.
        
        Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 45,
            "notes": "Morning cardio session"
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response structure (Requirement 4.1)
        assert "id" in data
        assert data["id"] > 0
        
        # Verify all fields are returned correctly (Requirements 4.2, 4.3, 4.4)
        assert data["user_id"] == test_user.id
        assert data["date"] == "2024-01-15"
        assert data["duration_minutes"] == 45
        assert data["notes"] == "Morning cardio session"
        
        # Verify exercises list is empty (Requirement 4.5)
        assert "exercises" in data
        assert data["exercises"] == []
    
    def test_create_workout_without_notes(self, client, test_user):
        """
        Test creating a workout without notes (optional field).
        
        Validates: Requirement 4.4
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 30
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["notes"] is None
        assert data["exercises"] == []
    
    def test_create_workout_with_empty_notes(self, client, test_user):
        """
        Test creating a workout with empty string notes.
        
        Validates: Requirement 4.4
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 30,
            "notes": ""
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["notes"] == ""
    
    def test_create_workout_with_nonexistent_user_id(self, client):
        """
        Test creating a workout with non-existent user_id returns 404.
        
        Validates: Requirements 4.2, 4.6
        """
        workout_data = {
            "user_id": 99999,  # Non-existent user
            "date": "2024-01-15",
            "duration_minutes": 45,
            "notes": "Test workout"
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 404
        data = response.json()
        
        assert "detail" in data
        assert "User with id 99999 not found" in data["detail"]
    
    def test_create_workout_with_zero_duration(self, client, test_user):
        """
        Test creating a workout with duration_minutes = 0 returns 422.
        
        Validates: Requirement 4.3
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 0,
            "notes": "Invalid workout"
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 422
        data = response.json()
        
        assert "detail" in data
    
    def test_create_workout_with_negative_duration(self, client, test_user):
        """
        Test creating a workout with negative duration_minutes returns 422.
        
        Validates: Requirement 4.3
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": -10,
            "notes": "Invalid workout"
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 422
        data = response.json()
        
        assert "detail" in data
    
    def test_create_workout_with_minimum_valid_duration(self, client, test_user):
        """
        Test creating a workout with duration_minutes = 1 (minimum valid).
        
        Validates: Requirement 4.3
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 1
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["duration_minutes"] == 1
    
    def test_create_workout_missing_user_id(self, client):
        """
        Test creating a workout without user_id returns 422.
        
        Validates: Requirement 4.2
        """
        workout_data = {
            "date": "2024-01-15",
            "duration_minutes": 45
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 422
    
    def test_create_workout_missing_date(self, client, test_user):
        """
        Test creating a workout without date returns 422.
        """
        workout_data = {
            "user_id": test_user.id,
            "duration_minutes": 45
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 422
    
    def test_create_workout_missing_duration(self, client, test_user):
        """
        Test creating a workout without duration_minutes returns 422.
        
        Validates: Requirement 4.3
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15"
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 422
    
    def test_create_workout_with_invalid_date_format(self, client, test_user):
        """
        Test creating a workout with invalid date format returns 422.
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "15-01-2024",  # Wrong format
            "duration_minutes": 45
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 422
    
    def test_create_multiple_workouts_for_same_user(self, client, test_user):
        """
        Test creating multiple workouts for the same user.
        
        Validates: Requirement 4.1 (unique IDs)
        """
        workout_data_1 = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 30
        }
        
        workout_data_2 = {
            "user_id": test_user.id,
            "date": "2024-01-16",
            "duration_minutes": 45
        }
        
        response1 = client.post("/api/workouts/", json=workout_data_1)
        response2 = client.post("/api/workouts/", json=workout_data_2)
        
        assert response1.status_code == 201
        assert response2.status_code == 201
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Verify unique IDs (Requirement 4.1)
        assert data1["id"] != data2["id"]
        assert data1["id"] > 0
        assert data2["id"] > 0
    
    def test_create_workout_persists_to_database(self, client, test_user, test_db):
        """
        Test that created workout is persisted to the database.
        
        Validates: Requirement 4.1
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 60,
            "notes": "Evening strength training"
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 201
        data = response.json()
        workout_id = data["id"]
        
        # Query database to verify persistence
        db_workout = test_db.query(Workout).filter(Workout.id == workout_id).first()
        
        assert db_workout is not None
        assert db_workout.user_id == test_user.id
        assert str(db_workout.date) == "2024-01-15"
        assert db_workout.duration_minutes == 60
        assert db_workout.notes == "Evening strength training"
    
    def test_create_workout_with_long_notes(self, client, test_user):
        """
        Test creating a workout with long notes text.
        
        Validates: Requirement 4.4
        """
        long_notes = "A" * 1000  # 1000 character notes
        
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 45,
            "notes": long_notes
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["notes"] == long_notes
    
    def test_create_workout_with_large_duration(self, client, test_user):
        """
        Test creating a workout with large duration value.
        
        Validates: Requirement 4.3
        """
        workout_data = {
            "user_id": test_user.id,
            "date": "2024-01-15",
            "duration_minutes": 480  # 8 hours
        }
        
        response = client.post("/api/workouts/", json=workout_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["duration_minutes"] == 480
