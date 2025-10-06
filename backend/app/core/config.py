"""
Configuration management for Voice-to-App SaaS Platform
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import structlog


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Voice-to-App SaaS Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str
    JWT_SECRET: str
    ENCRYPTION_KEY: str
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: Optional[str] = None
    UPSTASH_REDIS_URL: Optional[str] = None
    UPSTASH_REDIS_REST_URL: Optional[str] = None
    UPSTASH_REDIS_REST_TOKEN: Optional[str] = None
    
    # Payment Providers
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str
    RAZORPAY_WEBHOOK_SECRET: str
    
    PAYPAL_CLIENT_ID: str
    PAYPAL_CLIENT_SECRET: str
    PAYPAL_WEBHOOK_ID: str
    
    GOOGLE_PAY_MERCHANT_ID: str
    
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
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
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
    SMTP_HOST: str = "mail.cognomega.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "postmaster@cognomega.com"
    SMTP_PASS: str
    
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