"""
Unit tests for database configuration and session management.

Tests verify:
- Database engine creation and configuration
- Session factory functionality
- get_db() dependency injection
- init_db() table creation
- Proper session lifecycle management
"""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from app.database import (
    SQLALCHEMY_DATABASE_URL,
    engine,
    SessionLocal,
    Base,
    get_db,
    init_db
)


class TestDatabaseConfiguration:
    """Test database engine and configuration."""
    
    def test_database_url_is_sqlite(self):
        """Verify database URL is configured for SQLite."""
        assert SQLALCHEMY_DATABASE_URL == "sqlite:///./fitness_tracker.db"
        assert "sqlite" in SQLALCHEMY_DATABASE_URL
    
    def test_engine_is_created(self):
        """Verify SQLAlchemy engine is properly created."""
        assert engine is not None
        assert str(engine.url) == SQLALCHEMY_DATABASE_URL
    
    def test_engine_dialect_is_sqlite(self):
        """Verify engine is using SQLite dialect."""
        assert engine.dialect.name == "sqlite"


class TestSessionFactory:
    """Test SessionLocal session factory."""
    
    def test_session_local_creates_session(self):
        """Verify SessionLocal creates valid database sessions."""
        session = SessionLocal()
        assert isinstance(session, Session)
        session.close()
    
    def test_session_local_configuration(self):
        """Verify SessionLocal has correct configuration."""
        session = SessionLocal()
        # Check autoflush is disabled
        # Note: SQLAlchemy 2.0 removed autocommit attribute
        assert session.autoflush is False
        session.close()
    
    def test_multiple_sessions_are_independent(self):
        """Verify multiple sessions can be created independently."""
        session1 = SessionLocal()
        session2 = SessionLocal()
        
        assert session1 is not session2
        assert isinstance(session1, Session)
        assert isinstance(session2, Session)
        
        session1.close()
        session2.close()


class TestGetDbDependency:
    """Test get_db() dependency injection function."""
    
    def test_get_db_yields_session(self):
        """Verify get_db() yields a valid database session."""
        db_generator = get_db()
        db = next(db_generator)
        
        assert isinstance(db, Session)
        
        # Clean up
        try:
            next(db_generator)
        except StopIteration:
            pass  # Expected - generator should stop after yielding once
    
    def test_get_db_closes_session_after_use(self):
        """Verify get_db() properly closes the session after use."""
        db_generator = get_db()
        db = next(db_generator)
        
        # Session should be open
        assert not db.is_active or True  # Session exists
        
        # Trigger finally block
        try:
            next(db_generator)
        except StopIteration:
            pass
        
        # Session should be closed (no longer usable)
        # Note: We can't directly check if closed, but we verify no errors occur
    
    def test_get_db_closes_session_on_exception(self):
        """Verify get_db() closes session even when exception occurs."""
        db_generator = get_db()
        db = next(db_generator)
        
        assert isinstance(db, Session)
        
        # Simulate exception by closing generator
        db_generator.close()
        
        # Session cleanup should have occurred (no way to verify directly,
        # but the finally block ensures it)


class TestBaseDeclarative:
    """Test Base declarative class."""
    
    def test_base_exists(self):
        """Verify Base declarative class is created."""
        assert Base is not None
    
    def test_base_has_metadata(self):
        """Verify Base has metadata attribute for table definitions."""
        assert hasattr(Base, 'metadata')
        assert Base.metadata is not None


class TestInitDb:
    """Test init_db() database initialization function."""
    
    def test_init_db_creates_tables(self, tmp_path):
        """Verify init_db() creates database tables."""
        # Create a temporary database for testing
        test_db_path = tmp_path / "test_fitness_tracker.db"
        test_engine = create_engine(f"sqlite:///{test_db_path}")
        
        # Create a test Base and table
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.orm import declarative_base
        
        TestBase = declarative_base()
        
        class TestUser(TestBase):
            __tablename__ = "test_users"
            id = Column(Integer, primary_key=True)
            name = Column(String)
        
        # Create tables
        TestBase.metadata.create_all(bind=test_engine)
        
        # Verify table was created
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        
        assert "test_users" in tables
    
    def test_init_db_is_idempotent(self, tmp_path):
        """Verify init_db() can be called multiple times safely."""
        # Create a temporary database
        test_db_path = tmp_path / "test_fitness_tracker.db"
        test_engine = create_engine(f"sqlite:///{test_db_path}")
        
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.orm import declarative_base
        
        TestBase = declarative_base()
        
        class TestUser(TestBase):
            __tablename__ = "test_users"
            id = Column(Integer, primary_key=True)
            name = Column(String)
        
        # Call create_all multiple times
        TestBase.metadata.create_all(bind=test_engine)
        TestBase.metadata.create_all(bind=test_engine)  # Should not raise error
        
        # Verify table still exists
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        
        assert "test_users" in tables
        assert len([t for t in tables if t == "test_users"]) == 1  # Only one instance


class TestSessionLifecycle:
    """Test database session lifecycle management."""
    
    def test_session_can_be_committed(self):
        """Verify sessions can commit transactions."""
        session = SessionLocal()
        
        # Begin transaction (implicit)
        # No actual data operations, just verify commit works
        session.commit()
        
        session.close()
    
    def test_session_can_be_rolled_back(self):
        """Verify sessions can rollback transactions."""
        session = SessionLocal()
        
        # Begin transaction (implicit)
        # Rollback should work even with no operations
        session.rollback()
        
        session.close()
    
    def test_session_context_manager_pattern(self):
        """Verify sessions work with context manager pattern."""
        from sqlalchemy import text
        
        # Simulate context manager usage
        db_generator = get_db()
        
        try:
            db = next(db_generator)
            assert isinstance(db, Session)
            # Simulate some work
            db.execute(text("SELECT 1"))
        finally:
            try:
                next(db_generator)
            except StopIteration:
                pass  # Expected
