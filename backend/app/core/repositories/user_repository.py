"""
User Repository Implementation
Concrete repository following Repository Pattern and SOLID principles
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
import structlog

from app.core.repositories.base_repository import GenericRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

logger = structlog.get_logger()


class UserRepository(GenericRepository[User, UserCreate, UserUpdate]):
    """
    User repository implementation
    Follows Single Responsibility Principle - only handles user data access
    Follows Interface Segregation Principle - focused user operations
    """
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        try:
            query = select(User).where(User.email == email)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error("User repository get_by_email error", email=email, error=str(e))
            raise
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            query = select(User).where(User.username == username)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error("User repository get_by_username error", username=username, error=str(e))
            raise
    
    async def get_active_users(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Get active users with pagination"""
        try:
            query = (
                select(User)
                .where(User.is_active == True)
                .offset(skip)
                .limit(limit)
                .order_by(User.created_at.desc())
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("User repository get_active_users error", error=str(e))
            raise
    
    async def get_users_by_role(
        self, 
        role: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Get users by role with pagination"""
        try:
            query = (
                select(User)
                .where(User.role == role)
                .offset(skip)
                .limit(limit)
                .order_by(User.created_at.desc())
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("User repository get_users_by_role error", role=role, error=str(e))
            raise
    
    async def search_users(
        self, 
        search_term: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """Search users by email, username, or full name"""
        try:
            search_pattern = f"%{search_term}%"
            query = (
                select(User)
                .where(
                    or_(
                        User.email.ilike(search_pattern),
                        User.username.ilike(search_pattern),
                        User.full_name.ilike(search_pattern)
                    )
                )
                .offset(skip)
                .limit(limit)
                .order_by(User.created_at.desc())
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("User repository search_users error", search_term=search_term, error=str(e))
            raise
    
    async def get_user_with_2fa(self, user_id: Any) -> Optional[User]:
        """Get user with 2FA information"""
        try:
            query = (
                select(User)
                .options(selectinload(User.two_factor_auth))
                .where(User.id == user_id)
            )
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error("User repository get_user_with_2fa error", user_id=user_id, error=str(e))
            raise
    
    async def update_last_login(self, user_id: Any) -> Optional[User]:
        """Update user's last login timestamp"""
        try:
            from datetime import datetime
            
            query = (
                select(User)
                .where(User.id == user_id)
            )
            result = await self.db_session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                user.last_login = datetime.utcnow()
                await self.db_session.flush()
                await self.db_session.refresh(user)
                
            return user
            
        except Exception as e:
            logger.error("User repository update_last_login error", user_id=user_id, error=str(e))
            raise
    
    async def deactivate_user(self, user_id: Any) -> bool:
        """Deactivate user account"""
        try:
            query = (
                select(User)
                .where(User.id == user_id)
            )
            result = await self.db_session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                user.is_active = False
                await self.db_session.flush()
                return True
                
            return False
            
        except Exception as e:
            logger.error("User repository deactivate_user error", user_id=user_id, error=str(e))
            raise
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """Apply filters to query"""
        if filters.get('is_active') is not None:
            query = query.where(User.is_active == filters['is_active'])
        
        if filters.get('role'):
            query = query.where(User.role == filters['role'])
        
        if filters.get('created_after'):
            query = query.where(User.created_at >= filters['created_after'])
        
        if filters.get('created_before'):
            query = query.where(User.created_at <= filters['created_before'])
        
        return query
