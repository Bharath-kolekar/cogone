# Deployment Guide

## ⚠️ Pre-Deployment Checklist

- [ ] All syntax errors fixed (verify with `python check_all_backend_syntax.py`)
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Frontend restored/rebuilt
- [ ] Database migrations applied
- [ ] Security audit completed

## Current Status

🔴 **NOT READY FOR PRODUCTION**

**Blockers:**
1. Frontend missing/quarantined
2. Architecture consolidation needed (see `ARCHITECTURE_IMPROVEMENT_PLAN.md`)
3. Security audit pending

**Timeline to Production:** 6-8 weeks (see Architecture Improvement Plan)

## Deployment Architecture

### Target Infrastructure

```
┌─────────────────────────────────────────┐
│     Frontend: Vercel (Edge)             │
└─────────────────────────────────────────┘
                    ↓ HTTPS
┌─────────────────────────────────────────┐
│     Backend: Render/AWS ECS             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Database: Supabase (Managed Postgres)  │
│  Cache: Upstash Redis                   │
└─────────────────────────────────────────┘
```

## Deployment Steps (When Ready)

### 1. Database Setup
```bash
# Apply migrations
cd supabase
supabase db push

# Verify tables
supabase db remote status
```

### 2. Backend Deployment (Render)
```bash
# Build Docker image
cd backend
docker build -t cognomega-backend .

# Deploy via Render dashboard or CLI
# Set environment variables in Render
```

### 3. Frontend Deployment (Vercel)
```bash
# After frontend is restored
cd frontend
vercel --prod
```

### 4. DNS Configuration
```bash
# Point domain to Vercel (frontend)
# Point api.domain.com to Render (backend)
```

### 5. SSL/TLS
- Vercel provides automatic HTTPS
- Render provides automatic HTTPS
- Ensure all traffic uses HTTPS

## Environment Variables

### Production Variables

**Backend (Render):**
```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<strong-random-secret-32-chars>
JWT_SECRET=<strong-random-secret-32-chars>
SUPABASE_URL=<production-supabase-url>
SUPABASE_ANON_KEY=<production-anon-key>
SUPABASE_SERVICE_KEY=<production-service-key>
DATABASE_URL=<production-postgres-url>
REDIS_URL=<production-redis-url>
```

**Frontend (Vercel):**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_SUPABASE_URL=<production-supabase-url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<production-anon-key>
```

## Monitoring

Setup after deployment:
- **Error Tracking**: Sentry
- **Metrics**: Datadog or Prometheus
- **Logs**: Structured logging via structlog
- **Uptime**: UptimeRobot or Pingdom

## Rollback Procedure

If deployment fails:
1. **Frontend**: Revert via Vercel dashboard
2. **Backend**: Rollback via Render dashboard
3. **Database**: Use Supabase point-in-time recovery

## Next Steps

Follow the **8-week Architecture Improvement Plan** before attempting production deployment.

---

*Last Updated: October 10, 2025*

