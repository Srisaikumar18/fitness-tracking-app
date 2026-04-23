# Error Handling Guide

## Overview
This guide documents the comprehensive error handling implemented in the Fitness Tracking API backend.

---

## Error Types

### 1. Client Errors (4xx)

#### 400 Bad Request
**When**: Invalid input data that passes Pydantic validation but fails business logic

**Examples**:
- Duration <= 0
- Duration > 1440 minutes (24 hours)
- Empty user_name after stripping
- Empty activity after stripping
- Activity name > 100 characters

**Response Format**:
```json
{
  "error": "Invalid input",
  "message": "Duration must be greater than 0",
  "field": "duration",
  "value": 0
}
```

#### 422 Unprocessable Entity
**When**: Pydantic validation fails (automatic)

**Examples**:
- Missing required fields
- Wrong data types
- Field constraints violated

**Response Format**:
```json
{
  "error": "Validation error",
  "message": "The request contains invalid data",
  "details": [
    {
      "field": "body.duration",
      "message": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### 2. Server Errors (5xx)

#### 500 Internal Server Error
**When**: Database errors or unexpected exceptions

**Types**:
1. **Database Integrity Error**: Data constraint violation
2. **Database Operational Error**: Connection failure
3. **Database Error**: General SQLAlchemy error
4. **Internal Server Error**: Unexpected exception

**Response Format**:
```json
{
  "error": "Database error",
  "message": "An unexpected database error occurred while creating the workout",
  "hint": "Please try again later"
}
```

#### 503 Service Unavailable
**When**: Health check fails (database not connected)

**Response Format**:
```json
{
  "status": "unhealthy",
  "message": "API is running but database connection failed",
  "database": "disconnected"
}
```

---

## Error Handling Implementation

### Routes Layer (`backend/app/routes/workouts.py`)

#### Input Validation
```python
# Duration validation
if workout.duration <= 0:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "Invalid input",
            "message": "Duration must be greater than 0",
            "field": "duration",
            "value": workout.duration
        }
    )

# Empty field validation
if not workout.user_name or not workout.user_name.strip():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "Invalid input",
            "message": "User name cannot be empty",
            "field": "user_name"
        }
    )

# Range validation
if workout.duration > 1440:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": "Invalid input",
            "message": "Duration cannot exceed 1440 minutes (24 hours)",
            "field": "duration",
            "value": workout.duration
        }
    )
```

#### Database Error Handling
```python
try:
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    
except IntegrityError as e:
    db.rollback()
    logger.error(f"Database integrity error: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error": "Database integrity error",
            "message": "Failed to create workout due to data constraint violation",
            "hint": "Please check your input data"
        }
    )

except OperationalError as e:
    db.rollback()
    logger.error(f"Database operational error: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error": "Database connection error",
            "message": "Failed to connect to the database",
            "hint": "Please try again later or contact support"
        }
    )

except SQLAlchemyError as e:
    db.rollback()
    logger.error(f"Database error: {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error": "Database error",
            "message": "An unexpected database error occurred",
            "hint": "Please try again later"
        }
    )
```

#### Catch-All Handler
```python
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "hint": "Please try again later or contact support"
        }
    )
```

---

### Database Layer (`backend/app/database.py`)

#### Session Management
```python
def get_db() -> Generator[Session, None, None]:
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
```

#### Database Initialization
```python
def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {str(e)}")
        raise
```

---

### Application Layer (`backend/app/main.py`)

#### Global Exception Handlers

**Validation Error Handler**:
```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "message": "The request contains invalid data",
            "details": errors
        }
    )
```

**Database Error Handler**:
```python
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error on {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database error",
            "message": "A database error occurred",
            "hint": "Please try again later or contact support"
        }
    )
```

**General Error Handler**:
```python
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.url.path}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "hint": "Please try again later or contact support"
        }
    )
```

---

## Logging

### Configuration
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Log Levels

**INFO**: Successful operations
```python
logger.info(f"Workout created successfully: ID={db_workout.id}")
logger.info(f"Retrieved {len(workouts)} workouts successfully")
```

**WARNING**: Invalid input
```python
logger.warning(f"Invalid duration provided: {workout.duration}")
logger.warning("Empty user_name provided")
```

**ERROR**: Exceptions and failures
```python
logger.error(f"Database error: {str(e)}")
logger.error(f"Unexpected error: {str(e)}", exc_info=True)
```

---

## Error Response Examples

### Example 1: Invalid Duration (400)

**Request**:
```bash
POST /api/workouts/
{
  "user_name": "John Doe",
  "activity": "running",
  "duration": 0
}
```

**Response**:
```json
{
  "error": "Invalid input",
  "message": "Duration must be greater than 0",
  "field": "duration",
  "value": 0
}
```

---

### Example 2: Missing Field (422)

**Request**:
```bash
POST /api/workouts/
{
  "user_name": "John Doe",
  "activity": "running"
}
```

**Response**:
```json
{
  "error": "Validation error",
  "message": "The request contains invalid data",
  "details": [
    {
      "field": "body.duration",
      "message": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### Example 3: Empty User Name (400)

**Request**:
```bash
POST /api/workouts/
{
  "user_name": "   ",
  "activity": "running",
  "duration": 30
}
```

**Response**:
```json
{
  "error": "Invalid input",
  "message": "User name cannot be empty",
  "field": "user_name"
}
```

---

### Example 4: Duration Too Large (400)

**Request**:
```bash
POST /api/workouts/
{
  "user_name": "John Doe",
  "activity": "running",
  "duration": 2000
}
```

**Response**:
```json
{
  "error": "Invalid input",
  "message": "Duration cannot exceed 1440 minutes (24 hours)",
  "field": "duration",
  "value": 2000
}
```

---

### Example 5: Database Error (500)

**Scenario**: Database connection lost

**Response**:
```json
{
  "error": "Database connection error",
  "message": "Failed to connect to the database",
  "hint": "Please try again later or contact support"
}
```

---

### Example 6: Health Check Failure (503)

**Request**:
```bash
GET /health
```

**Response** (when database is down):
```json
{
  "status": "unhealthy",
  "message": "API is running but database connection failed",
  "database": "disconnected"
}
```

---

## Validation Rules

### User Name
- ✅ Required
- ✅ Must not be empty after stripping
- ✅ 1-100 characters (Pydantic)

### Activity
- ✅ Required
- ✅ Must not be empty after stripping
- ✅ 1-100 characters (Pydantic)
- ✅ Automatically converted to lowercase

### Duration
- ✅ Required
- ✅ Must be > 0
- ✅ Must be <= 1440 minutes (24 hours)
- ✅ Must be an integer

---

## Testing Error Handling

### Test Invalid Duration
```bash
curl -X POST http://localhost:8000/api/workouts/ \
  -H "Content-Type: application/json" \
  -d '{"user_name":"Test","activity":"running","duration":0}'
```

### Test Missing Field
```bash
curl -X POST http://localhost:8000/api/workouts/ \
  -H "Content-Type: application/json" \
  -d '{"user_name":"Test","activity":"running"}'
```

### Test Empty User Name
```bash
curl -X POST http://localhost:8000/api/workouts/ \
  -H "Content-Type: application/json" \
  -d '{"user_name":"   ","activity":"running","duration":30}'
```

### Test Duration Too Large
```bash
curl -X POST http://localhost:8000/api/workouts/ \
  -H "Content-Type: application/json" \
  -d '{"user_name":"Test","activity":"running","duration":2000}'
```

### Test Health Check
```bash
curl http://localhost:8000/health
```

---

## Best Practices

### 1. Always Use Try-Except
```python
try:
    # Database operation
    db.commit()
except SQLAlchemyError as e:
    db.rollback()
    logger.error(f"Error: {str(e)}")
    raise HTTPException(...)
```

### 2. Log All Errors
```python
logger.error(f"Error description: {str(e)}", exc_info=True)
```

### 3. Provide Meaningful Messages
```python
detail={
    "error": "Clear error type",
    "message": "User-friendly message",
    "hint": "What the user should do"
}
```

### 4. Always Rollback on Error
```python
except SQLAlchemyError as e:
    db.rollback()  # Important!
    raise
```

### 5. Use Appropriate Status Codes
- 400: Client error (invalid input)
- 422: Validation error
- 500: Server error
- 503: Service unavailable

---

## Summary

### Error Handling Features
- ✅ Comprehensive input validation
- ✅ Database error handling
- ✅ Meaningful error messages
- ✅ Proper logging
- ✅ Transaction rollback on errors
- ✅ Global exception handlers
- ✅ Health check with database connectivity
- ✅ Structured error responses

### Validation Checks
- ✅ Duration > 0
- ✅ Duration <= 1440 minutes
- ✅ User name not empty
- ✅ Activity not empty
- ✅ Activity <= 100 characters
- ✅ Required fields present
- ✅ Correct data types

### Error Types Handled
- ✅ Invalid input (400)
- ✅ Validation errors (422)
- ✅ Database integrity errors (500)
- ✅ Database connection errors (500)
- ✅ General database errors (500)
- ✅ Unexpected exceptions (500)
- ✅ Service unavailable (503)

---

**Last Updated**: April 2026  
**Status**: ✅ Complete  
**Coverage**: Comprehensive
