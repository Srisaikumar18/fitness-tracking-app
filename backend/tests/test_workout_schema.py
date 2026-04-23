"""
Unit tests for Workout Pydantic schemas.

Tests validation rules for WorkoutBase, WorkoutCreate, WorkoutUpdate,
and WorkoutResponse schemas.
"""

import pytest
from datetime import date, timedelta
from pydantic import ValidationError
from app.schemas.workout import (
    WorkoutBase,
    WorkoutCreate,
    WorkoutUpdate,
    WorkoutResponse
)


class TestWorkoutBase:
    """Tests for WorkoutBase schema."""
    
    def test_valid_workout_base(self):
        """Test WorkoutBase with valid data."""
        workout = WorkoutBase(
            date=date(2024, 1, 15),
            duration_minutes=45,
            notes="Morning cardio session"
        )
        assert workout.date == date(2024, 1, 15)
        assert workout.duration_minutes == 45
        assert workout.notes == "Morning cardio session"
    
    def test_valid_workout_without_notes(self):
        """Test WorkoutBase without optional notes."""
        workout = WorkoutBase(
            date=date(2024, 1, 15),
            duration_minutes=30
        )
        assert workout.date == date(2024, 1, 15)
        assert workout.duration_minutes == 30
        assert workout.notes is None
    
    def test_duration_zero_fails(self):
        """Test that duration_minutes of 0 is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutBase(
                date=date(2024, 1, 15),
                duration_minutes=0
            )
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('duration_minutes',) for error in errors)
    
    def test_negative_duration_fails(self):
        """Test that negative duration_minutes is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutBase(
                date=date(2024, 1, 15),
                duration_minutes=-10
            )
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('duration_minutes',) for error in errors)
    
    def test_missing_date_fails(self):
        """Test that date is required."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutBase(duration_minutes=30)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('date',) for error in errors)
    
    def test_missing_duration_fails(self):
        """Test that duration_minutes is required."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutBase(date=date(2024, 1, 15))
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('duration_minutes',) for error in errors)
    
    def test_invalid_date_format_fails(self):
        """Test that invalid date format is rejected."""
        with pytest.raises(ValidationError):
            WorkoutBase(
                date="not-a-date",
                duration_minutes=30
            )


class TestWorkoutCreate:
    """Tests for WorkoutCreate schema."""
    
    def test_valid_workout_create(self):
        """Test WorkoutCreate with valid data."""
        workout = WorkoutCreate(
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=60,
            notes="Strength training"
        )
        assert workout.user_id == 1
        assert workout.date == date(2024, 1, 15)
        assert workout.duration_minutes == 60
        assert workout.notes == "Strength training"
    
    def test_valid_workout_create_without_notes(self):
        """Test WorkoutCreate without optional notes."""
        workout = WorkoutCreate(
            user_id=2,
            date=date(2024, 1, 15),
            duration_minutes=45
        )
        assert workout.user_id == 2
        assert workout.date == date(2024, 1, 15)
        assert workout.duration_minutes == 45
        assert workout.notes is None
    
    def test_missing_user_id_fails(self):
        """Test that user_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutCreate(
                date=date(2024, 1, 15),
                duration_minutes=30
            )
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('user_id',) for error in errors)
    
    def test_duration_must_be_positive(self):
        """Test that duration_minutes must be greater than 0."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutCreate(
                user_id=1,
                date=date(2024, 1, 15),
                duration_minutes=0
            )
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('duration_minutes',) for error in errors)
    
    def test_minimum_valid_duration(self):
        """Test that duration_minutes of 1 is accepted."""
        workout = WorkoutCreate(
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=1
        )
        assert workout.duration_minutes == 1


class TestWorkoutUpdate:
    """Tests for WorkoutUpdate schema."""
    
    def test_all_fields_optional(self):
        """Test that all fields are optional in WorkoutUpdate."""
        update = WorkoutUpdate()
        assert update.date is None
        assert update.duration_minutes is None
        assert update.notes is None
    
    def test_partial_update_date_only(self):
        """Test updating only date."""
        update = WorkoutUpdate(date=date(2024, 2, 1))
        assert update.date == date(2024, 2, 1)
        assert update.duration_minutes is None
        assert update.notes is None
    
    def test_partial_update_duration_only(self):
        """Test updating only duration_minutes."""
        update = WorkoutUpdate(duration_minutes=90)
        assert update.duration_minutes == 90
        assert update.date is None
        assert update.notes is None
    
    def test_partial_update_notes_only(self):
        """Test updating only notes."""
        update = WorkoutUpdate(notes="Updated notes")
        assert update.notes == "Updated notes"
        assert update.date is None
        assert update.duration_minutes is None
    
    def test_update_all_fields(self):
        """Test updating all fields."""
        update = WorkoutUpdate(
            date=date(2024, 3, 1),
            duration_minutes=120,
            notes="Full body workout"
        )
        assert update.date == date(2024, 3, 1)
        assert update.duration_minutes == 120
        assert update.notes == "Full body workout"
    
    def test_duration_zero_fails_when_provided(self):
        """Test that duration_minutes of 0 is rejected when provided."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutUpdate(duration_minutes=0)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('duration_minutes',) for error in errors)
    
    def test_negative_duration_fails_when_provided(self):
        """Test that negative duration_minutes is rejected when provided."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutUpdate(duration_minutes=-5)
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('duration_minutes',) for error in errors)
    
    def test_clear_notes_with_none(self):
        """Test that notes can be set to None to clear them."""
        update = WorkoutUpdate(notes=None)
        assert update.notes is None


class TestWorkoutResponse:
    """Tests for WorkoutResponse schema."""
    
    def test_valid_workout_response(self):
        """Test WorkoutResponse with valid data."""
        workout = WorkoutResponse(
            id=1,
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=45,
            notes="Morning run",
            exercises=[]
        )
        assert workout.id == 1
        assert workout.user_id == 1
        assert workout.date == date(2024, 1, 15)
        assert workout.duration_minutes == 45
        assert workout.notes == "Morning run"
        assert workout.exercises == []
    
    def test_workout_response_without_notes(self):
        """Test WorkoutResponse without notes."""
        workout = WorkoutResponse(
            id=2,
            user_id=3,
            date=date(2024, 1, 20),
            duration_minutes=30,
            exercises=[]
        )
        assert workout.id == 2
        assert workout.user_id == 3
        assert workout.notes is None
        assert workout.exercises == []
    
    def test_missing_id_fails(self):
        """Test that id is required."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutResponse(
                user_id=1,
                date=date(2024, 1, 15),
                duration_minutes=30,
                exercises=[]
            )
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('id',) for error in errors)
    
    def test_missing_user_id_fails(self):
        """Test that user_id is required."""
        with pytest.raises(ValidationError) as exc_info:
            WorkoutResponse(
                id=1,
                date=date(2024, 1, 15),
                duration_minutes=30,
                exercises=[]
            )
        
        errors = exc_info.value.errors()
        assert any(error['loc'] == ('user_id',) for error in errors)
    
    def test_exercises_defaults_to_empty_list(self):
        """Test that exercises defaults to empty list if not provided."""
        workout = WorkoutResponse(
            id=1,
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=30
        )
        assert workout.exercises == []
    
    def test_from_attributes_config(self):
        """Test that from_attributes is configured for ORM compatibility."""
        assert WorkoutResponse.model_config['from_attributes'] is True


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_duration_exactly_one_minute(self):
        """Test that duration_minutes of exactly 1 is accepted."""
        workout = WorkoutCreate(
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=1
        )
        assert workout.duration_minutes == 1
    
    def test_very_long_duration(self):
        """Test that very long duration is accepted."""
        workout = WorkoutCreate(
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=1440  # 24 hours
        )
        assert workout.duration_minutes == 1440
    
    def test_date_in_past(self):
        """Test that past dates are accepted."""
        past_date = date.today() - timedelta(days=365)
        workout = WorkoutCreate(
            user_id=1,
            date=past_date,
            duration_minutes=30
        )
        assert workout.date == past_date
    
    def test_date_today(self):
        """Test that today's date is accepted."""
        today = date.today()
        workout = WorkoutCreate(
            user_id=1,
            date=today,
            duration_minutes=30
        )
        assert workout.date == today
    
    def test_date_in_future(self):
        """Test that future dates are accepted (validation at application level)."""
        future_date = date.today() + timedelta(days=30)
        workout = WorkoutCreate(
            user_id=1,
            date=future_date,
            duration_minutes=30
        )
        assert workout.date == future_date
    
    def test_empty_notes_string(self):
        """Test that empty string for notes is accepted."""
        workout = WorkoutCreate(
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=30,
            notes=""
        )
        assert workout.notes == ""
    
    def test_very_long_notes(self):
        """Test that very long notes are accepted."""
        long_notes = "a" * 10000
        workout = WorkoutCreate(
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=30,
            notes=long_notes
        )
        assert len(workout.notes) == 10000
    
    def test_notes_with_special_characters(self):
        """Test that notes with special characters are accepted."""
        special_notes = "Workout with émojis 💪 and symbols: @#$%^&*()"
        workout = WorkoutCreate(
            user_id=1,
            date=date(2024, 1, 15),
            duration_minutes=30,
            notes=special_notes
        )
        assert workout.notes == special_notes
    
    def test_user_id_zero(self):
        """Test that user_id of 0 is accepted (validation at application level)."""
        workout = WorkoutCreate(
            user_id=0,
            date=date(2024, 1, 15),
            duration_minutes=30
        )
        assert workout.user_id == 0
    
    def test_negative_user_id(self):
        """Test that negative user_id is accepted (validation at application level)."""
        workout = WorkoutCreate(
            user_id=-1,
            date=date(2024, 1, 15),
            duration_minutes=30
        )
        assert workout.user_id == -1


class TestDateValidation:
    """Tests specifically for date field validation."""
    
    def test_date_string_format_iso(self):
        """Test that ISO date string is accepted and converted."""
        workout = WorkoutCreate(
            user_id=1,
            date="2024-01-15",
            duration_minutes=30
        )
        assert workout.date == date(2024, 1, 15)
    
    def test_invalid_date_string_fails(self):
        """Test that invalid date string is rejected."""
        with pytest.raises(ValidationError):
            WorkoutCreate(
                user_id=1,
                date="15-01-2024",  # Wrong format
                duration_minutes=30
            )
    
    def test_date_object_accepted(self):
        """Test that date object is accepted."""
        workout_date = date(2024, 1, 15)
        workout = WorkoutCreate(
            user_id=1,
            date=workout_date,
            duration_minutes=30
        )
        assert workout.date == workout_date
