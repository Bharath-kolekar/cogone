"""
AI Agent Repository Implementation
Concrete repository for AI agent data access following SOLID principles
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
import structlog

from app.core.repositories.base_repository import GenericRepository
from app.models.ai_agent import AIAgent, AgentType, AgentStatus
from app.schemas.ai_agent import AIAgentCreate, AIAgentUpdate

logger = structlog.get_logger()


class AIAgentRepository(GenericRepository[AIAgent, AIAgentCreate, AIAgentUpdate]):
    """
    AI Agent repository implementation
    Follows Single Responsibility Principle - only handles AI agent data access
    Follows Interface Segregation Principle - focused AI agent operations
    """
    
    async def get_by_user_id(
        self, 
        user_id: Any, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AIAgent]:
        """Get AI agents by user ID with pagination"""
        try:
            query = (
                select(AIAgent)
                .where(AIAgent.user_id == user_id)
                .offset(skip)
                .limit(limit)
                .order_by(AIAgent.created_at.desc())
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("AI Agent repository get_by_user_id error", user_id=user_id, error=str(e))
            raise
    
    async def get_by_agent_type(
        self, 
        agent_type: AgentType, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AIAgent]:
        """Get AI agents by type with pagination"""
        try:
            query = (
                select(AIAgent)
                .where(AIAgent.agent_type == agent_type)
                .offset(skip)
                .limit(limit)
                .order_by(AIAgent.created_at.desc())
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("AI Agent repository get_by_agent_type error", agent_type=agent_type.value, error=str(e))
            raise
    
    async def get_active_agents(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AIAgent]:
        """Get active AI agents with pagination"""
        try:
            query = (
                select(AIAgent)
                .where(AIAgent.status == AgentStatus.ACTIVE)
                .offset(skip)
                .limit(limit)
                .order_by(AIAgent.last_used.desc())
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("AI Agent repository get_active_agents error", error=str(e))
            raise
    
    async def get_agents_by_status(
        self, 
        status: AgentStatus, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AIAgent]:
        """Get AI agents by status with pagination"""
        try:
            query = (
                select(AIAgent)
                .where(AIAgent.status == status)
                .offset(skip)
                .limit(limit)
                .order_by(AIAgent.updated_at.desc())
            )
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("AI Agent repository get_agents_by_status error", status=status.value, error=str(e))
            raise
    
    async def search_agents(
        self, 
        search_term: str, 
        user_id: Optional[Any] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[AIAgent]:
        """Search AI agents by name or description"""
        try:
            search_pattern = f"%{search_term}%"
            query = (
                select(AIAgent)
                .where(
                    or_(
                        AIAgent.name.ilike(search_pattern),
                        AIAgent.description.ilike(search_pattern)
                    )
                )
                .offset(skip)
                .limit(limit)
                .order_by(AIAgent.created_at.desc())
            )
            
            if user_id:
                query = query.where(AIAgent.user_id == user_id)
            
            result = await self.db_session.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error("AI Agent repository search_agents error", search_term=search_term, error=str(e))
            raise
    
    async def get_agent_with_interactions(self, agent_id: Any) -> Optional[AIAgent]:
        """Get AI agent with interaction history"""
        try:
            query = (
                select(AIAgent)
                .options(selectinload(AIAgent.interactions))
                .where(AIAgent.id == agent_id)
            )
            result = await self.db_session.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error("AI Agent repository get_agent_with_interactions error", agent_id=agent_id, error=str(e))
            raise
    
    async def update_agent_status(
        self, 
        agent_id: Any, 
        status: AgentStatus
    ) -> Optional[AIAgent]:
        """Update AI agent status"""
        try:
            query = (
                select(AIAgent)
                .where(AIAgent.id == agent_id)
            )
            result = await self.db_session.execute(query)
            agent = result.scalar_one_or_none()
            
            if agent:
                agent.status = status
                await self.db_session.flush()
                await self.db_session.refresh(agent)
                
            return agent
            
        except Exception as e:
            logger.error("AI Agent repository update_agent_status error", agent_id=agent_id, status=status.value, error=str(e))
            raise
    
    async def increment_usage_count(self, agent_id: Any) -> Optional[AIAgent]:
        """Increment agent usage count"""
        try:
            from datetime import datetime
            
            query = (
                select(AIAgent)
                .where(AIAgent.id == agent_id)
            )
            result = await self.db_session.execute(query)
            agent = result.scalar_one_or_none()
            
            if agent:
                agent.usage_count += 1
                agent.last_used = datetime.utcnow()
                await self.db_session.flush()
                await self.db_session.refresh(agent)
                
            return agent
            
        except Exception as e:
            logger.error("AI Agent repository increment_usage_count error", agent_id=agent_id, error=str(e))
            raise
    
    async def get_agent_statistics(self, user_id: Optional[Any] = None) -> Dict[str, Any]:
        """Get AI agent statistics"""
        try:
            base_query = select(AIAgent)
            if user_id:
                base_query = base_query.where(AIAgent.user_id == user_id)
            
            # Total agents
            total_query = select(func.count(AIAgent.id))
            if user_id:
                total_query = total_query.where(AIAgent.user_id == user_id)
            total_result = await self.db_session.execute(total_query)
            total_agents = total_result.scalar() or 0
            
            # Active agents
            active_query = select(func.count(AIAgent.id))
            if user_id:
                active_query = active_query.where(
                    and_(AIAgent.user_id == user_id, AIAgent.status == AgentStatus.ACTIVE)
                )
            else:
                active_query = active_query.where(AIAgent.status == AgentStatus.ACTIVE)
            active_result = await self.db_session.execute(active_query)
            active_agents = active_result.scalar() or 0
            
            # Total usage
            usage_query = select(func.sum(AIAgent.usage_count))
            if user_id:
                usage_query = usage_query.where(AIAgent.user_id == user_id)
            usage_result = await self.db_session.execute(usage_query)
            total_usage = usage_result.scalar() or 0
            
            # Agents by type
            type_query = (
                select(AIAgent.agent_type, func.count(AIAgent.id))
                .group_by(AIAgent.agent_type)
            )
            if user_id:
                type_query = type_query.where(AIAgent.user_id == user_id)
            type_result = await self.db_session.execute(type_query)
            agents_by_type = {row[0].value: row[1] for row in type_result.fetchall()}
            
            return {
                "total_agents": total_agents,
                "active_agents": active_agents,
                "total_usage": total_usage,
                "agents_by_type": agents_by_type
            }
            
        except Exception as e:
            logger.error("AI Agent repository get_agent_statistics error", error=str(e))
            raise
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """Apply filters to query"""
        if filters.get('user_id'):
            query = query.where(AIAgent.user_id == filters['user_id'])
        
        if filters.get('agent_type'):
            query = query.where(AIAgent.agent_type == filters['agent_type'])
        
        if filters.get('status'):
            query = query.where(AIAgent.status == filters['status'])
        
        if filters.get('is_active') is not None:
            query = query.where(AIAgent.is_active == filters['is_active'])
        
        if filters.get('created_after'):
            query = query.where(AIAgent.created_at >= filters['created_after'])
        
        if filters.get('created_before'):
            query = query.where(AIAgent.created_at <= filters['created_before'])
        
        return query
