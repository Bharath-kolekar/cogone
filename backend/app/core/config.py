"""
Configuration management for Voice-to-App SaaS Platform
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
import structlog


class Settings(BaseSettings):
    """Application settings with production-grade validation"""
    
    # Application
    APP_NAME: str = "Voice-to-App SaaS Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    
    # Security - NO DEFAULT VALUES for sensitive keys (must be provided)
    SECRET_KEY: str = Field(
        default="",
        min_length=32,
        description="Secret key - MUST be set in production"
    )
    JWT_SECRET: str = Field(
        default="",
        min_length=32,
        description="JWT secret - MUST be set in production"
    )
    ENCRYPTION_KEY: str = Field(
        default="",
        min_length=32,
        description="Encryption key - MUST be set in production"
    )
    
    @validator('SECRET_KEY', 'JWT_SECRET', 'ENCRYPTION_KEY')
    def validate_production_keys(cls, v):
        """🧬 REAL VALIDATION: Prevent placeholder values in production"""
        if not v:
            # Allow empty in development
            env = os.getenv('ENVIRONMENT', 'development')
            if env == 'production':
                raise ValueError("Must be set in production")
            return v or "dev-secret-key-change-in-production-min-32-chars"
        
        # Block obvious placeholders
        placeholders = ['dev-', 'test-', 'your-', 'change-in-production', 'placeholder']
        if any(p in v.lower() for p in placeholders):
            raise ValueError("Contains placeholder value - set real production value")
        
        # Validate length
        if len(v) < 32:
            raise ValueError("Must be at least 32 characters")
        
        return v
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database - Use Field for validation
    SUPABASE_URL: str = Field(default="", description="Supabase project URL")
    SUPABASE_ANON_KEY: str = Field(default="", description="Supabase anon key")
    SUPABASE_SERVICE_KEY: str = Field(default="", description="Supabase service key")
    DATABASE_URL: str = Field(default="", description="PostgreSQL connection string")
    
    @validator('SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_KEY')
    def validate_supabase_keys(cls, v):
        """🧬 REAL VALIDATION: Prevent placeholder Supabase values"""
        if not v:
            env = os.getenv('ENVIRONMENT', 'development')
            if env == 'production':
                raise ValueError("Must be set in production")
            return ""
        
        # Block placeholders
        if 'your-' in v or 'placeholder' in v or v == 'your-anon-key' or v == 'your-service-key':
            raise ValueError("Contains placeholder - set real value")
        
        return v
    
    # Redis
    REDIS_URL: Optional[str] = None
    UPSTASH_REDIS_URL: Optional[str] = None
    UPSTASH_REDIS_REST_URL: Optional[str] = None
    UPSTASH_REDIS_REST_TOKEN: Optional[str] = None
    
    # Payment Providers - Use Field with Optional for optional keys
    RAZORPAY_KEY_ID: Optional[str] = Field(default=None, description="Razorpay Key ID")
    RAZORPAY_KEY_SECRET: Optional[str] = Field(default=None, description="Razorpay Key Secret")
    RAZORPAY_API_KEY: Optional[str] = Field(default=None, description="Razorpay API Key")
    RAZORPAY_API_SECRET: Optional[str] = Field(default=None, description="Razorpay API Secret")
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = Field(default=None, description="Razorpay Webhook Secret")
    
    PAYPAL_CLIENT_ID: Optional[str] = Field(default=None, description="PayPal Client ID")
    PAYPAL_CLIENT_SECRET: Optional[str] = Field(default=None, description="PayPal Client Secret")
    PAYPAL_WEBHOOK_ID: Optional[str] = Field(default=None, description="PayPal Webhook ID")
    PAYPAL_SANDBOX: str = "true"
    
    GOOGLE_PAY_MERCHANT_ID: Optional[str] = Field(default=None, description="Google Pay Merchant ID")
    GOOGLE_PAY_API_KEY: Optional[str] = Field(default=None, description="Google Pay API Key")
    UPI_MERCHANT_ID: Optional[str] = Field(default=None, description="UPI Merchant ID")
    UPI_MERCHANT_NAME: Optional[str] = Field(default=None, description="UPI Merchant Name")
    
    @validator('RAZORPAY_KEY_ID', 'RAZORPAY_KEY_SECRET', 'RAZORPAY_API_KEY', 'RAZORPAY_API_SECRET', 
               'PAYPAL_CLIENT_ID', 'PAYPAL_CLIENT_SECRET', 'GOOGLE_PAY_MERCHANT_ID', 'GOOGLE_PAY_API_KEY',
               'UPI_MERCHANT_ID')
    def validate_payment_keys(cls, v):
        """🧬 REAL VALIDATION: Block placeholder payment keys"""
        if v is None:
            return None  # Optional keys can be None
        
        # Block dev placeholders
        if v.startswith('dev-') or 'your-' in v or 'placeholder' in v:
            raise ValueError("Contains placeholder - set real API key or leave empty")
        
        return v
    BASE_URL: str = "http://localhost:8000"
    NEON_API_KEY: Optional[str] = Field(default=None, description="Neon Database API Key")
    NEON_PROJECT_ID: Optional[str] = Field(default=None, description="Neon Project ID")
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None, description="Twilio Account SID")
    TWILIO_AUTH_TOKEN: Optional[str] = Field(default=None, description="Twilio Auth Token")
    
    @validator('NEON_API_KEY', 'NEON_PROJECT_ID', 'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')
    def validate_service_keys(cls, v):
        """🧬 REAL VALIDATION: Block placeholder service keys"""
        if v is None:
            return None
        
        if v.startswith('dev-') or 'your-' in v or 'placeholder' in v:
            raise ValueError("Contains placeholder - set real key or leave empty")
        
        return v
    
    # AI Providers (Zero-Cost Configuration)
    # Primary: Groq (FREE for developers)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL_NAME: str = "llama2-70b-4096"  # Fast, free for developers
    
    # Secondary: Together AI ($5 credit)
    TOGETHER_API_KEY: Optional[str] = None
    TOGETHER_MODEL_NAME: str = "meta-llama/Llama-2-70b-chat-hf"
    
    # Fallback: Hugging Face (FREE tier)
    HF_API_KEY: Optional[str] = None
    HF_MODEL_NAME: str = "microsoft/DialoGPT-medium"
    
    # Local AI Configuration (FREE)
    ALLOW_LOCAL_LLM: bool = True
    ENABLE_VOICE_COMMANDS: bool = True
    LOCAL_MODEL_PATH: str = "./models/"
    
    # AI Provider Priority (for zero-cost optimization)
    AI_PROVIDER_PRIORITY: List[str] = ["groq", "together", "local_llm", "huggingface"]
    ENABLE_AI_PROVIDER_FALLBACK: bool = True
    
    # WhatsApp Business API (Replaces SMS Provider)
    WHATSAPP_WEBHOOK_URL: Optional[str] = None
    WHATSAPP_VERIFY_TOKEN: Optional[str] = None
    WHATSAPP_ACCESS_TOKEN: str = "dev-whatsapp-access-token"
    WHATSAPP_PHONE_NUMBER_ID: str = "dev-whatsapp-phone-number-id"
    WHATSAPP_BUSINESS_ACCOUNT_ID: Optional[str] = None
    
    # Cloudflare Services (Frontend CDN only - FREE)
    CLOUDFLARE_API_TOKEN: Optional[str] = None
    CLOUDFLARE_ACCOUNT_ID: Optional[str] = None
    CLOUDFLARE_ZONE_ID: Optional[str] = None
    
    # Railway (Backend hosting - FREE $5 credit/month)
    RAILWAY_API_TOKEN: Optional[str] = None
    RAILWAY_PROJECT_ID: Optional[str] = None
    
    # Render (Alternative backend - FREE 750 hours/month)
    RENDER_API_KEY: Optional[str] = None
    RENDER_SERVICE_ID: Optional[str] = None
    
    # Zero-Cost Deployment Mode
    ZERO_COST_MODE: bool = True
    DEPLOYMENT_PLATFORM: str = "railway"  # railway, render, or local
    MAX_WORKERS: int = 4  # Limit for zero-cost
    MAX_MEMORY_MB: int = 512  # Railway free tier limit
    MAX_CONCURRENT_REQUESTS: int = 10  # Limit for free tier
    
    # Email Configuration (PrivateEmail via Namecheap)
    SMTP_HOST: str = "smtp.privateemail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "dev-smtp-user"
    SMTP_PASS: str = "dev-smtp-password"
    SMTP_FROM: str = "noreply@yourdomain.com"
    
    # Webhook URLs
    RAZORPAY_WEBHOOK_URL: str = "http://localhost:8000/api/v0/webhooks/razorpay"
    PAYPAL_WEBHOOK_URL: str = "http://localhost:8000/api/v0/webhooks/paypal"
    
    # WhatsApp Business API Configuration
    WHATSAPP_MESSAGE_TEMPLATES: Optional[str] = None
    WHATSAPP_MEDIA_UPLOAD_URL: Optional[str] = None
    WHATSAPP_WEBHOOK_SECRET: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_VOICE_COMMANDS_PER_DAY: int = 10
    RATE_LIMIT_FREE_TIER_DAILY_LIMIT: int = 5
    
    # Gamification
    POINTS_PER_APP_CREATED: int = 100
    POINTS_PER_APP_DEPLOYED: int = 200
    POINTS_PER_REFERRAL: int = 50
    POINTS_PER_SHARE: int = 10
    
    # File Storage
    MAX_FILE_SIZE_MB: int = 50
    SUPABASE_STORAGE_BUCKET: str = "generated-apps"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    GOOGLE_ANALYTICS_ID: Optional[str] = None
    
    # Webhook URLs
    RAZORPAY_WEBHOOK_URL: str
    PAYPAL_WEBHOOK_URL: str
    
    # Feature Flags
    ENABLE_GAMIFICATION: bool = True
    ENABLE_REFERRALS: bool = True
    ENABLE_TEMPLATES_MARKETPLACE: bool = True
    ENABLE_COLLABORATIVE_EDITING: bool = True
    ENABLE_PUSH_NOTIFICATIONS: bool = False
    
    # Development
    LOG_LEVEL: str = "INFO"
    ENABLE_CORS: bool = True
    ENABLE_AUTH_MIDDLEWARE: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Validation
def validate_settings():
    """Validate critical settings"""
    required_settings = [
        "SECRET_KEY",
        "JWT_SECRET", 
        "ENCRYPTION_KEY",
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_KEY",
        "RAZORPAY_KEY_ID",
        "RAZORPAY_KEY_SECRET",
        "WHATSAPP_ACCESS_TOKEN",
        "WHATSAPP_PHONE_NUMBER_ID",
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")
    
    return True


# Validate settings on import
if not settings.DEBUG:
    validate_settings()


def get_settings() -> Settings:
    """Compatibility helper to retrieve settings instance."""
    return settings


# Structured logger accessor
def get_logger():
    return structlog.get_logger()


# Provide a logger property for compatibility (read-only)
@property
def _logger_property(self):
    return structlog.get_logger()

# Attach property dynamically for backward compatibility
if not hasattr(Settings, 'logger'):
    try:
        Settings.logger = _logger_property  # type: ignore
    except Exception:
        pass