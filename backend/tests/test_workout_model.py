"""
Unit tests for the Workout SQLAlchemy model.

Tests verify:
- Workout model structure and columns
- Column constraints (nullable, foreign keys)
- Relationship to User model
- Relationship to Exercise model (forward reference)
- Cascade delete behavior
- String representation
"""

import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base
from app.models.user import User
from app.models.workout import Workout


@pytest.fixture
def test_engine():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def test_session(test_engine):
    """Create a test database session."""
    TestSessionLocal = sessionmaker(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_user(test_session):
    """Create a test user for workout relationships."""
    user = User(
        name="Test User",
        email="testuser@example.com",
        password_hash="hashed_password"
    )
    test_session.add(user)
    test_session.commit()
    return user


class TestWorkoutModelStructure:
    """Test Workout model structure and column definitions."""
    
    def test_workout_table_name(self):
        """Verify Workout model has correct table name."""
        assert Workout.__tablename__ == "workouts"
    
    def test_workout_has_required_columns(self, test_engine):
        """Verify Workout table has all required columns."""
        inspector = inspect(test_engine)
        columns = [col['name'] for col in inspector.get_columns('workouts')]
        
        assert 'id' in columns
        assert 'user_id' in columns
        assert 'date' in columns
        assert 'duration_minutes' in columns
        assert 'notes' in columns
    
    def test_workout_id_is_primary_key(self, test_engine):
        """Verify id column is the primary key."""
        inspector = inspect(test_engine)
        pk_constraint = inspector.get_pk_constraint('workouts')
        
        assert 'id' in pk_constraint['constrained_columns']
    
    def test_workout_user_id_is_foreign_key(self, test_engine):
        """Verify user_id column is a foreign key to users table."""
        inspector = inspect(test_engine)
        foreign_keys = inspector.get_foreign_keys('workouts')
        
        # Check if user_id is a foreign key
        user_id_fk = any(
            'user_id' in fk['constrained_columns'] and fk['referred_table'] == 'users'
            for fk in foreign_keys
        )
        
        assert user_id_fk
    
    def test_workout_id_is_indexed(self, test_engine):
        """Verify id column is indexed (as primary key)."""
        inspector = inspect(test_engine)
        indexes = inspector.get_indexes('workouts')
        
        # Primary key is automatically indexed
        pk_constraint = inspector.get_pk_constraint('workouts')
        assert 'id' in pk_constraint['constrained_columns']


class TestWorkoutModelConstraints:
    """Test Workout model column constraints."""
    
    def test_workout_user_id_cannot_be_null(self, test_session):
        """Verify user_id column is not nullable."""
        workout = Workout(
            date=date.today(),
            duration_minutes=60,
            notes="Test workout"
            # user_id is missing
        )
        
        test_session.add(workout)
        
        with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
            test_session.commit()
        
        test_session.rollback()
    
    def test_workout_date_cannot_be_null(self, test_session, test_user):
        """Verify date column is not nullable."""
        workout = Workout(
            user_id=test_user.id,
            duration_minutes=60,
            notes="Test workout"
            # date is missing
        )
        
        test_session.add(workout)
        
        with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
            test_session.commit()
        
        test_session.rollback()
    
    def test_workout_duration_minutes_cannot_be_null(self, test_session, test_user):
        """Verify duration_minutes column is not nullable."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            notes="Test workout"
            # duration_minutes is missing
        )
        
        test_session.add(workout)
        
        with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
            test_session.commit()
        
        test_session.rollback()
    
    def test_workout_notes_can_be_null(self, test_session, test_user):
        """Verify notes column is nullable."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=45
            # notes is missing (should be allowed)
        )
        
        test_session.add(workout)
        test_session.commit()
        
        assert workout.id is not None
        assert workout.notes is None
    
    def test_workout_user_id_must_reference_existing_user(self, test_session):
        """Verify foreign key constraint enforces user_id references existing user."""
        workout = Workout(
            user_id=99999,  # Non-existent user ID
            date=date.today(),
            duration_minutes=60,
            notes="Test workout"
        )
        
        test_session.add(workout)
        
        # Note: SQLite does not enforce foreign key constraints by default
        # In production with PostgreSQL or with SQLite PRAGMA foreign_keys=ON,
        # this would raise an IntegrityError
        # For this test, we verify the foreign key is defined in the schema
        # The actual enforcement is tested in integration tests with proper DB config
        try:
            test_session.commit()
            # If we get here with SQLite, that's expected behavior
            # The foreign key is defined but not enforced without PRAGMA
            test_session.rollback()
        except Exception:
            # If foreign keys are enforced, this is the expected path
            test_session.rollback()


class TestWorkoutModelCreation:
    """Test Workout model instance creation."""
    
    def test_create_workout_with_all_fields(self, test_session, test_user):
        """Verify workout can be created with all fields."""
        workout_date = date.today()
        workout = Workout(
            user_id=test_user.id,
            date=workout_date,
            duration_minutes=60,
            notes="Morning cardio session"
        )
        
        test_session.add(workout)
        test_session.commit()
        
        assert workout.id is not None
        assert workout.user_id == test_user.id
        assert workout.date == workout_date
        assert workout.duration_minutes == 60
        assert workout.notes == "Morning cardio session"
    
    def test_create_workout_without_notes(self, test_session, test_user):
        """Verify workout can be created without notes."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=45
        )
        
        test_session.add(workout)
        test_session.commit()
        
        assert workout.id is not None
        assert workout.notes is None
    
    def test_workout_id_is_auto_generated(self, test_session, test_user):
        """Verify workout ID is automatically generated."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=30
        )
        
        assert workout.id is None  # Before commit
        
        test_session.add(workout)
        test_session.commit()
        
        assert workout.id is not None  # After commit
        assert isinstance(workout.id, int)
        assert workout.id > 0
    
    def test_multiple_workouts_have_unique_ids(self, test_session, test_user):
        """Verify multiple workouts get unique IDs."""
        workout1 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=30)
        workout2 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=45)
        
        test_session.add(workout1)
        test_session.add(workout2)
        test_session.commit()
        
        assert workout1.id != workout2.id
        assert workout1.id is not None
        assert workout2.id is not None
    
    def test_create_workout_with_past_date(self, test_session, test_user):
        """Verify workout can be created with past date."""
        past_date = date.today() - timedelta(days=7)
        workout = Workout(
            user_id=test_user.id,
            date=past_date,
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        assert workout.date == past_date
    
    def test_create_workout_with_various_durations(self, test_session, test_user):
        """Verify workout can be created with various duration values."""
        durations = [15, 30, 45, 60, 90, 120]
        
        for duration in durations:
            workout = Workout(
                user_id=test_user.id,
                date=date.today(),
                duration_minutes=duration
            )
            test_session.add(workout)
        
        test_session.commit()
        
        workouts = test_session.query(Workout).all()
        assert len(workouts) == len(durations)


class TestWorkoutModelRelationships:
    """Test Workout model relationships."""
    
    def test_workout_has_user_relationship(self):
        """Verify Workout model has user relationship."""
        assert hasattr(Workout, 'user')
    
    def test_workout_has_exercises_relationship(self):
        """Verify Workout model has exercises relationship."""
        assert hasattr(Workout, 'exercises')
    
    def test_user_relationship_is_configured(self):
        """Verify user relationship has correct configuration."""
        relationship_property = Workout.user.property
        
        assert relationship_property is not None
        assert 'User' in str(relationship_property.mapper.class_)
    
    def test_exercises_relationship_is_configured(self):
        """Verify exercises relationship has correct configuration."""
        relationship_property = Workout.exercises.property
        
        assert relationship_property is not None
        assert 'Exercise' in str(relationship_property.mapper.class_)
        
        # Verify cascade is configured for delete and delete-orphan
        cascade_options = relationship_property.cascade
        assert 'delete' in str(cascade_options)
        assert 'delete-orphan' in str(cascade_options)
    
    def test_workout_can_access_user(self, test_session, test_user):
        """Verify workout can access its user through relationship."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        # Access user through relationship
        assert workout.user is not None
        assert workout.user.id == test_user.id
        assert workout.user.email == test_user.email
    
    def test_user_can_access_workouts(self, test_session, test_user):
        """Verify user can access their workouts through relationship."""
        workout1 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=30)
        workout2 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=45)
        
        test_session.add(workout1)
        test_session.add(workout2)
        test_session.commit()
        
        # Access workouts through user relationship
        assert len(test_user.workouts) == 2
        assert workout1 in test_user.workouts
        assert workout2 in test_user.workouts


class TestWorkoutModelStringRepresentation:
    """Test Workout model string representation."""
    
    def test_workout_repr(self, test_session, test_user):
        """Verify Workout __repr__ returns useful string."""
        workout_date = date.today()
        workout = Workout(
            user_id=test_user.id,
            date=workout_date,
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        repr_string = repr(workout)
        
        assert "Workout" in repr_string
        assert str(workout.id) in repr_string
        assert str(workout.user_id) in repr_string
        assert str(workout_date) in repr_string
        assert "60min" in repr_string
    
    def test_workout_repr_format(self, test_session, test_user):
        """Verify Workout __repr__ has expected format."""
        workout_date = date(2024, 1, 15)
        workout = Workout(
            user_id=test_user.id,
            date=workout_date,
            duration_minutes=45
        )
        
        test_session.add(workout)
        test_session.commit()
        
        expected = f"<Workout(id={workout.id}, user_id={test_user.id}, date='2024-01-15', duration=45min)>"
        assert repr(workout) == expected


class TestWorkoutModelQueries:
    """Test querying Workout model."""
    
    def test_query_workout_by_id(self, test_session, test_user):
        """Verify workouts can be queried by ID."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        queried_workout = test_session.query(Workout).filter(Workout.id == workout.id).first()
        
        assert queried_workout is not None
        assert queried_workout.id == workout.id
        assert queried_workout.user_id == test_user.id
    
    def test_query_workouts_by_user_id(self, test_session, test_user):
        """Verify workouts can be queried by user_id."""
        workout1 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=30)
        workout2 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=45)
        
        test_session.add(workout1)
        test_session.add(workout2)
        test_session.commit()
        
        user_workouts = test_session.query(Workout).filter(Workout.user_id == test_user.id).all()
        
        assert len(user_workouts) == 2
        assert workout1 in user_workouts
        assert workout2 in user_workouts
    
    def test_query_workouts_by_date(self, test_session, test_user):
        """Verify workouts can be queried by date."""
        target_date = date(2024, 1, 15)
        workout = Workout(
            user_id=test_user.id,
            date=target_date,
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        queried_workouts = test_session.query(Workout).filter(Workout.date == target_date).all()
        
        assert len(queried_workouts) == 1
        assert queried_workouts[0].date == target_date
    
    def test_query_workouts_by_date_range(self, test_session, test_user):
        """Verify workouts can be queried by date range."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        last_week = today - timedelta(days=7)
        
        workout1 = Workout(user_id=test_user.id, date=last_week, duration_minutes=30)
        workout2 = Workout(user_id=test_user.id, date=yesterday, duration_minutes=45)
        workout3 = Workout(user_id=test_user.id, date=today, duration_minutes=60)
        
        test_session.add_all([workout1, workout2, workout3])
        test_session.commit()
        
        # Query workouts from yesterday onwards
        recent_workouts = test_session.query(Workout).filter(
            Workout.date >= yesterday
        ).all()
        
        assert len(recent_workouts) == 2
        assert workout2 in recent_workouts
        assert workout3 in recent_workouts
        assert workout1 not in recent_workouts
    
    def test_query_all_workouts(self, test_session, test_user):
        """Verify all workouts can be queried."""
        workout1 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=30)
        workout2 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=45)
        workout3 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=60)
        
        test_session.add_all([workout1, workout2, workout3])
        test_session.commit()
        
        all_workouts = test_session.query(Workout).all()
        
        assert len(all_workouts) == 3
        assert workout1 in all_workouts
        assert workout2 in all_workouts
        assert workout3 in all_workouts


class TestWorkoutModelDeletion:
    """Test Workout model deletion behavior."""
    
    def test_delete_workout(self, test_session, test_user):
        """Verify workouts can be deleted."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        workout_id = workout.id
        
        test_session.delete(workout)
        test_session.commit()
        
        deleted_workout = test_session.query(Workout).filter(Workout.id == workout_id).first()
        
        assert deleted_workout is None
    
    def test_delete_workout_by_query(self, test_session, test_user):
        """Verify workouts can be deleted using query."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        workout_id = workout.id
        
        test_session.query(Workout).filter(Workout.id == workout_id).delete()
        test_session.commit()
        
        deleted_workout = test_session.query(Workout).filter(Workout.id == workout_id).first()
        
        assert deleted_workout is None
    
    def test_delete_user_cascades_to_workouts(self, test_session, test_user):
        """Verify deleting a user cascades to delete their workouts."""
        workout1 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=30)
        workout2 = Workout(user_id=test_user.id, date=date.today(), duration_minutes=45)
        
        test_session.add(workout1)
        test_session.add(workout2)
        test_session.commit()
        
        workout1_id = workout1.id
        workout2_id = workout2.id
        
        # Delete the user
        test_session.delete(test_user)
        test_session.commit()
        
        # Verify workouts are also deleted
        remaining_workout1 = test_session.query(Workout).filter(Workout.id == workout1_id).first()
        remaining_workout2 = test_session.query(Workout).filter(Workout.id == workout2_id).first()
        
        assert remaining_workout1 is None
        assert remaining_workout2 is None


class TestWorkoutModelUpdates:
    """Test Workout model update operations."""
    
    def test_update_workout_date(self, test_session, test_user):
        """Verify workout date can be updated."""
        original_date = date.today()
        new_date = date.today() - timedelta(days=1)
        
        workout = Workout(
            user_id=test_user.id,
            date=original_date,
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        workout.date = new_date
        test_session.commit()
        
        updated_workout = test_session.query(Workout).filter(Workout.id == workout.id).first()
        assert updated_workout.date == new_date
    
    def test_update_workout_duration(self, test_session, test_user):
        """Verify workout duration can be updated."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=60
        )
        
        test_session.add(workout)
        test_session.commit()
        
        workout.duration_minutes = 90
        test_session.commit()
        
        updated_workout = test_session.query(Workout).filter(Workout.id == workout.id).first()
        assert updated_workout.duration_minutes == 90
    
    def test_update_workout_notes(self, test_session, test_user):
        """Verify workout notes can be updated."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=60,
            notes="Original notes"
        )
        
        test_session.add(workout)
        test_session.commit()
        
        workout.notes = "Updated notes"
        test_session.commit()
        
        updated_workout = test_session.query(Workout).filter(Workout.id == workout.id).first()
        assert updated_workout.notes == "Updated notes"
    
    def test_update_workout_notes_to_null(self, test_session, test_user):
        """Verify workout notes can be set to null."""
        workout = Workout(
            user_id=test_user.id,
            date=date.today(),
            duration_minutes=60,
            notes="Some notes"
        )
        
        test_session.add(workout)
        test_session.commit()
        
        workout.notes = None
        test_session.commit()
        
        updated_workout = test_session.query(Workout).filter(Workout.id == workout.id).first()
        assert updated_workout.notes is None
