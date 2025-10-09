"""
Task Orchestration Module
Handles orchestration and execution of smart coding tasks

Dependencies: 5 (MetaOrchestrator, smart_coding_ai, GoalIntegrity, ai_integration_types, uuid)
Production-grade: Complete implementation with comprehensive error handling
"""

import structlog
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from app.services.ai_integration_types import AIIntegrationContext, IntegratedAIResponse

logger = structlog.get_logger(__name__)


class TaskOrchestrator:
    """
    Orchestrates smart coding tasks
    Breaks down complex tasks and executes them systematically
    """
    
    def __init__(
        self,
        smart_coding_ai: Any,
        meta_orchestrator: Optional[Any] = None,
        goal_integrity: Optional[Any] = None
    ):
        """
        Initialize task orchestrator
        
        Args:
            smart_coding_ai: Smart Coding AI service (required)
            meta_orchestrator: Optional meta orchestrator for planning
            goal_integrity: Optional goal integrity validation service
        """
        self.smart_coding_ai = smart_coding_ai
        self.meta_orchestrator = meta_orchestrator
        self.goal_integrity = goal_integrity
        
        logger.info("Task orchestrator initialized",
                   meta_orchestrator_available=meta_orchestrator is not None,
                   goal_integrity_available=goal_integrity is not None)
    
    async def orchestrate(
        self, 
        task_description: str, 
        context: AIIntegrationContext
    ) -> IntegratedAIResponse:
        """
        Orchestrate a smart coding task using Meta Orchestrator
        
        Args:
            task_description: Description of the coding task
            context: Integration context
            
        Returns:
            IntegratedAIResponse with orchestration results
            
        Raises:
            ValueError: If task_description or context is invalid
            Exception: For critical failures (after logging)
        """
        try:
            # Validate inputs
            if not task_description or not task_description.strip():
                raise ValueError("Task description cannot be empty")
            
            if not context or not context.user_id:
                raise ValueError("Valid context with user_id is required")
            
            logger.info("Orchestrating smart coding task", 
                       user_id=context.user_id,
                       task_length=len(task_description))
            
            # Step 1: Use Meta Orchestrator to plan the task
            orchestration_plan = await self._create_orchestration_plan(
                task_description, context
            )
            
            # Step 2: Break down the plan into coding tasks
            coding_tasks = await self._break_down_into_tasks(
                orchestration_plan, context
            )
            
            if not coding_tasks:
                logger.warning("No coding tasks created from plan",
                             user_id=context.user_id)
                coding_tasks = [self._create_fallback_task(task_description)]
            
            # Step 3: Execute coding tasks using Smart Coding AI
            execution_results = []
            for task in coding_tasks:
                task_result = await self._execute_task(task, context)
                execution_results.append(task_result)
            
            # Step 4: Combine and optimize results
            final_result = await self._combine_results(execution_results, context)
            
            # Create integrated response
            response = IntegratedAIResponse(
                response_id=str(uuid.uuid4()),
                primary_response=final_result,
                supporting_responses={
                    "orchestration_plan": orchestration_plan,
                    "coding_tasks": coding_tasks,
                    "execution_results": execution_results
                },
                confidence=final_result.get("confidence", 0.85),
                integration_metadata={
                    "orchestrated": True,
                    "tasks_executed": len(execution_results),
                    "successful_tasks": len([r for r in execution_results if r["success"]]),
                    "meta_orchestrator_used": self.meta_orchestrator is not None
                },
                timestamp=datetime.now()
            )
            
            logger.info("Smart coding task orchestration completed",
                       user_id=context.user_id,
                       tasks_executed=len(execution_results),
                       confidence=response.confidence)
            
            return response
            
        except ValueError as e:
            logger.error("Validation error in task orchestration", error=str(e))
            raise
        except Exception as e:
            logger.error("Failed to orchestrate smart coding task", 
                        error=str(e),
                        error_type=type(e).__name__,
                        user_id=context.user_id if context else "unknown")
            raise
    
    async def _create_orchestration_plan(
        self, 
        task_description: str, 
        context: AIIntegrationContext
    ) -> Dict[str, Any]:
        """
        Create orchestration plan for the task
        
        Args:
            task_description: Task description
            context: Integration context
            
        Returns:
            Orchestration plan dict
        """
        try:
            if self.meta_orchestrator and context.user_id:
                logger.debug("Creating orchestration plan with meta orchestrator")
                plan = await self.meta_orchestrator.orchestrate_plan(
                    task_description, context.user_id
                )
                return plan
            else:
                # Fallback: create simple plan
                logger.debug("Using fallback orchestration plan")
                return {
                    "steps": [
                        {
                            "id": "analyze",
                            "action": "analyze",
                            "description": f"Analyze: {task_description}"
                        },
                        {
                            "id": "implement",
                            "action": "implement",
                            "description": f"Implement: {task_description}"
                        },
                        {
                            "id": "test",
                            "action": "test",
                            "description": f"Test: {task_description}"
                        }
                    ],
                    "confidence": 0.8,
                    "fallback": True
                }
                
        except Exception as e:
            logger.error("Failed to create orchestration plan", error=str(e))
            # Return minimal fallback plan
            return {
                "steps": [
                    {
                        "id": "implement",
                        "action": "implement",
                        "description": task_description
                    }
                ],
                "confidence": 0.7,
                "fallback": True,
                "error": str(e)
            }
    
    async def _break_down_into_tasks(
        self, 
        orchestration_plan: Dict, 
        context: AIIntegrationContext
    ) -> List[Dict[str, Any]]:
        """
        Break down orchestration plan into executable coding tasks
        
        Args:
            orchestration_plan: Plan from meta orchestrator
            context: Integration context
            
        Returns:
            List of coding task dicts
        """
        try:
            tasks = []
            
            if "steps" in orchestration_plan:
                for step in orchestration_plan["steps"]:
                    action = step.get("action", "")
                    
                    # Only include coding-related actions
                    if action in ["scaffold", "implement", "optimize", "test", "refactor", "debug"]:
                        tasks.append({
                            "task_id": str(uuid.uuid4()),
                            "action": action,
                            "description": step.get("description", ""),
                            "confidence": step.get("confidence", 0.8),
                            "priority": step.get("priority", "medium"),
                            "estimated_time": step.get("estimated_time", "unknown")
                        })
            
            logger.debug("Broke down plan into tasks",
                        total_tasks=len(tasks),
                        actions=[t["action"] for t in tasks])
            
            return tasks
            
        except Exception as e:
            logger.error("Failed to break down tasks", error=str(e))
            return []
    
    def _create_fallback_task(self, description: str) -> Dict[str, Any]:
        """
        Create a fallback task when planning fails
        
        Args:
            description: Task description
            
        Returns:
            Simple task dict
        """
        return {
            "task_id": str(uuid.uuid4()),
            "action": "implement",
            "description": description,
            "confidence": 0.7,
            "priority": "medium",
            "fallback": True
        }
    
    async def _execute_task(
        self, 
        task: Dict, 
        context: AIIntegrationContext
    ) -> Dict[str, Any]:
        """
        Execute a single coding task using Smart Coding AI
        
        Args:
            task: Task dict with action and description
            context: Integration context
            
        Returns:
            Task execution result dict
        """
        try:
            action = task.get("action", "implement")
            description = task.get("description", "")
            task_id = task.get("task_id", str(uuid.uuid4()))
            
            logger.debug("Executing coding task",
                        task_id=task_id,
                        action=action,
                        description_length=len(description))
            
            # Select appropriate query based on action
            query_templates = {
                "scaffold": f"Create scaffolding for: {description}",
                "implement": f"Implement: {description}",
                "optimize": f"Optimize code for: {description}",
                "test": f"Create tests for: {description}",
                "refactor": f"Refactor code for: {description}",
                "debug": f"Debug and fix: {description}"
            }
            
            query = query_templates.get(action, f"Handle task: {description}")
            
            # Execute with Smart Coding AI
            result = await self.smart_coding_ai.chat_with_codebase(
                query=query,
                project_id=context.project_id or "orchestration",
                context_type=action
            )
            
            # Determine success
            has_answer = bool(result.get("answer", "").strip())
            success = has_answer and result.get("confidence", 0) > 0.5
            
            execution_result = {
                "task_id": task_id,
                "action": action,
                "description": description,
                "result": result,
                "success": success,
                "confidence": result.get("confidence", 0.8),
                "has_code": has_answer,
                "error": None
            }
            
            logger.info("Task executed",
                       task_id=task_id,
                       action=action,
                       success=success,
                       confidence=execution_result["confidence"])
            
            return execution_result
            
        except Exception as e:
            logger.error("Failed to execute coding task", 
                        error=str(e),
                        error_type=type(e).__name__,
                        task_id=task.get("task_id", "unknown"))
            
            return {
                "task_id": task.get("task_id", str(uuid.uuid4())),
                "action": task.get("action", "unknown"),
                "description": task.get("description", ""),
                "result": {"error": str(e)},
                "success": False,
                "confidence": 0.0,
                "has_code": False,
                "error": str(e)
            }
    
    async def _combine_results(
        self, 
        results: List[Dict], 
        context: AIIntegrationContext
    ) -> Dict[str, Any]:
        """
        Combine multiple coding task results
        
        Args:
            results: List of task execution results
            context: Integration context
            
        Returns:
            Combined result dict
        """
        try:
            if not results:
                logger.warning("No results to combine")
                return {
                    "combined_code": "",
                    "total_tasks": 0,
                    "successful_tasks": 0,
                    "confidence": 0.0,
                    "recommendations": ["No tasks were executed"]
                }
            
            successful_tasks = [r for r in results if r.get("success", False)]
            failed_tasks = [r for r in results if not r.get("success", False)]
            
            # Combine code from successful tasks
            code_parts = [
                r["result"].get("answer", "") 
                for r in successful_tasks 
                if r["result"].get("answer", "").strip()
            ]
            combined_code = "\n\n# " + "="*60 + "\n\n".join(code_parts)
            
            # Calculate overall confidence
            if results:
                total_confidence = sum(r.get("confidence", 0.0) for r in results) / len(results)
            else:
                total_confidence = 0.0
            
            # Generate recommendations
            recommendations = self._generate_recommendations(results, successful_tasks, failed_tasks)
            
            combined = {
                "combined_code": combined_code,
                "total_tasks": len(results),
                "successful_tasks": len(successful_tasks),
                "failed_tasks": len(failed_tasks),
                "confidence": round(total_confidence, 3),
                "task_details": results,
                "recommendations": recommendations,
                "success_rate": len(successful_tasks) / len(results) if results else 0.0
            }
            
            logger.info("Results combined",
                       total_tasks=len(results),
                       successful=len(successful_tasks),
                       failed=len(failed_tasks),
                       confidence=total_confidence)
            
            return combined
            
        except Exception as e:
            logger.error("Failed to combine coding results", error=str(e))
            # Return partial results rather than failing completely
            return {
                "combined_code": "",
                "total_tasks": len(results) if results else 0,
                "successful_tasks": 0,
                "confidence": 0.0,
                "error": str(e),
                "recommendations": ["Failed to combine results"]
            }
    
    def _generate_recommendations(
        self, 
        all_results: List[Dict],
        successful_tasks: List[Dict],
        failed_tasks: List[Dict]
    ) -> List[str]:
        """
        Generate recommendations based on task results
        
        Args:
            all_results: All task results
            successful_tasks: Successful task results
            failed_tasks: Failed task results
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if not all_results:
            return ["No tasks were executed"]
        
        success_count = len(successful_tasks)
        total_count = len(all_results)
        success_rate = success_count / total_count if total_count > 0 else 0.0
        
        # Overall success assessment
        if success_rate == 1.0:
            recommendations.append("✓ All tasks completed successfully!")
        elif success_rate >= 0.8:
            recommendations.append("✓ Most tasks completed successfully. Review any failed tasks.")
        elif success_rate >= 0.5:
            recommendations.append("⚠ Partial success. Several tasks need attention.")
        else:
            recommendations.append("⚠ Many tasks failed. Consider reviewing the approach or breaking down further.")
        
        # Specific recommendations based on failures
        if failed_tasks:
            failed_actions = [t.get("action", "unknown") for t in failed_tasks]
            recommendations.append(f"Failed actions: {', '.join(set(failed_actions))}")
            
            # Check for patterns in failures
            if all(action == "test" for action in failed_actions):
                recommendations.append("Consider simplifying test requirements")
            elif all(action == "optimize" for action in failed_actions):
                recommendations.append("Optimization may need more context or simpler goals")
        
        # Confidence-based recommendations
        avg_confidence = sum(r.get("confidence", 0) for r in all_results) / total_count
        if avg_confidence < 0.7:
            recommendations.append("Consider providing more context or breaking tasks into smaller steps")
        
        return recommendations
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get task orchestrator status
        
        Returns:
            Dict with status information
        """
        return {
            "meta_orchestrator_available": self.meta_orchestrator is not None,
            "goal_integrity_available": self.goal_integrity is not None,
            "smart_coding_ai_configured": self.smart_coding_ai is not None,
            "module": "task_orchestration",
            "version": "1.0.0"
        }

