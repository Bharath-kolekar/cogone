# 🚀 Zero-Cost Deployment Guide for CognOmega

## Complete guide to deploy your Super Intelligent AI Coding System for $0-5/month

---

## 📋 Prerequisites

### Required Accounts (All FREE):
1. ✅ **GitHub** - For CI/CD (you already have)
2. ✅ **Supabase** - Database + Auth (FREE tier)
3. ✅ **Upstash** - Redis cache (FREE tier)
4. ✅ **Groq** - AI API (FREE for developers)
5. ✅ **Railway** - Backend hosting (FREE $5 credit)
6. ✅ **Vercel** - Frontend hosting (FREE)

### Optional:
- **Together AI** - You have $5 credit
- **Render** - Alternative to Railway (FREE 750 hrs/month)
- **Cloudflare** - CDN (FREE)

---

## 🎯 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ZERO-COST STACK                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Frontend (Next.js)                                         │
│  ├─ Vercel (FREE)                                          │
│  └─ Cloudflare CDN (FREE)                                  │
│                                                             │
│  Backend (FastAPI)                                          │
│  ├─ Railway (FREE $5 credit) - Primary                     │
│  └─ Render (FREE 750 hrs) - Backup                         │
│                                                             │
│  Database                                                   │
│  └─ Supabase Postgres (FREE 500MB)                         │
│                                                             │
│  Cache/Queue                                                │
│  └─ Upstash Redis (FREE 10k commands/day)                  │
│                                                             │
│  AI Processing                                              │
│  ├─ Groq API (FREE) - Primary                              │
│  ├─ Together AI ($5 credit) - Secondary                    │
│  └─ Local Ollama (FREE) - Fallback                         │
│                                                             │
│  Total Cost: $0/month                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Deployment

### Step 1: Set Up Supabase (Database)

1. Go to [https://supabase.com](https://supabase.com)
2. Create new project (FREE tier)
3. Note your credentials:
   - Project URL: `https://xxxxx.supabase.co`
   - Anon Key: `eyJhbGc...`
   - Service Role Key: `eyJhbGc...`

4. Run database migrations:
```sql
-- In Supabase SQL Editor, create tables:
-- (Your existing Supabase schema)
```

---

### Step 2: Set Up Upstash Redis (Cache)

1. Go to [https://upstash.com](https://upstash.com)
2. Create new Redis database (FREE tier)
3. Select region closest to your users
4. Note your credentials:
   - Redis URL: `rediss://xxxxx.upstash.io:6379`
   - REST URL: `https://xxxxx.upstash.io`
   - REST Token: `xxxxx`

---

### Step 3: Set Up Groq API (AI)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (FREE for developers)
3. Create API key
4. Note your key: `gsk_xxxxx`

**Groq Free Tier:**
- Unlimited requests during beta
- Fast inference (300+ tokens/sec)
- Models: Llama 2 70B, Mixtral, etc.

---

### Step 4: Set Up Railway (Backend Hosting)

1. Go to [https://railway.app](https://railway.app)
2. Sign up with GitHub (FREE $5 credit/month)
3. Create new project
4. Note your project ID

**Railway Free Tier:**
- $5 credit/month
- ~500 hours runtime
- 512 MB RAM
- 1 GB storage

---

### Step 5: Set Up Vercel (Frontend Hosting)

1. Go to [https://vercel.com](https://vercel.com)
2. Sign up with GitHub (FREE)
3. Import your repository
4. Note your project details

**Vercel Free Tier:**
- Unlimited deployments
- 100 GB bandwidth/month
- Automatic HTTPS
- Edge network

---

### Step 6: Configure Environment Variables

1. Copy the template:
```bash
cp env.zerocost.template .env
```

2. Fill in your credentials:
```bash
# Edit .env with your actual values
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
REDIS_URL=rediss://your-upstash-url:6379
GROQ_API_KEY=gsk_your-groq-key
TOGETHER_API_KEY=your-together-key
```

3. Set GitHub Secrets (for CI/CD):
   - Go to: Repository → Settings → Secrets → Actions
   - Add all secrets from `.env`

---

### Step 7: Deploy Backend to Railway

**Option A: Using Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up

# Set environment variables
railway variables set ZERO_COST_MODE=true
railway variables set GROQ_API_KEY=your-key
# ... (set all variables)
```

**Option B: Using GitHub Actions (Automatic)**
```bash
# Just push to main branch
git add .
git commit -m "Deploy to Railway"
git push origin main

# GitHub Actions will automatically deploy!
```

---

### Step 8: Deploy Frontend to Vercel

**Option A: Using Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod
```

**Option B: Using GitHub Integration (Automatic)**
1. Go to [https://vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure:
   - Framework: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your Railway backend URL
   - `NEXT_PUBLIC_SUPABASE_URL`: Your Supabase URL
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Your Supabase anon key
5. Deploy!

---

### Step 9: Verify Deployment

1. **Check Backend Health:**
```bash
curl https://your-railway-app.railway.app/health
```

2. **Check Frontend:**
```bash
# Visit your Vercel URL
https://your-app.vercel.app
```

3. **Test API:**
```bash
curl https://your-railway-app.railway.app/docs
```

4. **Test Voice-to-App:**
- Open frontend
- Click "Voice to App"
- Speak: "Create a todo app"
- Watch it generate!

---

## 📊 Resource Usage Monitoring

### Railway Dashboard:
- Monitor CPU, RAM, bandwidth usage
- Check $5 credit consumption
- View logs and metrics

### Supabase Dashboard:
- Monitor database size (limit: 500 MB)
- Check bandwidth usage (limit: 2 GB/month)
- View active users

### Upstash Dashboard:
- Monitor Redis commands (limit: 10k/day)
- Check memory usage
- View connection stats

### Groq Dashboard:
- Monitor API usage (unlimited during beta)
- Check response times
- View model usage

---

## 🎯 Optimization Tips for Zero-Cost

### 1. Reduce Database Queries
```python
# Use caching aggressively
# Already implemented in your system!
```

### 2. Batch AI Requests
```python
# Use Groq's batch API when possible
# Fallback to Together AI for heavy loads
```

### 3. Optimize Images and Assets
```python
# Use Cloudflare CDN for static assets
# Compress images before upload
```

### 4. Monitor Free Tier Limits
```bash
# Check daily usage
railway status
# View logs
railway logs
```

---

## 🚨 Staying Within Free Tier Limits

### Railway ($5 credit/month):
- **Limit:** ~500 hours runtime
- **Strategy:** Sleep during low-traffic hours
- **Monitor:** `railway status`

### Supabase (500 MB database):
- **Limit:** 500 MB storage
- **Strategy:** Archive old data, compress logs
- **Monitor:** Dashboard → Database size

### Upstash Redis (10k commands/day):
- **Limit:** 10,000 commands/day
- **Strategy:** Use memory cache first, Redis second
- **Monitor:** Dashboard → Daily commands

### Groq API (Unlimited during beta):
- **Limit:** None currently
- **Strategy:** Use as primary AI provider
- **Monitor:** Console → Usage stats

---

## 🔄 CI/CD Workflows Created

### 1. `deploy-backend.yml`
- Runs on push to main
- Tests → Deploy to Railway → Health check
- Automatic deployment

### 2. `deploy-frontend.yml`
- Runs on push to main
- Build → Deploy to Vercel
- Automatic deployment

### 3. `ci-tests.yml`
- Runs on every PR
- Linting, testing, security scans
- Quality gates

### 4. `zero-cost-optimization.yml`
- Runs daily
- Checks resource usage
- Generates optimization reports

---

## 🎉 Deployment Complete!

Your system is now:
- ✅ Deployed on zero-cost infrastructure
- ✅ Automatically deployed via CI/CD
- ✅ Monitored for resource usage
- ✅ Optimized for minimal hardware
- ✅ Running on 4-8 cores, 8-16 GB RAM

### Access Your System:
- **Frontend:** https://your-app.vercel.app
- **Backend API:** https://your-app.railway.app
- **API Docs:** https://your-app.railway.app/docs
- **Admin:** https://your-app.vercel.app/admin

### Total Monthly Cost: **$0** 🎉

---

## 📈 Next Steps

1. **Monitor Usage:** Check dashboards daily for first week
2. **Optimize Queries:** Use built-in caching and optimization
3. **Scale When Needed:** Upgrade to paid tiers only when necessary
4. **Add Features:** All features work on zero-cost infrastructure!

---

## 🆘 Troubleshooting

### Backend not starting on Railway:
```bash
railway logs
# Check for missing environment variables
```

### Frontend build failing:
```bash
cd frontend
npm run build
# Check for TypeScript errors
```

### Database connection issues:
```bash
# Verify Supabase URL and keys in Railway dashboard
railway variables
```

### Redis connection issues:
```bash
# Verify Upstash URL format: rediss:// (with double 's')
```

---

## 💰 Cost Breakdown

| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| Railway | $5 credit | Backend hosting | $0 |
| Vercel | Unlimited | Frontend | $0 |
| Supabase | 500 MB | Database | $0 |
| Upstash | 10k cmds/day | Cache | $0 |
| Groq | Unlimited | AI API | $0 |
| Together AI | $5 credit | Backup AI | $0 |
| **Total** | | | **$0/month** |

**Estimated capacity:** 100-1000 users, 3000-5000 requests/day

---

## 🚀 You're Live!

Your Super Intelligent AI Coding System is now running on zero-cost infrastructure! 🎉
