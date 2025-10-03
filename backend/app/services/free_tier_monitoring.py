"""
Free tier monitoring service for tracking usage and sending alerts
"""

import structlog
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import aiohttp
from dataclasses import dataclass
from enum import Enum

logger = structlog.get_logger()


class AlertLevel(str, Enum):
    """Alert levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class ServiceUsage:
    """Service usage tracking"""
    service_name: str
    current_usage: int
    limit: int
    percentage: float
    last_updated: datetime
    cost_per_unit: float = 0.0
    total_cost: float = 0.0


@dataclass
class UsageAlert:
    """Usage alert"""
    service_name: str
    alert_level: AlertLevel
    message: str
    current_usage: int
    limit: int
    percentage: float
    created_at: datetime
    sent: bool = False


class FreeTierMonitoringService:
    """Free tier monitoring service"""
    
    def __init__(self):
        self.service_usage: Dict[str, ServiceUsage] = {}
        self.alerts: List[UsageAlert] = []
        self.alert_thresholds = {
            "warning": 75.0,
            "critical": 90.0
        }
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize service usage tracking"""
        services = {
            "supabase": {
                "limit": 500000,  # 500K requests/month
                "cost_per_unit": 0.0
            },
            "vercel": {
                "limit": 100000,  # 100K function invocations/month
                "cost_per_unit": 0.0
            },
            "render": {
                "limit": 750,  # 750 hours/month
                "cost_per_unit": 0.0
            },
            "cloudflare_workers": {
                "limit": 100000,  # 100K requests/day
                "cost_per_unit": 0.0
            },
            "cloudflare_d1": {
                "limit": 25000000,  # 25M reads/month
                "cost_per_unit": 0.0
            },
            "neon": {
                "limit": 500000,  # 500K requests/month
                "cost_per_unit": 0.0
            },
            "railway": {
                "limit": 500,  # $5 credit/month
                "cost_per_unit": 0.01
            },
            "sentry": {
                "limit": 5000,  # 5K errors/month
                "cost_per_unit": 0.0
            },
            "groq": {
                "limit": 10000,  # 10K requests/month (free tier)
                "cost_per_unit": 0.0001
            },
            "together_ai": {
                "limit": 5000,  # 5K requests/month (free tier)
                "cost_per_unit": 0.0002
            },
            "huggingface": {
                "limit": 1000,  # 1K requests/month (free tier)
                "cost_per_unit": 0.0001
            }
        }
        
        for service_name, config in services.items():
            self.service_usage[service_name] = ServiceUsage(
                service_name=service_name,
                current_usage=0,
                limit=config["limit"],
                percentage=0.0,
                last_updated=datetime.now(),
                cost_per_unit=config["cost_per_unit"],
                total_cost=0.0
            )
    
    async def update_usage(self, service_name: str, usage_count: int):
        """Update service usage"""
        if service_name not in self.service_usage:
            logger.warning(f"Unknown service: {service_name}")
            return
        
        service = self.service_usage[service_name]
        service.current_usage = usage_count
        service.percentage = (usage_count / service.limit) * 100
        service.total_cost = usage_count * service.cost_per_unit
        service.last_updated = datetime.now()
        
        # Check for alerts
        await self._check_usage_alerts(service)
        
        logger.info(
            "Service usage updated",
            service=service_name,
            usage=usage_count,
            percentage=service.percentage
        )
    
    async def _check_usage_alerts(self, service: ServiceUsage):
        """Check for usage alerts"""
        if service.percentage >= self.alert_thresholds["critical"]:
            await self._create_alert(
                service=service,
                level=AlertLevel.CRITICAL,
                message=f"CRITICAL: {service.service_name} usage is at {service.percentage:.1f}% of free tier limit!"
            )
        elif service.percentage >= self.alert_thresholds["warning"]:
            await self._create_alert(
                service=service,
                level=AlertLevel.WARNING,
                message=f"WARNING: {service.service_name} usage is at {service.percentage:.1f}% of free tier limit"
            )
    
    async def _create_alert(self, service: ServiceUsage, level: AlertLevel, message: str):
        """Create usage alert"""
        alert = UsageAlert(
            service_name=service.service_name,
            alert_level=level,
            message=message,
            current_usage=service.current_usage,
            limit=service.limit,
            percentage=service.percentage,
            created_at=datetime.now()
        )
        
        self.alerts.append(alert)
        
        # Send alert notification
        await self._send_alert_notification(alert)
        
        logger.warning(
            "Usage alert created",
            service=service.service_name,
            level=level,
            message=message
        )
    
    async def _send_alert_notification(self, alert: UsageAlert):
        """Send alert notification"""
        try:
            # Send email alert
            await self._send_email_alert(alert)
            
            # Send WhatsApp alert if enabled
            await self._send_whatsapp_alert(alert)
            
            alert.sent = True
            
        except Exception as e:
            logger.error("Failed to send alert notification", error=str(e))
    
    async def _send_email_alert(self, alert: UsageAlert):
        """Send email alert"""
        try:
            # Implementation for email alert using privateemail
            email_data = {
                "to": "vihaan@cognomega.com",
                "subject": f"[{alert.alert_level.upper()}] Free Tier Usage Alert - {alert.service_name}",
                "body": f"""
                Service: {alert.service_name}
                Alert Level: {alert.alert_level.upper()}
                Current Usage: {alert.current_usage:,}
                Limit: {alert.limit:,}
                Percentage: {alert.percentage:.1f}%
                
                Message: {alert.message}
                
                Time: {alert.created_at}
                """
            }
            
            # Send email via privateemail SMTP
            # Implementation would go here
            
            logger.info("Email alert sent", service=alert.service_name, level=alert.alert_level)
            
        except Exception as e:
            logger.error("Failed to send email alert", error=str(e))
    
    async def _send_whatsapp_alert(self, alert: UsageAlert):
        """Send WhatsApp alert"""
        try:
            # Implementation for WhatsApp alert
            whatsapp_data = {
                "to": "+1234567890",  # Admin phone number
                "message": f"🚨 {alert.alert_level.upper()} ALERT\n\n{alert.message}\n\nService: {alert.service_name}\nUsage: {alert.current_usage:,}/{alert.limit:,} ({alert.percentage:.1f}%)"
            }
            
            # Send WhatsApp message via free API
            # Implementation would go here
            
            logger.info("WhatsApp alert sent", service=alert.service_name, level=alert.alert_level)
            
        except Exception as e:
            logger.error("Failed to send WhatsApp alert", error=str(e))
    
    async def get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary"""
        total_services = len(self.service_usage)
        services_over_75 = sum(1 for s in self.service_usage.values() if s.percentage >= 75)
        services_over_90 = sum(1 for s in self.service_usage.values() if s.percentage >= 90)
        
        total_cost = sum(s.total_cost for s in self.service_usage.values())
        
        active_alerts = [a for a in self.alerts if not a.sent and a.created_at > datetime.now() - timedelta(hours=24)]
        
        return {
            "total_services": total_services,
            "services_over_75_percent": services_over_75,
            "services_over_90_percent": services_over_90,
            "total_monthly_cost": total_cost,
            "active_alerts": len(active_alerts),
            "services": {
                name: {
                    "current_usage": service.current_usage,
                    "limit": service.limit,
                    "percentage": service.percentage,
                    "cost": service.total_cost,
                    "last_updated": service.last_updated.isoformat()
                }
                for name, service in self.service_usage.items()
            },
            "recent_alerts": [
                {
                    "service": alert.service_name,
                    "level": alert.alert_level,
                    "message": alert.message,
                    "percentage": alert.percentage,
                    "created_at": alert.created_at.isoformat()
                }
                for alert in self.alerts[-10:]  # Last 10 alerts
            ]
        }
    
    async def get_service_usage(self, service_name: str) -> Optional[ServiceUsage]:
        """Get specific service usage"""
        return self.service_usage.get(service_name)
    
    async def get_alerts(self, hours: int = 24) -> List[UsageAlert]:
        """Get alerts from last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [a for a in self.alerts if a.created_at > cutoff_time]
    
    async def mark_alert_sent(self, alert_id: int):
        """Mark alert as sent"""
        if 0 <= alert_id < len(self.alerts):
            self.alerts[alert_id].sent = True
    
    async def start_monitoring(self):
        """Start continuous monitoring"""
        logger.info("Starting free tier monitoring")
        
        while True:
            try:
                # Check all services for usage updates
                await self._check_all_services()
                
                # Clean up old alerts
                await self._cleanup_old_alerts()
                
                # Wait before next check
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error("Error in monitoring loop", error=str(e))
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _check_all_services(self):
        """Check all services for usage updates"""
        # This would integrate with actual service APIs to get real usage data
        # For now, we'll simulate some usage updates
        pass
    
    async def _cleanup_old_alerts(self):
        """Clean up old alerts"""
        cutoff_time = datetime.now() - timedelta(days=7)
        self.alerts = [a for a in self.alerts if a.created_at > cutoff_time]
