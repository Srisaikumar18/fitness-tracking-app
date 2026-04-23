"""
Integration tests for workout retrieval endpoints.

This module tests the complete workflow of creating and retrieving workouts
with exercises to ensure all components work together correctly.

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


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_workout_retrieval_integration.db"
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
def test_user(db_session):
    """Create a test user."""
    user = User(
        name="Integration Test User",
        email="integration@example.com",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_complete_workout_workflow(client, test_user):
    """
    Test complete workflow: create multiple workouts and retrieve them.
    
    This integration test verifies:
    - Creating multiple workouts
    - Retrieving all workouts for a user
    - Retrieving specific workout by ID
    - Date filtering
    - Ordering by date descending
    """
    today = date.today()
    
    # Step 1: Create three workouts on different dates
    workout1_data = {
        "user_id": test_user.id,
        "date": str(today - timedelta(days=7)),
        "duration_minutes": 30,
        "notes": "Week old workout"
    }
    
    workout2_data = {
        "user_id": test_user.id,
        "date": str(today - timedelta(days=3)),
        "duration_minutes": 45,
        "notes": "Recent workout"
    }
    
    workout3_data = {
        "user_id": test_user.id,
        "date": str(today),
        "duration_minutes": 60,
        "notes": "Today's workout"
    }
    
    response1 = client.post("/api/workouts/", json=workout1_data)
    response2 = client.post("/api/workouts/", json=workout2_data)
    response3 = client.post("/api/workouts/", json=workout3_data)
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201
    
    workout1_id = response1.json()["id"]
    workout2_id = response2.json()["id"]
    workout3_id = response3.json()["id"]
    
    # Step 2: Retrieve all workouts for the user
    response = client.get(f"/api/workouts?user_id={test_user.id}")
    
    assert response.status_code == 200
    all_workouts = response.json()
    
    assert len(all_workouts) == 3
    
    # Verify ordering (most recent first)
    assert all_workouts[0]["notes"] == "Today's workout"
    assert all_workouts[1]["notes"] == "Recent workout"
    assert all_workouts[2]["notes"] == "Week old workout"
    
    # Step 3: Retrieve specific workout by ID
    response = client.get(f"/api/workouts/{workout2_id}")
    
    assert response.status_code == 200
    workout_detail = response.json()
    
    assert workout_detail["id"] == workout2_id
    assert workout_detail["notes"] == "Recent workout"
    assert workout_detail["duration_minutes"] == 45
    
    # Step 4: Test date filtering - get workouts from last 5 days
    start_date = today - timedelta(days=5)
    response = client.get(f"/api/workouts?user_id={test_user.id}&start_date={start_date}")
    
    assert response.status_code == 200
    filtered_workouts = response.json()
    
    assert len(filtered_workouts) == 2
    assert filtered_workouts[0]["notes"] == "Today's workout"
    assert filtered_workouts[1]["notes"] == "Recent workout"
    
    # Step 5: Test date range filtering
    end_date = today - timedelta(days=2)
    response = client.get(
        f"/api/workouts?user_id={test_user.id}&start_date={start_date}&end_date={end_date}"
    )
    
    assert response.status_code == 200
    range_workouts = response.json()
    
    assert len(range_workouts) == 1
    assert range_workouts[0]["notes"] == "Recent workout"


def test_workout_not_found_after_creation(client, test_user):
    """
    Test that retrieving a non-existent workout returns 404,
    even after successfully creating other workouts.
    """
    # Create a workout
    workout_data = {
        "user_id": test_user.id,
        "date": str(date.today()),
        "duration_minutes": 30,
        "notes": "Test workout"
    }
    
    response = client.post("/api/workouts/", json=workout_data)
    assert response.status_code == 201
    
    created_id = response.json()["id"]
    
    # Try to retrieve a non-existent workout
    non_existent_id = created_id + 1000
    response = client.get(f"/api/workouts/{non_existent_id}")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_empty_workout_list_for_new_user(client, test_user):
    """
    Test that a new user with no workouts gets an empty list.
    """
    response = client.get(f"/api/workouts?user_id={test_user.id}")
    
    assert response.status_code == 200
    workouts = response.json()
    
    assert workouts == []


def test_date_filtering_with_no_matches(client, test_user):
    """
    Test date filtering that returns no results.
    """
    # Create a workout today
    workout_data = {
        "user_id": test_user.id,
        "date": str(date.today()),
        "duration_minutes": 30,
        "notes": "Today's workout"
    }
    
    response = client.post("/api/workouts/", json=workout_data)
    assert response.status_code == 201
    
    # Query for workouts from next week (should be empty)
    future_date = date.today() + timedelta(days=7)
    response = client.get(f"/api/workouts?user_id={test_user.id}&start_date={future_date}")
    
    assert response.status_code == 200
    workouts = response.json()
    
    assert workouts == []


def test_multiple_users_workout_isolation(client, db_session):
    """
    Test that workouts are properly isolated between users.
    """
    # Create two users
    user1 = User(name="User 1", email="user1@example.com", password_hash="hash1")
    user2 = User(name="User 2", email="user2@example.com", password_hash="hash2")
    
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)
    
    # Create workouts for both users
    workout1_data = {
        "user_id": user1.id,
        "date": str(date.today()),
        "duration_minutes": 30,
        "notes": "User 1 workout"
    }
    
    workout2_data = {
        "user_id": user2.id,
        "date": str(date.today()),
        "duration_minutes": 45,
        "notes": "User 2 workout"
    }
    
    client.post("/api/workouts/", json=workout1_data)
    client.post("/api/workouts/", json=workout2_data)
    
    # Retrieve workouts for user 1
    response = client.get(f"/api/workouts?user_id={user1.id}")
    assert response.status_code == 200
    user1_workouts = response.json()
    
    assert len(user1_workouts) == 1
    assert user1_workouts[0]["notes"] == "User 1 workout"
    
    # Retrieve workouts for user 2
    response = client.get(f"/api/workouts?user_id={user2.id}")
    assert response.status_code == 200
    user2_workouts = response.json()
    
    assert len(user2_workouts) == 1
    assert user2_workouts[0]["notes"] == "User 2 workout"
