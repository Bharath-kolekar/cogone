# 🪟 Windows Local Setup Guide - CognOmega Platform

Complete guide to build and run the CognOmega AI platform on Windows 10/11.

---

## 📋 Prerequisites

### Required Software

1. **Node.js 18+**
   - Download: https://nodejs.org/
   - Verify installation:
     ```powershell
     node --version  # Should show v18.x or higher
     npm --version
     ```

2. **Python 3.10+**
   - Download: https://www.python.org/downloads/
   - ⚠️ **Important**: Check "Add Python to PATH" during installation
   - Verify installation:
     ```powershell
     python --version  # Should show 3.10 or higher
     pip --version
     ```

3. **Git**
   - Download: https://git-scm.com/download/win
   - Verify installation:
     ```powershell
     git --version
     ```

4. **Visual Studio Code** (Recommended)
   - Download: https://code.microsoft.com/

---

## 🚀 Quick Start (Development Mode)

### Step 1: Clone the Repository

```powershell
# Open PowerShell or Command Prompt
cd C:\
git clone https://github.com/your-username/cogone.git
cd cogone
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```powershell
# Copy the template
copy ENHANCED_ENV_TEMPLATE.md .env

# Open in notepad to edit
notepad .env
```

**Minimum Required Configuration:**

```bash
# Core Settings
SECRET_KEY=your-secret-key-change-this-min-32-chars
ENCRYPTION_KEY=your-encryption-key-change-this-min-32-chars
JWT_SECRET=your-jwt-secret-change-this-min-32-chars
ENVIRONMENT=development
DEBUG=true

# Database - You'll set this up in Step 4
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# Redis - Optional for development (can use in-memory cache)
REDIS_URL=redis://localhost:6379

# AI Provider - Use Groq for free tier (optional for basic testing)
GROQ_API_KEY=your-groq-api-key-optional
LOCAL_AI_ENABLED=true

# Frontend URLs
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Step 3: Install Backend Dependencies

```powershell
# Navigate to backend directory
cd C:\cogone\backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# You should see (venv) in your prompt now

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Common Installation Issues:**

- **If you get SSL errors**: Use `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt`
- **If torch installation fails**: Install CPU-only version: `pip install torch==2.1.1 --index-url https://download.pytorch.org/whl/cpu`
- **If psycopg2 fails**: Install binary version: `pip install psycopg2-binary==2.9.9`

### Step 4: Set Up Database (Supabase)

#### Option A: Cloud Supabase (Recommended for Quick Start)

1. Go to https://supabase.com and create a free account
2. Create a new project (choose a region close to you)
3. Wait 2-3 minutes for the project to be ready
4. Get your credentials:
   - Go to **Settings** > **API**
   - Copy `Project URL` → Use as `SUPABASE_URL`
   - Copy `anon public` key → Use as `SUPABASE_ANON_KEY`
   - Copy `service_role` key → Use as `SUPABASE_SERVICE_KEY`
5. Run database migrations:
   - Go to **SQL Editor**
   - Copy content from `C:\cogone\supabase\schema.sql` (if exists)
   - Run the SQL to create tables

#### Option B: Local PostgreSQL

1. Download PostgreSQL: https://www.postgresql.org/download/windows/
2. Install with default settings (remember the password!)
3. Create database:
   ```powershell
   # Open Command Prompt
   psql -U postgres
   # Enter your password
   CREATE DATABASE cognomega;
   \q
   ```
4. Update `.env`:
   ```bash
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/cognomega
   ```

### Step 5: Set Up Redis (Optional but Recommended)

#### Option A: Upstash Redis (Free Cloud)

1. Go to https://upstash.com and create account
2. Create a new Redis database (free tier)
3. Copy the `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`
4. Add to `.env`:
   ```bash
   UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
   UPSTASH_REDIS_REST_TOKEN=your-token
   ```

#### Option B: Local Redis (Windows)

1. Download Redis for Windows:
   - **Option 1**: Memurai (https://www.memurai.com/get-memurai)
   - **Option 2**: Redis on WSL2
2. Install and start Redis
3. Verify it's running:
   ```powershell
   redis-cli ping
   # Should return: PONG
   ```

#### Option C: Skip Redis (Use In-Memory Cache)

For development, you can run without Redis. The app will use in-memory caching.

### Step 6: Install Local AI (Optional - Ollama)

For local AI processing without API costs:

1. **Download Ollama**:
   - Go to https://ollama.ai/download
   - Download Windows installer
   - Run installer (default settings)

2. **Install AI Model**:
   ```powershell
   # Open new PowerShell window
   ollama serve
   
   # In another PowerShell window
   ollama pull llama3:8b-instruct-q4_K_M
   ```

3. **Verify Installation**:
   ```powershell
   ollama list
   # Should show llama3:8b-instruct-q4_K_M
   ```

4. **Update `.env`**:
   ```bash
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3:8b-instruct-q4_K_M
   LOCAL_AI_ENABLED=true
   ```

### Step 7: Start the Backend

```powershell
# Make sure you're in backend directory with venv activated
cd C:\cogone\backend
.\venv\Scripts\activate

# Start the FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test Backend:**
Open browser and go to:
- http://localhost:8000 - API Status
- http://localhost:8000/docs - Interactive API Documentation
- http://localhost:8000/health - Health Check

### Step 8: Install Frontend Dependencies

**Open a NEW PowerShell window** (keep backend running):

```powershell
# Navigate to frontend
cd C:\cogone\frontend

# Install dependencies
npm install
```

**If you get errors:**
```powershell
# Clear cache and try again
npm cache clean --force
rmdir node_modules -Recurse -Force
del package-lock.json
npm install
```

### Step 9: Start the Frontend

```powershell
# Make sure you're in frontend directory
cd C:\cogone\frontend

# Start Next.js development server
npm run dev
```

**Expected Output:**
```
   ▲ Next.js 14.0.4
   - Local:        http://localhost:3000
   - Environments: .env.local

 ✓ Ready in 2.5s
```

**Access the Application:**
Open your browser and go to: http://localhost:3000

---

## 🎯 What Should Be Running

You should have **2 or 3 terminal windows** running:

1. **Terminal 1 - Backend**:
   ```powershell
   cd C:\cogone\backend
   .\venv\Scripts\activate
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Terminal 2 - Frontend**:
   ```powershell
   cd C:\cogone\frontend
   npm run dev
   ```

3. **Terminal 3 - Ollama** (Optional if using local AI):
   ```powershell
   ollama serve
   ```

---

## 🧪 Testing Your Setup

### Test Backend API

```powershell
# In a new PowerShell window
curl http://localhost:8000/health

# Or open in browser:
# http://localhost:8000/docs
```

### Test Frontend

1. Open http://localhost:3000 in your browser
2. You should see the CognOmega landing page
3. Try creating an account or logging in

### Test Database Connection

```powershell
# In backend directory with venv activated
cd C:\cogone\backend
.\venv\Scripts\activate

# Run a test script (if available)
python -c "from app.core.database import get_database; print('Database connected!')"
```

---

## 📦 Building for Production

### Build Backend

```powershell
cd C:\cogone\backend

# Create optimized requirements
pip freeze > requirements_prod.txt

# Test production startup
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Build Frontend

```powershell
cd C:\cogone\frontend

# Build for production
npm run build

# Test production build
npm run start
```

---

## 🛠️ Common Issues and Solutions

### Issue 1: Python Not Found

**Error**: `python: command not found`

**Solution**:
1. Reinstall Python from https://python.org
2. ✅ Check "Add Python to PATH" during installation
3. Restart PowerShell
4. Verify: `python --version`

### Issue 2: Port Already in Use

**Error**: `Address already in use: 8000` or `3000`

**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different ports:
# Backend
python -m uvicorn app.main:app --reload --port 8001

# Frontend
npm run dev -- --port 3001
```

### Issue 3: Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```powershell
# Make sure venv is activated
cd C:\cogone\backend
.\venv\Scripts\activate

# Should see (venv) in prompt

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 4: Permission Errors

**Error**: `Access is denied` or `Permission denied`

**Solution**:
1. Run PowerShell as Administrator
2. Or change execution policy:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Issue 5: Supabase Connection Failed

**Error**: `Connection to Supabase failed`

**Solution**:
1. Verify credentials in `.env`
2. Check Supabase project is active at https://app.supabase.com
3. Check internet connection
4. Verify firewall isn't blocking connections

### Issue 6: Frontend Can't Connect to Backend

**Error**: `Failed to fetch` or `Network Error`

**Solution**:
1. Verify backend is running: http://localhost:8000/health
2. Check `.env` has correct values:
   ```bash
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
3. Restart frontend after changing `.env`
4. Check CORS settings in backend

### Issue 7: Redis Connection Error

**Error**: `Redis connection failed`

**Solution**:
1. If using local Redis, verify it's running:
   ```powershell
   redis-cli ping
   ```
2. If using Upstash, verify credentials
3. For development, you can comment out Redis and use in-memory cache

### Issue 8: Ollama Not Starting

**Error**: `Ollama server not responding`

**Solution**:
1. Check Windows Defender/Firewall isn't blocking Ollama
2. Run as Administrator
3. Restart Ollama:
   ```powershell
   # Kill existing Ollama
   taskkill /F /IM ollama.exe
   
   # Start again
   ollama serve
   ```

---

## 🔍 Development Tools

### Recommended VS Code Extensions

1. **Python** (ms-python.python)
2. **Pylance** (ms-python.vscode-pylance)
3. **ESLint** (dbaeumer.vscode-eslint)
4. **Prettier** (esbenp.prettier-vscode)
5. **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)
6. **GitLens** (eamodio.gitlens)

### VS Code Configuration

Create `.vscode/settings.json` in project root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}\\backend\\venv\\Scripts\\python.exe",
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

---

## 📊 Monitoring Your Development Environment

### Check Resource Usage

```powershell
# Open Task Manager
taskmgr

# Look for these processes:
# - python.exe (Backend)
# - node.exe (Frontend)
# - ollama.exe (AI)
# - postgres.exe (Database - if local)
# - redis-server.exe (Cache - if local)
```

### Expected Resource Usage

- **Python Backend**: ~300-500 MB RAM
- **Node Frontend**: ~200-400 MB RAM  
- **Ollama (if running)**: ~2-8 GB RAM (depends on model)
- **PostgreSQL (if local)**: ~100-200 MB RAM
- **Redis (if local)**: ~10-50 MB RAM

**Total**: ~3-9 GB RAM required

---

## 🚀 Next Steps

### After Setup is Complete:

1. **Explore the API**:
   - Visit http://localhost:8000/docs
   - Try API endpoints interactively

2. **Test Features**:
   - User registration and login
   - Voice recording (if microphone available)
   - AI code completion
   - Dashboard features

3. **Read Documentation**:
   - `README.md` - Project overview
   - `API_DOCUMENTATION.md` - API reference
   - `DEVELOPMENT_WORKFLOW.md` - Development guidelines

4. **Join Development**:
   - Check `CONTRIBUTING.md` (if exists)
   - Review open issues on GitHub
   - Start building features!

---

## 📝 Quick Reference Commands

### Start Everything (Quick Commands)

```powershell
# Terminal 1 - Backend
cd C:\cogone\backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend  
cd C:\cogone\frontend && npm run dev

# Terminal 3 - Ollama (Optional)
ollama serve
```

### Stop Everything

- Press `CTRL+C` in each terminal window
- Or close all terminal windows

### Reset Everything

```powershell
# Stop all processes first (CTRL+C in all terminals)

# Clean backend
cd C:\cogone\backend
rmdir venv -Recurse -Force
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Clean frontend
cd C:\cogone\frontend
rmdir node_modules -Recurse -Force
del package-lock.json
npm install
```

---

## 🆘 Getting Help

### If You're Still Stuck:

1. **Check logs**:
   - Backend logs in terminal
   - Frontend logs in browser console (F12)
   
2. **Search documentation**:
   - Review all `.md` files in project root
   - Check `backend/README.md` and `frontend/README.md` if they exist

3. **Check GitHub Issues**:
   - Search existing issues
   - Create new issue with error details

4. **Community Support**:
   - Discord/Slack (if available)
   - GitHub Discussions

---

## ✅ Checklist for Successful Setup

- [ ] Python 3.10+ installed and in PATH
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] Project cloned to `C:\cogone`
- [ ] `.env` file created with all required variables
- [ ] Backend dependencies installed (`requirements.txt`)
- [ ] Frontend dependencies installed (`package.json`)
- [ ] Supabase project created and configured
- [ ] Backend starts successfully (http://localhost:8000)
- [ ] Frontend starts successfully (http://localhost:3000)
- [ ] Can access API docs (http://localhost:8000/docs)
- [ ] Can access frontend in browser
- [ ] (Optional) Ollama installed and model downloaded
- [ ] (Optional) Redis installed and running

---

## 🎉 Success!

If you can access both:
- ✅ **Backend**: http://localhost:8000/docs
- ✅ **Frontend**: http://localhost:3000

**Congratulations! Your CognOmega development environment is ready! 🚀**

You're now ready to:
- Develop new features
- Test AI capabilities
- Contribute to the project
- Build amazing voice-to-app solutions

Happy coding! 💻✨
