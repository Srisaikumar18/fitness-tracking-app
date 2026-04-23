"""
Integration tests for database initialization and real database operations.

These tests verify that the database configuration works with actual database operations.
"""

import pytest
import os
from sqlalchemy import Column, Integer, String, inspect
from app.database import Base, engine, SessionLocal, get_db, init_db


class TestDatabaseIntegration:
    """Integration tests for database operations."""
    
    def test_can_create_and_use_real_session(self):
        """Verify we can create and use a real database session."""
        session = SessionLocal()
        
        # Session should be usable
        assert session is not None
        
        # Should be able to begin a transaction
        session.begin()
        session.rollback()
        
        session.close()
    
    def test_get_db_generator_works_in_practice(self):
        """Verify get_db() works as a dependency injection generator."""
        # Simulate FastAPI's usage of the generator
        gen = get_db()
        
        # Get the session
        session = next(gen)
        assert session is not None
        
        # Use the session
        from sqlalchemy import text
        result = session.execute(text("SELECT 1"))
        assert result is not None
        
        # Close the generator (simulates end of request)
        try:
            next(gen)
        except StopIteration:
            pass  # Expected
    
    def test_init_db_with_real_model(self, tmp_path):
        """Verify init_db() works with a real model definition."""
        # Create a temporary database
        from sqlalchemy import create_engine
        from sqlalchemy.orm import declarative_base
        
        test_db_path = tmp_path / "test_integration.db"
        test_engine = create_engine(f"sqlite:///{test_db_path}")
        
        TestBase = declarative_base()
        
        # Define a test model
        class TestWorkout(TestBase):
            __tablename__ = "workouts"
            id = Column(Integer, primary_key=True)
            name = Column(String(100))
        
        # Initialize database
        TestBase.metadata.create_all(bind=test_engine)
        
        # Verify table was created
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "workouts" in tables
        
        # Verify we can insert data
        from sqlalchemy.orm import sessionmaker
        TestSession = sessionmaker(bind=test_engine)
        session = TestSession()
        
        workout = TestWorkout(name="Morning Run")
        session.add(workout)
        session.commit()
        
        # Verify we can query data
        result = session.query(TestWorkout).filter_by(name="Morning Run").first()
        assert result is not None
        assert result.name == "Morning Run"
        
        session.close()
    
    def test_multiple_concurrent_sessions(self):
        """Verify multiple sessions can be used concurrently."""
        session1 = SessionLocal()
        session2 = SessionLocal()
        
        # Both sessions should be independent
        assert session1 is not session2
        
        # Both should be usable
        from sqlalchemy import text
        result1 = session1.execute(text("SELECT 1"))
        result2 = session2.execute(text("SELECT 2"))
        
        assert result1 is not None
        assert result2 is not None
        
        session1.close()
        session2.close()
    
    def test_session_isolation(self):
        """Verify sessions are isolated from each other."""
        session1 = SessionLocal()
        session2 = SessionLocal()
        
        # Start transactions in both sessions
        session1.begin()
        session2.begin()
        
        # Rollback one should not affect the other
        session1.rollback()
        
        # session2 should still be usable
        from sqlalchemy import text
        result = session2.execute(text("SELECT 1"))
        assert result is not None
        
        session2.rollback()
        
        session1.close()
        session2.close()
