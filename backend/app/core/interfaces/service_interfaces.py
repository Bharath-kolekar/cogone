"""
Service Interfaces following Interface Segregation Principle
Each interface focuses on a specific responsibility
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class IUserService(ABC):
    """
    User service interface - focused on user operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def create_user(self, user_data: BaseModel) -> Any:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: Any) -> Optional[Any]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[Any]:
        """Get user by email"""
        pass
    
    @abstractmethod
    async def update_user(self, user_id: Any, user_data: BaseModel) -> Optional[Any]:
        """Update user"""
        pass
    
    @abstractmethod
    async def delete_user(self, user_id: Any) -> bool:
        """Delete user"""
        pass


class IAuthService(ABC):
    """
    Auth service interface - focused on authentication operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        pass
    
    @abstractmethod
    async def create_access_token(self, user_id: Any) -> str:
        """Create access token for user"""
        pass
    
    @abstractmethod
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode token"""
        pass
    
    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh access token"""
        pass
    
    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        """Revoke token"""
        pass


class IAuthenticationService(ABC):
    """
    Authentication service interface - focused on authentication operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        pass
    
    @abstractmethod
    async def generate_access_token(self, user_id: Any) -> str:
        """Generate access token for user"""
        pass
    
    @abstractmethod
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify access token"""
        pass
    
    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> Optional[str]:
        """Refresh access token"""
        pass


class IAuthorizationService(ABC):
    """
    Authorization service interface - focused on authorization operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def check_permission(self, user_id: Any, permission: str) -> bool:
        """Check if user has specific permission"""
        pass
    
    @abstractmethod
    async def check_role(self, user_id: Any, role: str) -> bool:
        """Check if user has specific role"""
        pass
    
    @abstractmethod
    async def get_user_permissions(self, user_id: Any) -> List[str]:
        """Get all permissions for user"""
        pass
    
    @abstractmethod
    async def grant_permission(self, user_id: Any, permission: str) -> bool:
        """Grant permission to user"""
        pass


class ITwoFactorAuthService(ABC):
    """
    Two-factor authentication service interface
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def setup_2fa(self, user_id: Any) -> Dict[str, Any]:
        """Setup 2FA for user"""
        pass
    
    @abstractmethod
    async def verify_2fa(self, user_id: Any, code: str) -> bool:
        """Verify 2FA code"""
        pass
    
    @abstractmethod
    async def disable_2fa(self, user_id: Any) -> bool:
        """Disable 2FA for user"""
        pass
    
    @abstractmethod
    async def generate_backup_codes(self, user_id: Any) -> List[str]:
        """Generate backup codes for user"""
        pass


class IAIAgentService(ABC):
    """
    AI Agent service interface - focused on AI agent operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def create_agent(self, agent_data: BaseModel) -> Any:
        """Create a new AI agent"""
        pass
    
    @abstractmethod
    async def get_agent_by_id(self, agent_id: Any) -> Optional[Any]:
        """Get AI agent by ID"""
        pass
    
    @abstractmethod
    async def get_user_agents(self, user_id: Any) -> List[Any]:
        """Get all agents for user"""
        pass
    
    @abstractmethod
    async def update_agent(self, agent_id: Any, agent_data: BaseModel) -> Optional[Any]:
        """Update AI agent"""
        pass
    
    @abstractmethod
    async def delete_agent(self, agent_id: Any) -> bool:
        """Delete AI agent"""
        pass


class IAIAgentExecutionService(ABC):
    """
    AI Agent execution service interface - focused on agent execution
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def execute_agent(self, agent_id: Any, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI agent with input data"""
        pass
    
    @abstractmethod
    async def get_agent_status(self, agent_id: Any) -> str:
        """Get agent execution status"""
        pass
    
    @abstractmethod
    async def stop_agent(self, agent_id: Any) -> bool:
        """Stop agent execution"""
        pass
    
    @abstractmethod
    async def get_execution_history(self, agent_id: Any) -> List[Dict[str, Any]]:
        """Get agent execution history"""
        pass


class IVoiceProcessingService(ABC):
    """
    Voice processing service interface - focused on voice operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def transcribe_audio(self, audio_data: bytes, language: str = "en") -> str:
        """Transcribe audio to text"""
        pass
    
    @abstractmethod
    async def extract_intent(self, text: str) -> Dict[str, Any]:
        """Extract intent from text"""
        pass
    
    @abstractmethod
    async def generate_response(self, intent: Dict[str, Any]) -> str:
        """Generate response from intent"""
        pass


class IAppGenerationService(ABC):
    """
    App generation service interface - focused on app generation
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def generate_app(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate app from requirements"""
        pass
    
    @abstractmethod
    async def get_app_templates(self) -> List[Dict[str, Any]]:
        """Get available app templates"""
        pass
    
    @abstractmethod
    async def deploy_app(self, app_id: Any, deployment_config: Dict[str, Any]) -> bool:
        """Deploy app to specified platform"""
        pass


class IAnalyticsService(ABC):
    """
    Analytics service interface - focused on analytics operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def track_event(self, event_name: str, user_id: Any, metadata: Dict[str, Any]) -> bool:
        """Track analytics event"""
        pass
    
    @abstractmethod
    async def get_user_analytics(self, user_id: Any) -> Dict[str, Any]:
        """Get analytics for user"""
        pass
    
    @abstractmethod
    async def get_system_analytics(self) -> Dict[str, Any]:
        """Get system-wide analytics"""
        pass


class INotificationService(ABC):
    """
    Notification service interface - focused on notification operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email notification"""
        pass
    
    @abstractmethod
    async def send_sms(self, to: str, message: str) -> bool:
        """Send SMS notification"""
        pass
    
    @abstractmethod
    async def send_push_notification(self, user_id: Any, title: str, body: str) -> bool:
        """Send push notification"""
        pass


class ICacheService(ABC):
    """
    Cache service interface - focused on caching operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache"""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        pass
    
    @abstractmethod
    async def clear_pattern(self, pattern: str) -> int:
        """Clear cache entries matching pattern"""
        pass


class ILoggingService(ABC):
    """
    Logging service interface - focused on logging operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def log_info(self, message: str, metadata: Dict[str, Any]) -> None:
        """Log info message"""
        pass
    
    @abstractmethod
    async def log_error(self, message: str, error: Exception, metadata: Dict[str, Any]) -> None:
        """Log error message"""
        pass
    
    @abstractmethod
    async def log_audit(self, action: str, user_id: Any, metadata: Dict[str, Any]) -> None:
        """Log audit event"""
        pass


class IValidationService(ABC):
    """
    Validation service interface - focused on validation operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pass
    
    @abstractmethod
    async def validate_password(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        pass
    
    @abstractmethod
    async def validate_input(self, data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data against schema"""
        pass


class IMonitoringService(ABC):
    """
    Monitoring service interface - focused on monitoring operations
    Follows Interface Segregation Principle
    """
    
    @abstractmethod
    async def start_monitoring(self, service_name: str) -> bool:
        """Start monitoring a service"""
        pass
    
    @abstractmethod
    async def stop_monitoring(self, service_name: str) -> bool:
        """Stop monitoring a service"""
        pass
    
    @abstractmethod
    async def get_metrics(self, service_name: str) -> Dict[str, Any]:
        """Get metrics for a service"""
        pass
    
    @abstractmethod
    async def get_health_status(self, service_name: str) -> Dict[str, Any]:
        """Get health status for a service"""
        pass
    
    @abstractmethod
    async def set_alert_threshold(self, service_name: str, metric: str, threshold: float) -> bool:
        """Set alert threshold for a metric"""
        pass
