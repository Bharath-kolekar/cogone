"""
Base Repository Pattern Implementation
Abstract base repository following SOLID principles
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import DeclarativeBase
import structlog

logger = structlog.get_logger()

T = TypeVar('T', bound=DeclarativeBase)
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)


class BaseRepository(ABC, Generic[T, CreateSchema, UpdateSchema]):
    """
    Abstract base repository implementing Repository Pattern
    Follows Single Responsibility Principle and Dependency Inversion Principle
    """
    
    def __init__(self, db_session: AsyncSession, model: type[T]):
        self.db_session = db_session
        self.model = model
    
    @abstractmethod
    async def create(self, obj_in: CreateSchema) -> T:
        """Create a new entity"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def get_many(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """Get multiple entities with pagination and filtering"""
        pass
    
    @abstractmethod
    async def update(self, id: Any, obj_in: UpdateSchema) -> Optional[T]:
        """Update entity by ID"""
        pass
    
    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Delete entity by ID"""
        pass
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities with optional filters"""
        try:
            query = select(func.count(self.model.id))
            
            if filters:
                query = self._apply_filters(query, filters)
            
            result = await self.db_session.execute(query)
            return result.scalar() or 0
            
        except Exception as e:
            logger.error("Repository count error", model=self.model.__name__, error=str(e))
            raise
    
    async def exists(self, id: Any) -> bool:
        """Check if entity exists by ID"""
        try:
            entity = await self.get_by_id(id)
            return entity is not None
            
        except Exception as e:
            logger.error("Repository exists error", model=self.model.__name__, id=id, error=str(e))
            return False
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """Apply filters to query - to be overridden by concrete repositories"""
        return query
    
    async def commit(self):
        """Commit transaction"""
        try:
            await self.db_session.commit()
        except Exception as e:
            await self.db_session.rollback()
            logger.error("Repository commit error", error=str(e))
            raise
    
    async def rollback(self):
        """Rollback transaction"""
        try:
            await self.db_session.rollback()
        except Exception as e:
            logger.error("Repository rollback error", error=str(e))
            raise


class GenericRepository(BaseRepository[T, CreateSchema, UpdateSchema]):
    """
    Generic repository implementation for common CRUD operations
    Follows Open/Closed Principle - can be extended without modification
    """
    
    async def create(self, obj_in: CreateSchema) -> T:
        """Create a new entity"""
        try:
            # Convert Pydantic model to SQLAlchemy model
            obj_data = obj_in.dict() if hasattr(obj_in, 'dict') else obj_in
            db_obj = self.model(**obj_data)
            
            self.db_session.add(db_obj)
            await self.db_session.flush()
            await self.db_session.refresh(db_obj)
            
            logger.debug("Entity created", model=self.model.__name__, id=getattr(db_obj, 'id', None))
            return db_obj
            
        except Exception as e:
            logger.error("Repository create error", model=self.model.__name__, error=str(e))
            raise
    
    async def get_by_id(self, id: Any) -> Optional[T]:
        """Get entity by ID"""
        try:
            query = select(self.model).where(self.model.id == id)
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error("Repository get_by_id error", model=self.model.__name__, id=id, error=str(e))
            raise
    
    async def get_many(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[T]:
        """Get multiple entities with pagination and filtering"""
        try:
            query = select(self.model).offset(skip).limit(limit)
            
            if filters:
                query = self._apply_filters(query, filters)
            
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("Repository get_many error", model=self.model.__name__, error=str(e))
            raise
    
    async def update(self, id: Any, obj_in: UpdateSchema) -> Optional[T]:
        """Update entity by ID"""
        try:
            # Get existing entity
            existing_obj = await self.get_by_id(id)
            if not existing_obj:
                return None
            
            # Convert Pydantic model to dict, excluding unset fields
            update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, 'dict') else obj_in
            
            # Update entity
            for field, value in update_data.items():
                if hasattr(existing_obj, field):
                    setattr(existing_obj, field, value)
            
            await self.db_session.flush()
            await self.db_session.refresh(existing_obj)
            
            logger.debug("Entity updated", model=self.model.__name__, id=id)
            return existing_obj
            
        except Exception as e:
            logger.error("Repository update error", model=self.model.__name__, id=id, error=str(e))
            raise
    
    async def delete(self, id: Any) -> bool:
        """Delete entity by ID"""
        try:
            query = delete(self.model).where(self.model.id == id)
            result = await self.db_session.execute(query)
            
            deleted = result.rowcount > 0
            if deleted:
                logger.debug("Entity deleted", model=self.model.__name__, id=id)
            
            return deleted
            
        except Exception as e:
            logger.error("Repository delete error", model=self.model.__name__, id=id, error=str(e))
            raise


class RepositoryFactory:
    """
    Factory for creating repositories
    Follows Factory Pattern and Dependency Inversion Principle
    """
    
    _repositories: Dict[str, type] = {}
    
    @classmethod
    def register_repository(cls, name: str, repository_class: type):
        """Register a repository class"""
        cls._repositories[name] = repository_class
        logger.debug("Repository registered", name=name, class_name=repository_class.__name__)
    
    @classmethod
    def create_repository(cls, name: str, db_session: AsyncSession, model: type) -> BaseRepository:
        """Create a repository instance"""
        if name not in cls._repositories:
            raise ValueError(f"Repository '{name}' not registered")
        
        repository_class = cls._repositories[name]
        return repository_class(db_session, model)
    
    @classmethod
    def get_registered_repositories(cls) -> List[str]:
        """Get list of registered repository names"""
        return list(cls._repositories.keys())


class UnitOfWork:
    """
    Unit of Work Pattern implementation
    Manages transactions and repositories
    Follows Single Responsibility Principle
    """
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self._repositories: Dict[str, BaseRepository] = {}
        self._committed = False
    
    def get_repository(self, name: str, model: type) -> BaseRepository:
        """Get or create a repository"""
        if name not in self._repositories:
            self._repositories[name] = RepositoryFactory.create_repository(name, self.db_session, model)
        
        return self._repositories[name]
    
    async def commit(self):
        """Commit all changes"""
        try:
            await self.db_session.commit()
            self._committed = True
            logger.debug("Unit of work committed")
        except Exception as e:
            await self.db_session.rollback()
            logger.error("Unit of work commit error", error=str(e))
            raise
    
    async def rollback(self):
        """Rollback all changes"""
        try:
            await self.db_session.rollback()
            self._committed = False
            logger.debug("Unit of work rolled back")
        except Exception as e:
            logger.error("Unit of work rollback error", error=str(e))
            raise
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if exc_type is not None:
            await self.rollback()
        elif not self._committed:
            await self.commit()
