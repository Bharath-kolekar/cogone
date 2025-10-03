# Deployment Guide - Voice-to-App SaaS Platform

## 🎯 **Latest Updates (October 2025)**

### **Consolidated AI Agent System**
- **Real Accuracy Validation**: Production-ready validation for 98%, 99%, 100% accuracy levels
- **Advanced Monitoring**: Real-time accuracy monitoring and enforcement
- **Autonomous Capabilities**: Self-managing, self-optimizing, self-healing AI systems
- **Zero-Cost Infrastructure**: Local AI models with free-tier cloud services
- **Consolidated Services**: Single, optimized service handling all AI agent functionality

## Overview
This guide covers the complete deployment process for the Voice-to-App SaaS Platform across different environments.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Vercel)      │◄──►│   (Render)      │◄──►│   (Supabase)    │
│   Next.js       │    │   FastAPI       │    │   PostgreSQL    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN           │    │   Redis Cache   │    │   Storage       │
│   (Vercel Edge) │    │   (Upstash)     │    │   (Supabase)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Models     │    │   Accuracy      │    │   Monitoring    │
│   (Local/Cloud) │    │   Validation    │    │   (Real-time)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Environment Setup

### 1. Supabase Setup
1. Create a new Supabase project
2. Run the database schema:
   ```sql
   -- Apply schema from supabase/schema.sql
   ```
3. Enable Row Level Security (RLS) for all tables
4. Configure authentication settings
5. Set up storage buckets for file uploads

**Required Environment Variables**:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### 2. Redis Setup (Upstash)
1. Create Upstash Redis database
2. Configure connection settings
3. Set up persistence and backups

**Required Environment Variables**:
```bash
REDIS_URL=redis://username:password@host:port
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your_token
```

### 3. Payment Providers Setup

#### Stripe
1. Create Stripe account and get API keys
2. Configure webhook endpoints
3. Set up products and pricing

**Required Environment Variables**:
```bash
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

#### Razorpay
1. Create Razorpay account
2. Get API keys from dashboard
3. Configure webhook settings

**Required Environment Variables**:
```bash
RAZORPAY_KEY_ID=rzp_live_xxx
RAZORPAY_KEY_SECRET=your_secret
```

## Frontend Deployment (Vercel)

### 1. Vercel Setup
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project root
cd frontend
vercel --prod
```

### 2. Environment Variables (Vercel Dashboard)
```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

### 3. Custom Domain Setup
1. Add domain in Vercel dashboard
2. Configure DNS records
3. Enable SSL certificate

### 4. Build Configuration
```javascript
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "functions": {
    "pages/api/**/*.ts": {
      "runtime": "nodejs18.x"
    }
  }
}
```

## Backend Deployment (Render)

### 1. Render Setup
1. Connect GitHub repository to Render
2. Create new Web Service
3. Configure build and start commands

### 2. Build Configuration
```yaml
# render.yaml
services:
  - type: web
    name: voice-to-app-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SUPABASE_URL
        value: https://your-project.supabase.co
      - key: SUPABASE_SERVICE_ROLE_KEY
        value: your_service_role_key
      - key: REDIS_URL
        value: redis://your-redis-url
      - key: SECRET_KEY
        value: your_secret_key
```

### 3. Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Authentication
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Redis
REDIS_URL=redis://username:password@host:port

# Payment Providers
STRIPE_SECRET_KEY=sk_live_xxx
RAZORPAY_KEY_ID=rzp_live_xxx
RAZORPAY_KEY_SECRET=your_secret

# External Services
OPENAI_API_KEY=sk-xxx
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
```

### 4. Docker Deployment (Alternative)
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - redis
      - db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
```

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
```

## Monitoring and Logging

### 1. Sentry Integration
```python
# backend/app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your_sentry_dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

### 2. Health Checks
```python
# backend/app/routers/health.py
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
```

### 3. Logging Configuration
```python
# backend/app/core/logging.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)
```

## Security Considerations

### 1. Environment Variables
- Never commit sensitive data to version control
- Use secure secret management
- Rotate keys regularly
- Use different keys for different environments

### 2. Database Security
- Enable RLS on all tables
- Use connection pooling
- Regular backups
- Monitor access logs

### 3. API Security
- Rate limiting
- Input validation
- CORS configuration
- HTTPS enforcement

### 4. Authentication
- JWT token expiration
- Secure cookie settings
- 2FA enforcement for admin users
- Regular security audits

## Backup and Recovery

### 1. Database Backups
```bash
# Automated daily backups
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore from backup
psql $DATABASE_URL < backup_20251003.sql
```

### 2. File Storage Backups
- Supabase storage automatic backups
- Regular export of user data
- Disaster recovery procedures

### 3. Configuration Backups
- Version control all configuration
- Document all environment variables
- Regular infrastructure audits

## Performance Optimization

### 1. Frontend Optimization
- Next.js automatic optimization
- Image optimization
- Code splitting
- CDN caching

### 2. Backend Optimization
- Database indexing
- Query optimization
- Redis caching
- Connection pooling

### 3. Monitoring
- Response time monitoring
- Error rate tracking
- Resource usage monitoring
- User experience metrics

## Troubleshooting

### Common Issues

#### 1. Build Failures
```bash
# Check Node.js version
node --version

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

#### 2. Database Connection Issues
```bash
# Test database connection
psql $DATABASE_URL -c "SELECT 1;"

# Check connection pool settings
# Verify environment variables
```

#### 3. Redis Connection Issues
```bash
# Test Redis connection
redis-cli -u $REDIS_URL ping

# Check Redis memory usage
redis-cli -u $REDIS_URL info memory
```

### Log Analysis
```bash
# Backend logs
tail -f app.log

# Frontend build logs
vercel logs --follow

# Database logs
# Check Supabase dashboard
```

## Rollback Procedures

### 1. Frontend Rollback
```bash
# Vercel rollback
vercel rollback [deployment-url]

# Manual rollback
git checkout previous-commit
vercel --prod
```

### 2. Backend Rollback
```bash
# Render rollback
# Use Render dashboard to rollback to previous deployment

# Manual rollback
git checkout previous-commit
# Trigger new deployment
```

### 3. Database Rollback
```bash
# Restore from backup
psql $DATABASE_URL < backup_previous_version.sql
```

## Scaling Considerations

### 1. Horizontal Scaling
- Load balancer configuration
- Multiple backend instances
- Database read replicas
- CDN optimization

### 2. Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching strategies
- Monitor resource usage

### 3. Cost Optimization
- Monitor usage patterns
- Optimize resource allocation
- Use reserved instances
- Regular cost reviews

---
**Last Updated**: October 3, 2025  
**Version**: 1.0
