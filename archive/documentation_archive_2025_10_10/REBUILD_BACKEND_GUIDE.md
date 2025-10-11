# 🔧 Backend Rebuild Guide - CognOmega

Complete guide to rebuild the backend from scratch on Windows.

---

## 🎯 Quick Rebuild (5-10 minutes)

### Step 1: Clean Existing Setup

```powershell
# Navigate to backend directory
cd C:\cogone\backend

# Deactivate virtual environment if active
deactivate

# Remove existing virtual environment
Remove-Item -Recurse -Force .venv

# Optional: Clear Python cache
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force
```

### Step 2: Create Fresh Virtual Environment

```powershell
# Still in C:\cogone\backend
python -m venv .venv

# Activate new virtual environment
.\.venv\Scripts\activate

# You should see (.venv) in your prompt

# Upgrade pip to latest version
python -m pip install --upgrade pip
```

### Step 3: Install Dependencies

```powershell
# Install all requirements
pip install -r requirements.txt

# If you get errors, try with cache disabled:
pip install --no-cache-dir -r requirements.txt
```

### Step 4: Verify Installation

```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Verify key packages are installed
pip show fastapi uvicorn supabase
```

### Step 5: Configure Environment

```powershell
# Make sure .env exists in project root
cd C:\cogone
dir .env

# If not found, create it:
copy env.example .env
notepad .env
```

**Required in `.env`**:
```bash
SECRET_KEY=your-secret-key-32-chars-min
ENCRYPTION_KEY=your-encryption-key-32-chars-min
JWT_SECRET=your-jwt-secret-32-chars-min

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

ENVIRONMENT=development
DEBUG=true
```

### Step 6: Test Backend

```powershell
# Make sure you're in backend with venv active
cd C:\cogone\backend
.\.venv\Scripts\activate

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Will watch for changes in these directories: ['C:\\cogone\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 7: Verify Working

Open browser and test:
- ✅ http://localhost:8000/health
- ✅ http://localhost:8000/docs
- ✅ http://localhost:8000/redoc

---

## 🐛 Troubleshooting Common Issues

### Issue 1: "python: command not found"

**Solution**:
```powershell
# Check if Python is in PATH
python --version

# If not found, find Python installation
where python

# Add to PATH or use full path:
C:\Users\YourUsername\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv
```

### Issue 2: "Cannot activate virtual environment"

**Solution**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activation again
.\.venv\Scripts\activate
```

### Issue 3: "pip install fails with SSL errors"

**Solution**:
```powershell
# Install with trusted hosts
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Issue 4: "torch installation fails or takes too long"

**Solution**:
```powershell
# Install CPU-only version (much smaller and faster)
pip install torch==2.1.1 --index-url https://download.pytorch.org/whl/cpu

# Then install remaining dependencies
pip install -r requirements.txt
```

### Issue 5: "psycopg2 installation fails"

**Solution**:
```powershell
# Already using psycopg2-binary which should work
# If still fails, try:
pip install psycopg2-binary==2.9.9 --no-cache-dir
```

### Issue 6: "ModuleNotFoundError when starting server"

**Solution**:
```powershell
# Make sure venv is active
.\.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check if app module exists
dir app\main.py
```

### Issue 7: "Port 8000 already in use"

**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Issue 8: "Supabase connection failed"

**Solution**:
```powershell
# Verify .env file exists and has correct values
cd C:\cogone
notepad .env

# Test connection
cd backend
.\.venv\Scripts\activate
python -c "from app.core.config import settings; print(settings.SUPABASE_URL)"
```

---

## 🧪 Testing Your Backend

### Test 1: Health Check

```powershell
# In browser or PowerShell
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-06T..."
}
```

### Test 2: API Documentation

Open in browser:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

### Test 3: Database Connection

```powershell
cd C:\cogone\backend
.\.venv\Scripts\activate
python -c "from app.core.database import get_database; print('Database connected successfully!')"
```

### Test 4: Import All Modules

```powershell
python -c "from app.main import app; print('All imports successful!')"
```

---

## 📦 Optional: Install Development Tools

```powershell
# Activate venv first
cd C:\cogone\backend
.\.venv\Scripts\activate

# Install development tools
pip install black isort flake8 mypy pytest pytest-asyncio

# Format code
black .

# Sort imports
isort .

# Check code style
flake8 .

# Run tests
pytest
```

---

## 🔄 Clean Rebuild Script

Create a file `rebuild_backend.ps1`:

```powershell
# Save this as: C:\cogone\rebuild_backend.ps1

Write-Host "🔧 Starting Backend Rebuild..." -ForegroundColor Cyan

# Step 1: Navigate to backend
Set-Location C:\cogone\backend

# Step 2: Deactivate if active
try { deactivate } catch {}

# Step 3: Remove old venv
Write-Host "Removing old virtual environment..." -ForegroundColor Yellow
if (Test-Path .venv) {
    Remove-Item -Recurse -Force .venv
}

# Step 4: Clean Python cache
Write-Host "Cleaning Python cache..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force

# Step 5: Create new venv
Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
python -m venv .venv

# Step 6: Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Step 7: Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Step 8: Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Step 9: Verify
Write-Host "Verifying installation..." -ForegroundColor Yellow
pip list

Write-Host "✅ Backend rebuild complete!" -ForegroundColor Green
Write-Host "Run: python -m uvicorn app.main:app --reload --port 8000" -ForegroundColor Cyan
```

**To use**:
```powershell
# Run the script
powershell -ExecutionPolicy Bypass -File C:\cogone\rebuild_backend.ps1
```

---

## 📋 Post-Rebuild Checklist

After rebuilding, verify:

- [ ] Virtual environment created (`.venv` folder exists)
- [ ] Virtual environment activated (see `(.venv)` in prompt)
- [ ] All dependencies installed (`pip list` shows packages)
- [ ] `.env` file configured with required values
- [ ] Backend starts without errors
- [ ] http://localhost:8000/health returns 200 OK
- [ ] http://localhost:8000/docs loads API documentation
- [ ] No import errors in terminal
- [ ] Database connection working (if using Supabase)

---

## 🚀 Quick Commands Reference

```powershell
# Clean rebuild in one go:
cd C:\cogone\backend
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Start backend:
python -m uvicorn app.main:app --reload --port 8000

# In separate terminal - test:
curl http://localhost:8000/health
```

---

## 💡 Pro Tips

### Tip 1: Create Batch File for Easy Start

Create `start_backend.bat`:
```batch
@echo off
cd C:\cogone\backend
call .venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
```

Double-click to start!

### Tip 2: Use VS Code Integrated Terminal

In VS Code:
1. Open `C:\cogone` folder
2. Press `` Ctrl+` `` to open terminal
3. Terminal automatically uses project directory
4. Run commands from there

### Tip 3: Check Requirements Before Installing

```powershell
# See what will be installed
pip install --dry-run -r requirements.txt

# Install only specific packages
pip install fastapi uvicorn supabase
```

### Tip 4: Create Requirements Lock File

```powershell
# After successful install, freeze versions
pip freeze > requirements.lock

# Later, install exact versions
pip install -r requirements.lock
```

---

## 🔍 Verify Installation Details

```powershell
# Check Python location
where python

# Check pip location
where pip

# Check installed packages with versions
pip list --format=freeze

# Check specific package details
pip show fastapi
pip show uvicorn
pip show supabase

# Check virtual environment activation
python -c "import sys; print(sys.prefix)"
# Should show: C:\cogone\backend\.venv
```

---

## 📊 Expected Package List

After successful installation, you should see (among others):

```
fastapi==0.104.1
uvicorn==0.24.0
supabase==2.3.0
pydantic==2.5.0
sqlalchemy==2.0.23
redis==5.0.1
httpx>=0.24.0
python-jose==3.3.0
passlib==1.7.4
transformers==4.36.0
torch==2.1.1
```

---

## ✅ Success Indicators

You know the rebuild worked when:

1. ✅ No errors during `pip install`
2. ✅ Virtual environment activates properly
3. ✅ Server starts with "Application startup complete"
4. ✅ http://localhost:8000/docs shows Swagger UI
5. ✅ http://localhost:8000/health returns healthy status
6. ✅ No module import errors in logs
7. ✅ Can create/read from database (if configured)

---

## 🆘 Still Having Issues?

If rebuild fails:

1. **Check Python version**: Must be 3.10+
   ```powershell
   python --version
   ```

2. **Check available disk space**: Need at least 2GB free
   ```powershell
   Get-PSDrive C
   ```

3. **Check internet connection**: Packages download from PyPI

4. **Try manual install**:
   ```powershell
   pip install fastapi
   pip install uvicorn[standard]
   pip install supabase
   # ... continue with key packages
   ```

5. **Check for antivirus interference**: Some antivirus software blocks pip

6. **Use verbose mode** to see what's failing:
   ```powershell
   pip install -r requirements.txt -vvv
   ```

---

**Need more help?** See [WINDOWS_LOCAL_SETUP_GUIDE.md](WINDOWS_LOCAL_SETUP_GUIDE.md) for detailed troubleshooting.

---

**Last Updated**: October 6, 2025  
**Version**: 1.0.0

