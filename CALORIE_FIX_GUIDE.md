# 🔧 Calorie Fix Guide

## Overview

This guide explains how to fix inconsistent calorie values in your existing database. The scripts will recalculate calories for all workouts based on the correct rules.

---

## 📋 Calorie Calculation Rules

| Activity | Calorie Rate | Formula |
|----------|--------------|---------|
| **running** | 10 cal/min | `duration × 10` |
| **cycling** | 8 cal/min | `duration × 8` |
| **walking** | 5 cal/min | `duration × 5` |
| **others** | 6 cal/min | `duration × 6` |

**Note:** Activity names are stored in lowercase in the database.

---

## 🛠️ Available Scripts

### 1. verify_calories.py

**Purpose:** Check calorie values WITHOUT modifying the database.

**What it does:**
- Reads all workouts from the database
- Calculates correct calories for each workout
- Compares current vs. correct values
- Reports any inconsistencies
- Shows statistics and breakdown by activity

**Usage:**
```bash
cd backend
python verify_calories.py
```

**Example Output:**
```
======================================================================
Verifying Calorie Values in Database
======================================================================

Found 10 workout(s) in database.

Checking calorie values...

======================================================================
⚠️  Found 3 workout(s) with INCORRECT calorie values!
======================================================================

Incorrect workouts:

❌ Workout ID 1:
   User: John Doe
   Activity: running
   Duration: 45 minutes
   Current Calories: 360
   Correct Calories: 450
   Difference: 90

❌ Workout ID 2:
   User: Jane Smith
   Activity: cycling
   Duration: 60 minutes
   Current Calories: 480
   Correct Calories: 480
   Difference: 0

======================================================================
Summary:
======================================================================
  Total workouts: 10
  Correct: 7 (70%)
  Incorrect: 3 (30%)

Breakdown by activity:
  cycling: 3 workout(s) (8 cal/min)
  running: 5 workout(s) (10 cal/min)
  walking: 2 workout(s) (5 cal/min)

======================================================================
💡 To fix incorrect calorie values, run:
   python fix_calories.py
   or
   fix_calories.bat
======================================================================

======================================================================
Verification Complete!
======================================================================
```

---

### 2. fix_calories.py

**Purpose:** Fix incorrect calorie values by updating the database.

**What it does:**
- Reads all workouts from the database
- Calculates correct calories for each workout
- Updates workouts with incorrect values
- Commits changes to the database
- Shows detailed report of changes

**Usage:**
```bash
cd backend
python fix_calories.py
```

**Example Output:**
```
======================================================================
Fixing Calorie Values in Database
======================================================================

Found 10 workout(s) in database.

Analyzing workouts...

❌ Workout ID 1:
   User: John Doe
   Activity: running
   Duration: 45 minutes
   Current Calories: 360
   Correct Calories: 450
   → Updating to 450

❌ Workout ID 3:
   User: Bob Wilson
   Activity: walking
   Duration: 30 minutes
   Current Calories: 120
   Correct Calories: 150
   → Updating to 150

❌ Workout ID 5:
   User: Alice Brown
   Activity: swimming
   Duration: 40 minutes
   Current Calories: 200
   Correct Calories: 240
   → Updating to 240

======================================================================
✅ Database updated successfully!
======================================================================

Summary:
  Total workouts: 10
  Already correct: 7
  Fixed: 3

Breakdown by activity:
  cycling: 3 workout(s) (8 cal/min)
  running: 5 workout(s) (10 cal/min)
  swimming: 1 workout(s) (6 cal/min)
  walking: 1 workout(s) (5 cal/min)

======================================================================
Calorie Fix Complete!
======================================================================
```

---

### 3. fix_calories.bat

**Purpose:** Windows batch file to run fix_calories.py easily.

**What it does:**
- Checks if virtual environment exists
- Activates virtual environment
- Runs fix_calories.py
- Deactivates virtual environment

**Usage:**
```bash
cd backend
fix_calories.bat
```

---

## 📝 Step-by-Step Instructions

### Step 1: Verify Current State

Before making any changes, check if there are any incorrect calorie values:

```bash
cd backend
python verify_calories.py
```

**What to look for:**
- Total number of workouts
- Number of incorrect calorie values
- Which workouts need fixing
- Breakdown by activity type

### Step 2: Backup Database (Optional but Recommended)

Create a backup of your database before making changes:

```bash
cd backend
copy fitness_tracker.db fitness_tracker_backup.db
```

Or on Linux/Mac:
```bash
cd backend
cp fitness_tracker.db fitness_tracker_backup.db
```

### Step 3: Fix Calorie Values

Run the fix script to update incorrect values:

**Option A: Using Python directly**
```bash
cd backend
python fix_calories.py
```

**Option B: Using batch file (Windows)**
```bash
cd backend
fix_calories.bat
```

### Step 4: Verify Fix

After running the fix script, verify that all values are now correct:

```bash
cd backend
python verify_calories.py
```

**Expected output:**
```
======================================================================
✅ All calorie values are CORRECT!
======================================================================
```

### Step 5: Test Application

Start your application and verify workouts display correctly:

```bash
# Start backend
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload

# In another terminal, start frontend
cd frontend
npm run dev
```

Open `http://localhost:5173` and check:
- ✅ All workouts display with correct calorie values
- ✅ Statistics show correct totals
- ✅ New workouts calculate calories correctly

---

## 🔍 Understanding the Scripts

### How Calorie Calculation Works

```python
def calculate_calories(activity: str, duration: int) -> int:
    """
    Calculate calories based on activity type and duration.
    """
    calorie_rates = {
        "running": 10,
        "cycling": 8,
        "walking": 5
    }
    
    # Get calorie rate for activity (default to 6 for unknown activities)
    calorie_rate = calorie_rates.get(activity.lower(), 6)
    
    return duration * calorie_rate
```

**Examples:**
- Running 45 minutes: `45 × 10 = 450 calories`
- Cycling 60 minutes: `60 × 8 = 480 calories`
- Walking 30 minutes: `30 × 5 = 150 calories`
- Swimming 40 minutes: `40 × 6 = 240 calories` (default rate)

### Database Update Process

1. **Read:** Fetch all workouts from database
2. **Calculate:** Compute correct calories for each workout
3. **Compare:** Check if current value matches correct value
4. **Update:** Modify workouts with incorrect values
5. **Commit:** Save all changes to database
6. **Report:** Show summary of changes

---

## ⚠️ Important Notes

### Safety Features

1. **Read-Only Verification:** `verify_calories.py` never modifies the database
2. **Transaction Safety:** `fix_calories.py` uses database transactions (all changes committed together or rolled back on error)
3. **Error Handling:** If an error occurs, all changes are rolled back
4. **Detailed Logging:** Shows exactly what changes are being made

### When to Run These Scripts

Run the fix script when:
- ✅ You've updated the calorie calculation logic in your API
- ✅ You've imported workouts from an external source
- ✅ You've manually edited workout data
- ✅ You suspect calorie values are incorrect
- ✅ After restoring from a backup

### What Gets Updated

The scripts update **ONLY** the `calories` field in the `workouts` table. They do NOT modify:
- ❌ Workout ID
- ❌ User name
- ❌ Activity
- ❌ Duration
- ❌ Any other fields

---

## 🐛 Troubleshooting

### Issue: "No module named 'app'"

**Cause:** Script is not being run from the correct directory.

**Solution:**
```bash
cd backend
python fix_calories.py
```

### Issue: "Unable to open database file"

**Cause:** Database file doesn't exist or is in a different location.

**Solution:**
1. Check if `fitness_tracker.db` exists in the `backend/` directory
2. If not, run `python recreate_db.py` to create it
3. Or run the backend server once to auto-create it

### Issue: "Virtual environment not found" (when using .bat file)

**Cause:** Virtual environment hasn't been created.

**Solution:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Or run:
```bash
setupdev.bat
```

### Issue: Changes not visible in frontend

**Cause:** Frontend is caching old data.

**Solution:**
1. Refresh the frontend page (F5 or Ctrl+R)
2. Click the "🔄 Refresh" button in the WorkoutList component
3. Clear browser cache if needed

---

## 📊 Example Scenarios

### Scenario 1: All Workouts Correct

```bash
$ python verify_calories.py

======================================================================
Verifying Calorie Values in Database
======================================================================

Found 5 workout(s) in database.

Checking calorie values...

======================================================================
✅ All calorie values are CORRECT!
======================================================================

Summary:
  Total workouts: 5
  Correct: 5 (100%)
  Incorrect: 0 (0%)

Breakdown by activity:
  cycling: 2 workout(s) (8 cal/min)
  running: 3 workout(s) (10 cal/min)

======================================================================
Verification Complete!
======================================================================
```

**Action:** No fix needed! ✅

---

### Scenario 2: Some Workouts Incorrect

```bash
$ python verify_calories.py

======================================================================
⚠️  Found 2 workout(s) with INCORRECT calorie values!
======================================================================

Incorrect workouts:

❌ Workout ID 1:
   User: John Doe
   Activity: running
   Duration: 45 minutes
   Current Calories: 360
   Correct Calories: 450
   Difference: 90

❌ Workout ID 3:
   User: Bob Wilson
   Activity: walking
   Duration: 30 minutes
   Current Calories: 120
   Correct Calories: 150
   Difference: 30
```

**Action:** Run `python fix_calories.py` to fix! 🔧

---

### Scenario 3: After Running Fix

```bash
$ python fix_calories.py

======================================================================
Fixing Calorie Values in Database
======================================================================

Found 5 workout(s) in database.

Analyzing workouts...

❌ Workout ID 1:
   User: John Doe
   Activity: running
   Duration: 45 minutes
   Current Calories: 360
   Correct Calories: 450
   → Updating to 450

❌ Workout ID 3:
   User: Bob Wilson
   Activity: walking
   Duration: 30 minutes
   Current Calories: 120
   Correct Calories: 150
   → Updating to 150

======================================================================
✅ Database updated successfully!
======================================================================

Summary:
  Total workouts: 5
  Already correct: 3
  Fixed: 2

======================================================================
Calorie Fix Complete!
======================================================================
```

**Result:** Database updated! ✅

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| **Check for issues** | `python verify_calories.py` |
| **Fix issues** | `python fix_calories.py` |
| **Fix issues (Windows)** | `fix_calories.bat` |
| **Backup database** | `copy fitness_tracker.db fitness_tracker_backup.db` |
| **Restore backup** | `copy fitness_tracker_backup.db fitness_tracker.db` |

---

## ✅ Checklist

Before running fix script:
- [ ] Backend server is stopped (to avoid conflicts)
- [ ] Database backup created (optional but recommended)
- [ ] Verified which workouts need fixing (`verify_calories.py`)

After running fix script:
- [ ] Verified all values are correct (`verify_calories.py`)
- [ ] Tested application (backend + frontend)
- [ ] Checked workout list displays correctly
- [ ] Checked statistics are accurate

---

## 📚 Related Documentation

- **README.md** - Main project documentation
- **TESTING_CHECKLIST.md** - Comprehensive testing guide
- **ERROR_HANDLING_GUIDE.md** - Error handling documentation
- **SDK_FIX_SUMMARY.md** - Python SDK usage guide

---

## 🎉 Summary

You now have three tools to manage calorie values:

1. **verify_calories.py** - Check without modifying ✅
2. **fix_calories.py** - Fix incorrect values 🔧
3. **fix_calories.bat** - Easy Windows execution 🪟

Always verify first, then fix if needed!
