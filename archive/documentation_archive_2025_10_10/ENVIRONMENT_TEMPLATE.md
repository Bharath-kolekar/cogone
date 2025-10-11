# 🌍 **Environment Variables Template - CognOmega Platform**

## **📋 Setup Instructions**

1. **Copy the template**: Create a `.env` file in your project root
2. **Fill in values**: Replace placeholder values with your actual credentials
3. **Never commit**: Add `.env` to `.gitignore` to keep secrets safe

---

## **🔧 Required Environment Variables**

### **Core Application Settings**
```bash
# Essential for application startup
SECRET_KEY=your-secret-key-here-change-this-in-production
ENCRYPTION_KEY=your-encryption-key-here-change-this-in-production
```

### **Database Configuration**
```bash
# Supabase (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# Primary Database
DATABASE_URL=postgresql://user:password@localhost:5432/cognomega
```

### **Redis Configuration**
```bash
# Upstash Redis (Production)
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-redis-token

# Local Redis (Development)
REDIS_URL=redis://localhost:6379
```

### **Payment Integrations**
```bash
# Razorpay
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
RAZORPAY_WEBHOOK_SECRET=your-razorpay-webhook-secret
RAZORPAY_WEBHOOK_URL=https://your-domain.com/api/webhooks/razorpay

# PayPal
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_WEBHOOK_ID=your-paypal-webhook-id
PAYPAL_WEBHOOK_URL=https://your-domain.com/api/webhooks/paypal

# Google Pay
GOOGLE_PAY_MERCHANT_ID=your-google-pay-merchant-id
```

### **Email Configuration**
```bash
# SMTP Settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

### **Frontend Environment Variables**
```bash
# Frontend Public Variables (Required for client-side access)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_APP_URL=https://your-frontend-url.com
```

### **OAuth Configuration**
```bash
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-domain.com/auth/google/callback

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=https://your-domain.com/auth/github/callback
```

### **AI Service Configuration**
```bash
# OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=4000

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

---

## **⚙️ Optional Configuration**

### **Application Settings**
```bash
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
API_VERSION=v0
```

### **Rate Limiting**
```bash
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_REQUESTS_PER_HOUR=1000
RATE_LIMIT_REQUESTS_PER_DAY=10000
RATE_LIMIT_BURST_LIMIT=10
```

### **Cache & Queue Settings**
```bash
CACHE_BACKEND=memory
CACHE_DEFAULT_TTL=3600
CACHE_MAX_SIZE=1000

QUEUE_BACKEND=memory
QUEUE_MAX_RETRIES=3
QUEUE_RETRY_DELAY=5
```

### **Security Settings**
```bash
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_SPECIAL_CHARS=true
SESSION_TIMEOUT_MINUTES=30
```

### **Smart Coding AI Settings**
```bash
MEMORY_ENABLED=true
MEMORY_MAX_SIZE=10000
MEMORY_TTL=86400

CODEBASE_ANALYSIS_ENABLED=true
CODEBASE_ANALYSIS_INTERVAL=3600

PATTERN_RECOGNITION_ENABLED=true
PATTERN_RECOGNITION_THRESHOLD=0.8
```

### **Orchestration Settings**
```bash
ORCHESTRATION_ENABLED=true
ORCHESTRATION_MAX_CONCURRENT_TASKS=10
ORCHESTRATION_TIMEOUT_SECONDS=300

MULTI_AGENT_ENABLED=true
MULTI_AGENT_MAX_AGENTS=5
MULTI_AGENT_TIMEOUT_SECONDS=600
```

### **Logging & Monitoring**
```bash
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/app.log

HEALTH_CHECK_ENABLED=true
METRICS_ENABLED=true
```

---

## **🚀 Quick Start**

### **1. Create .env file:**
```bash
cp ENVIRONMENT_TEMPLATE.md .env
```

### **2. Fill in minimum required values:**
```bash
# Minimum for development
SECRET_KEY=dev-secret-key-change-in-production
ENCRYPTION_KEY=dev-encryption-key-change-in-production
JWT_SECRET=dev-jwt-secret-change-in-production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
DATABASE_URL=postgresql://user:password@localhost:5432/cognomega

# Frontend variables (required for client-side access)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_APP_URL=https://your-frontend-url.com
```

### **3. Start the application:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

---

## **🔒 Security Notes**

1. **Never commit `.env` files** to version control
2. **Use strong, unique secrets** for production
3. **Rotate API keys regularly**
4. **Use different values** for dev/staging/production
5. **Consider secrets management** for production
6. **Test integrations** after updating variables

---

## **📝 Environment-Specific Configurations**

### **Development**
```bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
CACHE_BACKEND=memory
QUEUE_BACKEND=memory
```

### **Staging**
```bash
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
CACHE_BACKEND=redis
QUEUE_BACKEND=redis
```

### **Production**
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
CACHE_BACKEND=redis
QUEUE_BACKEND=redis
SECURE_HEADERS=true
HTTPS_ONLY=true
```

---

## **✅ Validation Checklist**

- [ ] All required variables set
- [ ] No placeholder values in production
- [ ] Secrets are strong and unique
- [ ] Database connections work
- [ ] Redis connections work
- [ ] OAuth providers configured
- [ ] AI services have valid keys
- [ ] Payment integrations configured
- [ ] Email service configured
- [ ] Application starts successfully

---

## **🆘 Troubleshooting**

### **Common Issues:**

1. **"Field required" errors**: Missing required environment variables
2. **Database connection errors**: Check DATABASE_URL format
3. **Redis connection errors**: Verify UPSTASH_REDIS_REST_URL
4. **OAuth errors**: Check client IDs and secrets
5. **Payment errors**: Verify webhook URLs and secrets

### **Quick Fixes:**

```bash
# Check if variables are loaded
python -c "import os; print(os.getenv('SECRET_KEY'))"

# Test database connection
python -c "from app.core.config import get_settings; print(get_settings().DATABASE_URL)"

# Validate configuration
python -c "from app.core.config import Settings; Settings()"
```

---

## **🎯 Next Steps**

1. **Set up your `.env` file** with required values
2. **Test the application** starts successfully
3. **Configure external services** (Supabase, Redis, etc.)
4. **Set up OAuth providers** for authentication
5. **Configure AI services** for Smart Coding AI features

**Your CognOmega platform is ready to run! 🚀**
