"""
Admin service for feature management and system configuration
"""

import structlog
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import aiohttp
from app.models.admin import (
    FeatureConfig, AdminDashboard, FeatureToggleRequest, 
    FeatureConfigurationRequest, UsageAlert, SystemConfiguration,
    FeatureStatus, FeatureCategory
)
from app.core.config import settings

logger = structlog.get_logger()


class AdminService:
    """Admin service for managing features and system configuration"""
    
    def __init__(self):
        self.features: Dict[str, FeatureConfig] = {}
        self.system_config = SystemConfiguration()
        self.usage_alerts: List[UsageAlert] = []
        self._initialize_features()
    
    def _initialize_features(self):
        """Initialize default features"""
        default_features = [
            # AI Services
            FeatureConfig(
                feature_id="groq_ai",
                name="GROQ AI Service",
                description="Primary AI processing using GROQ API",
                category=FeatureCategory.AI_SERVICES,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0001,
                free_tier_limit=10000,
                configuration={"api_key": settings.GROQ_API_KEY, "model": "llama2-7b-chat"}
            ),
            FeatureConfig(
                feature_id="together_ai",
                name="Together AI Service",
                description="Secondary AI processing using Together AI",
                category=FeatureCategory.AI_SERVICES,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0002,
                free_tier_limit=5000,
                configuration={"api_key": settings.TOGETHER_API_KEY, "model": "meta-llama/Llama-2-7b-chat-hf"}
            ),
            FeatureConfig(
                feature_id="huggingface_ai",
                name="Hugging Face AI Service",
                description="AI processing using Hugging Face API",
                category=FeatureCategory.AI_SERVICES,
                status=FeatureStatus.DISABLED,
                cost_per_request=0.0001,
                free_tier_limit=1000,
                configuration={"api_key": settings.HF_API_KEY, "model": "microsoft/DialoGPT-medium"}
            ),
            
            # Communication Services
            FeatureConfig(
                feature_id="sms_service",
                name="SMS Service",
                description="SMS notifications via Twilio",
                category=FeatureCategory.COMMUNICATION,
                status=FeatureStatus.DISABLED,
                cost_per_request=0.0075,
                free_tier_limit=100,
                configuration={"twilio_sid": settings.TWILIO_ACCOUNT_SID, "twilio_token": settings.TWILIO_AUTH_TOKEN}
            ),
            FeatureConfig(
                feature_id="whatsapp_service",
                name="WhatsApp Service",
                description="WhatsApp notifications via free API",
                category=FeatureCategory.COMMUNICATION,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0,
                free_tier_limit=1000,
                configuration={"webhook_url": "https://api.whatsapp.com/business"}
            ),
            FeatureConfig(
                feature_id="email_service",
                name="Email Service",
                description="Email notifications via privateemail",
                category=FeatureCategory.COMMUNICATION,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0,
                free_tier_limit=10000,
                configuration={"smtp_host": "mail.cognomega.com", "smtp_port": 587}
            ),
            
            # Payment Services
            FeatureConfig(
                feature_id="paypal_payments",
                name="PayPal Payments",
                description="PayPal payment processing",
                category=FeatureCategory.PAYMENT,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.029,
                free_tier_limit=1000,
                configuration={"client_id": settings.PAYPAL_CLIENT_ID, "client_secret": settings.PAYPAL_CLIENT_SECRET}
            ),
            FeatureConfig(
                feature_id="razorpay_payments",
                name="Razorpay Payments",
                description="Razorpay payment processing (disabled for development)",
                category=FeatureCategory.PAYMENT,
                status=FeatureStatus.DISABLED,
                cost_per_request=0.02,
                free_tier_limit=0,
                configuration={"key_id": settings.RAZORPAY_KEY_ID, "key_secret": settings.RAZORPAY_KEY_SECRET}
            ),
            
            # Storage Services
            FeatureConfig(
                feature_id="cloudflare_d1",
                name="Cloudflare D1 Database",
                description="Free tier database storage",
                category=FeatureCategory.STORAGE,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0,
                free_tier_limit=25000000,
                configuration={"database_url": "https://api.cloudflare.com/client/v4/accounts"}
            ),
            FeatureConfig(
                feature_id="supabase_storage",
                name="Supabase Storage",
                description="Supabase database and storage",
                category=FeatureCategory.STORAGE,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0,
                free_tier_limit=500000,
                configuration={"url": settings.SUPABASE_URL, "anon_key": settings.SUPABASE_ANON_KEY}
            ),
            
            # Monitoring Services
            FeatureConfig(
                feature_id="sentry_monitoring",
                name="Sentry Monitoring",
                description="Error monitoring and performance tracking",
                category=FeatureCategory.MONITORING,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0,
                free_tier_limit=5000,
                configuration={"dsn": "https://your-sentry-dsn@sentry.io/project"}
            ),
            FeatureConfig(
                feature_id="cloudflare_analytics",
                name="Cloudflare Analytics",
                description="Free analytics and monitoring",
                category=FeatureCategory.MONITORING,
                status=FeatureStatus.ENABLED,
                cost_per_request=0.0,
                free_tier_limit=1000000,
                configuration={"zone_id": "your-cloudflare-zone-id"}
            ),
        ]
        
        for feature in default_features:
            self.features[feature.feature_id] = feature
    
    async def get_dashboard(self) -> AdminDashboard:
        """Get admin dashboard data"""
        try:
            enabled_count = sum(1 for f in self.features.values() if f.status == FeatureStatus.ENABLED)
            disabled_count = sum(1 for f in self.features.values() if f.status == FeatureStatus.DISABLED)
            maintenance_count = sum(1 for f in self.features.values() if f.status == FeatureStatus.MAINTENANCE)
            
            # Calculate total cost
            total_cost = sum(f.cost_per_request * f.current_usage for f in self.features.values())
            
            # Calculate free tier usage
            free_tier_usage = {}
            for feature in self.features.values():
                if feature.free_tier_limit:
                    usage_percentage = (feature.current_usage / feature.free_tier_limit) * 100
                    free_tier_usage[feature.feature_id] = usage_percentage
            
            # Get active alerts
            alerts = await self._get_active_alerts()
            
            return AdminDashboard(
                total_features=len(self.features),
                enabled_features=enabled_count,
                disabled_features=disabled_count,
                maintenance_features=maintenance_count,
                total_cost=total_cost,
                free_tier_usage=free_tier_usage,
                alerts=alerts
            )
            
        except Exception as e:
            logger.error("Failed to get dashboard data", error=str(e))
            raise e
    
    async def toggle_feature(self, request: FeatureToggleRequest) -> FeatureConfig:
        """Toggle feature status"""
        try:
            if request.feature_id not in self.features:
                raise ValueError(f"Feature {request.feature_id} not found")
            
            feature = self.features[request.feature_id]
            old_status = feature.status
            feature.status = request.status
            feature.last_updated = datetime.now()
            feature.updated_by = "admin"
            
            logger.info(
                "Feature status toggled",
                feature_id=request.feature_id,
                old_status=old_status,
                new_status=request.status,
                reason=request.reason
            )
            
            return feature
            
        except Exception as e:
            logger.error("Failed to toggle feature", error=str(e))
            raise e
    
    async def configure_feature(self, request: FeatureConfigurationRequest) -> FeatureConfig:
        """Configure feature settings"""
        try:
            if request.feature_id not in self.features:
                raise ValueError(f"Feature {request.feature_id} not found")
            
            feature = self.features[request.feature_id]
            feature.configuration.update(request.configuration)
            feature.last_updated = datetime.now()
            feature.updated_by = "admin"
            
            logger.info(
                "Feature configured",
                feature_id=request.feature_id,
                configuration=request.configuration,
                reason=request.reason
            )
            
            return feature
            
        except Exception as e:
            logger.error("Failed to configure feature", error=str(e))
            raise e
    
    async def get_feature_status(self, feature_id: str) -> Optional[FeatureConfig]:
        """Get feature status"""
        return self.features.get(feature_id)
    
    async def get_features_by_category(self, category: FeatureCategory) -> List[FeatureConfig]:
        """Get features by category"""
        return [f for f in self.features.values() if f.category == category]
    
    async def update_usage(self, feature_id: str, usage_count: int):
        """Update feature usage"""
        if feature_id in self.features:
            feature = self.features[feature_id]
            feature.current_usage = usage_count
            if feature.free_tier_limit:
                feature.usage_percentage = (usage_count / feature.free_tier_limit) * 100
            
            # Check for alerts
            await self._check_usage_alerts(feature)
    
    async def _check_usage_alerts(self, feature: FeatureConfig):
        """Check for usage alerts"""
        if feature.free_tier_limit and feature.usage_percentage >= 75:
            alert_level = "critical" if feature.usage_percentage >= 90 else "warning"
            alert = UsageAlert(
                service_name=feature.name,
                current_usage=feature.current_usage,
                limit=feature.free_tier_limit,
                percentage=feature.usage_percentage,
                alert_level=alert_level,
                message=f"{feature.name} usage is at {feature.usage_percentage:.1f}% of free tier limit"
            )
            self.usage_alerts.append(alert)
            
            # Send alert notification
            await self._send_usage_alert(alert)
    
    async def _send_usage_alert(self, alert: UsageAlert):
        """Send usage alert notification"""
        try:
            # Send email alert
            await self._send_email_alert(alert)
            
            # Send WhatsApp alert if enabled
            if self.features.get("whatsapp_service", {}).status == FeatureStatus.ENABLED:
                await self._send_whatsapp_alert(alert)
            
            logger.info("Usage alert sent", alert=alert.message)
            
        except Exception as e:
            logger.error("Failed to send usage alert", error=str(e))
    
    async def _send_email_alert(self, alert: UsageAlert):
        """Send email alert"""
        # Implementation for email alert
        pass
    
    async def _send_whatsapp_alert(self, alert: UsageAlert):
        """Send WhatsApp alert"""
        # Implementation for WhatsApp alert
        pass
    
    async def _get_active_alerts(self) -> List[str]:
        """Get active alerts"""
        return [alert.message for alert in self.usage_alerts if alert.created_at > datetime.now() - timedelta(hours=24)]
    
    async def get_system_configuration(self) -> SystemConfiguration:
        """Get system configuration"""
        return self.system_config
    
    async def update_system_configuration(self, config: SystemConfiguration):
        """Update system configuration"""
        self.system_config = config
        logger.info("System configuration updated", config=config.dict())
    
    async def get_ai_assistant_config(self) -> Dict[str, Any]:
        """Get AI assistant configuration"""
        return {
            "name": self.system_config.ai_assistant_name,
            "wake_word": self.system_config.wake_word,
            "chat_consolidation_enabled": self.system_config.chat_consolidation_enabled,
            "nlp_enhancement_enabled": self.system_config.nlp_enhancement_enabled
        }
    
    async def update_ai_assistant_config(self, name: str = None, wake_word: str = None):
        """Update AI assistant configuration"""
        if name:
            self.system_config.ai_assistant_name = name
        if wake_word:
            self.system_config.wake_word = wake_word
        
        logger.info("AI assistant configuration updated", name=name, wake_word=wake_word)
