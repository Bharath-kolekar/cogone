# 🌍 **Enhanced Environment Template - CognOmega Platform**

## **📋 Zero Cost Infrastructure Setup (16GB RAM Optimized)**

### **Setup Instructions:**
1. **Copy this template**: Create a `.env` file in your project root
2. **Fill in your values**: Replace placeholder values with your actual credentials
3. **Local AI Setup**: Configure Ollama paths for local LLM processing
4. **Never commit**: Add `.env` to `.gitignore` to keep secrets safe

---

## **🔧 CORE APPLICATION SETTINGS**

```bash
# =============================================================================
# CORE APPLICATION SETTINGS
# =============================================================================
SECRET_KEY=your-secret-key-here-change-this-in-production
ENCRYPTION_KEY=your-encryption-key-here-change-this-in-production

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
API_VERSION=v0

# CORS Origins
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

---

## **🗄️ DATABASE CONFIGURATION (Free Tiers)**

```bash
# =============================================================================
# DATABASE CONFIGURATION - SUPABASE FREE TIER
# =============================================================================
# Supabase Configuration (Free: 500MB DB, 2 projects)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# Primary Database
DATABASE_URL=postgresql://user:password@localhost:5432/cognomega

# Database Pool Settings (Optimized for 16GB RAM)
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

---

## **⚡ CACHE & QUEUE (Free Tiers)**

```bash
# =============================================================================
# REDIS CONFIGURATION - UPSTASH FREE TIER
# =============================================================================
# Upstash Redis (Free: 10K requests/day - ample for dev)
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-redis-token

# Local Redis (Development fallback)
REDIS_URL=redis://localhost:6379

# Cache Settings (Optimized for 16GB RAM)
CACHE_BACKEND=redis
CACHE_DEFAULT_TTL=3600
CACHE_MAX_SIZE=1000
CACHE_MEMORY_LIMIT=512MB

# Queue Settings
QUEUE_BACKEND=redis
QUEUE_MAX_RETRIES=3
QUEUE_RETRY_DELAY=5
QUEUE_MAX_WORKERS=4
```

---

## **🤖 LOCAL AI CONFIGURATION (Zero Cost)**

```bash
# =============================================================================
# LOCAL AI CONFIGURATION - OLLAMA + LLAMA 3
# =============================================================================
# Ollama Configuration (Local LLM - 8GB RAM usage)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3:8b-instruct-q4_K_M
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=4000
OLLAMA_TIMEOUT=120

# Local AI Paths (Windows)
OLLAMA_BIN_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama.exe
OLLAMA_MODELS_PATH=C:\Users\%USERNAME%\.ollama\models
OLLAMA_SERVER_PATH=http://localhost:11434

# AI Model Settings
LOCAL_AI_ENABLED=true
LOCAL_AI_FALLBACK_TO_REMOTE=true
LOCAL_AI_BATCH_SIZE=4
LOCAL_AI_MAX_CONCURRENT=2

# AI Service Priority (Groq first for speed, then local, then others)
AI_SERVICE_PRIORITY=groq,local,openai,anthropic
AI_SERVICE_TIMEOUT=30
AI_SERVICE_RETRY_COUNT=3
```

---

## **🌐 REMOTE AI SERVICES (Pay-per-Use)**

```bash
# =============================================================================
# REMOTE AI SERVICES - PAY PER USE
# =============================================================================
# OpenAI Configuration (Fallback)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7

# Anthropic Configuration (Fallback)
ANTHROPIC_API_KEY=your-anthropic-api-key
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=4000

# Groq Configuration (Primary AI Service - Free for developers)
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-8b-8192
GROQ_MAX_TOKENS=8000
GROQ_TEMPERATURE=0.7
GROQ_TOP_P=0.9
GROQ_FREQUENCY_PENALTY=0.0
GROQ_PRESENCE_PENALTY=0.0

# AI Service Limits (Cost Control)
AI_DAILY_LIMIT=100
AI_MONTHLY_LIMIT=1000
AI_COST_THRESHOLD=10.00
```

---

## **🔐 AUTHENTICATION & SECURITY**

```bash
# =============================================================================
# AUTHENTICATION & SECURITY
# =============================================================================
# JWT Settings
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Password Settings
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_SPECIAL_CHARS=true
PASSWORD_HASH_ALGORITHM=bcrypt

# Session Settings (Optimized for 16GB RAM)
SESSION_TIMEOUT_MINUTES=30
SESSION_MAX_CONCURRENT=5
SESSION_CLEANUP_INTERVAL=300
SESSION_STORAGE_BACKEND=redis
```

---

## **🔗 OAUTH CONFIGURATION**

```bash
# =============================================================================
# FRONTEND ENVIRONMENT VARIABLES
# =============================================================================
# Frontend Public Variables (Required for client-side access)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_APP_URL=https://your-frontend-url.com

# =============================================================================
# OAUTH CONFIGURATION
# =============================================================================
# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-domain.com/auth/google/callback

# GitHub OAuth
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=https://your-domain.com/auth/github/callback

# OAuth Settings
OAUTH_STATE_EXPIRE_MINUTES=10
OAUTH_TOKEN_EXPIRE_HOURS=1
```

---

## **💳 PAYMENT INTEGRATIONS (Test Mode)**

```bash
# =============================================================================
# PAYMENT INTEGRATIONS - TEST MODE (ZERO COST)
# =============================================================================
# Razorpay Configuration (Test Mode)
RAZORPAY_KEY_ID=your-razorpay-test-key-id
RAZORPAY_KEY_SECRET=your-razorpay-test-key-secret
RAZORPAY_WEBHOOK_SECRET=your-razorpay-webhook-secret
RAZORPAY_WEBHOOK_URL=https://your-domain.com/api/webhooks/razorpay

# PayPal Configuration (Sandbox Mode)
PAYPAL_CLIENT_ID=your-paypal-sandbox-client-id
PAYPAL_CLIENT_SECRET=your-paypal-sandbox-client-secret
PAYPAL_WEBHOOK_ID=your-paypal-webhook-id
PAYPAL_WEBHOOK_URL=https://your-domain.com/api/webhooks/paypal

# Google Pay Configuration
GOOGLE_PAY_MERCHANT_ID=your-google-pay-merchant-id

# Payment Settings
PAYMENT_MODE=test
PAYMENT_CURRENCY=USD
PAYMENT_WEBHOOK_TIMEOUT=30
```

---

## **📧 EMAIL CONFIGURATION**

```bash
# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================
# SMTP Settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_USE_TLS=true

# Email Settings
EMAIL_FROM_NAME=CognOmega Platform
EMAIL_FROM_ADDRESS=noreply@your-domain.com
EMAIL_TEMPLATE_DIR=app/templates/email
```

---

## **📊 MONITORING & ANALYTICS**

```bash
# =============================================================================
# MONITORING & ANALYTICS - FREE TIERS
# =============================================================================
# OpenTelemetry Configuration (Free)
OTEL_SERVICE_NAME=cognomega-platform
OTEL_SERVICE_VERSION=1.0.0
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_RESOURCE_ATTRIBUTES=service.name=cognomega,service.version=1.0.0

# Prometheus Configuration (Free)
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090
PROMETHEUS_METRICS_PATH=/metrics

# Grafana Configuration (Free)
GRAFANA_ENABLED=true
GRAFANA_PORT=3000
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin

# Telemetry Settings
TELEMETRY_ENABLED=true
TELEMETRY_BACKEND=prometheus
TELEMETRY_BATCH_SIZE=100
TELEMETRY_FLUSH_INTERVAL=60
```

---

## **🚀 PERFORMANCE OPTIMIZATION (16GB RAM)**

```bash
# =============================================================================
# PERFORMANCE OPTIMIZATION
# =============================================================================
# Memory Management
MAX_MEMORY_USAGE=14GB
MEMORY_CLEANUP_INTERVAL=300
MEMORY_MONITORING_ENABLED=true

# Worker Processes
WORKER_PROCESSES=4
WORKER_THREADS=2
WORKER_MAX_REQUESTS=1000
WORKER_TIMEOUT=30

# Connection Pooling
CONNECTION_POOL_SIZE=20
CONNECTION_POOL_MAX_OVERFLOW=30
CONNECTION_POOL_TIMEOUT=30

# Caching Strategy
CACHE_STRATEGY=lru
CACHE_HIT_RATIO_TARGET=0.8
CACHE_WARMUP_ENABLED=true
```

---

## **🔧 DEVELOPMENT SETTINGS**

```bash
# =============================================================================
# DEVELOPMENT SETTINGS
# =============================================================================
# Development Mode
DEV_MODE=true
DEV_AUTO_RELOAD=true
DEV_DEBUG_TOOLBAR=true
DEV_HOT_RELOAD=true

# Testing
TESTING=false
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/cognomega_test
TEST_REDIS_URL=redis://localhost:6379/1

# Local Development Tools
NGROK_ENABLED=true
NGROK_AUTH_TOKEN=your-ngrok-auth-token
NGROK_DOMAIN=your-domain.ngrok.io

# Development AI Settings
DEV_AI_MOCK_RESPONSES=true
DEV_AI_RESPONSE_DELAY=1000
DEV_AI_ERROR_RATE=0.1
```

---

## **📱 MESSAGING & COMMUNICATION**

```bash
# =============================================================================
# MESSAGING & COMMUNICATION - FREE TIERS
# =============================================================================
# WhatsApp Integration (Twilio Sandbox - Free)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
TWILIO_SANDBOX_ENABLED=true

# Alternative: WATI (Free Dev Plan)
WATI_API_TOKEN=your-wati-api-token
WATI_INSTANCE_ID=your-wati-instance-id
WATI_BASE_URL=https://live-server-1000.wati.io

# Messaging Settings
MESSAGING_RATE_LIMIT=100
MESSAGING_QUEUE_SIZE=1000
MESSAGING_RETRY_COUNT=3
```

---

## **🛡️ SECURITY & VALIDATION**

```bash
# =============================================================================
# SECURITY & VALIDATION
# =============================================================================
# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_REQUESTS_PER_HOUR=1000
RATE_LIMIT_REQUESTS_PER_DAY=10000
RATE_LIMIT_BURST_LIMIT=10

# Security Headers
SECURE_HEADERS=true
HTTPS_ONLY=true
CSP_ENABLED=true
HSTS_ENABLED=true

# Input Validation
INPUT_VALIDATION_ENABLED=true
MAX_REQUEST_SIZE=10MB
MAX_FILE_UPLOAD_SIZE=50MB
ALLOWED_FILE_TYPES=pdf,doc,docx,txt,py,js,ts,json

# API Security
API_KEY_REQUIRED=false
API_RATE_LIMIT_ENABLED=true
API_LOGGING_ENABLED=true
```

---

## **🎯 SMART CODING AI SETTINGS**

```bash
# =============================================================================
# SMART CODING AI SETTINGS
# =============================================================================
# Memory System
MEMORY_ENABLED=true
MEMORY_MAX_SIZE=10000
MEMORY_TTL=86400
MEMORY_BACKEND=redis

# Codebase Analysis
CODEBASE_ANALYSIS_ENABLED=true
CODEBASE_ANALYSIS_INTERVAL=3600
CODEBASE_ANALYSIS_DEPTH=5
CODEBASE_ANALYSIS_CONCURRENT=3

# Pattern Recognition
PATTERN_RECOGNITION_ENABLED=true
PATTERN_RECOGNITION_THRESHOLD=0.8
PATTERN_RECOGNITION_MIN_OCCURRENCES=3

# Code Generation
CODE_GENERATION_ENABLED=true
CODE_GENERATION_MAX_LENGTH=5000
CODE_GENERATION_TEMPERATURE=0.7
CODE_GENERATION_TOP_P=0.9
```

---

## **🔄 ORCHESTRATION SETTINGS**

```bash
# =============================================================================
# ORCHESTRATION SETTINGS
# =============================================================================
# AI Orchestration
ORCHESTRATION_ENABLED=true
ORCHESTRATION_MAX_CONCURRENT_TASKS=10
ORCHESTRATION_TIMEOUT_SECONDS=300
ORCHESTRATION_RETRY_COUNT=3

# Multi-Agent Coordination
MULTI_AGENT_ENABLED=true
MULTI_AGENT_MAX_AGENTS=5
MULTI_AGENT_TIMEOUT_SECONDS=600
MULTI_AGENT_COORDINATION_STRATEGY=adaptive

# Task Decomposition
TASK_DECOMPOSITION_ENABLED=true
TASK_DECOMPOSITION_MAX_DEPTH=5
TASK_DECOMPOSITION_STRATEGY=hierarchical

# Hierarchical Orchestration
HIERARCHICAL_ORCHESTRATION_ENABLED=true
HIERARCHICAL_MAX_LEVELS=6
HIERARCHICAL_LOAD_BALANCING=true
```

---

## **📈 ANALYTICS & METRICS**

```bash
# =============================================================================
# ANALYTICS & METRICS
# =============================================================================
# Performance Metrics
PERFORMANCE_METRICS_ENABLED=true
PERFORMANCE_METRICS_INTERVAL=60
PERFORMANCE_METRICS_RETENTION_DAYS=30

# User Analytics
USER_ANALYTICS_ENABLED=true
USER_ANALYTICS_TRACKING_ID=your-tracking-id
USER_ANALYTICS_PRIVACY_MODE=true

# Business Metrics
BUSINESS_METRICS_ENABLED=true
BUSINESS_METRICS_DASHBOARD=true
BUSINESS_METRICS_ALERTS=true
```

---

## **🔧 LOCAL DEVELOPMENT TOOLS**

```bash
# =============================================================================
# LOCAL DEVELOPMENT TOOLS
# =============================================================================
# Ollama Installation Path
OLLAMA_INSTALL_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Ollama
OLLAMA_DATA_PATH=C:\Users\%USERNAME%\.ollama

# Python Virtual Environment
PYTHON_VENV_PATH=.\venv
PYTHON_REQUIREMENTS_FILE=requirements.txt

# Node.js Settings
NODE_ENV=development
NODE_OPTIONS=--max-old-space-size=8192

# Development Ports
BACKEND_PORT=8000
FRONTEND_PORT=3000
REDIS_PORT=6379
POSTGRES_PORT=5432
```

---

## **🚀 QUICK START COMMANDS**

### **1. Create .env file:**
```bash
copy ENHANCED_ENV_TEMPLATE.md .env
```

### **2. Install Ollama (Local AI):**
```bash
# Download from https://ollama.ai/download
# Install and run:
ollama serve
ollama pull llama3:8b-instruct-q4_K_M
```

### **3. Start the application:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **4. Verify local AI:**
```bash
curl http://localhost:11434/api/generate -d '{"model": "llama3:8b-instruct-q4_K_M", "prompt": "Hello"}'
```

---

## **✅ VALIDATION CHECKLIST**

### **Required for Startup:**
- [ ] SECRET_KEY set (strong, unique)
- [ ] ENCRYPTION_KEY set (strong, unique)
- [ ] JWT_SECRET set (strong, unique)
- [ ] SUPABASE_URL configured
- [ ] SUPABASE_ANON_KEY configured
- [ ] GROQ_API_KEY configured (primary AI service)
- [ ] OLLAMA_HOST configured (fallback AI service)
- [ ] OLLAMA_MODEL set to llama3:8b-instruct-q4_K_M

### **Required for Frontend:**
- [ ] NEXT_PUBLIC_SUPABASE_URL configured
- [ ] NEXT_PUBLIC_SUPABASE_ANON_KEY configured
- [ ] NEXT_PUBLIC_API_URL configured
- [ ] NEXT_PUBLIC_APP_URL configured

### **Optional for Development:**
- [ ] OpenAI API key (fallback)
- [ ] Anthropic API key (fallback)
- [ ] Redis URL configured
- [ ] Database URL configured
- [ ] OAuth providers configured

### **Performance Verification:**
- [ ] Ollama running on port 11434
- [ ] Model downloaded and accessible
- [ ] Memory usage under 14GB
- [ ] All services responding

---

## **🎯 ZERO COST VERIFICATION**

### **Free Tier Limits:**
- **Supabase**: 500MB DB, 2 projects ✅
- **Upstash Redis**: 10K requests/day ✅
- **Ollama**: Local processing, no limits ✅
- **Vercel**: 100GB bandwidth/month ✅
- **Twilio Sandbox**: Free WhatsApp testing ✅

### **Cost Monitoring:**
- **AI API Calls**: Pay-per-use only
- **Database**: Free tier limits
- **Redis**: Free tier limits
- **Storage**: Local + Supabase free tier

**Total Monthly Cost: $0 (development) → $50-100 (growth) → $200-500 (production)**

---

## **🆘 TROUBLESHOOTING**

### **Common Issues:**

1. **Ollama not starting**: Check Windows Defender, run as admin
2. **Model not found**: Run `ollama pull llama3:8b-instruct-q4_K_M`
3. **Memory issues**: Reduce WORKER_PROCESSES, check RAM usage
4. **Redis connection**: Verify Upstash URL and token
5. **Database connection**: Check Supabase credentials

### **Performance Tips:**
- Use `llama3:8b-instruct-q4_K_M` for best RAM efficiency
- Enable caching for frequently used data
- Monitor memory usage with `htop` or Task Manager
- Use connection pooling for database operations

---

## **🎉 READY FOR ZERO COST DEVELOPMENT!**

Your CognOmega platform is now configured for:
- ✅ **Zero cost startup** (free tiers only)
- ✅ **16GB RAM optimization** (all services fit)
- ✅ **Local AI processing** (Ollama + Llama 3)
- ✅ **Production scalability** (clear upgrade path)
- ✅ **Development efficiency** (hot reload, debugging)

**Start developing with confidence - no monthly costs! 🚀**
