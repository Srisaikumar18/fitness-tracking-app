"""
Script to recreate the database with only the workouts table.
Run this script to reset the database after refactoring.
"""

import os
import sys

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, engine

def recreate_database():
    """Drop all tables and recreate them based on current models."""
    print("Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully.")
    
    print("\nCreating new tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    
    print("\n✓ Database recreated with only workouts table!")
    print("  You can now start the application with: python -m app.main")

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE RECREATION SCRIPT")
    print("=" * 60)
    print("\nThis will delete ALL existing data and recreate the database")
    print("with only the workouts table (no users, no exercises).\n")
    
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        recreate_database()
    else:
        print("\nOperation cancelled.")
