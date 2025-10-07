"""
Database Service for Supabase Operations
Handles all CRUD operations with proper error handling and type safety
"""

import structlog
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from app.core.database import get_supabase_client
from app.models.ai_agent import AgentDefinition, AgentInteraction, TaskDefinition
from app.models.user import User

logger = structlog.get_logger()


class DatabaseService:
    """Service for handling all database operations with Supabase"""
    
    def __init__(self):
        self.client = None
    
    def _get_client(self):
        """Get Supabase client, initialize if needed"""
        if self.client is None:
            self.client = get_supabase_client()
        return self.client
    
    # Agent Operations
    async def create_agent(self, agent: AgentDefinition) -> AgentDefinition:
        """Create a new agent in the database"""
        try:
            client = self._get_client()
            
            # Convert agent to dict for Supabase
            agent_data = {
                "id": str(agent.id),
                "user_id": str(agent.user_id),
                "name": agent.name,
                "description": agent.description,
                "type": agent.type.value if hasattr(agent.type, 'value') else str(agent.type),
                "status": agent.status.value if hasattr(agent.status, 'value') else str(agent.status),
                "capabilities": [cap.value if hasattr(cap, 'value') else str(cap) for cap in agent.capabilities],
                "config": agent.config.dict() if hasattr(agent.config, 'dict') else agent.config,
                "metrics": agent.metrics.dict() if hasattr(agent.metrics, 'dict') else agent.metrics,
                "created_at": agent.created_at.isoformat() if agent.created_at else datetime.utcnow().isoformat(),
                "updated_at": agent.updated_at.isoformat() if agent.updated_at else datetime.utcnow().isoformat()
            }
            
            result = client.table("agents").insert(agent_data).execute()
            
            if result.data:
                logger.info(f"Agent created successfully: {agent.id}")
                return agent
            else:
                raise Exception("Failed to create agent in database")
                
        except Exception as e:
            logger.error(f"Failed to create agent: {e}")
            raise
    
    async def get_agent(self, agent_id: str, user_id: str) -> Optional[AgentDefinition]:
        """Get agent by ID and user ID"""
        try:
            client = self._get_client()
            
            result = client.table("agents").select("*").eq("id", agent_id).eq("user_id", user_id).execute()
            
            if result.data:
                agent_data = result.data[0]
                # Convert back to AgentDefinition object
                return self._dict_to_agent(agent_data)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {e}")
            raise
    
    async def list_agents(self, user_id: str, agent_type: Optional[str] = None, 
                         status: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[AgentDefinition]:
        """List agents for a user with optional filters"""
        try:
            client = self._get_client()
            
            query = client.table("agents").select("*").eq("user_id", user_id)
            
            if agent_type:
                query = query.eq("type", agent_type)
            if status:
                query = query.eq("status", status)
            
            query = query.range(offset, offset + limit - 1)
            result = query.execute()
            
            agents = []
            for agent_data in result.data:
                agents.append(self._dict_to_agent(agent_data))
            
            return agents
            
        except Exception as e:
            logger.error(f"Failed to list agents: {e}")
            raise
    
    async def update_agent(self, agent_id: str, user_id: str, updates: Dict[str, Any]) -> Optional[AgentDefinition]:
        """Update agent with new data"""
        try:
            client = self._get_client()
            
            # Add updated_at timestamp
            updates["updated_at"] = datetime.utcnow().isoformat()
            
            result = client.table("agents").update(updates).eq("id", agent_id).eq("user_id", user_id).execute()
            
            if result.data:
                logger.info(f"Agent updated successfully: {agent_id}")
                return self._dict_to_agent(result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Failed to update agent {agent_id}: {e}")
            raise
    
    async def delete_agent(self, agent_id: str, user_id: str) -> bool:
        """Delete agent"""
        try:
            client = self._get_client()
            
            result = client.table("agents").delete().eq("id", agent_id).eq("user_id", user_id).execute()
            
            if result.data:
                logger.info(f"Agent deleted successfully: {agent_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete agent {agent_id}: {e}")
            raise
    
    # Interaction Operations
    async def create_interaction(self, interaction: AgentInteraction) -> AgentInteraction:
        """Create a new interaction"""
        try:
            client = self._get_client()
            
            interaction_data = {
                "id": str(interaction.id),
                "agent_id": str(interaction.agent_id),
                "user_id": str(interaction.user_id),
                "message": interaction.message,
                "response": interaction.response,
                "context": interaction.context,
                "metadata": interaction.metadata,
                "created_at": interaction.created_at.isoformat() if interaction.created_at else datetime.utcnow().isoformat()
            }
            
            result = client.table("agent_interactions").insert(interaction_data).execute()
            
            if result.data:
                logger.info(f"Interaction created successfully: {interaction.id}")
                return interaction
            else:
                raise Exception("Failed to create interaction in database")
                
        except Exception as e:
            logger.error(f"Failed to create interaction: {e}")
            raise
    
    async def get_interactions(self, agent_id: str, user_id: str, limit: int = 50, offset: int = 0) -> List[AgentInteraction]:
        """Get interactions for an agent"""
        try:
            client = self._get_client()
            
            result = client.table("agent_interactions").select("*").eq("agent_id", agent_id).eq("user_id", user_id).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            
            interactions = []
            for interaction_data in result.data:
                interactions.append(self._dict_to_interaction(interaction_data))
            
            return interactions
            
        except Exception as e:
            logger.error(f"Failed to get interactions: {e}")
            raise
    
    # Task Operations
    async def create_task(self, task: TaskDefinition) -> TaskDefinition:
        """Create a new task"""
        try:
            client = self._get_client()
            
            task_data = {
                "id": str(task.id),
                "agent_id": str(task.agent_id),
                "user_id": str(task.user_id),
                "title": task.title,
                "description": task.description,
                "type": task.type.value if hasattr(task.type, 'value') else str(task.type),
                "status": task.status.value if hasattr(task.status, 'value') else str(task.status),
                "priority": task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
                "parameters": task.parameters,
                "result": task.result,
                "created_at": task.created_at.isoformat() if task.created_at else datetime.utcnow().isoformat(),
                "updated_at": task.updated_at.isoformat() if task.updated_at else datetime.utcnow().isoformat()
            }
            
            result = client.table("agent_tasks").insert(task_data).execute()
            
            if result.data:
                logger.info(f"Task created successfully: {task.id}")
                return task
            else:
                raise Exception("Failed to create task in database")
                
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            raise
    
    async def get_tasks(self, agent_id: str, user_id: str, limit: int = 50, offset: int = 0) -> List[TaskDefinition]:
        """Get tasks for an agent"""
        try:
            client = self._get_client()
            
            result = client.table("agent_tasks").select("*").eq("agent_id", agent_id).eq("user_id", user_id).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            
            tasks = []
            for task_data in result.data:
                tasks.append(self._dict_to_task(task_data))
            
            return tasks
            
        except Exception as e:
            logger.error(f"Failed to get tasks: {e}")
            raise
    
    # Helper methods to convert dict to model objects
    def _dict_to_agent(self, data: Dict[str, Any]) -> AgentDefinition:
        """Convert dictionary to AgentDefinition object"""
        try:
            from app.models.ai_agent import AgentType, AgentStatus, AgentCapability, AgentConfig, AgentMetrics
            
            # Parse capabilities
            capabilities = []
            if data.get("capabilities"):
                for cap in data["capabilities"]:
                    try:
                        capabilities.append(AgentCapability(cap))
                    except:
                        capabilities.append(AgentCapability.OTHER)
            
            # Parse config
            config_data = data.get("config", {})
            config = AgentConfig(**config_data) if config_data else AgentConfig()
            
            # Parse metrics
            metrics_data = data.get("metrics", {})
            metrics = AgentMetrics(**metrics_data) if metrics_data else AgentMetrics()
            
            return AgentDefinition(
                id=data["id"],
                user_id=data["user_id"],
                name=data["name"],
                description=data.get("description", ""),
                type=AgentType(data["type"]) if data.get("type") else AgentType.GENERAL,
                status=AgentStatus(data["status"]) if data.get("status") else AgentStatus.ACTIVE,
                capabilities=capabilities,
                config=config,
                metrics=metrics,
                created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.utcnow(),
                updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Failed to convert dict to agent: {e}")
            raise
    
    def _dict_to_interaction(self, data: Dict[str, Any]) -> AgentInteraction:
        """Convert dictionary to AgentInteraction object"""
        try:
            return AgentInteraction(
                id=data["id"],
                agent_id=data["agent_id"],
                user_id=data["user_id"],
                message=data["message"],
                response=data.get("response", ""),
                context=data.get("context", {}),
                metadata=data.get("metadata", {}),
                created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Failed to convert dict to interaction: {e}")
            raise
    
    def _dict_to_task(self, data: Dict[str, Any]) -> TaskDefinition:
        """Convert dictionary to TaskDefinition object"""
        try:
            from app.models.ai_agent import TaskType, TaskStatus, TaskPriority
            
            return TaskDefinition(
                id=data["id"],
                agent_id=data["agent_id"],
                user_id=data["user_id"],
                title=data["title"],
                description=data.get("description", ""),
                type=TaskType(data["type"]) if data.get("type") else TaskType.GENERAL,
                status=TaskStatus(data["status"]) if data.get("status") else TaskStatus.PENDING,
                priority=TaskPriority(data["priority"]) if data.get("priority") else TaskPriority.MEDIUM,
                parameters=data.get("parameters", {}),
                result=data.get("result", ""),
                created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.utcnow(),
                updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Failed to convert dict to task: {e}")
            raise


# Global database service instance
database_service = DatabaseService()
