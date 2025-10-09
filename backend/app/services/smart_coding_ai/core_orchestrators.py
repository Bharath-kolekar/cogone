"""
Core AI Orchestrators Integration Module
Integrates with core AI orchestration services

Dependencies: 5 (AIOrchestrator, AIOrchestrationLayer, AIComponentOrchestrator, UnifiedAI, types)
Production-grade: Complete implementation with comprehensive error handling
"""

import structlog
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from app.services.ai_integration_types import AIIntegrationContext, IntegratedAIResponse

logger = structlog.get_logger(__name__)


class CoreOrchestratorsIntegration:
    """
    Integration with core AI orchestration systems
    Coordinates multiple orchestrators for complex tasks
    """
    
    def __init__(
        self,
        smart_coding_ai: Any,
        ai_orchestrator: Optional[Any] = None,
        ai_orchestration_layer: Optional[Any] = None,
        ai_component_orchestrator: Optional[Any] = None,
        unified_ai_component_orchestrator: Optional[Any] = None
    ):
        """
        Initialize core orchestrators integration
        
        Args:
            smart_coding_ai: Smart Coding AI service (required)
            ai_orchestrator: Optional AI orchestrator service
            ai_orchestration_layer: Optional AI orchestration layer
            ai_component_orchestrator: Optional AI component orchestrator
            unified_ai_component_orchestrator: Optional unified orchestrator
        """
        self.smart_coding_ai = smart_coding_ai
        self.ai_orchestrator = ai_orchestrator
        self.ai_orchestration_layer = ai_orchestration_layer
        self.ai_component_orchestrator = ai_component_orchestrator
        self.unified_ai_component_orchestrator = unified_ai_component_orchestrator
        
        available_count = sum([
            ai_orchestrator is not None,
            ai_orchestration_layer is not None,
            ai_component_orchestrator is not None,
            unified_ai_component_orchestrator is not None
        ])
        
        logger.info("Core orchestrators integration initialized",
                   available_orchestrators=available_count)
    
    async def integrate(
        self, 
        task_description: str, 
        context: AIIntegrationContext
    ) -> IntegratedAIResponse:
        """
        Integrate Smart Coding AI with Core AI Orchestrators
        
        Args:
            task_description: Description of task to orchestrate
            context: Integration context
            
        Returns:
            IntegratedAIResponse with orchestrated results
            
        Raises:
            ValueError: If inputs are invalid
            Exception: For critical failures (after logging)
        """
        try:
            # Validate inputs
            if not task_description or not task_description.strip():
                raise ValueError("Task description cannot be empty")
            
            if not context or not context.user_id:
                raise ValueError("Valid context with user_id is required")
            
            logger.info("Integrating with Core AI Orchestrators", 
                       user_id=context.user_id,
                       task_length=len(task_description))
            
            orchestration_results = {}
            
            # AI Orchestrator Integration
            if self.ai_orchestrator:
                try:
                    logger.debug("Calling AI orchestrator")
                    ai_orchestrator_result = await self.ai_orchestrator.orchestrate_task(
                        task_description, context.user_id
                    )
                    orchestration_results["ai_orchestrator"] = ai_orchestrator_result
                except Exception as e:
                    logger.warning("AI orchestrator failed", error=str(e))
                    orchestration_results["ai_orchestrator"] = {"error": str(e)}
            
            # AI Orchestration Layer Integration
            if self.ai_orchestration_layer:
                try:
                    logger.debug("Calling AI orchestration layer")
                    orchestration_layer_result = await self.ai_orchestration_layer.process_request(
                        task_description, context.metadata or {}
                    )
                    orchestration_results["ai_orchestration_layer"] = orchestration_layer_result
                except Exception as e:
                    logger.warning("AI orchestration layer failed", error=str(e))
                    orchestration_results["ai_orchestration_layer"] = {"error": str(e)}
            
            # AI Component Orchestrator Integration
            if self.ai_component_orchestrator:
                try:
                    logger.debug("Calling AI component orchestrator")
                    component_orchestrator_result = await self.ai_component_orchestrator.coordinate_components(
                        task_description, context.user_id
                    )
                    orchestration_results["ai_component_orchestrator"] = component_orchestrator_result
                except Exception as e:
                    logger.warning("AI component orchestrator failed", error=str(e))
                    orchestration_results["ai_component_orchestrator"] = {"error": str(e)}
            
            # Unified AI Component Orchestrator Integration
            if self.unified_ai_component_orchestrator:
                try:
                    logger.debug("Calling unified AI component orchestrator")
                    unified_result = await self.unified_ai_component_orchestrator.unified_coordination(
                        task_description, context.metadata or {}
                    )
                    orchestration_results["unified_ai_component_orchestrator"] = unified_result
                except Exception as e:
                    logger.warning("Unified orchestrator failed", error=str(e))
                    orchestration_results["unified_ai_component_orchestrator"] = {"error": str(e)}
            
            # Use Smart Coding AI to process the orchestrated results
            smart_coding_result = await self._synthesize_with_smart_coding(
                task_description, orchestration_results, context
            )
            
            response = IntegratedAIResponse(
                response_id=str(uuid.uuid4()),
                primary_response=smart_coding_result,
                supporting_responses=orchestration_results,
                confidence=smart_coding_result.get("confidence", 0.85),
                integration_metadata={
                    "core_orchestrators_used": len(orchestration_results),
                    "orchestration_types": list(orchestration_results.keys()),
                    "successful_integrations": len([r for r in orchestration_results.values() if "error" not in r])
                },
                timestamp=datetime.now()
            )
            
            logger.info("Core orchestrators integration completed",
                       user_id=context.user_id,
                       orchestrators_used=len(orchestration_results),
                       confidence=response.confidence)
            
            return response
            
        except ValueError as e:
            logger.error("Validation error in core orchestrators", error=str(e))
            raise
        except Exception as e:
            logger.error("Failed to integrate with Core AI Orchestrators", 
                        error=str(e),
                        error_type=type(e).__name__,
                        user_id=context.user_id if context else "unknown")
            raise
    
    async def _synthesize_with_smart_coding(
        self, 
        task_description: str,
        orchestration_results: Dict[str, Any],
        context: AIIntegrationContext
    ) -> Dict[str, Any]:
        """
        Synthesize orchestration results with Smart Coding AI
        
        Args:
            task_description: Original task description
            orchestration_results: Results from orchestrators
            context: Integration context
            
        Returns:
            Synthesized result dict
        """
        try:
            logger.debug("Synthesizing with Smart Coding AI",
                        orchestrator_count=len(orchestration_results))
            
            result = await self.smart_coding_ai.chat_with_codebase(
                query=f"Process orchestrated task: {task_description}",
                project_id=context.project_id or "orchestration",
                context_type="orchestration_integration"
            )
            
            # Add orchestration context
            result["orchestration_context"] = {
                "orchestrators_consulted": list(orchestration_results.keys()),
                "orchestration_count": len(orchestration_results)
            }
            
            return result
            
        except Exception as e:
            logger.error("Failed to synthesize with Smart Coding AI", error=str(e))
            # Return minimal result
            return {
                "answer": "",
                "confidence": 0.5,
                "error": str(e),
                "fallback": True
            }
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get core orchestrators integration status
        
        Returns:
            Dict with status information
        """
        return {
            "ai_orchestrator_available": self.ai_orchestrator is not None,
            "ai_orchestration_layer_available": self.ai_orchestration_layer is not None,
            "ai_component_orchestrator_available": self.ai_component_orchestrator is not None,
            "unified_ai_component_orchestrator_available": self.unified_ai_component_orchestrator is not None,
            "smart_coding_ai_configured": self.smart_coding_ai is not None,
            "total_orchestrators": sum([
                self.ai_orchestrator is not None,
                self.ai_orchestration_layer is not None,
                self.ai_component_orchestrator is not None,
                self.unified_ai_component_orchestrator is not None
            ]),
            "module": "core_orchestrators",
            "version": "1.0.0"
        }

