# ⚡ Quick Start - Windows (TL;DR)

**The fastest way to get CognOmega running on Windows.**

---

## 🎯 Prerequisites (5 minutes)

1. **Install Python 3.10+**: https://python.org (✅ Check "Add to PATH")
2. **Install Node.js 18+**: https://nodejs.org
3. **Install Git**: https://git-scm.com/download/win

---

## 🚀 One-Time Setup (15-30 minutes)

### 1. Clone & Install

```powershell
# Clone repository
cd C:\
git clone https://github.com/your-username/cogone.git
cd cogone

# Setup Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Setup Frontend (in NEW terminal)
cd C:\cogone\frontend
npm install
```

### 2. Configure Environment

Create `C:\cogone\.env`:

```bash
# Copy from template
copy ENHANCED_ENV_TEMPLATE.md .env

# Edit with notepad
notepad .env
```

**Minimum required values:**

```bash
SECRET_KEY=change-this-to-random-32-chars
ENCRYPTION_KEY=change-this-to-random-32-chars
JWT_SECRET=change-this-to-random-32-chars

# Get these from https://supabase.com (free)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 3. Setup Supabase Database (5 minutes)

1. Go to https://supabase.com → Create free account
2. Create new project → Wait 2-3 minutes
3. Settings → API → Copy credentials to `.env`

---

## 🎬 Daily Usage (30 seconds)

### Start Development (3 terminals)

**Terminal 1 - Backend:**
```powershell
cd C:\cogone\backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd C:\cogone\frontend
npm run dev
```

**Terminal 3 - Ollama (Optional):**
```powershell
ollama serve
```

### Access Application

- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000/docs
- ✅ **Health Check**: http://localhost:8000/health

---

## 🛑 Stop Development

Press `CTRL + C` in each terminal, or close terminal windows.

---

## 🐛 Quick Troubleshooting

### Backend won't start?

```powershell
# Check Python
python --version  # Should be 3.10+

# Reinstall dependencies
cd C:\cogone\backend
.\venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

### Frontend won't start?

```powershell
# Check Node
node --version  # Should be 18+

# Clear and reinstall
cd C:\cogone\frontend
rmdir node_modules -Recurse -Force
del package-lock.json
npm install
```

### Port already in use?

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Python/Node not found?

Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then restart PowerShell and verify:
```powershell
python --version
node --version
```

---

## 📚 Full Documentation

For detailed setup, troubleshooting, and development:
- **Complete Guide**: `WINDOWS_LOCAL_SETUP_GUIDE.md`
- **Project Overview**: `README.md`
- **API Documentation**: http://localhost:8000/docs (when running)

---

## 🎯 Development Workflow

```powershell
# 1. Pull latest changes
git pull origin main

# 2. Update dependencies
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt

cd ../frontend
npm install

# 3. Start development
# Run backend and frontend (see above)

# 4. Make changes
# Edit files in VS Code

# 5. Test changes
# Check browser: http://localhost:3000
# Check API: http://localhost:8000/docs

# 6. Commit changes
git add .
git commit -m "Your descriptive commit message"
git push origin your-branch-name
```

---

## 🔧 Useful Commands

### Backend

```powershell
# Activate virtual environment
cd C:\cogone\backend
.\venv\Scripts\activate

# Run tests
pytest

# Check code style
black .
flake8 .

# Run specific module
python -m app.main
```

### Frontend

```powershell
cd C:\cogone\frontend

# Development mode
npm run dev

# Production build
npm run build
npm run start

# Run tests
npm test

# Lint code
npm run lint

# Type checking
npm run type-check
```

### Database

```powershell
# Run migrations (if using Alembic)
cd C:\cogone\backend
.\venv\Scripts\activate
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

---

## 💡 Pro Tips

### VS Code Multi-Root Workspace

Create `.vscode/cogone.code-workspace`:

```json
{
  "folders": [
    { "path": "backend", "name": "Backend (Python)" },
    { "path": "frontend", "name": "Frontend (Next.js)" }
  ],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder:Backend (Python)}/venv/Scripts/python.exe"
  }
}
```

### PowerShell Aliases (Optional)

Add to your PowerShell profile (`notepad $PROFILE`):

```powershell
# CognOmega aliases
function cog-backend {
  cd C:\cogone\backend
  .\venv\Scripts\activate
  python -m uvicorn app.main:app --reload --port 8000
}

function cog-frontend {
  cd C:\cogone\frontend
  npm run dev
}

function cog-start {
  Start-Process powershell -ArgumentList "-NoExit", "-Command", "cog-backend"
  Start-Process powershell -ArgumentList "-NoExit", "-Command", "cog-frontend"
}
```

Then just run:
```powershell
cog-start
```

### Windows Terminal Configuration

If using Windows Terminal, add to `settings.json`:

```json
{
  "profiles": {
    "list": [
      {
        "name": "CognOmega Backend",
        "commandline": "powershell.exe -NoExit -Command \"cd C:\\cogone\\backend; .\\venv\\Scripts\\activate; python -m uvicorn app.main:app --reload --port 8000\"",
        "icon": "🔧"
      },
      {
        "name": "CognOmega Frontend",
        "commandline": "powershell.exe -NoExit -Command \"cd C:\\cogone\\frontend; npm run dev\"",
        "icon": "🌐"
      }
    ]
  }
}
```

---

## 📊 System Requirements

**Minimum:**
- Windows 10/11
- 4 GB RAM
- 10 GB free disk space
- Internet connection (for cloud services)

**Recommended:**
- Windows 10/11
- 16 GB RAM
- 50 GB free disk space
- SSD drive
- Fast internet connection

---

## ✅ Health Check

Run this to verify everything is working:

```powershell
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# Check if all processes are running
Get-Process | Where-Object {$_.ProcessName -match "python|node|ollama"}
```

---

## 🎉 You're Ready!

**Next Steps:**
1. ✅ Start backend and frontend
2. ✅ Open http://localhost:3000
3. ✅ Create an account
4. ✅ Start building!

**Need help?** Check `WINDOWS_LOCAL_SETUP_GUIDE.md` for detailed troubleshooting.

---

**Last Updated**: October 6, 2025  
**Version**: 1.0.0
