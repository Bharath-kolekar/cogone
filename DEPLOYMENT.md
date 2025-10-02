# Voice-to-App SaaS Platform - Deployment Guide

This guide covers deploying the Voice-to-App SaaS Platform to production using Vercel (frontend) and Render (backend).

## Prerequisites

- GitHub repository with the code
- Vercel account
- Render account
- Supabase project
- Domain name (optional)

## 1. Environment Setup

### 1.1 Supabase Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Run the database schema:
   ```bash
   # Copy the schema to Supabase SQL editor
   cat supabase/schema.sql
   ```
3. Note down your project URL and API keys from Settings > API

### 1.2 Payment Providers Setup

#### Razorpay (Primary for India)
1. Sign up at [razorpay.com](https://razorpay.com)
2. Get your Key ID and Key Secret from Dashboard > Settings > API Keys
3. Set up webhook endpoint: `https://your-backend-url.com/api/v0/webhooks/razorpay`

#### PayPal (International)
1. Create app at [developer.paypal.com](https://developer.paypal.com)
2. Get Client ID and Client Secret
3. Set up webhook endpoint: `https://your-backend-url.com/api/v0/webhooks/paypal`

#### SMS Provider (Twilio)
1. Sign up at [twilio.com](https://twilio.com)
2. Get Account SID, Auth Token, and Phone Number
3. Verify your phone number for testing

### 1.3 AI Providers (Optional)

#### Hugging Face
1. Create account at [huggingface.co](https://huggingface.co)
2. Generate API token from Settings > Access Tokens

#### Together AI
1. Sign up at [together.ai](https://together.ai)
2. Get API key from dashboard

#### Groq
1. Sign up at [groq.com](https://groq.com)
2. Get API key from console

## 2. Backend Deployment (Render)

### 2.1 Create Render Service

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" > "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `voice-to-app-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`

### 2.2 Environment Variables

Add these environment variables in Render dashboard:

```bash
# Application
SECRET_KEY=your-super-secret-key-32-chars-min
JWT_SECRET=your-jwt-secret-key-32-chars-min
ENCRYPTION_KEY=your-encryption-key-32-chars-min
DEBUG=false
ENVIRONMENT=production

# Database
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
DATABASE_URL=postgres://postgres:password@host:port/database

# Redis
UPSTASH_REDIS_REST_URL=your-upstash-redis-url
UPSTASH_REDIS_REST_TOKEN=your-upstash-redis-token

# Payments
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
RAZORPAY_WEBHOOK_SECRET=your-razorpay-webhook-secret
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
GOOGLE_PAY_MERCHANT_ID=your-google-pay-merchant-id

# SMS
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# AI Providers (Optional)
HF_API_KEY=your-huggingface-api-key
TOGETHER_API_KEY=your-together-api-key
GROQ_API_KEY=your-groq-api-key

# Feature Flags
ALLOW_LOCAL_LLM=true
ENABLE_VOICE_COMMANDS=true
ENABLE_GAMIFICATION=true
ENABLE_REFERRALS=true
ENABLE_TEMPLATES_MARKETPLACE=true
ENABLE_COLLABORATIVE_EDITING=true
```

### 2.3 Deploy Backend

1. Click "Create Web Service"
2. Wait for deployment to complete
3. Note the service URL (e.g., `https://voice-to-app-backend.onrender.com`)

## 3. Frontend Deployment (Vercel)

### 3.1 Create Vercel Project

1. Go to [vercel.com](https://vercel.com) and sign up
2. Click "New Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 3.2 Environment Variables

Add these environment variables in Vercel dashboard:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your-supabase-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# API
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com/api/trpc

# App Configuration
NEXT_PUBLIC_APP_URL=https://your-frontend-url.vercel.app
```

### 3.3 Deploy Frontend

1. Click "Deploy"
2. Wait for deployment to complete
3. Note the deployment URL (e.g., `https://voice-to-app.vercel.app`)

## 4. Webhook Configuration

### 4.1 Razorpay Webhooks

1. Go to Razorpay Dashboard > Settings > Webhooks
2. Add webhook URL: `https://your-backend-url.onrender.com/api/v0/webhooks/razorpay`
3. Select events:
   - `payment.captured`
   - `payment.failed`
   - `subscription.activated`
   - `subscription.cancelled`
4. Copy webhook secret and add to environment variables

### 4.2 PayPal Webhooks

1. Go to PayPal Developer Dashboard > Webhooks
2. Add webhook URL: `https://your-backend-url.onrender.com/api/v0/webhooks/paypal`
3. Select events:
   - `PAYMENT.CAPTURE.COMPLETED`
   - `PAYMENT.CAPTURE.DENIED`
   - `BILLING.SUBSCRIPTION.ACTIVATED`
   - `BILLING.SUBSCRIPTION.CANCELLED`

## 5. Domain Configuration (Optional)

### 5.1 Custom Domain for Frontend

1. In Vercel dashboard, go to your project > Settings > Domains
2. Add your custom domain (e.g., `voice-to-app.com`)
3. Configure DNS records as instructed by Vercel

### 5.2 Custom Domain for Backend

1. In Render dashboard, go to your service > Settings > Custom Domains
2. Add your custom domain (e.g., `api.voice-to-app.com`)
3. Configure DNS records as instructed by Render

## 6. SSL and Security

### 6.1 SSL Certificates

- Vercel automatically provides SSL certificates
- Render automatically provides SSL certificates
- Ensure all custom domains have SSL enabled

### 6.2 Security Headers

The application includes security headers in:
- `frontend/next.config.js` (CORS, security headers)
- `backend/app/main.py` (CORS middleware, security middleware)

## 7. Monitoring and Analytics

### 7.1 Application Monitoring

1. Set up Sentry for error tracking:
   - Add `SENTRY_DSN` to environment variables
   - Sentry will automatically track errors

2. Set up Google Analytics:
   - Add `GOOGLE_ANALYTICS_ID` to environment variables
   - Analytics will be automatically included

### 7.2 Performance Monitoring

- Vercel provides built-in analytics
- Render provides built-in monitoring
- Use Supabase dashboard for database monitoring

## 8. Testing Deployment

### 8.1 Health Checks

Test these endpoints:
- Frontend: `https://your-domain.com`
- Backend: `https://your-backend-url.onrender.com/health`
- API: `https://your-backend-url.onrender.com/api/v0/status`

### 8.2 Feature Testing

1. **Authentication**:
   - Test email OTP signup
   - Test mobile OTP signup
   - Test OAuth (Google, GitHub)

2. **Voice Processing**:
   - Test voice recording
   - Test transcription
   - Test app generation

3. **Payments**:
   - Test Razorpay integration
   - Test PayPal integration
   - Test webhook processing

4. **Gamification**:
   - Test points system
   - Test referrals
   - Test achievements

## 9. Scaling Considerations

### 9.1 Database Scaling

- Supabase automatically scales PostgreSQL
- Monitor connection limits
- Consider read replicas for heavy read workloads

### 9.2 Backend Scaling

- Render automatically scales based on traffic
- Monitor CPU and memory usage
- Consider upgrading to higher tier for production

### 9.3 Frontend Scaling

- Vercel automatically scales with global CDN
- Monitor bandwidth usage
- Consider upgrading for higher limits

## 10. Backup and Recovery

### 10.1 Database Backups

- Supabase provides automatic daily backups
- Set up additional backup strategies if needed
- Test restore procedures regularly

### 10.2 Code Backups

- GitHub provides code versioning
- Set up additional backup strategies for critical data
- Document recovery procedures

## 11. Maintenance

### 11.1 Regular Updates

- Keep dependencies updated
- Monitor security advisories
- Test updates in staging environment first

### 11.2 Performance Optimization

- Monitor Core Web Vitals
- Optimize images and assets
- Use caching strategies effectively

## 12. Troubleshooting

### 12.1 Common Issues

1. **CORS Errors**:
   - Check CORS configuration in backend
   - Verify frontend URL in CORS origins

2. **Database Connection Issues**:
   - Verify Supabase credentials
   - Check connection limits

3. **Payment Webhook Issues**:
   - Verify webhook URLs
   - Check webhook signatures
   - Monitor webhook logs

### 12.2 Debug Mode

Enable debug mode for troubleshooting:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

## 13. Production Checklist

- [ ] All environment variables configured
- [ ] SSL certificates active
- [ ] Webhooks configured and tested
- [ ] Payment flows tested
- [ ] Authentication flows tested
- [ ] Voice processing tested
- [ ] Monitoring configured
- [ ] Backup strategies in place
- [ ] Security headers configured
- [ ] Performance optimized
- [ ] Error tracking active
- [ ] Analytics configured

## Support

For deployment issues:
1. Check application logs in Render/Vercel
2. Monitor Supabase dashboard for database issues
3. Check webhook logs for payment issues
4. Review error tracking in Sentry

## Next Steps

After successful deployment:
1. Set up monitoring alerts
2. Configure automated backups
3. Set up staging environment
4. Implement CI/CD pipelines
5. Plan for scaling as user base grows