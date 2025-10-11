# Configuration Guide

## Environment Variables

### Required Variables

#### Backend (FastAPI)
```env
# Application
ENVIRONMENT=development  # development | staging | production
DEBUG=True
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET=your-jwt-secret-min-32-chars

# Database (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
DATABASE_URL=postgresql://...

# Redis (Upstash)
REDIS_URL=redis://...
UPSTASH_REDIS_URL=https://...
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=your-token
```

#### Frontend (Next.js) - When Restored
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Optional Variables

#### Payment Providers
```env
# Razorpay
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-key-secret

# PayPal
PAYPAL_CLIENT_ID=your-client-id
PAYPAL_CLIENT_SECRET=your-client-secret
PAYPAL_SANDBOX=true
```

#### AI Providers (Optional)
```env
HUGGINGFACE_API_KEY=your-hf-key
TOGETHER_API_KEY=your-together-key
GROQ_API_KEY=your-groq-key
```

## Configuration Files

### Backend
- `backend/app/core/config.py` - Configuration management
- `backend/requirements.txt` - Python dependencies

### Frontend (When Restored)
- `frontend/next.config.js` - Next.js configuration
- `frontend/package.json` - Node dependencies

## Development Setup

1. **Copy environment template**:
   ```bash
   cp env.example .env
   ```

2. **Fill in required variables**:
   - Get Supabase credentials from Supabase dashboard
   - Generate secret keys (min 32 characters)

3. **Validate configuration**:
   ```bash
   cd backend
   python -c "from app.core.config import settings; print('Config valid!')"
   ```

## Production Considerations

- ⚠️ **Never commit** `.env` files to git
- ✅ **Use strong secrets** (min 32 characters, random)
- ✅ **Rotate secrets** regularly
- ✅ **Use environment-specific** values
- ✅ **Validate in CI/CD** before deployment

## Troubleshooting

See `TROUBLESHOOTING.md` for common configuration issues.

---

*Last Updated: October 10, 2025*

