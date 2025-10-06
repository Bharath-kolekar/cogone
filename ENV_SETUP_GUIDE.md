# 🔧 Environment Variables Setup Guide

**Quick guide to configure your `.env` file for CognOmega platform.**

---

## 📋 Quick Setup

### Step 1: Copy Template

```powershell
# In project root (C:\cogone)
copy env.example .env
```

### Step 2: Edit Configuration

```powershell
notepad .env
```

### Step 3: Fill Required Values

See sections below for what values to use.

---

## ✅ Required Configuration (Minimum to Start)

These are **REQUIRED** to run the application:

### 1. Security Keys

Generate random secure keys (32+ characters):

```powershell
# Generate in PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Replace these in `.env`:
```bash
SECRET_KEY=<your-generated-key-1>
ENCRYPTION_KEY=<your-generated-key-2>
JWT_SECRET=<your-generated-key-3>
```

### 2. Supabase Database (Free)

**Get Free Account**: https://supabase.com

**Steps**:
1. Create account → New Project
2. Wait 2-3 minutes for setup
3. Go to **Settings** → **API**
4. Copy values:

```bash
# From Supabase Dashboard
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Frontend needs these too
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Frontend URLs

For local development, use:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## 🎯 That's It for Basic Setup!

With just these 3 sections configured, you can run the application locally:

```bash
✅ Security keys generated
✅ Supabase configured
✅ Frontend URLs set
```

**Start the app**: See `QUICK_START_WINDOWS.md`

---

## 🚀 Optional Enhancements

These are **OPTIONAL** but recommended for full features:

### AI Provider - Groq (Free Tier)

**Why**: Fast AI responses, free tier available

**Get Free API Key**: https://console.groq.com

```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Local AI - Ollama (Completely Free)

**Why**: No API costs, runs on your PC, works offline

**Setup**:
1. Download: https://ollama.ai/download
2. Install and run:
   ```powershell
   ollama serve
   ollama pull llama3:8b-instruct-q4_K_M
   ```
3. Already configured in template! Just enable:
   ```bash
   LOCAL_AI_ENABLED=true
   ```

### Redis Cache - Upstash (Free Tier)

**Why**: Faster app performance, caching

**Get Free Account**: https://console.upstash.com

```bash
UPSTASH_REDIS_REST_URL=https://xxxxx-xxxxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxx
```

**Or use local Redis**: (if installed)
```bash
REDIS_URL=redis://localhost:6379
```

---

## 📊 Configuration Priority

### For Local Development:

**Must Have** (🔴 Required):
- ✅ Security Keys (SECRET_KEY, etc.)
- ✅ Supabase (Database)
- ✅ Frontend URLs

**Nice to Have** (🟡 Recommended):
- ⭐ Groq API Key (Free tier AI)
- ⭐ Ollama (Local AI)
- ⭐ Redis/Upstash (Caching)

**Optional** (🟢 Advanced):
- OAuth providers (Google, GitHub)
- Payment providers (Razorpay, PayPal)
- Email (SMTP)
- Monitoring (Sentry)

---

## 🔑 How to Get Each Service

### Required Services (Free Forever):

#### Supabase (Database)
- **Website**: https://supabase.com
- **Free Tier**: 500MB database, 2GB bandwidth
- **What to copy**: URL, anon key, service key
- **Where in dashboard**: Settings → API

### Recommended Services (Free Tier):

#### Groq (AI Provider)
- **Website**: https://console.groq.com
- **Free Tier**: Yes, generous limits
- **What to copy**: API Key
- **Where in dashboard**: API Keys section

#### Upstash (Redis)
- **Website**: https://console.upstash.com
- **Free Tier**: 10,000 commands/day
- **What to copy**: REST URL and Token
- **Where in dashboard**: Database details

#### Ollama (Local AI)
- **Website**: https://ollama.ai/download
- **Cost**: Completely FREE (runs on your PC)
- **Setup**: Install → Run → Pull model
- **No sign-up needed**

### Optional Services:

#### Google OAuth
- **Website**: https://console.cloud.google.com
- **Free**: Yes
- **Setup**: Create project → Enable OAuth → Get credentials

#### GitHub OAuth
- **Website**: https://github.com/settings/developers
- **Free**: Yes
- **Setup**: New OAuth App → Get client ID and secret

#### Razorpay (Payments)
- **Website**: https://dashboard.razorpay.com
- **Free**: Test mode free, 2% transaction fee in production
- **Setup**: Create account → API Keys

---

## 📝 Complete Example .env File

Here's a working example with all required values filled:

```bash
# ============================================================================
# MINIMUM WORKING CONFIGURATION
# ============================================================================

# Security Keys (REQUIRED - generate unique values)
SECRET_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
ENCRYPTION_KEY=xyz987wvu654tsr321pon098mlk765jih432gfe109dcb876
JWT_SECRET=qwe456rty789uio012asd345fgh678jkl901zxc234vbn567

# Supabase (REQUIRED - get from supabase.com)
SUPABASE_URL=https://abcdefghijk.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc1NjM5NzgsImV4cCI6MjAxMzEzOTk3OH0.abcdefghijklmnopqrstuvwxyz123456
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5NzU2Mzk3OCwiZXhwIjoyMDEzMTM5OTc4fQ.xyz987654321abcdefghijklmnopqrstuv

# Frontend URLs (REQUIRED for Next.js)
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijk.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc1NjM5NzgsImV4cCI6MjAxMzEzOTk3OH0.abcdefghijklmnopqrstuvwxyz123456
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
DEBUG=true

# Optional: Groq AI (RECOMMENDED - free tier)
GROQ_API_KEY=gsk_abcdefghijklmnopqrstuvwxyz1234567890

# Optional: Local AI (RECOMMENDED - completely free)
LOCAL_AI_ENABLED=true
OLLAMA_HOST=http://localhost:11434

# Optional: Redis Cache (RECOMMENDED)
UPSTASH_REDIS_REST_URL=https://abcd-1234.upstash.io
UPSTASH_REDIS_REST_TOKEN=AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz

# ... rest of the optional settings from env.example
```

---

## ⚠️ Important Security Notes

### DO:
- ✅ Generate unique, random keys for each environment
- ✅ Keep `.env` file in `.gitignore`
- ✅ Use different keys for development/production
- ✅ Store production keys securely (1Password, etc.)

### DON'T:
- ❌ Commit `.env` file to Git
- ❌ Share your keys publicly
- ❌ Use the same keys for dev and production
- ❌ Use example keys in production

---

## 🧪 Testing Your Configuration

### Test Backend Connection:

```powershell
# Start backend
cd C:\cogone\backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000

# In browser, check:
# http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-06T12:00:00Z"
}
```

### Test Frontend Connection:

```powershell
# Start frontend
cd C:\cogone\frontend
npm run dev

# In browser, check:
# http://localhost:3000
```

**Expected**: Landing page loads successfully

### Test Database Connection:

```powershell
# In backend terminal
cd C:\cogone\backend
.\venv\Scripts\activate
python -c "from app.core.database import get_database; print('✅ Database connected!')"
```

---

## 🐛 Troubleshooting

### Error: "SUPABASE_URL not found"

**Fix**: Make sure `.env` file exists in project root:
```powershell
ls C:\cogone\.env
```

If not found:
```powershell
copy env.example .env
notepad .env
```

### Error: "Invalid API key"

**Fix**: Check you copied the complete key including any trailing characters

### Error: "Cannot connect to Supabase"

**Fix**: 
1. Verify project is active at https://app.supabase.com
2. Check firewall isn't blocking connections
3. Verify keys are correct (re-copy from dashboard)

### Error: "Module not found"

**Fix**: Backend dependencies not installed:
```powershell
cd C:\cogone\backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📚 Additional Resources

- **Full Setup Guide**: `WINDOWS_LOCAL_SETUP_GUIDE.md`
- **Quick Start**: `QUICK_START_WINDOWS.md`
- **Template File**: `env.example`
- **API Documentation**: http://localhost:8000/docs (when running)

---

## ✅ Configuration Checklist

Before starting the application, verify:

- [ ] `.env` file exists in `C:\cogone`
- [ ] All REQUIRED variables are filled
- [ ] Security keys are unique (not from example)
- [ ] Supabase credentials are correct
- [ ] Frontend URLs point to localhost
- [ ] Supabase project is active online
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed

If all checked, you're ready to run:
```powershell
# Terminal 1: Backend
cd C:\cogone\backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd C:\cogone\frontend
npm run dev
```

---

**Last Updated**: October 6, 2025  
**Version**: 1.0.0
