"""
Database configuration and session management for the Fitness Tracking App.

This module provides:
- SQLAlchemy engine configuration for SQLite
- Session factory for database connections
- Base class for declarative models
- Dependency injection function for route handlers
- Database initialization function with error handling
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator
import logging

# Configure logging
logger = logging.getLogger(__name__)

# SQLite database URL - creates fitness_tracker.db in the current directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness_tracker.db"

# Create SQLAlchemy engine
# check_same_thread=False is required for SQLite to work with FastAPI's async nature
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,  # Verify connections before using them
        echo=False  # Set to True for SQL query logging
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

# Create SessionLocal class for database sessions
# autocommit=False: transactions must be explicitly committed
# autoflush=False: changes are not automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session to route handlers.
    
    This function is used with FastAPI's Depends() to inject database sessions
    into route handlers. It ensures proper session lifecycle management:
    - Creates a new session for each request
    - Yields the session to the route handler
    - Closes the session after the request completes (even if an error occurs)
    - Rolls back any uncommitted transactions on error
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/users/{user_id}")
        async def get_user(user_id: int, db: Session = Depends(get_db)):
            return db.query(User).filter(User.id == user_id).first()
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error in database session: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize the database by creating all tables.
    
    This function creates all tables defined by SQLAlchemy models that inherit
    from Base. It should be called once when the application starts.
    
    Note:
        - This function is idempotent - it's safe to call multiple times
        - Tables that already exist will not be recreated
        - For production, use Alembic migrations instead of this function
        
    Raises:
        SQLAlchemyError: If database initialization fails
        
    Example:
        # In main.py or application startup
        from app.database import init_db
        try:
            init_db()
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {str(e)}")
        raise
