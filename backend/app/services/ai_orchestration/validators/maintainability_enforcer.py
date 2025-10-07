"""
Maintainability Enforcer for AI Orchestration
Prevents technical debt and ensures maintainability
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class MaintainabilityEnforcer:
    """Prevents technical debt and ensures maintainability"""
    
    def __init__(self):
        self.maintainability_rules = self._load_maintainability_rules()
        self.quality_metrics = self._load_quality_metrics()
        
    def _load_maintainability_rules(self) -> Dict[str, Any]:
        """Load maintainability rules"""
        return {
            "max_function_length": 50,
            "max_class_size": 200,
            "max_parameters": 5,
            "min_documentation": 0.8,
            "max_complexity": 10
        }
    
    def _load_quality_metrics(self) -> Dict[str, Any]:
        """Load quality metrics"""
        return {
            "cyclomatic_complexity": 10,
            "nesting_depth": 5,
            "parameter_count": 5,
            "line_count": 1000,
            "comment_ratio": 0.2
        }
    
    async def enforce_maintainability(self, code: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enforce code maintainability"""
        try:
            maintainability_result = {
                "is_maintainable": True,
                "maintainability_issues": [],
                "quality_metrics": {},
                "improvement_suggestions": []
            }
            
            # Check maintainability issues
            issues = await self._check_maintainability_issues(code)
            maintainability_result["maintainability_issues"].extend(issues)
            
            # Calculate quality metrics
            metrics = await self._calculate_quality_metrics(code)
            maintainability_result["quality_metrics"] = metrics
            
            # Generate improvement suggestions
            suggestions = await self._generate_improvement_suggestions(code)
            maintainability_result["improvement_suggestions"].extend(suggestions)
            
            # Update maintainability status
            maintainability_result["is_maintainable"] = len(issues) == 0
            
            return maintainability_result
            
        except Exception as e:
            logger.error(f"Error enforcing maintainability: {e}")
            return {"is_maintainable": False, "maintainability_issues": [f"Maintainability error: {str(e)}"]}
    
    async def _check_maintainability_issues(self, code: str) -> List[str]:
        """Check for maintainability issues"""
        issues = []
        
        # Check function length
        functions = re.findall(r'def\s+\w+.*?:\s*(.*?)(?=\ndef|\nclass|\n$)', code, re.DOTALL)
        for func in functions:
            if len(func.split('\n')) > self.maintainability_rules["max_function_length"]:
                issues.append("Function too long - consider breaking into smaller functions")
        
        # Check class size
        classes = re.findall(r'class\s+\w+.*?:\s*(.*?)(?=\nclass|\n$)', code, re.DOTALL)
        for cls in classes:
            if len(cls.split('\n')) > self.maintainability_rules["max_class_size"]:
                issues.append("Class too large - consider breaking into smaller classes")
        
        # Check parameter count
        functions = re.findall(r'def\s+\w+\((.*?)\):', code)
        for params in functions:
            param_count = len([p for p in params.split(',') if p.strip()])
            if param_count > self.maintainability_rules["max_parameters"]:
                issues.append("Too many parameters - consider using a configuration object")
        
        return issues
    
    async def _calculate_quality_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate quality metrics"""
        metrics = {
            "cyclomatic_complexity": 0,
            "nesting_depth": 0,
            "parameter_count": 0,
            "line_count": 0,
            "comment_ratio": 0.0
        }
        
        # Calculate cyclomatic complexity
        metrics["cyclomatic_complexity"] = len(re.findall(r'\b(if|elif|for|while|except|and|or)\b', code))
        
        # Calculate nesting depth
        max_nesting = 0
        current_nesting = 0
        for char in code:
            if char in '{[(':
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif char in '}])':
                current_nesting -= 1
        metrics["nesting_depth"] = max_nesting
        
        # Calculate parameter count
        functions = re.findall(r'def\s+\w+\((.*?)\):', code)
        total_params = 0
        for params in functions:
            total_params += len([p for p in params.split(',') if p.strip()])
        metrics["parameter_count"] = total_params
        
        # Calculate line count
        metrics["line_count"] = len(code.split('\n'))
        
        # Calculate comment ratio
        lines = code.split('\n')
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        metrics["comment_ratio"] = comment_lines / len(lines) if lines else 0
        
        return metrics
    
    async def _generate_improvement_suggestions(self, code: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Suggest adding documentation
        if 'def ' in code and '"""' not in code:
            suggestions.append("Add docstrings to functions")
        
        # Suggest adding type hints
        if 'def ' in code and '->' not in code:
            suggestions.append("Add type hints to function signatures")
        
        # Suggest adding tests
        if 'def ' in code and 'test' not in code.lower():
            suggestions.append("Add unit tests for functions")
        
        return suggestions

