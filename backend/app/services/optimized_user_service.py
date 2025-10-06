"""
Optimized User Service Implementation
Follows SOLID principles and uses Repository Pattern
"""

from typing import Any, Dict, List, Optional
import structlog
from datetime import datetime
import uuid

from app.core.interfaces.service_interfaces import IUserService
from app.core.repositories.user_repository import UserRepository
from app.core.observers.observer_pattern import event_manager, EventType, EventPriority
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logger = structlog.get_logger()


class OptimizedUserService(IUserService):
    """
    Optimized User Service following SOLID principles
    - Single Responsibility: Only handles user business logic
    - Open/Closed: Extensible through interfaces
    - Liskov Substitution: Implements IUserService interface
    - Interface Segregation: Uses focused interfaces
    - Dependency Inversion: Depends on abstractions (repository)
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        logger.info("Optimized User Service initialized")
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user
        Follows Single Responsibility Principle
        """
        try:
            # Validate user data
            await self._validate_user_data(user_data)
            
            # Check if user already exists
            existing_user = await self.user_repository.get_by_email(user_data.email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Create user
            user = await self.user_repository.create(user_data)
            
            # Publish event
            await event_manager.publish_event(
                event_type=EventType.USER_CREATED,
                data={
                    "user_id": str(user.id),
                    "email": user.email,
                    "username": user.username
                },
                user_id=str(user.id),
                priority=EventPriority.MEDIUM,
                source="user_service"
            )
            
            logger.info("User created successfully", user_id=str(user.id), email=user.email)
            return user
            
        except Exception as e:
            logger.error("User creation failed", email=user_data.email, error=str(e))
            raise
    
    async def get_user_by_id(self, user_id: Any) -> Optional[User]:
        """
        Get user by ID
        Follows Single Responsibility Principle
        """
        try:
            user = await self.user_repository.get_by_id(user_id)
            
            if user:
                logger.debug("User retrieved", user_id=str(user_id))
            else:
                logger.debug("User not found", user_id=str(user_id))
            
            return user
            
        except Exception as e:
            logger.error("Failed to get user by ID", user_id=str(user_id), error=str(e))
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        Follows Single Responsibility Principle
        """
        try:
            user = await self.user_repository.get_by_email(email)
            
            if user:
                logger.debug("User retrieved by email", email=email)
            else:
                logger.debug("User not found by email", email=email)
            
            return user
            
        except Exception as e:
            logger.error("Failed to get user by email", email=email, error=str(e))
            raise
    
    async def update_user(self, user_id: Any, user_data: UserUpdate) -> Optional[User]:
        """
        Update user
        Follows Single Responsibility Principle
        """
        try:
            # Check if user exists
            existing_user = await self.user_repository.get_by_id(user_id)
            if not existing_user:
                return None
            
            # Update user
            updated_user = await self.user_repository.update(user_id, user_data)
            
            if updated_user:
                # Publish event
                await event_manager.publish_event(
                    event_type=EventType.USER_UPDATED,
                    data={
                        "user_id": str(user_id),
                        "updated_fields": list(user_data.dict(exclude_unset=True).keys())
                    },
                    user_id=str(user_id),
                    priority=EventPriority.LOW,
                    source="user_service"
                )
                
                logger.info("User updated successfully", user_id=str(user_id))
            
            return updated_user
            
        except Exception as e:
            logger.error("User update failed", user_id=str(user_id), error=str(e))
            raise
    
    async def delete_user(self, user_id: Any) -> bool:
        """
        Delete user
        Follows Single Responsibility Principle
        """
        try:
            # Check if user exists
            existing_user = await self.user_repository.get_by_id(user_id)
            if not existing_user:
                return False
            
            # Delete user
            success = await self.user_repository.delete(user_id)
            
            if success:
                # Publish event
                await event_manager.publish_event(
                    event_type=EventType.USER_DELETED,
                    data={
                        "user_id": str(user_id),
                        "email": existing_user.email
                    },
                    user_id=str(user_id),
                    priority=EventPriority.HIGH,
                    source="user_service"
                )
                
                logger.info("User deleted successfully", user_id=str(user_id))
            
            return success
            
        except Exception as e:
            logger.error("User deletion failed", user_id=str(user_id), error=str(e))
            raise
    
    async def get_users_with_pagination(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        """
        Get users with pagination and filtering
        Follows Single Responsibility Principle
        """
        try:
            users = await self.user_repository.get_many(skip=skip, limit=limit, filters=filters)
            
            logger.debug("Users retrieved with pagination", 
                        count=len(users), skip=skip, limit=limit)
            
            return users
            
        except Exception as e:
            logger.error("Failed to get users with pagination", error=str(e))
            raise
    
    async def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Search users
        Follows Single Responsibility Principle
        """
        try:
            users = await self.user_repository.search_users(search_term, skip=skip, limit=limit)
            
            logger.debug("Users search completed", 
                        search_term=search_term, count=len(users))
            
            return users
            
        except Exception as e:
            logger.error("User search failed", search_term=search_term, error=str(e))
            raise
    
    async def get_user_statistics(self) -> Dict[str, Any]:
        """
        Get user statistics
        Follows Single Responsibility Principle
        """
        try:
            # Get total user count
            total_users = await self.user_repository.count()
            
            # Get active users count
            active_users = await self.user_repository.count({"is_active": True})
            
            # Get users by role
            admin_count = await self.user_repository.count({"role": "admin"})
            user_count = await self.user_repository.count({"role": "user"})
            
            statistics = {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": total_users - active_users,
                "admin_users": admin_count,
                "regular_users": user_count,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("User statistics generated", statistics=statistics)
            return statistics
            
        except Exception as e:
            logger.error("Failed to generate user statistics", error=str(e))
            raise
    
    async def activate_user(self, user_id: Any) -> bool:
        """
        Activate user account
        Follows Single Responsibility Principle
        """
        try:
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                return False
            
            # Update user to active
            update_data = UserUpdate(is_active=True)
            updated_user = await self.user_repository.update(user_id, update_data)
            
            if updated_user:
                logger.info("User activated", user_id=str(user_id))
                return True
            
            return False
            
        except Exception as e:
            logger.error("User activation failed", user_id=str(user_id), error=str(e))
            raise
    
    async def deactivate_user(self, user_id: Any) -> bool:
        """
        Deactivate user account
        Follows Single Responsibility Principle
        """
        try:
            success = await self.user_repository.deactivate_user(user_id)
            
            if success:
                logger.info("User deactivated", user_id=str(user_id))
            
            return success
            
        except Exception as e:
            logger.error("User deactivation failed", user_id=str(user_id), error=str(e))
            raise
    
    async def _validate_user_data(self, user_data: UserCreate) -> None:
        """
        Validate user data
        Follows Single Responsibility Principle
        """
        # Email validation
        if not user_data.email or "@" not in user_data.email:
            raise ValueError("Invalid email format")
        
        # Password validation
        if not user_data.password or len(user_data.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Username validation
        if not user_data.username or len(user_data.username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        logger.debug("User data validation passed", email=user_data.email)
