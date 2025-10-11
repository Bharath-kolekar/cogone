"""
Smarty Agent Integration Router

API endpoints for the Smarty Agent Integration service.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
import structlog
from datetime import datetime
from uuid import UUID, uuid4

from app.services.smarty_agent_integration import (
    smarty_agent_integration,
    AgentSmartyMode,
    AgentCodeCapability,
    AgentSmartyConfig,
    AgentCodeGenerationRequest,
    AgentCodeGenerationResponse
)
from app.models.ai_agent import AgentCreationRequest, AgentType, AgentCapability

logger = structlog.get_logger(__name__)

router = APIRouter()

class SmartyAgentCreationRequest(BaseModel):
    """Request model for creating a Smarty-enhanced agent"""
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    agent_type: AgentType = Field(..., description="Agent type")
    capabilities: List[AgentCapability] = Field(default_factory=list, description="Agent capabilities")
    smarty_mode: AgentSmartyMode = Field(..., description="Smarty integration mode")
    code_capability: AgentCodeCapability = Field(..., description="Code generation capability")
    ethical_validation_level: str = Field(default="standard", description="Ethical validation level")

class SmartyAgentCodeGenerationRequest(BaseModel):
    """Request model for agent code generation"""
    agent_id: str = Field(..., description="Agent identifier")
    user_id: str = Field(..., description="User identifier")
    prompt: str = Field(..., description="Code generation prompt")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    code_type: str = Field(default="general", description="Type of code to generate")
    complexity_level: str = Field(default="medium", description="Complexity level")
    requirements: Dict[str, Any] = Field(default_factory=dict, description="Specific requirements")
    ethical_constraints: List[str] = Field(default_factory=list, description="Ethical constraints")
    quality_requirements: List[str] = Field(default_factory=list, description="Quality requirements")

class SmartyAgentStatusResponse(BaseModel):
    """Response model for agent Smarty status"""
    agent_id: str
    smarty_mode: str
    code_capability: str
    ethical_validation_level: str
    total_interactions: int
    metrics: Dict[str, Any]
    last_interaction: Optional[str]
    status: str

class SmartyAgentMetricsResponse(BaseModel):
    """Response model for integration metrics"""
    integration_metrics: Dict[str, Any]
    active_agents_count: int
    total_interactions_across_agents: int

class SmartyAgentConfigUpdateRequest(BaseModel):
    """Request model for updating agent Smarty configuration"""
    smarty_mode: Optional[AgentSmartyMode] = None
    code_capability: Optional[AgentCodeCapability] = None
    ethical_validation_level: Optional[str] = None
    quality_threshold: Optional[float] = None
    security_threshold: Optional[float] = None
    consistency_threshold: Optional[float] = None
    enable_real_time_validation: Optional[bool] = None
    enable_context_sharing: Optional[bool] = None
    enable_monitoring: Optional[bool] = None

@router.post("/create-agent")
async def create_smarty_agent(request: SmartyAgentCreationRequest):
    """Create a new AI agent with Smarty integration capabilities"""
    try:
        logger.info(f"Creating Smarty-enabled agent", 
                   name=request.name,
                   smarty_mode=request.smarty_mode.value)
        
        # Create agent creation request
        agent_creation_request = AgentCreationRequest(
            name=request.name,
            description=request.description,
            agent_type=request.agent_type,
            capabilities=request.capabilities
        )
        
        # Create Smarty-enhanced agent
        agent = await smarty_agent_integration.create_smarty_agent(
            agent_creation_request=agent_creation_request,
            smarty_mode=request.smarty_mode,
            code_capability=request.code_capability,
            ethical_validation_level=request.ethical_validation_level
        )
        
        return {
            "success": True,
            "agent": {
                "agent_id": str(agent.agent_id),
                "name": agent.name,
                "description": agent.description,
                "agent_type": agent.agent_type.value,
                "capabilities": [cap.value for cap in agent.capabilities],
                "smarty_mode": request.smarty_mode.value,
                "code_capability": request.code_capability.value,
                "ethical_validation_level": request.ethical_validation_level,
                "status": agent.status.value,
                "created_at": agent.created_at.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Smarty agent creation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Agent creation failed: {str(e)}")

@router.post("/generate-code", response_model=AgentCodeGenerationResponse)
async def generate_code_with_smarty_agent(request: SmartyAgentCodeGenerationRequest):
    """Generate code using a Smarty-enhanced agent"""
    try:
        logger.info(f"Starting code generation with Smarty agent", 
                   agent_id=request.agent_id,
                   user_id=request.user_id,
                   code_type=request.code_type)
        
        # Create code generation request
        code_request = AgentCodeGenerationRequest(
            agent_id=request.agent_id,
            user_id=request.user_id,
            prompt=request.prompt,
            context=request.context,
            code_type=request.code_type,
            complexity_level=request.complexity_level,
            requirements=request.requirements,
            ethical_constraints=request.ethical_constraints,
            quality_requirements=request.quality_requirements
        )
        
        # Generate code using Smarty agent
        response = await smarty_agent_integration.interact_with_smarty_agent(code_request)
        
        return response
        
    except Exception as e:
        logger.error(f"Code generation with Smarty agent failed", 
                    error=str(e), 
                    agent_id=request.agent_id)
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")

@router.get("/status/{agent_id}", response_model=SmartyAgentStatusResponse)
async def get_smarty_agent_status(agent_id: str):
    """Get Smarty integration status for an agent"""
    try:
        status = await smarty_agent_integration.get_agent_smarty_status(agent_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Agent not found or not Smarty-enhanced")
        
        return SmartyAgentStatusResponse(
            agent_id=status['agent_id'],
            smarty_mode=status['smarty_mode'],
            code_capability=status['code_capability'],
            ethical_validation_level=status['ethical_validation_level'],
            total_interactions=status['total_interactions'],
            metrics=status['metrics'],
            last_interaction=status['last_interaction'],
            status=status['status']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status retrieval failed", error=str(e), agent_id=agent_id)
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.get("/metrics", response_model=SmartyAgentMetricsResponse)
async def get_integration_metrics():
    """Get overall Smarty agent integration metrics"""
    try:
        metrics = await smarty_agent_integration.get_integration_metrics()
        
        return SmartyAgentMetricsResponse(
            integration_metrics=metrics.get('integration_metrics', {}),
            active_agents_count=metrics.get('active_agents_count', 0),
            total_interactions_across_agents=metrics.get('total_interactions_across_agents', 0)
        )
        
    except Exception as e:
        logger.error(f"Integration metrics retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@router.put("/config/{agent_id}")
async def update_agent_smarty_config(agent_id: str, request: SmartyAgentConfigUpdateRequest):
    """Update Smarty configuration for an agent"""
    try:
        # Get current config
        current_status = await smarty_agent_integration.get_agent_smarty_status(agent_id)
        if not current_status:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Create updated config
        updated_config = AgentSmartyConfig(
            agent_id=agent_id,
            smarty_mode=request.smarty_mode or AgentSmartyMode(current_status['smarty_mode']),
            code_capability=request.code_capability or AgentCodeCapability(current_status['code_capability']),
            ethical_validation_level=request.ethical_validation_level or current_status['ethical_validation_level'],
            quality_threshold=request.quality_threshold or 0.8,
            security_threshold=request.security_threshold or 0.9,
            consistency_threshold=request.consistency_threshold or 0.85,
            enable_real_time_validation=request.enable_real_time_validation if request.enable_real_time_validation is not None else True,
            enable_context_sharing=request.enable_context_sharing if request.enable_context_sharing is not None else True,
            enable_monitoring=request.enable_monitoring if request.enable_monitoring is not None else True
        )
        
        success = await smarty_agent_integration.update_agent_smarty_config(agent_id, updated_config)
        
        if not success:
            raise HTTPException(status_code=500, detail="Configuration update failed")
        
        return {
            "success": True,
            "message": "Agent Smarty configuration updated successfully",
            "agent_id": agent_id,
            "updated_config": {
                "smarty_mode": updated_config.smarty_mode.value,
                "code_capability": updated_config.code_capability.value,
                "ethical_validation_level": updated_config.ethical_validation_level,
                "quality_threshold": updated_config.quality_threshold,
                "security_threshold": updated_config.security_threshold,
                "consistency_threshold": updated_config.consistency_threshold
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Configuration update failed", error=str(e), agent_id=agent_id)
        raise HTTPException(status_code=500, detail=f"Configuration update failed: {str(e)}")

@router.delete("/remove/{agent_id}")
async def remove_smarty_agent(agent_id: str):
    """Remove Smarty integration from an agent"""
    try:
        success = await smarty_agent_integration.remove_smarty_agent(agent_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Agent not found or not Smarty-enhanced")
        
        return {
            "success": True,
            "message": "Smarty integration removed from agent successfully",
            "agent_id": agent_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent removal failed", error=str(e), agent_id=agent_id)
        raise HTTPException(status_code=500, detail=f"Agent removal failed: {str(e)}")

@router.get("/modes")
async def get_smarty_modes():
    """Get available Smarty integration modes"""
    return {
        "modes": [
            {
                "name": mode.value,
                "description": _get_mode_description(mode)
            }
            for mode in AgentSmartyMode
        ]
    }

@router.get("/capabilities")
async def get_code_capabilities():
    """Get available code generation capabilities"""
    return {
        "capabilities": [
            {
                "name": capability.value,
                "description": _get_capability_description(capability)
            }
            for capability in AgentCodeCapability
        ]
    }

@router.get("/agents")
async def list_smarty_agents():
    """List all Smarty-enhanced agents"""
    try:
        agents = []
        
        # Get all agent configurations
        for agent_id, config in smarty_agent_integration.agent_configs.items():
            status = await smarty_agent_integration.get_agent_smarty_status(agent_id)
            if status:
                agents.append({
                    "agent_id": agent_id,
                    "smarty_mode": config.smarty_mode.value,
                    "code_capability": config.code_capability.value,
                    "ethical_validation_level": config.ethical_validation_level,
                    "total_interactions": status['total_interactions'],
                    "performance_score": status['metrics'].get('performance_score', 0.0),
                    "status": status['status'],
                    "last_interaction": status['last_interaction']
                })
        
        return {
            "agents": agents,
            "total_count": len(agents)
        }
        
    except Exception as e:
        logger.error(f"Agent listing failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Agent listing failed: {str(e)}")

@router.post("/batch-code-generation")
async def batch_code_generation(requests: List[SmartyAgentCodeGenerationRequest]):
    """Generate code for multiple requests in batch"""
    try:
        if len(requests) > 5:
            raise HTTPException(status_code=400, detail="Maximum 5 batch requests allowed")
        
        logger.info(f"Starting batch code generation", count=len(requests))
        
        results = []
        for request in requests:
            try:
                code_request = AgentCodeGenerationRequest(
                    agent_id=request.agent_id,
                    user_id=request.user_id,
                    prompt=request.prompt,
                    context=request.context,
                    code_type=request.code_type,
                    complexity_level=request.complexity_level,
                    requirements=request.requirements,
                    ethical_constraints=request.ethical_constraints,
                    quality_requirements=request.quality_requirements
                )
                
                response = await smarty_agent_integration.interact_with_smarty_agent(code_request)
                
                results.append({
                    "agent_id": response.agent_id,
                    "user_id": response.user_id,
                    "generated_code": response.generated_code,
                    "confidence_score": response.confidence_score,
                    "quality_metrics": response.quality_metrics,
                    "execution_time": response.execution_time,
                    "success": True
                })
                
            except Exception as e:
                logger.error(f"Batch code generation item failed", error=str(e), agent_id=request.agent_id)
                results.append({
                    "agent_id": request.agent_id,
                    "user_id": request.user_id,
                    "error": str(e),
                    "success": False
                })
        
        successful_count = sum(1 for result in results if result.get('success', False))
        
        return {
            "batch_results": results,
            "successful_count": successful_count,
            "failed_count": len(results) - successful_count,
            "total_count": len(results)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch code generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Batch code generation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for Smarty agent integration"""
    try:
        metrics = await smarty_agent_integration.get_integration_metrics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "integration_status": "operational",
            "active_agents": metrics.get('active_agents_count', 0),
            "total_interactions": metrics.get('total_interactions_across_agents', 0)
        }
        
    except Exception as e:
        logger.error(f"Health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

def _get_mode_description(mode: AgentSmartyMode) -> str:
    """Get description for Smarty mode"""
    descriptions = {
        AgentSmartyMode.CODE_GENERATION_ASSISTANT: "Assists with general code generation tasks",
        AgentSmartyMode.CODE_REVIEW_ASSISTANT: "Provides code review and improvement suggestions",
        AgentSmartyMode.DEBUGGING_ASSISTANT: "Helps with debugging and issue resolution",
        AgentSmartyMode.TESTING_ASSISTANT: "Generates and validates test code",
        AgentSmartyMode.DOCUMENTATION_ASSISTANT: "Creates documentation and code comments",
        AgentSmartyMode.ARCHITECTURE_ASSISTANT: "Provides architectural guidance and patterns",
        AgentSmartyMode.OPTIMIZATION_ASSISTANT: "Optimizes code for performance and efficiency",
        AgentSmartyMode.SECURITY_ASSISTANT: "Focuses on security best practices and validation"
    }
    return descriptions.get(mode, "Unknown mode")

def _get_capability_description(capability: AgentCodeCapability) -> str:
    """Get description for code capability"""
    descriptions = {
        AgentCodeCapability.BASIC_CODE: "Generate basic, functional code",
        AgentCodeCapability.ADVANCED_CODE: "Generate advanced code with sophisticated patterns",
        AgentCodeCapability.ARCHITECTURAL_CODE: "Generate code following architectural patterns",
        AgentCodeCapability.OPTIMIZED_CODE: "Generate highly optimized code",
        AgentCodeCapability.SECURE_CODE: "Generate secure code with proper validation",
        AgentCodeCapability.TESTED_CODE: "Generate code with comprehensive test coverage",
        AgentCodeCapability.DOCUMENTED_CODE: "Generate well-documented code"
    }
    return descriptions.get(capability, "Unknown capability")
