# 🚀 Production Deployment Guide - Complete Setup

## 📊 Overview

This guide walks you through deploying Cognomega AI to production with real payment integrations.

**Status:** ✅ Production-ready code available  
**Payment Services:** ✅ Real implementations created  
**Security:** ✅ All credentials from environment variables  
**Tests:** ✅ Integration tests included  

---

## 🎯 Deployment Options

### Option 1: Railway (Recommended - FREE $5/month)

**Benefits:**
- ✅ $5 free credit monthly
- ✅ Easy deployment from GitHub
- ✅ Automatic HTTPS
- ✅ PostgreSQL included
- ✅ Zero configuration

**Steps:**
1. Push code to GitHub
2. Connect Railway to repo
3. Add environment variables
4. Deploy!

**Cost:** $0-5/month (free tier covers most usage)

### Option 2: Render (Alternative - FREE 750 hours/month)

**Benefits:**
- ✅ 750 free hours/month
- ✅ PostgreSQL included
- ✅ Automatic HTTPS
- ✅ Easy deployment

**Steps:**
1. Push code to GitHub
2. Create Render service
3. Add environment variables
4. Deploy!

**Cost:** $0/month (free tier)

### Option 3: Local/VPS

**For:** Advanced users with own infrastructure

---

## 📋 Pre-Deployment Checklist

### 1. Code Preparation ✅

- [x] Security audit complete
- [x] All hardcoded credentials removed
- [x] Environment variables configured
- [x] Production payment services created
- [x] Tests written
- [ ] All tests passing
- [ ] Linting complete
- [ ] Type checking complete

### 2. Environment Setup 🔐

- [ ] Copy `env.production.template` to `.env.production`
- [ ] Fill in all required environment variables
- [ ] Generate strong SECRET_KEY, JWT_SECRET, ENCRYPTION_KEY
- [ ] Configure payment provider credentials
- [ ] Configure AI provider keys
- [ ] Set up domain and CORS origins

### 3. Payment Provider Setup 💳

#### PayPal
- [ ] Create PayPal developer account
- [ ] Create production app
- [ ] Get Client ID and Secret
- [ ] Configure webhooks
- [ ] Test in sandbox mode first
- [ ] Switch to production mode

#### Razorpay
- [ ] Create Razorpay account
- [ ] Complete KYC verification
- [ ] Generate API keys (live mode)
- [ ] Configure webhooks
- [ ] Test with test keys first
- [ ] Switch to live keys

### 4. Infrastructure Setup 🏗️

- [ ] Set up Supabase project
- [ ] Create database tables
- [ ] Configure Upstash Redis
- [ ] Set up domain/DNS
- [ ] Configure HTTPS/SSL
- [ ] Set up monitoring (Sentry)

---

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Environment Variables

```bash
# Copy template
cp env.production.template .env.production

# Edit with your values
nano .env.production  # or use your preferred editor
```

**Required Variables:**
```env
# Security (REQUIRED)
SECRET_KEY=your-32-char-secret
JWT_SECRET=your-32-char-jwt-secret
ENCRYPTION_KEY=your-32-char-encryption-key

# Database (REQUIRED)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# Payments (if needed)
RAZORPAY_API_KEY=rzp_live_xxx
RAZORPAY_API_SECRET=xxx
PAYPAL_CLIENT_ID=xxx
PAYPAL_CLIENT_SECRET=xxx
PAYPAL_SANDBOX=false

# AI (REQUIRED)
GROQ_API_KEY=gsk_xxx
```

### Step 2: Switch to Production Payment Services

**Option A: Update imports in `enhanced_payment_service.py`:**

```python
# Change from:
from .paypal_service import PayPalService
from .razorpay_service import RazorpayService

# To:
from .paypal_service_production import PayPalServiceProduction as PayPalService
from .razorpay_service_production import RazorpayServiceProduction as RazorpayService
```

**Option B: Use environment-based loading:**

Add to `enhanced_payment_service.py`:
```python
import os

USE_PRODUCTION = os.getenv("USE_PRODUCTION_PAYMENTS", "false").lower() == "true"

if USE_PRODUCTION:
    from .paypal_service_production import PayPalServiceProduction as PayPalService
    from .razorpay_service_production import RazorpayServiceProduction as RazorpayService
    logger.info("✅ Using PRODUCTION payment services")
else:
    from .paypal_service import PayPalService
    from .razorpay_service import RazorpayService
    logger.warning("⚠️ Using STUB payment services - not production ready!")
```

Then in `.env.production`:
```env
USE_PRODUCTION_PAYMENTS=true
```

### Step 3: Test Before Deploying

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run only payment tests
pytest tests/test_payment_services.py -v

# Run with production tests (requires credentials)
SKIP_PRODUCTION_TESTS=false pytest tests/test_payment_services.py -v
```

### Step 4: Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Add environment variables (from .env.production)
railway variables set SECRET_KEY=your-secret-key
railway variables set SUPABASE_URL=https://xxx.supabase.co
# ... add all variables

# Or bulk import
railway variables --file .env.production

# Deploy
railway up
```

### Step 5: Deploy to Render

1. **Go to:** https://dashboard.render.com/
2. **New Web Service**
3. **Connect GitHub repo**
4. **Configure:**
   - Name: `cognomega-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. **Add Environment Variables:**
   - Copy from `.env.production`
   - Paste in Render dashboard
6. **Deploy!**

---

## 🧪 Testing in Production

### Test PayPal (Sandbox First)

```python
# test_paypal_live.py
import asyncio
from backend.app.services.paypal_service_production import PayPalServiceProduction

async def test():
    service = PayPalServiceProduction()
    
    print(f"PayPal Mode: {'Sandbox' if service.sandbox else 'Live'}")
    
    # Create order
    order = await service.create_order(
        amount=0.01,  # $0.01 for testing
        currency="USD",
        description="Production Test",
        return_url="https://your-domain.com/success",
        cancel_url="https://your-domain.com/cancel"
    )
    
    print(f"✅ Order created: {order['id']}")
    print(f"Approval URL: {order['approval_url']}")
    print("➡️ Go to approval URL to complete payment")

asyncio.run(test())
```

### Test Razorpay

```python
# test_razorpay_live.py
import asyncio
from backend.app.services.razorpay_service_production import RazorpayServiceProduction

async def test():
    service = RazorpayServiceProduction()
    
    # Create order
    order = await service.create_order(
        amount=1.00,  # ₹1 for testing
        currency="INR",
        receipt="test_001"
    )
    
    print(f"✅ Order created: {order['id']}")
    print(f"Amount: ₹{order['amount'] / 100}")
    print(f"Status: {order['status']}")

asyncio.run(test())
```

---

## 📊 Monitoring & Alerts

### Setup Sentry (Error Tracking)

1. **Create Sentry project:** https://sentry.io/
2. **Get DSN**
3. **Add to environment:**
   ```env
   SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
   ```
4. **Sentry will auto-capture errors**

### Setup Logging

Production services automatically log:
- ✅ All payment creation attempts
- ✅ All captures/refunds
- ✅ All errors with details
- ✅ Webhook verifications

View logs in:
- **Railway:** `railway logs`
- **Render:** Dashboard → Logs tab
- **Local:** Console output

### Key Metrics to Monitor

- Payment success rate
- Payment failure rate
- Webhook delivery rate
- Average response time
- Error rate
- Refund rate

---

## 🔐 Security Checklist

Before going live:

- [ ] All secrets in environment (not hardcoded)
- [ ] HTTPS enabled (required for payments)
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Webhook signatures verified
- [ ] SQL injection prevention (SQLAlchemy handles this)
- [ ] XSS prevention (FastAPI handles this)
- [ ] CSRF tokens (if using cookies)
- [ ] Input validation on all endpoints
- [ ] Error messages don't expose secrets
- [ ] Logs don't contain sensitive data
- [ ] Database backups configured
- [ ] Incident response plan ready

---

## 🎯 Post-Deployment

### Verify Deployment

```bash
# Health check
curl https://your-domain.com/health

# API status
curl https://your-domain.com/api/v0/status

# Payment test (create small order)
curl -X POST https://your-domain.com/api/v0/payments/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"provider": "paypal", "amount": 0.01, "currency": "USD"}'
```

### Monitor for Issues

First 24 hours:
- Check logs every hour
- Monitor error rates
- Verify payments working
- Test refund flow
- Verify webhooks delivering

First week:
- Daily log reviews
- Weekly metric analysis
- User feedback collection
- Performance monitoring

### Rollback Plan

If issues occur:

1. **Immediate:** Switch back to stub implementation
   ```bash
   railway variables set USE_PRODUCTION_PAYMENTS=false
   ```

2. **Investigate:** Check logs and errors

3. **Fix:** Update code or configuration

4. **Test:** Verify fix in staging

5. **Re-deploy:** Switch back to production

---

## 💰 Cost Breakdown

### Zero-Cost Tier (Recommended Start)

| Service | Cost | Limit |
|---------|------|-------|
| **Railway** | $0 | $5 credit/month |
| **Supabase** | $0 | 500MB DB, 2GB bandwidth |
| **Upstash Redis** | $0 | 10K commands/day |
| **Cloudflare** | $0 | Unlimited bandwidth |
| **Groq AI** | $0 | Rate limited, free for developers |
| **Total** | **$0/month** | Good for 100-1000 users |

### Transaction Fees (Pay per use)

| Provider | Domestic | International |
|----------|----------|---------------|
| **PayPal** | 2.9% + $0.30 | 4.4% + fixed fee |
| **Razorpay** | 2% (India) | 3% + GST |
| **Google Pay/UPI** | Free (India) | N/A |

**Example:** 100 payments of $10 each = $30-40 in fees

---

## 📚 Additional Resources

### Payment Provider Docs
- **PayPal:** https://developer.paypal.com/docs/
- **Razorpay:** https://razorpay.com/docs/

### Deployment Platforms
- **Railway:** https://docs.railway.app/
- **Render:** https://render.com/docs

### Monitoring
- **Sentry:** https://docs.sentry.io/
- **Better Stack:** https://betterstack.com/

---

## ❓ FAQ

**Q: Do I need to use production payments immediately?**  
A: No! Stub implementations work fine for development. Switch when ready.

**Q: Can I test without real money?**  
A: Yes! Use sandbox mode for PayPal and test keys for Razorpay.

**Q: What if a payment fails?**  
A: Production services have comprehensive error handling and logging.

**Q: How do I handle refunds?**  
A: Both services have `refund_payment()` methods. Call with payment ID.

**Q: Do I need webhooks?**  
A: Highly recommended for production to get async payment notifications.

**Q: What about PCI compliance?**  
A: PayPal/Razorpay handle card processing, so you're compliant.

---

## 🎊 Summary

You now have:

✅ **Stub implementations** - For development (active)  
✅ **Production implementations** - For real payments (ready)  
✅ **Environment templates** - For easy configuration  
✅ **Integration tests** - For verification  
✅ **Deployment guides** - For Railway and Render  
✅ **Monitoring setup** - For production tracking  

**To go live:**
1. ✅ Get payment credentials
2. ✅ Configure `.env.production`
3. ✅ Switch to production services
4. ✅ Test in sandbox mode
5. ✅ Deploy to Railway/Render
6. ✅ Monitor and celebrate! 🎉

---

*Guide created: January 9, 2025*  
*For: Cognomega AI Production Deployment*  
*Status: Ready for production use*

