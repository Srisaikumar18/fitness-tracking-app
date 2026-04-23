# Requirements Document: Fitness Tracking App

## Introduction

The Fitness Tracking App is a simplified web-based application that enables anyone to log and view workout sessions. The system provides basic workout tracking with automatic calorie calculation based on activity type. There is no user authentication or account management - anyone can add workouts by providing their name, and all workouts are visible to everyone.

## Glossary

- **System**: The complete Fitness Tracking App including backend API and frontend interface
- **Workout**: A fitness session record containing user name, activity type, duration, and calculated calories
- **Backend**: The FastAPI server providing RESTful APIs and database management
- **Frontend**: The React web application providing the user interface
- **Database**: The SQLite database storing workout data
- **Database_Session**: A database connection session managed by SQLAlchemy
- **Schema**: A Pydantic model defining data validation rules
- **API_Client**: The Axios-based service handling HTTP requests from frontend to backend
- **Activity**: The type of exercise performed (e.g., running, cycling, walking)

## Requirements

### Requirement 1: Workout Creation

**User Story:** As anyone using the app, I want to create a new workout by providing my name, activity type, and duration, so that I can log my fitness activities with automatic calorie calculation.

#### Acceptance Criteria

1. WHEN a workout is created with valid data (user_name, activity, duration), THE System SHALL create a new workout record with a unique ID
2. WHEN a workout is created, THE System SHALL automatically calculate calories based on activity type and duration
3. WHEN a workout is created with activity "running", THE System SHALL calculate calories as duration * 10
4. WHEN a workout is created with activity "cycling", THE System SHALL calculate calories as duration * 8
5. WHEN a workout is created with activity "walking", THE System SHALL calculate calories as duration * 5
6. WHEN a workout is created with any other activity, THE System SHALL calculate calories as duration * 6
7. WHEN a workout is created, THE System SHALL standardize the activity value to lowercase
8. THE System SHALL require user_name to be a non-empty string (1-100 characters)
9. THE System SHALL require activity to be a non-empty string (1-100 characters)
10. THE System SHALL require duration to be a positive integer greater than zero
11. THE System SHALL reject duration values exceeding 1440 minutes (24 hours)
12. WHEN a workout is created successfully, THE System SHALL return the workout data with ID, user_name, standardized activity, duration, and calculated calories

### Requirement 2: Workout Retrieval

**User Story:** As anyone using the app, I want to view all workouts logged by everyone, so that I can see the workout history.

#### Acceptance Criteria

1. WHEN workouts are requested, THE System SHALL return all workouts in the database
2. THE System SHALL order workout results by ID in descending order (most recent first)
3. WHEN workouts are retrieved, THE System SHALL return each workout with ID, user_name, activity (in lowercase), duration, and calories
4. WHEN no workouts exist, THE System SHALL return an empty list
5. THE System SHALL successfully retrieve workouts even when the database is empty

### Requirement 3: Data Validation

**User Story:** As a system administrator, I want all user input to be validated against defined schemas, so that data integrity is maintained throughout the application.

#### Acceptance Criteria

1. THE System SHALL validate all API request data using Pydantic schemas before processing
2. IF validation fails, THEN THE System SHALL return a 422 status code with detailed field-specific error messages
3. THE System SHALL validate that user_name is not empty after stripping whitespace
4. THE System SHALL validate that activity is not empty after stripping whitespace
5. THE System SHALL validate that duration is a positive integer greater than zero
6. THE System SHALL validate that duration does not exceed 1440 minutes
7. THE System SHALL validate that user_name does not exceed 100 characters
8. THE System SHALL validate that activity does not exceed 100 characters after standardization
9. THE System SHALL sanitize string inputs by stripping leading and trailing whitespace

### Requirement 4: API Response Consistency

**User Story:** As a frontend developer, I want all API responses to follow consistent schemas, so that I can reliably process the data.

#### Acceptance Criteria

1. WHEN an API request succeeds, THE System SHALL return data matching the defined Pydantic response schema
2. THE System SHALL return appropriate HTTP status codes for all operations (200 for GET, 201 for POST, 400 for validation errors, 422 for schema errors, 500 for server errors)
3. WHEN an error occurs, THE System SHALL return a consistent error response format with error type, message, and optional details
4. THE System SHALL set Content-Type header to application/json for all JSON responses
5. THE System SHALL include all required fields in response objects (id, user_name, activity, duration, calories)
6. WHEN a workout is created, THE System SHALL return HTTP 201 status code with the created workout data

### Requirement 5: Database Session Management

**User Story:** As a system administrator, I want database sessions to be properly managed, so that connections are not leaked and resources are efficiently used.

#### Acceptance Criteria

1. THE System SHALL create a new Database_Session for each API request
2. WHEN a request completes successfully, THE System SHALL commit the transaction and close the Database_Session
3. IF an error occurs during request processing, THEN THE System SHALL rollback the transaction and close the Database_Session
4. THE System SHALL use dependency injection to provide Database_Session instances to route handlers
5. THE System SHALL configure the database engine with appropriate connection settings for SQLite

### Requirement 6: Frontend User Interface

**User Story:** As anyone using the app, I want an intuitive web interface to add and view workouts, so that I can easily track fitness activities without technical knowledge.

#### Acceptance Criteria

1. THE Frontend SHALL provide an AddWorkout component with fields for user_name, activity, and duration
2. THE Frontend SHALL provide a WorkoutList component displaying all workouts in a table
3. THE Frontend SHALL display workout statistics including total workouts, total duration, and total calories
4. THE Frontend SHALL display workouts ordered by most recent first (descending ID)
5. THE Frontend SHALL display loading states while API requests are in progress
6. WHEN an API error occurs, THE Frontend SHALL display user-friendly error messages
7. THE Frontend SHALL validate form inputs before submitting to the Backend
8. WHEN a workout is added successfully, THE Frontend SHALL clear the form and display a success message
9. THE Frontend SHALL display an empty state message when no workouts exist
10. THE Frontend SHALL provide a refresh button to reload the workout list

### Requirement 7: API Client Communication

**User Story:** As a frontend developer, I want a centralized API client, so that all HTTP communication is consistent and maintainable.

#### Acceptance Criteria

1. THE API_Client SHALL provide type-safe methods for workout operations (createWorkout, getWorkouts)
2. THE API_Client SHALL configure the base URL for the Backend API (http://localhost:8000)
3. THE API_Client SHALL set appropriate HTTP headers (Content-Type: application/json)
4. THE API_Client SHALL handle HTTP errors and provide meaningful error information
5. THE API_Client SHALL properly serialize request data and deserialize response data
6. THE API_Client SHALL use TypeScript interfaces matching the backend Pydantic schemas

### Requirement 8: Error Handling

**User Story:** As anyone using the app, I want clear error messages when something goes wrong, so that I understand what happened and how to fix it.

#### Acceptance Criteria

1. WHEN an empty user_name is provided, THE System SHALL return "User name cannot be empty" error
2. WHEN an empty activity is provided, THE System SHALL return "Activity cannot be empty" error
3. WHEN duration is zero or negative, THE System SHALL return "Duration must be greater than 0" error
4. WHEN duration exceeds 1440 minutes, THE System SHALL return "Duration cannot exceed 1440 minutes (24 hours)" error
5. WHEN validation fails, THE System SHALL return field-specific error messages indicating what is invalid
6. WHEN the database is unavailable, THE System SHALL return "Database connection error" with appropriate guidance
7. THE System SHALL log detailed error information for debugging while returning user-friendly messages to clients
8. WHEN a database integrity error occurs, THE System SHALL rollback the transaction and return a descriptive error
9. WHEN an unexpected error occurs, THE System SHALL return "Internal server error" with guidance to try again

### Requirement 9: Security

**User Story:** As a system administrator, I want the application to follow security best practices, so that the system is protected from common attacks.

#### Acceptance Criteria

1. THE System SHALL use parameterized queries via SQLAlchemy ORM to prevent SQL injection
2. THE System SHALL validate and sanitize all user input to prevent injection attacks
3. THE Frontend SHALL automatically escape rendered content to prevent XSS attacks
4. THE System SHALL configure CORS with explicit allowed origins (localhost:5173, localhost:3000)
5. THE System SHALL validate input lengths to prevent buffer overflow attacks
6. THE System SHALL strip whitespace from string inputs to prevent whitespace-based attacks
7. THE System SHALL validate numeric inputs are within acceptable ranges

