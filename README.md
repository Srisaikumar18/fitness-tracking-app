# 🏋️ Fitness Tracking App


A full-stack web application for tracking workout sessions with automatic calorie calculation, built with FastAPI and React.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [SDK Generation](#sdk-generation)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Fitness Tracking App is a modern web application that allows users to log and track their workout sessions. The application automatically calculates calories burned based on activity type and duration, providing a seamless experience for fitness enthusiasts.

### Key Highlights

- **Automatic Calorie Calculation**: No manual entry needed - calories are calculated based on activity type
- **Activity Standardization**: All activities are automatically standardized to lowercase for consistency
- **Real-time Statistics**: View total workouts, duration, and calories at a glance
- **RESTful API**: Well-documented API with OpenAPI/Swagger support
- **Type-Safe**: Full TypeScript support on frontend with Pydantic validation on backend
- **Error Handling**: Comprehensive error handling with meaningful error messages

---

## ✨ Features

### Core Features
- ✅ **Add Workouts**: Log workout sessions with user name, activity, and duration
- ✅ **View History**: Display all workouts in a sortable table
- ✅ **Statistics Dashboard**: Real-time statistics (total workouts, duration, calories)
- ✅ **Activity Breakdown**: See workout distribution by activity type
- ✅ **Automatic Calculations**: Calories calculated based on activity type
- ✅ **Responsive Design**: Works on desktop and mobile devices

### Technical Features
- ✅ **RESTful API**: Clean, well-documented REST API
- ✅ **OpenAPI Support**: Auto-generated API documentation
- ✅ **SDK Generation**: Generate Python SDK from OpenAPI spec
- ✅ **Input Validation**: Comprehensive validation with detailed error messages
- ✅ **Error Handling**: Graceful error handling with proper HTTP status codes
- ✅ **Database Migrations**: Alembic for database schema management
- ✅ **CORS Support**: Configured for local development

---

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast Python web framework
- **Database**: [SQLite](https://www.sqlite.org/) - Lightweight, file-based database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) - Database migration tool
- **Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type hints
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI server

### Frontend
- **Framework**: [React 18](https://reactjs.org/) - JavaScript library for building UIs
- **Language**: [TypeScript](https://www.typescriptlang.org/) - Typed superset of JavaScript
- **Build Tool**: [Vite](https://vitejs.dev/) - Next generation frontend tooling
- **HTTP Client**: [Axios](https://axios-http.com/) - Promise-based HTTP client
- **Styling**: CSS3 with custom styles

### Development Tools
- **API Documentation**: Swagger UI / ReDoc
- **SDK Generation**: OpenAPI Generator CLI
- **Version Control**: Git
- **Package Management**: pip (Python), npm (Node.js)

---

## 📁 Project Structure

```
Fitness_tracking_app/
├── backend/                      # FastAPI Backend
│   ├── alembic/                  # Database migrations
│   │   └── versions/             # Migration scripts
│   ├── app/
│   │   ├── models/               # SQLAlchemy models
│   │   │   └── workout.py        # Workout model
│   │   ├── routes/               # API routes
│   │   │   └── workouts.py       # Workout endpoints
│   │   ├── schemas/              # Pydantic schemas
│   │   │   └── workout.py        # Workout schemas
│   │   ├── database.py           # Database configuration
│   │   └── main.py               # FastAPI application
│   ├── tests/                    # Backend tests
│   ├── alembic.ini               # Alembic configuration
│   ├── requirements.txt          # Python dependencies
│   └── run_server.bat            # Start backend script
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── AddWorkout.tsx    # Add workout form
│   │   │   └── WorkoutList.tsx   # Workout table
│   │   ├── services/             # API services
│   │   │   └── api.ts            # API client
│   │   ├── types/                # TypeScript types
│   │   │   └── index.ts          # Type definitions
│   │   ├── App.tsx               # Main app component
│   │   └── main.tsx              # Entry point
│   ├── package.json              # Node dependencies
│   └── vite.config.ts            # Vite configuration
│
├── setupdev.bat                  # Setup script
├── runapplication.bat            # Run both servers
├── generate_sdk.bat              # Generate Python SDK
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### One-Command Setup

```bash
# Clone the repository
git clone <repository-url>
cd Fitness_tracking_app

# Setup development environment
setupdev.bat

# Start the application
runapplication.bat
```

That's it! The application will be running at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📦 Setup Instructions

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python -m alembic upgrade head
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

---

## 🎮 Running the Application

### Option 1: Automated (Recommended)

```bash
# Start both backend and frontend
runapplication.bat
```

This will:
- Start FastAPI backend on http://localhost:8000
- Start React frontend on http://localhost:5173
- Open two terminal windows for each server

### Option 2: Manual

**Terminal 1 - Backend**:
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Create Workout
**POST** `/api/workouts/`

Create a new workout session. Calories are calculated automatically.

**Request Body**:
```json
{
  "user_name": "John Doe",
  "activity": "running",
  "duration": 45
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "user_name": "John Doe",
  "activity": "running",
  "duration": 45,
  "calories": 450
}
```

**Calorie Calculation Rules**:
| Activity | Rate (cal/min) | Example (30 min) |
|----------|----------------|------------------|
| running  | 10             | 300 calories     |
| cycling  | 8              | 240 calories     |
| walking  | 5              | 150 calories     |
| others   | 6              | 180 calories     |

**Validation Rules**:
- `user_name`: Required, 1-100 characters
- `activity`: Required, 1-100 characters
- `duration`: Required, > 0, <= 1440 minutes (24 hours)

**Error Responses**:
- `400 Bad Request`: Invalid input (duration <= 0, empty fields, etc.)
- `422 Unprocessable Entity`: Validation error (missing fields, wrong types)
- `500 Internal Server Error`: Database error

---

#### 2. Get All Workouts
**GET** `/api/workouts/`

Retrieve all workouts ordered by most recent first.

**Response** (200 OK):
```json
[
  {
    "id": 2,
    "user_name": "Jane Smith",
    "activity": "cycling",
    "duration": 60,
    "calories": 480
  },
  {
    "id": 1,
    "user_name": "John Doe",
    "activity": "running",
    "duration": 45,
    "calories": 450
  }
]
```

**Error Responses**:
- `500 Internal Server Error`: Database error

---

#### 3. Health Check
**GET** `/health`

Check API and database health.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "message": "API is running",
  "database": "connected"
}
```

**Response** (503 Service Unavailable):
```json
{
  "status": "unhealthy",
  "message": "API is running but database connection failed",
  "database": "disconnected"
}
```

---

#### 4. API Information
**GET** `/api`

Get API information and available endpoints.

**Response** (200 OK):
```json
{
  "api_version": "1.0.0",
  "endpoints": {
    "workouts": {
      "create": "POST /api/workouts/",
      "list": "GET /api/workouts/"
    }
  },
  "documentation": {
    "swagger_ui": "/docs",
    "redoc": "/redoc",
    "openapi_schema": "/openapi.json"
  }
}
```

---

### Sample Requests

#### Using cURL

**Create Workout**:
```bash
curl -X POST http://localhost:8000/api/workouts/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John Doe",
    "activity": "running",
    "duration": 45
  }'
```

**Get All Workouts**:
```bash
curl http://localhost:8000/api/workouts/
```

**Health Check**:
```bash
curl http://localhost:8000/health
```

#### Using Python (requests)

```python
import requests

# Create workout
response = requests.post(
    "http://localhost:8000/api/workouts/",
    json={
        "user_name": "John Doe",
        "activity": "running",
        "duration": 45
    }
)
print(response.json())

# Get all workouts
response = requests.get("http://localhost:8000/api/workouts/")
print(response.json())
```

#### Using JavaScript (fetch)

```javascript
// Create workout
fetch('http://localhost:8000/api/workouts/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_name: 'John Doe',
    activity: 'running',
    duration: 45
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Get all workouts
fetch('http://localhost:8000/api/workouts/')
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 🔧 SDK Generation

Generate a Python SDK from the OpenAPI specification for easy API integration.

### Prerequisites

- **Java 8+** - Required for OpenAPI Generator
- **OpenAPI Generator CLI** - Install via npm

### Installation

```bash
npm install @openapitools/openapi-generator-cli -g
```

### Generate SDK

```bash
# Automated generation
generate_sdk.bat

# Or manually
curl http://localhost:8000/openapi.json -o openapi.json

openapi-generator-cli generate \
  -i openapi.json \
  -g python \
  -o fitness_tracker_sdk \
  --package-name fitness_tracker_client
```

### Install SDK

```bash
cd fitness_tracker_sdk
pip install -e .
```

### Use SDK

```python
import fitness_tracker_client
from fitness_tracker_client.api import workouts_api
from fitness_tracker_client.model.workout_create import WorkoutCreate

# Configure API
configuration = fitness_tracker_client.Configuration(
    host="http://localhost:8000"
)

# Create client
with fitness_tracker_client.ApiClient(configuration) as api_client:
    api = workouts_api.WorkoutsApi(api_client)
    
    # Create workout
    new_workout = WorkoutCreate(
        user_name="Jane Doe",
        activity="running",
        duration=45
    )
    
    result = api.create_workout_api_workouts_post(new_workout)
    print(f"Created workout ID: {result.id}")
    print(f"Calories: {result.calories}")
    
    # Get all workouts
    workouts = api.get_workouts_api_workouts_get()
    print(f"Total workouts: {len(workouts)}")
```

For detailed SDK generation instructions, see [SDK_GENERATION_GUIDE.md](SDK_GENERATION_GUIDE.md).

---

## 🛡️ Error Handling

The API provides comprehensive error handling with meaningful error messages.

### Error Response Format

```json
{
  "error": "Error type",
  "message": "User-friendly message",
  "hint": "What to do next"
}
```

### Error Codes

| Code | Type | Description |
|------|------|-------------|
| 400 | Bad Request | Invalid input (duration <= 0, empty fields, etc.) |
| 422 | Unprocessable Entity | Validation error (missing fields, wrong types) |
| 500 | Internal Server Error | Database error or unexpected exception |
| 503 | Service Unavailable | Database connection failed |

### Example Error Responses

**Invalid Duration (400)**:
```json
{
  "error": "Invalid input",
  "message": "Duration must be greater than 0",
  "field": "duration",
  "value": 0
}
```

**Missing Field (422)**:
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

**Database Error (500)**:
```json
{
  "error": "Database error",
  "message": "An unexpected database error occurred",
  "hint": "Please try again later"
}
```

For detailed error handling documentation, see [ERROR_HANDLING_GUIDE.md](ERROR_HANDLING_GUIDE.md).

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

**Test Coverage**:
- Database connection tests
- Workout model tests
- Workout creation tests
- Workout retrieval tests
- Schema validation tests

### Manual API Testing

```bash
# Test GET endpoint
python test_get_workouts.py

# Test POST endpoint
python test_post_workout.py

# Run complete test suite
python test_sdk_complete.py
```

### Frontend Testing

```bash
cd frontend
npm run test
```

---

## 📖 Additional Documentation

- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Comprehensive project documentation
- **[SDK_GENERATION_GUIDE.md](SDK_GENERATION_GUIDE.md)** - Complete SDK generation guide
- **[ERROR_HANDLING_GUIDE.md](ERROR_HANDLING_GUIDE.md)** - Error handling documentation
- **[SETUP_SCRIPTS_GUIDE.md](SETUP_SCRIPTS_GUIDE.md)** - Setup scripts documentation
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Detailed project structure

---

## 🔍 Features in Detail

### Automatic Calorie Calculation

The application automatically calculates calories based on activity type and duration:

```python
calorie_rates = {
    "running": 10,   # 10 cal/min
    "cycling": 8,    # 8 cal/min
    "walking": 5     # 5 cal/min
}
# Default: 6 cal/min for other activities

calories = duration * rate
```

**Example**:
- Running for 45 minutes: 45 × 10 = **450 calories**
- Cycling for 60 minutes: 60 × 8 = **480 calories**
- Walking for 30 minutes: 30 × 5 = **150 calories**

### Activity Standardization

All activities are automatically standardized to lowercase:

| Input | Output |
|-------|--------|
| `"RUNNING"` | `"running"` |
| `"CyClInG"` | `"cycling"` |
| `"  Walking  "` | `"walking"` |

This ensures data consistency and simplifies queries.

---

## 🚧 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Run from backend directory using Python module execution:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

**Issue**: `Database migration failed`

**Solution**: Run migrations manually:
```bash
cd backend
venv\Scripts\activate
python -m alembic upgrade head
```

---

**Issue**: `Port 8000 already in use`

**Solution**: Kill the process or use a different port:
```bash
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

---

### Frontend Issues

**Issue**: `Cannot connect to backend`

**Solution**:
1. Verify backend is running on http://localhost:8000
2. Check CORS settings in `backend/app/main.py`
3. Clear browser cache (Ctrl+Shift+Delete)

---

**Issue**: `npm install fails`

**Solution**:
```bash
# Delete node_modules and package-lock.json
rmdir /s /q node_modules
del package-lock.json

# Reinstall
npm install
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work*

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the amazing frontend library
- SQLAlchemy for the powerful ORM
- Vite for the blazing fast build tool
- OpenAPI Generator for SDK generation

---

## 📞 Support

For issues, questions, or suggestions:

- **Issues**: [GitHub Issues](https://github.com/yourusername/fitness-tracking-app/issues)
- **Documentation**: See the `docs/` folder
- **Email**: your.email@example.com

---

## 🗺️ Roadmap

### Planned Features

- [ ] User authentication and authorization
- [ ] Workout editing and deletion
- [ ] Exercise tracking within workouts
- [ ] Data visualization (charts and graphs)
- [ ] Export data to CSV/PDF
- [ ] Mobile app (React Native)
- [ ] Social features (share workouts)
- [ ] Workout templates and plans
- [ ] Progress tracking over time
- [ ] Integration with fitness devices

---

## 📊 Project Status

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: April 2026

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

**Made with ❤️ and ☕**
=======
# fitness-tracking-app
