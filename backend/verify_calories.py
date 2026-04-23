"""
Verify calorie values in the database without modifying them.

This script checks if all workouts have correct calorie values based on:
- running: duration * 10 calories/min
- cycling: duration * 8 calories/min
- walking: duration * 5 calories/min
- others: duration * 6 calories/min

Usage:
    python verify_calories.py
"""

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


def verify_calories():
    """
    Verify calorie values for all workouts in the database.
    """
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("Verifying Calorie Values in Database")
        print("=" * 70)
        
        # Fetch all workouts
        workouts = db.query(Workout).all()
        
        if not workouts:
            print("\n✅ No workouts found in database.")
            return
        
        print(f"\nFound {len(workouts)} workout(s) in database.")
        print("\nChecking calorie values...\n")
        
        # Track statistics
        total_workouts = len(workouts)
        incorrect_count = 0
        correct_count = 0
        incorrect_workouts = []
        
        # Process each workout
        for workout in workouts:
            # Calculate correct calories
            correct_calories = calculate_calories(workout.activity, workout.duration)
            
            # Check if calories are correct
            if workout.calories != correct_calories:
                incorrect_count += 1
                incorrect_workouts.append({
                    'id': workout.id,
                    'user_name': workout.user_name,
                    'activity': workout.activity,
                    'duration': workout.duration,
                    'current_calories': workout.calories,
                    'correct_calories': correct_calories
                })
            else:
                correct_count += 1
        
        # Print results
        if incorrect_count == 0:
            print("=" * 70)
            print("✅ All calorie values are CORRECT!")
            print("=" * 70)
        else:
            print("=" * 70)
            print(f"⚠️  Found {incorrect_count} workout(s) with INCORRECT calorie values!")
            print("=" * 70)
            print("\nIncorrect workouts:\n")
            
            for workout in incorrect_workouts:
                print(f"❌ Workout ID {workout['id']}:")
                print(f"   User: {workout['user_name']}")
                print(f"   Activity: {workout['activity']}")
                print(f"   Duration: {workout['duration']} minutes")
                print(f"   Current Calories: {workout['current_calories']}")
                print(f"   Correct Calories: {workout['correct_calories']}")
                print(f"   Difference: {workout['correct_calories'] - workout['current_calories']}")
                print()
        
        # Print summary
        print("=" * 70)
        print("Summary:")
        print("=" * 70)
        print(f"  Total workouts: {total_workouts}")
        print(f"  Correct: {correct_count} ({correct_count * 100 // total_workouts}%)")
        print(f"  Incorrect: {incorrect_count} ({incorrect_count * 100 // total_workouts}%)")
        
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
        
        if incorrect_count > 0:
            print("\n" + "=" * 70)
            print("💡 To fix incorrect calorie values, run:")
            print("   python fix_calories.py")
            print("   or")
            print("   fix_calories.bat")
            print("=" * 70)
        
        print("\n" + "=" * 70)
        print("Verification Complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
    finally:
        db.close()


if __name__ == "__main__":
    verify_calories()
