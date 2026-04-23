"""
Fix inconsistent calorie values in existing database.

This script recalculates calories for all existing workouts based on the correct rules:
- running: duration * 10 calories/min
- cycling: duration * 8 calories/min
- walking: duration * 5 calories/min
- others: duration * 6 calories/min

Usage:
    python fix_calories.py
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.workout import Workout

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness_tracker.db"

# Create engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def calculate_calories(activity: str, duration: int) -> int:
    """
    Calculate calories based on activity type and duration.
    
    Args:
        activity: Activity type (lowercase)
        duration: Duration in minutes
        
    Returns:
        Calculated calories
    """
    calorie_rates = {
        "running": 10,
        "cycling": 8,
        "walking": 5
    }
    
    # Get calorie rate for activity (default to 6 for unknown activities)
    calorie_rate = calorie_rates.get(activity.lower(), 6)
    
    return duration * calorie_rate


def fix_calories():
    """
    Fix calorie values for all workouts in the database.
    """
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("Fixing Calorie Values in Database")
        print("=" * 70)
        
        # Fetch all workouts
        workouts = db.query(Workout).all()
        
        if not workouts:
            print("\n✅ No workouts found in database. Nothing to fix.")
            return
        
        print(f"\nFound {len(workouts)} workout(s) in database.")
        print("\nAnalyzing workouts...\n")
        
        # Track statistics
        total_workouts = len(workouts)
        fixed_count = 0
        correct_count = 0
        
        # Process each workout
        for workout in workouts:
            # Calculate correct calories
            correct_calories = calculate_calories(workout.activity, workout.duration)
            
            # Check if calories need to be updated
            if workout.calories != correct_calories:
                print(f"❌ Workout ID {workout.id}:")
                print(f"   User: {workout.user_name}")
                print(f"   Activity: {workout.activity}")
                print(f"   Duration: {workout.duration} minutes")
                print(f"   Current Calories: {workout.calories}")
                print(f"   Correct Calories: {correct_calories}")
                print(f"   → Updating to {correct_calories}")
                print()
                
                # Update the workout
                workout.calories = correct_calories
                fixed_count += 1
            else:
                correct_count += 1
        
        # Commit all changes
        if fixed_count > 0:
            db.commit()
            print("=" * 70)
            print("✅ Database updated successfully!")
            print("=" * 70)
        else:
            print("=" * 70)
            print("✅ All calorie values are already correct!")
            print("=" * 70)
        
        # Print summary
        print(f"\nSummary:")
        print(f"  Total workouts: {total_workouts}")
        print(f"  Already correct: {correct_count}")
        print(f"  Fixed: {fixed_count}")
        
        # Show breakdown by activity
        print(f"\nBreakdown by activity:")
        activity_counts = {}
        for workout in workouts:
            activity = workout.activity
            if activity not in activity_counts:
                activity_counts[activity] = 0
            activity_counts[activity] += 1
        
        for activity, count in sorted(activity_counts.items()):
            calorie_rate = calculate_calories(activity, 1)
            print(f"  {activity}: {count} workout(s) ({calorie_rate} cal/min)")
        
        print("\n" + "=" * 70)
        print("Calorie Fix Complete!")
        print("=" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        print("Database changes have been rolled back.")
        sys.exit(1)
        
    finally:
        db.close()


if __name__ == "__main__":
    fix_calories()
