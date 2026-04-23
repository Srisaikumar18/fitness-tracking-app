# Setup Scripts Guide

## Overview
This guide explains how to use the automated setup and run scripts for the Fitness Tracking App.

---

## Scripts

### 1. setupdev.bat
**Purpose**: Sets up the complete development environment

**What it does**:
1. Creates Python virtual environment in `backend/venv`
2. Installs backend dependencies from `backend/requirements.txt`
3. Runs database migrations with Alembic
4. Installs frontend dependencies with npm

**Usage**:
```bash
setupdev.bat
```

**Requirements**:
- Python 3.8+ installed and in PATH
- Node.js 16+ installed and in PATH
- npm installed and in PATH

**Output**:
```
============================================================================
Fitness Tracking App - Development Environment Setup
============================================================================

[1/4] Setting up backend environment...
Creating Python virtual environment...
Virtual environment created successfully.

[2/4] Installing backend dependencies...
Upgrading pip...
Installing Python packages from requirements.txt...
Backend dependencies installed successfully.

[3/4] Running database migrations...
Running Alembic migrations...
Database migrations completed successfully.

[4/4] Setting up frontend environment...
Installing frontend dependencies with npm...
Frontend dependencies installed successfully.

============================================================================
Development Environment Setup Complete!
============================================================================
```

---

### 2. runapplication.bat
**Purpose**: Starts both backend and frontend servers

**What it does**:
1. Performs pre-flight checks (venv exists, node_modules exists)
2. Starts FastAPI backend on http://localhost:8000
3. Waits 5 seconds for backend to initialize
4. Starts React frontend on http://localhost:5173

**Usage**:
```bash
runapplication.bat
```

**Requirements**:
- Development environment must be set up (run `setupdev.bat` first)
- Python and Node.js must be in PATH

**Output**:
```
============================================================================
Fitness Tracking App - Starting Application
============================================================================

Performing pre-flight checks...
Pre-flight checks passed.

[1/2] Starting FastAPI backend server...
Starting backend on http://localhost:8000
API Documentation will be available at http://localhost:8000/docs

Waiting for backend to initialize...

[2/2] Starting React frontend server...
Starting frontend on http://localhost:5173

============================================================================
Application Started Successfully!
============================================================================

Backend Server:
  - URL: http://localhost:8000
  - API Docs: http://localhost:8000/docs
  - Interactive API: http://localhost:8000/redoc

Frontend Server:
  - URL: http://localhost:5173
  - Development mode with hot reload enabled

Two terminal windows have been opened:
  1. Backend (FastAPI) - Running on port 8000
  2. Frontend (React) - Running on port 5173
```

---

## Quick Start

### First Time Setup
```bash
# Step 1: Setup development environment
setupdev.bat

# Step 2: Start the application
runapplication.bat

# Step 3: Open browser
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### Subsequent Runs
```bash
# Just run the application
runapplication.bat
```

---

## Manual Setup (Alternative)

If you prefer to set up manually:

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python -m alembic upgrade head

# Start server
python -m uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

---

## Troubleshooting

### Issue 1: "Python is not installed or not in PATH"
**Solution**: 
1. Install Python 3.8+ from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your terminal

**Verify**:
```bash
python --version
```

### Issue 2: "Node.js is not installed or not in PATH"
**Solution**:
1. Install Node.js 16+ from https://nodejs.org/
2. Restart your terminal

**Verify**:
```bash
node --version
npm --version
```

### Issue 3: "Backend virtual environment not found"
**Solution**: Run setupdev.bat first
```bash
setupdev.bat
```

### Issue 4: "Frontend dependencies not installed"
**Solution**: Run setupdev.bat first
```bash
setupdev.bat
```

### Issue 5: "Database migration failed"
**Solution**: The script will continue anyway. You can manually run migrations:
```bash
cd backend
venv\Scripts\activate
python -m alembic upgrade head
```

### Issue 6: "Port 8000 already in use"
**Solution**: 
1. Find and kill the process using port 8000:
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

2. Or change the port in runapplication.bat:
```batch
python -m uvicorn app.main:app --reload --port 8001
```

### Issue 7: "Port 5173 already in use"
**Solution**: Vite will automatically use the next available port (5174, 5175, etc.)

---

## Script Details

### setupdev.bat Features

#### Error Handling
- Checks if Python is installed
- Checks if Node.js is installed
- Verifies directory structure
- Handles pip upgrade failures gracefully
- Continues even if migrations fail (with warning)

#### Directory Management
- Stores root directory at start
- Returns to root directory after each step
- Uses absolute paths for reliability

#### Virtual Environment
- Creates venv in `backend/venv`
- Activates venv before installing packages
- Deactivates venv before moving to frontend

#### Dependencies
- Upgrades pip before installing packages
- Installs from requirements.txt
- Installs from package.json

#### Database
- Runs Alembic migrations
- Uses `python -m alembic` for reliability
- Provides helpful error messages

---

### runapplication.bat Features

#### Pre-flight Checks
- Verifies virtual environment exists
- Verifies node_modules exists
- Checks Python availability
- Checks Node.js availability

#### Backend Startup
- Changes to backend directory
- Activates virtual environment
- Starts uvicorn with:
  - `--reload`: Auto-reload on code changes
  - `--host 0.0.0.0`: Accept connections from any IP
  - `--port 8000`: Use port 8000
- Opens in new terminal window

#### Frontend Startup
- Changes to frontend directory
- Starts npm dev server
- Opens in new terminal window

#### Timing
- Waits 5 seconds between backend and frontend
- Ensures backend is ready before starting frontend

---

## Port Configuration

### Backend (FastAPI)
- **Default Port**: 8000
- **URLs**:
  - API: http://localhost:8000
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc
  - OpenAPI Spec: http://localhost:8000/openapi.json

### Frontend (React + Vite)
- **Default Port**: 5173
- **URL**: http://localhost:5173
- **Auto-increment**: If 5173 is busy, Vite uses 5174, 5175, etc.

---

## Environment Variables

### Backend
No environment variables required for development. The app uses:
- SQLite database (file-based)
- Default CORS settings
- Default port 8000

### Frontend
No environment variables required. The app uses:
- API base URL: http://localhost:8000
- Default Vite port: 5173

---

## Directory Structure

After running setupdev.bat:

```
Fitness_tracking_app/
├── backend/
│   ├── venv/                    # ✅ Created by setupdev.bat
│   │   ├── Scripts/
│   │   │   └── activate.bat
│   │   └── Lib/
│   ├── alembic/
│   ├── app/
│   ├── fitness_tracker.db       # ✅ Created by migrations
│   └── requirements.txt
├── frontend/
│   ├── node_modules/            # ✅ Created by setupdev.bat
│   ├── src/
│   └── package.json
├── setupdev.bat
└── runapplication.bat
```

---

## Testing the Setup

### Test Backend
```bash
# After running setupdev.bat
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload

# Open browser: http://localhost:8000/docs
# You should see Swagger UI
```

### Test Frontend
```bash
# After running setupdev.bat
cd frontend
npm run dev

# Open browser: http://localhost:5173
# You should see the Fitness Tracker app
```

### Test Full Application
```bash
# Run both servers
runapplication.bat

# Open browser: http://localhost:5173
# Try adding a workout
# Check API docs: http://localhost:8000/docs
```

---

## Stopping the Servers

### Option 1: Close Terminal Windows
Simply close the two terminal windows that were opened by runapplication.bat

### Option 2: Ctrl+C
In each terminal window, press `Ctrl+C` to stop the server

### Option 3: Task Manager
1. Open Task Manager (Ctrl+Shift+Esc)
2. Find "python.exe" and "node.exe" processes
3. End the processes

---

## Updating Dependencies

### Backend Dependencies
```bash
cd backend
venv\Scripts\activate
pip install <package-name>
pip freeze > requirements.txt
```

### Frontend Dependencies
```bash
cd frontend
npm install <package-name>
# package.json is automatically updated
```

---

## Resetting the Environment

### Reset Backend
```bash
# Delete virtual environment
rmdir /s /q backend\venv

# Delete database
del backend\fitness_tracker.db

# Run setup again
setupdev.bat
```

### Reset Frontend
```bash
# Delete node_modules
rmdir /s /q frontend\node_modules

# Run setup again
setupdev.bat
```

### Complete Reset
```bash
# Delete everything
rmdir /s /q backend\venv
rmdir /s /q frontend\node_modules
del backend\fitness_tracker.db

# Run setup again
setupdev.bat
```

---

## Best Practices

1. **Always run setupdev.bat first** before using runapplication.bat
2. **Keep terminal windows open** to see server logs
3. **Check for errors** in the terminal windows
4. **Use Ctrl+C** to gracefully stop servers
5. **Run setupdev.bat again** after pulling new code
6. **Check port availability** before starting servers

---

## Common Workflows

### Daily Development
```bash
# Start servers
runapplication.bat

# Develop...

# Stop servers (Ctrl+C in each window)
```

### After Pulling New Code
```bash
# Update dependencies
setupdev.bat

# Start servers
runapplication.bat
```

### After Database Schema Changes
```bash
cd backend
venv\Scripts\activate
python -m alembic upgrade head
```

### Clean Start
```bash
# Reset everything
rmdir /s /q backend\venv
rmdir /s /q frontend\node_modules

# Setup again
setupdev.bat

# Start servers
runapplication.bat
```

---

## Script Modifications

### Change Backend Port
Edit `runapplication.bat`:
```batch
REM Change this line:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM To:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Change Frontend Port
Edit `frontend/vite.config.ts`:
```typescript
export default defineConfig({
  server: {
    port: 3000  // Change from default 5173
  }
})
```

### Disable Auto-reload
Edit `runapplication.bat`:
```batch
REM Remove --reload flag:
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Summary

### setupdev.bat
- ✅ Creates virtual environment
- ✅ Installs backend dependencies
- ✅ Runs database migrations
- ✅ Installs frontend dependencies
- ✅ One-time setup (run after cloning repo)

### runapplication.bat
- ✅ Starts backend on port 8000
- ✅ Starts frontend on port 5173
- ✅ Opens two terminal windows
- ✅ Run every time you want to develop

---

**Last Updated**: April 2026  
**Tested On**: Windows 10/11  
**Python Version**: 3.8+  
**Node.js Version**: 16+
