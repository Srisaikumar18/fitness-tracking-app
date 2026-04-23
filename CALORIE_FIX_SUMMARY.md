# 🔧 Calorie Fix - Quick Summary

## What Was Created

Three scripts to fix inconsistent calorie values in your database:

### 1. **verify_calories.py** ✅
- **Purpose:** Check calorie values WITHOUT modifying database
- **Usage:** `python backend/verify_calories.py`
- **Output:** Reports which workouts have incorrect calories

### 2. **fix_calories.py** 🔧
- **Purpose:** Fix incorrect calorie values by updating database
- **Usage:** `python backend/fix_calories.py`
- **Output:** Updates database and shows what was changed

### 3. **fix_calories.bat** 🪟
- **Purpose:** Windows batch file to run fix_calories.py easily
- **Usage:** `backend\fix_calories.bat`
- **Output:** Same as fix_calories.py

---

## Quick Start

### Step 1: Check for Issues
```bash
cd backend
python verify_calories.py
```

### Step 2: Fix Issues (if any found)
```bash
python fix_calories.py
```

### Step 3: Verify Fix
```bash
python verify_calories.py
```

Expected output: `✅ All calorie values are CORRECT!`

---

## Calorie Calculation Rules

| Activity | Rate | Example |
|----------|------|---------|
| running | 10 cal/min | 45 min = 450 cal |
| cycling | 8 cal/min | 60 min = 480 cal |
| walking | 5 cal/min | 30 min = 150 cal |
| others | 6 cal/min | 40 min = 240 cal |

---

## Example Output

### verify_calories.py (when issues found)
```
======================================================================
⚠️  Found 3 workout(s) with INCORRECT calorie values!
======================================================================

❌ Workout ID 1:
   User: John Doe
   Activity: running
   Duration: 45 minutes
   Current Calories: 360
   Correct Calories: 450
   Difference: 90

Summary:
  Total workouts: 10
  Correct: 7 (70%)
  Incorrect: 3 (30%)

💡 To fix incorrect calorie values, run:
   python fix_calories.py
```

### fix_calories.py (fixing issues)
```
======================================================================
Fixing Calorie Values in Database
======================================================================

❌ Workout ID 1:
   User: John Doe
   Activity: running
   Duration: 45 minutes
   Current Calories: 360
   Correct Calories: 450
   → Updating to 450

======================================================================
✅ Database updated successfully!
======================================================================

Summary:
  Total workouts: 10
  Already correct: 7
  Fixed: 3
```

---

## Safety Features

- ✅ **verify_calories.py** never modifies database (read-only)
- ✅ **fix_calories.py** uses transactions (all-or-nothing updates)
- ✅ Error handling with automatic rollback
- ✅ Detailed logging of all changes
- ✅ Shows before/after values

---

## Files Created

1. ✅ `backend/verify_calories.py` - Verification script
2. ✅ `backend/fix_calories.py` - Fix script
3. ✅ `backend/fix_calories.bat` - Windows batch file
4. ✅ `CALORIE_FIX_GUIDE.md` - Comprehensive guide
5. ✅ `CALORIE_FIX_SUMMARY.md` - This quick summary

---

## When to Use

Run these scripts when:
- You've updated calorie calculation logic
- You've imported workouts from external source
- You suspect calorie values are incorrect
- After restoring from backup
- Before submitting your project (to ensure consistency)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named 'app'" | Run from `backend/` directory |
| "Unable to open database file" | Check `fitness_tracker.db` exists |
| "Virtual environment not found" | Run `setupdev.bat` first |
| Changes not visible | Refresh frontend page |

---

## Complete Documentation

For detailed instructions, examples, and troubleshooting, see:
📖 **CALORIE_FIX_GUIDE.md**

---

## Quick Reference Commands

```bash
# Check for issues
cd backend
python verify_calories.py

# Fix issues
python fix_calories.py

# Or use batch file (Windows)
fix_calories.bat

# Backup database first (optional)
copy fitness_tracker.db fitness_tracker_backup.db
```

---

## ✅ Done!

Your database calorie values can now be easily verified and fixed! 🎉
