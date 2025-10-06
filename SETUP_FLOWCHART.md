# 🗺️ CognOmega Setup Flowchart

**Visual guide to setting up CognOmega on Windows**

---

## 📊 Setup Process Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    SETUP FLOWCHART                          │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐
│   START      │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Do you have prerequisites installed?   │
│  • Python 3.10+                         │
│  • Node.js 18+                          │
│  • Git                                  │
└─────┬──────────────────────┬────────────┘
      │ NO                   │ YES
      ▼                      ▼
┌──────────────┐      ┌──────────────────┐
│ Install them │      │  Clone Repository│
│ from websites│──────▶│  git clone ...   │
└──────────────┘      └────────┬─────────┘
                               │
                               ▼
                      ┌─────────────────┐
                      │ Create .env file│
                      │ copy env.example│
                      └────────┬────────┘
                               │
                               ▼
                      ┌────────────────────────┐
                      │ Do you have Supabase?  │
                      └──┬──────────────┬──────┘
                         │ NO           │ YES
                         ▼              ▼
              ┌──────────────────┐   ┌──────────────┐
              │ Create Supabase  │   │ Add Supabase │
              │ account (free)   │──▶│ to .env file │
              └──────────────────┘   └──────┬───────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │ Generate secret │
                                   │ keys for .env   │
                                   └────────┬────────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │ Install Backend │
                                   │ Dependencies    │
                                   │ pip install -r  │
                                   └────────┬────────┘
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │ Install Frontend│
                                   │ Dependencies    │
                                   │ npm install     │
                                   └────────┬────────┘
                                            │
                                            ▼
                      ┌─────────────────────────────────┐
                      │ Want optional features?         │
                      │ • Groq API (Free AI)            │
                      │ • Ollama (Local AI)             │
                      │ • Redis (Caching)               │
                      └──┬──────────────────┬───────────┘
                         │ YES              │ NO
                         ▼                  │
              ┌──────────────────┐          │
              │ Setup optional   │          │
              │ services & add   │          │
              │ to .env          │          │
              └─────────┬────────┘          │
                        │                   │
                        └───────┬───────────┘
                                ▼
                        ┌───────────────┐
                        │ Start Backend │
                        │ Port 8000     │
                        └───────┬───────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ Start Frontend│
                        │ Port 3000     │
                        └───────┬───────┘
                                │
                                ▼
                        ┌───────────────────┐
                        │ Test in Browser   │
                        │ localhost:3000    │
                        └───────┬───────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │   SUCCESS!    │
                        │   🎉 Ready    │
                        └───────────────┘
```

---

## 🎯 Decision Tree: Which Guide to Read?

```
                    ┌─────────────────┐
                    │   START HERE    │
                    └────────┬────────┘
                             │
                             ▼
            ┌────────────────────────────────┐
            │ First time setting up?         │
            └─┬──────────────────────────┬───┘
              │ YES                      │ NO
              ▼                          ▼
    ┌──────────────────┐      ┌─────────────────────┐
    │ Read COMPLETE    │      │ Need quick refresh? │
    │ WINDOWS GUIDE    │      └──┬───────────────┬──┘
    └──────────────────┘         │ YES           │ NO
                                 ▼               ▼
                        ┌──────────────┐  ┌─────────────┐
                        │ QUICK START  │  │ Specific    │
                        │ WINDOWS      │  │ issue?      │
                        └──────────────┘  └──┬──────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Troubleshooting │
                                    │ section in docs │
                                    └─────────────────┘
```

---

## 📁 File Structure Overview

```
C:\cogone\
│
├── 📄 env.example              ← COPY THIS to .env
├── 📘 SETUP_SUMMARY.md         ← Start here (overview)
├── 📘 ENV_SETUP_GUIDE.md       ← Environment variables guide
├── 📘 QUICK_START_WINDOWS.md   ← Quick commands
├── 📘 WINDOWS_LOCAL_SETUP_GUIDE.md ← Complete guide
├── 📘 README.md                ← Project features
│
├── backend/
│   ├── requirements.txt        ← Python dependencies
│   ├── app/
│   │   ├── main.py            ← Backend entry point
│   │   ├── routers/           ← API endpoints
│   │   └── services/          ← Business logic
│   └── venv/                  ← Python virtual env (create this)
│
└── frontend/
    ├── package.json           ← Node dependencies
    ├── app/                   ← Next.js app
    ├── components/            ← React components
    └── node_modules/          ← npm packages (auto-created)
```

---

## 🔧 Environment Variables Dependency Map

```
REQUIRED (Must have to start):
    ┌─────────────────┐
    │ Security Keys   │
    │ - SECRET_KEY    │
    │ - ENCRYPTION_KEY│
    │ - JWT_SECRET    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Supabase        │
    │ (Database)      │
    │ - URL           │
    │ - ANON_KEY      │
    │ - SERVICE_KEY   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Frontend URLs   │
    │ - API_URL       │
    │ - APP_URL       │
    └─────────────────┘

RECOMMENDED (Better performance):
    ┌─────────────────┐
    │ Groq API        │
    │ (Free AI)       │
    └─────────────────┘
             │
    ┌────────┼────────┐
    │                 │
    ▼                 ▼
┌─────────┐     ┌──────────┐
│ Ollama  │     │  Redis   │
│(Local AI)│     │(Caching) │
└─────────┘     └──────────┘

OPTIONAL (Advanced features):
    OAuth • Payments • Email • Monitoring
```

---

## 🚦 Setup Status Indicators

### ✅ Everything Working:
```
┌──────────────────────────────────┐
│ ✅ Python 3.10+ installed        │
│ ✅ Node.js 18+ installed         │
│ ✅ Git installed                 │
│ ✅ Repository cloned             │
│ ✅ .env configured               │
│ ✅ Backend deps installed        │
│ ✅ Frontend deps installed       │
│ ✅ Backend running (port 8000)   │
│ ✅ Frontend running (port 3000)  │
│ ✅ Browser shows app             │
└──────────────────────────────────┘
        👆 YOU ARE READY! 🎉
```

### ⚠️ Partial Setup:
```
┌──────────────────────────────────┐
│ ✅ Prerequisites installed       │
│ ✅ Repository cloned             │
│ ⚠️  .env needs configuration     │
│ ⚠️  Dependencies not installed   │
│ ❌ Services not running          │
└──────────────────────────────────┘
   👆 Continue with ENV_SETUP_GUIDE
```

### ❌ Just Starting:
```
┌──────────────────────────────────┐
│ ❌ No prerequisites yet          │
│ ❌ Repository not cloned         │
│ ❌ .env not configured           │
│ ❌ Dependencies not installed    │
│ ❌ Services not running          │
└──────────────────────────────────┘
   👆 Start with WINDOWS_LOCAL_SETUP_GUIDE
```

---

## 🎓 Skill Level Path

### 👶 Complete Beginner
```
Day 1: Install Prerequisites
       └─→ Follow WINDOWS_LOCAL_SETUP_GUIDE
           (Every step explained)

Day 2: Configure Environment
       └─→ Follow ENV_SETUP_GUIDE
           (What each variable means)

Day 3: Start Development
       └─→ Use QUICK_START_WINDOWS
           (Daily commands)
```

### 👨‍💻 Intermediate Developer
```
Step 1: Quick Prerequisites Check
        └─→ Python, Node, Git installed?

Step 2: Setup in 15 minutes
        └─→ Follow QUICK_START_WINDOWS
            (Commands only)

Step 3: Start Coding
        └─→ Refer to README.md
            (Features & API)
```

### 🚀 Advanced Developer
```
1. Copy env.example to .env     (30 sec)
2. Fill required values         (5 min)
3. Run setup commands           (10 min)
4. Start developing             (immediately)

Need help? → Troubleshooting sections
```

---

## 🔄 Daily Development Loop

```
┌─────────────────────────────────────────┐
│          DAILY WORKFLOW                 │
└─────────────────────────────────────────┘

Morning:
  1. Open 2 terminals
  2. Start Backend  (Terminal 1)
  3. Start Frontend (Terminal 2)
  4. Open browser → localhost:3000
  
During Day:
  1. Make code changes
  2. Save files
  3. Hot reload shows changes
  4. Test in browser
  
Evening:
  1. CTRL+C in terminals
  2. Commit changes to Git
  3. Close terminals

Next Day:
  Repeat from Morning
```

---

## 🆘 Troubleshooting Flowchart

```
┌─────────────────┐
│   ERROR?        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Which component failing?    │
└─┬───────┬──────────┬────────┘
  │       │          │
  ▼       ▼          ▼
┌────┐ ┌────┐  ┌─────────┐
│Back│ │Front│  │Database │
│end │ │end  │  │         │
└─┬──┘ └─┬──┘  └────┬────┘
  │      │          │
  ▼      ▼          ▼
Check: Check:   Check:
• venv • npm    • .env
active? installed? • Supabase
• deps  • port   online?
installed? 3000  • Keys
• .env  free?   correct?
loaded?

       ALL FIXED? ────┐
              │       │
              ▼       │
      ┌──────────┐    │
      │ Restart  │    │
      │ Services │    │
      └────┬─────┘    │
           │          │
           ▼          │
      ┌──────────┐    │
      │ Working? │    │
      └─┬────┬───┘    │
        │YES │NO      │
        ▼    └────────┘
    ┌─────────┐
    │ SUCCESS │
    └─────────┘
```

---

## 📊 Time Estimates

| Task | First Time | After That |
|------|-----------|------------|
| Install prerequisites | 15-20 min | N/A |
| Clone & setup | 10-15 min | N/A |
| Configure .env | 10-15 min | 2 min |
| Setup Supabase | 5 min | N/A |
| Install dependencies | 5-10 min | 2 min |
| Start services | 2 min | 30 sec |
| **Total First Time** | **45-60 min** | - |
| **Total Daily** | - | **3-5 min** |

---

## 🎯 Quick Reference Card

```
╔══════════════════════════════════════════╗
║     COGNOMEGA QUICK REFERENCE            ║
╠══════════════════════════════════════════╣
║                                          ║
║  📁 Setup Files:                         ║
║  • env.example        (copy to .env)     ║
║  • SETUP_SUMMARY.md   (overview)         ║
║  • QUICK_START.md     (commands)         ║
║                                          ║
║  🔧 Services:                            ║
║  • Supabase.com       (database)         ║
║  • console.groq.com   (AI - optional)    ║
║  • ollama.ai          (local AI)         ║
║                                          ║
║  🚀 Start Commands:                      ║
║  Backend:  uvicorn app.main:app          ║
║  Frontend: npm run dev                   ║
║                                          ║
║  🌐 Access:                              ║
║  • localhost:3000     (app)              ║
║  • localhost:8000/docs (API)             ║
║                                          ║
║  🆘 Help:                                ║
║  • Check troubleshooting in guides       ║
║  • Verify .env configuration             ║
║  • Check terminal logs                   ║
║                                          ║
╚══════════════════════════════════════════╝
```

---

## 🎉 Success Indicators

You know it's working when:

```
✅ Backend terminal shows:
   "Uvicorn running on http://0.0.0.0:8000"

✅ Frontend terminal shows:
   "Ready in X.Xs"

✅ Browser at localhost:3000 shows:
   CognOmega landing page

✅ Browser at localhost:8000/docs shows:
   Interactive API documentation

✅ No error messages in terminals

✅ You can create an account and log in
```

---

**Navigation**:
- [📘 Complete Setup Guide](WINDOWS_LOCAL_SETUP_GUIDE.md)
- [⚡ Quick Commands](QUICK_START_WINDOWS.md)
- [🔧 Environment Guide](ENV_SETUP_GUIDE.md)
- [📝 Summary](SETUP_SUMMARY.md)

---

**Last Updated**: October 6, 2025
