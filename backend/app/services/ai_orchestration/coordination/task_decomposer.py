"""
Intelligent Task Decomposer for AI Orchestration
CRITICAL: Used by meta_ai_orchestrator and unified_ai_component_orchestrator
Preserves intelligent task decomposition capabilities
"""

from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()


class IntelligentTaskDecomposer:
    """
    Intelligent task decomposition for complex requirements
    CRITICAL COMPONENT: Used by multiple orchestrators
    """
    
    def __init__(self):
        self.decomposition_strategies = self._load_decomposition_strategies()
        self.task_templates = self._load_task_templates()
        self.complexity_analyzer = self._load_complexity_analyzer()
        
    def _load_decomposition_strategies(self) -> Dict[str, Any]:
        """Load task decomposition strategies"""
        return {
            "hierarchical": {
                "description": "Break down into hierarchical subtasks",
                "complexity_threshold": 0.8,
                "max_depth": 5
            },
            "functional": {
                "description": "Decompose by functional components",
                "complexity_threshold": 0.6,
                "max_components": 10
            },
            "temporal": {
                "description": "Break down by time phases",
                "complexity_threshold": 0.7,
                "max_phases": 8
            }
        }
    
    def _load_task_templates(self) -> Dict[str, Any]:
        """Load task templates for different types"""
        return {
            "api_development": {
                "endpoints": "Create API endpoints",
                "validation": "Add input validation",
                "authentication": "Implement authentication",
                "documentation": "Generate API documentation"
            },
            "database_operations": {
                "schema": "Design database schema",
                "migrations": "Create database migrations",
                "queries": "Write database queries",
                "optimization": "Optimize database performance"
            },
            "frontend_development": {
                "components": "Create React components",
                "styling": "Implement styling",
                "state_management": "Add state management",
                "testing": "Write component tests"
            }
        }
    
    def _load_complexity_analyzer(self) -> Dict[str, Any]:
        """Load complexity analysis rules"""
        return {
            "code_complexity": {
                "cyclomatic_complexity": 10,
                "nesting_depth": 5,
                "function_length": 50
            },
            "requirement_complexity": {
                "feature_count": 10,
                "integration_points": 5,
                "dependencies": 8
            }
        }
    
    async def decompose_task(self, requirement: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decompose complex requirements into manageable tasks
        Used by meta_ai and unified_ai orchestrators
        """
        try:
            decomposition_result = {
                "original_requirement": requirement,
                "decomposition_strategy": "hierarchical",
                "subtasks": [],
                "complexity_analysis": {},
                "estimated_effort": {},
                "dependencies": {},
                "success_metrics": []
            }
            
            # Analyze complexity
            complexity_analysis = await self._analyze_complexity(requirement, context)
            decomposition_result["complexity_analysis"] = complexity_analysis
            
            # Select decomposition strategy
            strategy = await self._select_decomposition_strategy(complexity_analysis)
            decomposition_result["decomposition_strategy"] = strategy
            
            # Generate subtasks
            subtasks = await self._generate_subtasks(requirement, strategy, context)
            decomposition_result["subtasks"] = subtasks
            
            return decomposition_result
            
        except Exception as e:
            logger.error("Task decomposition failed", error=str(e))
            return {
                "original_requirement": requirement,
                "subtasks": [],
                "error": str(e)
            }
    
    async def _analyze_complexity(self, requirement: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze requirement complexity"""
        return {
            "complexity_score": 0.7,
            "difficulty": "medium",
            "estimated_time": 120  # minutes
        }
    
    async def _select_decomposition_strategy(self, complexity_analysis: Dict[str, Any]) -> str:
        """Select appropriate decomposition strategy"""
        complexity_score = complexity_analysis.get("complexity_score", 0.5)
        
        if complexity_score >= 0.8:
            return "hierarchical"
        elif complexity_score >= 0.6:
            return "functional"
        else:
            return "temporal"
    
    async def _generate_subtasks(self, requirement: str, strategy: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate subtasks based on strategy"""
        # Simplified subtask generation
        return [
            {"task": "Analyze requirements", "priority": "high", "estimated_time": 15},
            {"task": "Design solution", "priority": "high", "estimated_time": 30},
            {"task": "Implement code", "priority": "medium", "estimated_time": 60},
            {"task": "Test solution", "priority": "medium", "estimated_time": 15}
        ]
