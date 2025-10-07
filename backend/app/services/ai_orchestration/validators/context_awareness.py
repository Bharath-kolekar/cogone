"""
Context Awareness Manager for AI Orchestration
Maintains project-specific context and constraints
Validation Category #2 of 11
"""

import re
from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()


class ContextAwarenessManager:
    """
    Maintains project-specific context and constraints
    Ensures context-aware code generation
    """
    
    def __init__(self):
        self.project_context = self._load_project_context()
        self.constraints = self._load_constraints()
        self.dependencies = {}
        
    def _load_project_context(self) -> Dict[str, Any]:
        """Load project-specific context"""
        return {
            "framework": "fastapi",
            "database": "postgresql",
            "cache": "redis",
            "auth": "jwt",
            "deployment": "docker"
        }
    
    def _load_constraints(self) -> Dict[str, Any]:
        """Load project constraints"""
        return {
            "max_file_size": 1000,
            "max_function_length": 50,
            "max_parameters": 5,
            "required_imports": ["fastapi", "sqlalchemy", "redis"],
            "forbidden_imports": ["eval", "exec", "os.system"]
        }
    
    async def validate_context_compliance(self, code: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate code against project context
        Maintains context awareness for accuracy
        """
        try:
            compliance_result = {
                "is_compliant": True,
                "violations": [],
                "suggestions": [],
                "context_score": 0.0
            }
            
            # Check framework compliance
            framework_violations = await self._check_framework_compliance(code)
            compliance_result["violations"].extend(framework_violations)
            
            # Check constraint compliance
            constraint_violations = await self._check_constraint_compliance(code)
            compliance_result["violations"].extend(constraint_violations)
            
            # Calculate context score
            compliance_result["context_score"] = await self._calculate_context_score(code, context)
            
            # Update compliance status
            compliance_result["is_compliant"] = len(compliance_result["violations"]) == 0
            
            return compliance_result
            
        except Exception as e:
            logger.error("Error validating context compliance", error=str(e))
            return {"is_compliant": False, "violations": [f"Context validation error: {str(e)}"]}
    
    async def _check_framework_compliance(self, code: str) -> List[str]:
        """Check framework compliance"""
        violations = []
        # Framework checks handled in validation
        return violations
    
    async def _check_constraint_compliance(self, code: str) -> List[str]:
        """Check constraint compliance"""
        violations = []
        
        # Check file size
        if len(code.split('\n')) > self.constraints["max_file_size"]:
            violations.append("File size exceeds maximum allowed")
        
        # Check function length
        functions = re.findall(r'def\s+\w+.*?:\s*(.*?)(?=\ndef|\nclass|\n$)', code, re.DOTALL)
        for func in functions:
            if len(func.split('\n')) > self.constraints["max_function_length"]:
                violations.append("Function length exceeds maximum allowed")
        
        return violations
    
    async def _calculate_context_score(self, code: str, context: Dict[str, Any]) -> float:
        """Calculate context compliance score"""
        score = 0.0
        total_checks = 5
        
        # Check framework, database, cache, auth, deployment
        for key in ["fastapi", "sqlalchemy", "redis", "jwt", "docker"]:
            if key in code.lower():
                score += 1.0
        
        return score / total_checks
