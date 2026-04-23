"""
Unit tests for workout retrieval endpoints.

This module tests the GET /api/workouts and GET /api/workouts/{workout_id} endpoints
to ensure proper filtering, ordering, and error handling.

Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7
"""

import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.database import Base, get_db
from app.routes.workouts import router
from app.models.user import User
from app.models.workout import Workout
from app.models.exercise import Exercise


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_workout_retrieval.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency."""
    app = FastAPI()
    app.include_router(router)
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    return TestClient(app)


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def another_user(db_session):
    """Create another user for testing user isolation."""
    user = User(
        name="Another User",
        email="another@example.com",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_workouts(db_session, sample_user):
    """Create sample workouts with different dates."""
    today = date.today()
    
    workouts = [
        Workout(
            user_id=sample_user.id,
            date=today - timedelta(days=10),
            duration_minutes=30,
            notes="Old workout"
        ),
        Workout(
            user_id=sample_user.id,
            date=today - timedelta(days=5),
            duration_minutes=45,
            notes="Mid workout"
        ),
        Workout(
            user_id=sample_user.id,
            date=today,
            duration_minutes=60,
            notes="Recent workout"
        ),
    ]
    
    for workout in workouts:
        db_session.add(workout)
    
    db_session.commit()
    
    for workout in workouts:
        db_session.refresh(workout)
    
    return workouts


@pytest.fixture
def workouts_with_exercises(db_session, sample_user):
    """Create workouts with associated exercises."""
    workout1 = Workout(
        user_id=sample_user.id,
        date=date.today(),
        duration_minutes=60,
        notes="Strength training"
    )
    db_session.add(workout1)
    db_session.commit()
    db_session.refresh(workout1)
    
    # Add exercises to workout1
    exercises = [
        Exercise(
            workout_id=workout1.id,
            name="Bench Press",
            sets=3,
            reps=10,
            weight_kg=80.0
        ),
        Exercise(
            workout_id=workout1.id,
            name="Squats",
            sets=4,
            reps=8,
            weight_kg=100.0
        ),
    ]
    
    for exercise in exercises:
        db_session.add(exercise)
    
    db_session.commit()
    
    for exercise in exercises:
        db_session.refresh(exercise)
    
    return workout1, exercises


# Test GET /api/workouts endpoint

def test_get_workouts_by_user_id(client, sample_workouts):
    """
    Test retrieving all workouts for a specific user.
    
    Requirement 5.1: Return only workouts belonging to specified user_id
    """
    user_id = sample_workouts[0].user_id
    
    response = client.get(f"/api/workouts?user_id={user_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return all 3 workouts
    assert len(data) == 3
    
    # All workouts should belong to the specified user
    for workout in data:
        assert workout["user_id"] == user_id


def test_get_workouts_ordered_by_date_descending(client, sample_workouts):
    """
    Test that workouts are ordered by date descending (most recent first).
    
    Requirement 5.5: Order results by date descending
    """
    user_id = sample_workouts[0].user_id
    
    response = client.get(f"/api/workouts?user_id={user_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify ordering: most recent first
    assert data[0]["notes"] == "Recent workout"
    assert data[1]["notes"] == "Mid workout"
    assert data[2]["notes"] == "Old workout"
    
    # Verify dates are in descending order
    dates = [workout["date"] for workout in data]
    assert dates == sorted(dates, reverse=True)


def test_get_workouts_with_start_date_filter(client, sample_workouts):
    """
    Test filtering workouts by start_date (inclusive).
    
    Requirement 5.2: Apply start_date filter (date >= start_date)
    """
    user_id = sample_workouts[0].user_id
    start_date = date.today() - timedelta(days=6)
    
    response = client.get(f"/api/workouts?user_id={user_id}&start_date={start_date}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return only workouts from the last 6 days (2 workouts)
    assert len(data) == 2
    assert data[0]["notes"] == "Recent workout"
    assert data[1]["notes"] == "Mid workout"
    
    # Verify all dates are >= start_date
    for workout in data:
        workout_date = date.fromisoformat(workout["date"])
        assert workout_date >= start_date


def test_get_workouts_with_end_date_filter(client, sample_workouts):
    """
    Test filtering workouts by end_date (inclusive).
    
    Requirement 5.3: Apply end_date filter (date <= end_date)
    """
    user_id = sample_workouts[0].user_id
    end_date = date.today() - timedelta(days=6)
    
    response = client.get(f"/api/workouts?user_id={user_id}&end_date={end_date}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return only the old workout
    assert len(data) == 1
    assert data[0]["notes"] == "Old workout"
    
    # Verify all dates are <= end_date
    for workout in data:
        workout_date = date.fromisoformat(workout["date"])
        assert workout_date <= end_date


def test_get_workouts_with_date_range_filter(client, sample_workouts):
    """
    Test filtering workouts by both start_date and end_date.
    
    Requirements 5.2, 5.3: Apply both date filters
    """
    user_id = sample_workouts[0].user_id
    start_date = date.today() - timedelta(days=8)
    end_date = date.today() - timedelta(days=3)
    
    response = client.get(
        f"/api/workouts?user_id={user_id}&start_date={start_date}&end_date={end_date}"
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should return only the mid workout
    assert len(data) == 1
    assert data[0]["notes"] == "Mid workout"
    
    # Verify date is within range
    workout_date = date.fromisoformat(data[0]["date"])
    assert start_date <= workout_date <= end_date


def test_get_workouts_includes_exercises(client, workouts_with_exercises):
    """
    Test that retrieved workouts include associated exercises.
    
    Requirement 5.4: Include all associated exercises for each workout
    """
    workout, exercises = workouts_with_exercises
    
    response = client.get(f"/api/workouts?user_id={workout.user_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    workout_data = data[0]
    
    # Verify exercises are included
    assert "exercises" in workout_data
    assert len(workout_data["exercises"]) == 2
    
    # Verify exercise details
    exercise_names = [ex["name"] for ex in workout_data["exercises"]]
    assert "Bench Press" in exercise_names
    assert "Squats" in exercise_names


def test_get_workouts_empty_result(client, sample_user):
    """
    Test retrieving workouts when user has no workouts.
    
    Should return empty list, not an error.
    """
    response = client.get(f"/api/workouts?user_id={sample_user.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data == []


def test_get_workouts_user_isolation(client, sample_workouts, another_user, db_session):
    """
    Test that users can only see their own workouts.
    
    Requirement 5.1: Return only workouts belonging to specified user_id
    """
    # Create a workout for another user
    other_workout = Workout(
        user_id=another_user.id,
        date=date.today(),
        duration_minutes=30,
        notes="Other user's workout"
    )
    db_session.add(other_workout)
    db_session.commit()
    
    # Query for first user's workouts
    user_id = sample_workouts[0].user_id
    response = client.get(f"/api/workouts?user_id={user_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Should only return first user's workouts
    assert len(data) == 3
    for workout in data:
        assert workout["user_id"] == user_id
        assert workout["notes"] != "Other user's workout"


def test_get_workouts_missing_user_id(client):
    """
    Test that user_id query parameter is required.
    """
    response = client.get("/api/workouts")
    
    # Should return 422 validation error
    assert response.status_code == 422


# Test GET /api/workouts/{workout_id} endpoint

def test_get_workout_by_id(client, sample_workouts):
    """
    Test retrieving a specific workout by ID.
    
    Requirement 5.6: Return workout with all associated exercises
    """
    workout = sample_workouts[0]
    
    response = client.get(f"/api/workouts/{workout.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == workout.id
    assert data["user_id"] == workout.user_id
    assert data["date"] == str(workout.date)
    assert data["duration_minutes"] == workout.duration_minutes
    assert data["notes"] == workout.notes
    assert "exercises" in data


def test_get_workout_with_exercises(client, workouts_with_exercises):
    """
    Test that single workout retrieval includes exercises.
    
    Requirement 5.6: Return workout with all associated exercises
    """
    workout, exercises = workouts_with_exercises
    
    response = client.get(f"/api/workouts/{workout.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify exercises are included
    assert len(data["exercises"]) == 2
    
    # Verify exercise details
    exercise_names = [ex["name"] for ex in data["exercises"]]
    assert "Bench Press" in exercise_names
    assert "Squats" in exercise_names
    
    # Verify exercise data integrity
    bench_press = next(ex for ex in data["exercises"] if ex["name"] == "Bench Press")
    assert bench_press["sets"] == 3
    assert bench_press["reps"] == 10
    assert bench_press["weight_kg"] == 80.0


def test_get_workout_not_found(client):
    """
    Test retrieving a non-existent workout returns 404.
    
    Requirement 5.7: Return 404 if workout does not exist
    """
    non_existent_id = 99999
    
    response = client.get(f"/api/workouts/{non_existent_id}")
    
    assert response.status_code == 404
    data = response.json()
    
    assert "detail" in data
    assert f"Workout with id {non_existent_id} not found" in data["detail"]


def test_get_workout_with_empty_exercises(client, sample_workouts):
    """
    Test retrieving a workout with no exercises.
    
    Should return empty exercises list.
    """
    workout = sample_workouts[0]
    
    response = client.get(f"/api/workouts/{workout.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["exercises"] == []


# Edge case tests

def test_get_workouts_with_same_date(client, sample_user, db_session):
    """
    Test retrieving workouts when multiple workouts have the same date.
    
    Should return all workouts for that date.
    """
    same_date = date.today()
    
    workouts = [
        Workout(user_id=sample_user.id, date=same_date, duration_minutes=30, notes="Morning"),
        Workout(user_id=sample_user.id, date=same_date, duration_minutes=45, notes="Evening"),
    ]
    
    for workout in workouts:
        db_session.add(workout)
    db_session.commit()
    
    response = client.get(f"/api/workouts?user_id={sample_user.id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert all(w["date"] == str(same_date) for w in data)


def test_get_workouts_boundary_dates(client, sample_user, db_session):
    """
    Test date filtering with boundary conditions (exact match on start/end dates).
    
    Requirements 5.2, 5.3: Filters should be inclusive
    """
    target_date = date.today()
    
    workout = Workout(
        user_id=sample_user.id,
        date=target_date,
        duration_minutes=30,
        notes="Boundary test"
    )
    db_session.add(workout)
    db_session.commit()
    
    # Test with start_date equal to workout date
    response = client.get(f"/api/workouts?user_id={sample_user.id}&start_date={target_date}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # Test with end_date equal to workout date
    response = client.get(f"/api/workouts?user_id={sample_user.id}&end_date={target_date}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # Test with both dates equal to workout date
    response = client.get(
        f"/api/workouts?user_id={sample_user.id}&start_date={target_date}&end_date={target_date}"
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
