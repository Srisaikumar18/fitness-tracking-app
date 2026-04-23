# Fitness Tracking App - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Setup Instructions](#setup-instructions)
6. [API Documentation](#api-documentation)
7. [Activity Standardization](#activity-standardization)
8. [Calorie Calculation](#calorie-calculation)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

---

## Project Overview

A full-stack fitness tracking application that allows users to log workout sessions and track their fitness activities. The app automatically calculates calories burned based on activity type and duration.

### Key Features
- ✅ Add workout sessions (user name, activity, duration)
- ✅ Automatic calorie calculation based on activity type
- ✅ View workout history in a table
- ✅ Activity standardization (lowercase)
- ✅ Real-time statistics (total workouts, duration, calories)
- ✅ Responsive design

---

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Migrations**: Alembic
- **Validation**: Pydantic

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Styling**: CSS3

---

## Project Structure

```
Fitness_tracking_app/
├── backend/
│   ├── alembic/                    # Database migrations
│   ├── app/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── workout.py          # Workout model
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── workouts.py         # Workout endpoints
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── workout.py          # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── database.py             # Database configuration
│   │   └── main.py                 # FastAPI app
│   ├── tests/                      # Backend tests
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── run_server.bat              # Start backend server
│   └── recreate_db.bat             # Recreate database
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AddWorkout.tsx      # Add workout form
│   │   │   ├── AddWorkout.css
│   │   │   ├── WorkoutList.tsx     # Workout table
│   │   │   └── WorkoutList.css
│   │   ├── services/
│   │   │   └── api.ts              # API client
│   │   ├── types/
│   │   │   └── index.ts            # TypeScript types
│   │   ├── App.tsx                 # Main app component
│   │   ├── App.css
│   │   ├── main.tsx                # Entry point
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
├── setupdev.bat                    # Automated setup script
├── runapplication.bat              # Start both servers
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Option 1: Automated Setup (Recommended)

1. **Run setup script**:
   ```bash
   setupdev.bat
   ```
   This will:
   - Create Python virtual environment
   - Install backend dependencies
   - Run database migrations
   - Install frontend dependencies

2. **Start the application**:
   ```bash
   runapplication.bat
   ```
   This will:
   - Start backend on http://localhost:8000
   - Start frontend on http://localhost:5173

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start backend server**:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   Backend will run on http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```
   Frontend will run on http://localhost:5173

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Create Workout
**POST** `/api/workouts/`

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

**Validation Rules**:
- `user_name`: 1-100 characters, required
- `activity`: 1-100 characters, required
- `duration`: Integer > 0, required
- `calories`: Calculated automatically

#### 2. Get All Workouts
**GET** `/api/workouts/`

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

#### 3. Health Check
**GET** `/health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

#### 4. API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## Activity Standardization

All activity values are automatically standardized to lowercase before saving to the database.

### Rules
- **Lowercase Conversion**: All activities converted to lowercase
- **Whitespace Trimming**: Leading/trailing spaces removed

### Examples
| Input | Output |
|-------|--------|
| `"Running"` | `"running"` |
| `"CYCLING"` | `"cycling"` |
| `"  Walking  "` | `"walking"` |
| `"SwImMiNg"` | `"swimming"` |

### Benefits
- Consistent data storage
- Case-insensitive queries
- Uniform UI display

---

## Calorie Calculation

Calories are automatically calculated based on activity type and duration.

### Calculation Rules

| Activity | Rate (cal/min) | Formula | Example (30 min) |
|----------|----------------|---------|------------------|
| Running  | 10 | duration × 10 | 300 calories |
| Cycling  | 8 | duration × 8 | 240 calories |
| Walking  | 5 | duration × 5 | 150 calories |
| Others   | 6 | duration × 6 | 180 calories |

### Examples

```json
// Running for 45 minutes
Input:  {"activity": "running", "duration": 45}
Output: {"calories": 450}  // 45 × 10

// Cycling for 60 minutes
Input:  {"activity": "cycling", "duration": 60}
Output: {"calories": 480}  // 60 × 8

// Walking for 30 minutes
Input:  {"activity": "walking", "duration": 30}
Output: {"calories": 150}  // 30 × 5

// Swimming for 40 minutes (other activity)
Input:  {"activity": "swimming", "duration": 40}
Output: {"calories": 240}  // 40 × 6
```

### Benefits
- Simplified user experience (no manual calorie entry)
- Consistent calculations
- Activity-aware rates
- Reduced user errors

---

## Testing

### Backend Tests

Run backend tests:
```bash
cd backend
pytest
```

Test files:
- `test_database.py` - Database connection tests
- `test_database_integration.py` - Database integration tests
- `test_workout_*.py` - Workout-related tests

### Manual Testing

#### Test Workout Creation
```bash
curl -X POST http://localhost:8000/api/workouts/ \
  -H "Content-Type: application/json" \
  -d '{"user_name":"Test User","activity":"running","duration":30}'
```

Expected Response:
```json
{
  "id": 1,
  "user_name": "Test User",
  "activity": "running",
  "duration": 30,
  "calories": 300
}
```

#### Test Get Workouts
```bash
curl http://localhost:8000/api/workouts/
```

---

## Troubleshooting

### Backend Issues

#### Issue: ModuleNotFoundError
**Solution**: Make sure you're running from the backend directory:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

#### Issue: Database not found
**Solution**: Run migrations:
```bash
alembic upgrade head
```

#### Issue: Port 8000 already in use
**Solution**: Kill the process or use a different port:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

#### Issue: Cannot connect to backend
**Solution**: 
1. Verify backend is running on http://localhost:8000
2. Check CORS settings in `backend/app/main.py`
3. Clear browser cache (Ctrl+Shift+Delete)

#### Issue: npm install fails
**Solution**: 
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again

#### Issue: Port 5173 already in use
**Solution**: Kill the process or Vite will automatically use the next available port

### Database Issues

#### Issue: Need to reset database
**Solution**: Run the recreate script:
```bash
cd backend
recreate_db.bat
```

---

## Development Notes

### Database Schema

**Workouts Table**:
```sql
CREATE TABLE workouts (
    id INTEGER PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    activity VARCHAR(100) NOT NULL,
    duration INTEGER NOT NULL,
    calories INTEGER NOT NULL
);
```

### CORS Configuration

The backend allows requests from:
- http://localhost:5173 (Vite dev server)
- http://localhost:3000 (Alternative React dev server)
- http://127.0.0.1:5173
- http://127.0.0.1:3000

### Environment Variables

No environment variables required for development. The app uses:
- SQLite database (file-based)
- Default ports (8000 for backend, 5173 for frontend)

---

## Production Deployment

### Backend Deployment

1. Set up production database (PostgreSQL recommended)
2. Update `DATABASE_URL` in environment
3. Run migrations: `alembic upgrade head`
4. Use production ASGI server: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

### Frontend Deployment

1. Build production bundle:
   ```bash
   npm run build
   ```

2. Deploy `dist/` folder to static hosting (Netlify, Vercel, etc.)

3. Update API base URL in `frontend/src/services/api.ts`

---

## License

This project is for educational purposes.

---

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation at http://localhost:8000/docs
3. Check browser console for frontend errors
4. Check terminal output for backend errors

---

**Last Updated**: April 2026
**Version**: 1.0.0
