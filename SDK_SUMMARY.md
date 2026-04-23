# Python SDK Generation - Quick Reference

## 🚀 Quick Start (3 Steps)

### Step 1: Generate SDK
```bash
generate_sdk.bat
```

### Step 2: Install SDK
```bash
cd fitness_tracker_sdk
pip install -e .
cd ..
```

### Step 3: Test SDK
```bash
python test_get_workouts.py
python test_post_workout.py
```

---

## 📋 Prerequisites

- ✅ Java 8+ installed
- ✅ Python 3.8+ installed
- ✅ Backend running on http://localhost:8000
- ✅ OpenAPI Generator CLI installed

### Install OpenAPI Generator CLI
```bash
npm install @openapitools/openapi-generator-cli -g
```

---

## 📁 Files Created

### Scripts
- `generate_sdk.bat` - Generate SDK from OpenAPI spec
- `SDK_QUICK_START.bat` - Complete setup (generate + install + test)

### Test Scripts
- `test_get_workouts.py` - Test GET /api/workouts/
- `test_post_workout.py` - Test POST /api/workouts/

### Documentation
- `SDK_GENERATION_GUIDE.md` - Complete step-by-step guide
- `SDK_SUMMARY.md` - This file (quick reference)

---

## 🔧 Manual Commands

### Generate SDK
```bash
# Download OpenAPI spec
curl http://localhost:8000/openapi.json -o openapi.json

# Generate Python SDK
openapi-generator-cli generate ^
  -i openapi.json ^
  -g python ^
  -o fitness_tracker_sdk ^
  --package-name fitness_tracker_client ^
  --additional-properties=projectName=fitness-tracker-sdk,packageVersion=1.0.0
```

### Install SDK
```bash
cd fitness_tracker_sdk
pip install -e .
```

---

## 💻 Usage Examples

### Example 1: Get All Workouts
```python
import fitness_tracker_client
from fitness_tracker_client.api import workouts_api

configuration = fitness_tracker_client.Configuration(
    host="http://localhost:8000"
)

with fitness_tracker_client.ApiClient(configuration) as api_client:
    api = workouts_api.WorkoutsApi(api_client)
    workouts = api.get_workouts_api_workouts_get()
    
    print(f"Total workouts: {len(workouts)}")
    for workout in workouts:
        print(f"{workout.user_name}: {workout.activity} - {workout.duration} min")
```

### Example 2: Create Workout
```python
import fitness_tracker_client
from fitness_tracker_client.api import workouts_api
from fitness_tracker_client.model.workout_create import WorkoutCreate

configuration = fitness_tracker_client.Configuration(
    host="http://localhost:8000"
)

with fitness_tracker_client.ApiClient(configuration) as api_client:
    api = workouts_api.WorkoutsApi(api_client)
    
    new_workout = WorkoutCreate(
        user_name="Jane Doe",
        activity="running",
        duration=45
    )
    
    result = api.create_workout_api_workouts_post(new_workout)
    print(f"Created workout ID: {result.id}")
    print(f"Calories: {result.calories}")
```

---

## 🧪 Test Scripts

### Test GET Endpoint
```bash
python test_get_workouts.py
```

**Output**:
```
================================================================================
Fitness Tracker API - GET Workouts Test
================================================================================

📋 Fetching all workouts...

✅ Success! Retrieved 5 workouts

================================================================================
ID    User Name            Activity        Duration   Calories  
================================================================================
5     Eve Wilson           running         25         250       
4     Diana Prince         swimming        40         240       
3     Charlie Brown        walking         30         150       
2     Bob Smith            cycling         60         480       
1     Alice Johnson        running         45         450       
================================================================================

📊 Statistics:
   Total Workouts: 5
   Total Duration: 200 minutes
   Total Calories: 1570 cal

🏃 Activity Breakdown:
   cycling: 1 workout(s)
   running: 2 workout(s)
   swimming: 1 workout(s)
   walking: 1 workout(s)
```

### Test POST Endpoint
```bash
python test_post_workout.py
```

**Output**:
```
================================================================================
Fitness Tracker API - POST Workout Test
================================================================================

Test 1: Create Single Workout
--------------------------------------------------------------------------------
➕ Creating workout...
   User: John Doe
   Activity: running
   Duration: 30 minutes

✅ Workout created successfully!

================================================================================
Created Workout Details:
================================================================================
ID:           6
User Name:    John Doe
Activity:     running
Duration:     30 minutes
Calories:     300 cal (calculated automatically)
================================================================================

💡 Calorie Calculation:
   Running: 10 cal/min
   30 min × 10 cal/min = 300 cal
```

---

## 🔍 Troubleshooting

### Issue: "openapi-generator-cli: command not found"
**Solution**:
```bash
npm install @openapitools/openapi-generator-cli -g
```

### Issue: "Backend is not running"
**Solution**:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Issue: "Module not found: fitness_tracker_client"
**Solution**:
```bash
cd fitness_tracker_sdk
pip install -e .
cd ..
```

### Issue: "Java not found"
**Solution**: Install Java 8+ from https://www.java.com/download/

---

## 📚 SDK Structure

```
fitness_tracker_sdk/
├── fitness_tracker_client/
│   ├── api/
│   │   └── workouts_api.py          # API methods
│   ├── model/
│   │   ├── workout_create.py        # Input model
│   │   └── workout_response.py      # Output model
│   ├── configuration.py             # API config
│   └── api_client.py                # HTTP client
├── docs/                            # Documentation
├── setup.py                         # Package setup
└── requirements.txt                 # Dependencies
```

---

## 🎯 Key Features

### Automatic Calorie Calculation
The API automatically calculates calories based on activity:

| Activity | Rate | Example (30 min) |
|----------|------|------------------|
| running  | 10 cal/min | 300 calories |
| cycling  | 8 cal/min | 240 calories |
| walking  | 5 cal/min | 150 calories |
| others   | 6 cal/min | 180 calories |

### Activity Standardization
All activities are automatically converted to lowercase:
- Input: `"RUNNING"` → Output: `"running"`
- Input: `"CyClInG"` → Output: `"cycling"`
- Input: `"  Walking  "` → Output: `"walking"`

### Input Validation
- Duration must be > 0
- User name: 1-100 characters
- Activity: 1-100 characters

---

## 📖 Documentation

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### SDK Documentation
- **Complete Guide**: `SDK_GENERATION_GUIDE.md`
- **Project Docs**: `PROJECT_DOCUMENTATION.md`
- **README**: `README.md`

---

## ✅ Verification Checklist

Before using the SDK:
- [ ] Backend is running on http://localhost:8000
- [ ] OpenAPI Generator CLI is installed
- [ ] SDK is generated (`fitness_tracker_sdk/` folder exists)
- [ ] SDK is installed (`pip list | grep fitness`)
- [ ] Test scripts run successfully

---

## 🚀 Next Steps

1. ✅ Generate SDK: `generate_sdk.bat`
2. ✅ Install SDK: `pip install -e fitness_tracker_sdk`
3. ✅ Run tests: `python test_get_workouts.py`
4. ✅ Use SDK in your applications
5. ✅ Distribute SDK to other developers

---

## 📞 Support

For detailed instructions, see:
- `SDK_GENERATION_GUIDE.md` - Complete step-by-step guide
- `PROJECT_DOCUMENTATION.md` - API documentation
- http://localhost:8000/docs - Interactive API docs

---

**Last Updated**: April 2026  
**SDK Version**: 1.0.0  
**Python Version**: 3.8+
