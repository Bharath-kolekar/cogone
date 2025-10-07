"""
Practicality Validator for AI Orchestration
Ensures solutions are practical and not over-engineered
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class PracticalityValidator:
    """Ensures solutions are practical and not over-engineered"""
    
    def __init__(self):
        self.practicality_rules = self._load_practicality_rules()
        self.complexity_thresholds = self._load_complexity_thresholds()
        
    def _load_practicality_rules(self) -> Dict[str, Any]:
        """Load practicality rules"""
        return {
            "max_complexity": 10,
            "max_nesting": 5,
            "max_parameters": 5,
            "max_file_size": 1000,
            "min_functionality": 0.8
        }
    
    def _load_complexity_thresholds(self) -> Dict[str, int]:
        """Load complexity thresholds"""
        return {
            "cyclomatic_complexity": 10,
            "nesting_depth": 5,
            "parameter_count": 5,
            "line_count": 1000
        }
    
    async def validate_practicality(self, code: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate code practicality"""
        try:
            practicality_result = {
                "is_practical": True,
                "over_engineering": [],
                "complexity_issues": [],
                "simplification_suggestions": []
            }
            
            # Check for over-engineering
            over_engineering = await self._check_over_engineering(code)
            practicality_result["over_engineering"].extend(over_engineering)
            
            # Check complexity
            complexity_issues = await self._check_complexity(code)
            practicality_result["complexity_issues"].extend(complexity_issues)
            
            # Generate simplification suggestions
            simplifications = await self._generate_simplification_suggestions(code)
            practicality_result["simplification_suggestions"].extend(simplifications)
            
            # Update practicality status
            practicality_result["is_practical"] = len(over_engineering) == 0 and len(complexity_issues) == 0
            
            return practicality_result
            
        except Exception as e:
            logger.error(f"Error validating practicality: {e}")
            return {"is_practical": False, "over_engineering": [f"Practicality error: {str(e)}"]}
    
    async def _check_over_engineering(self, code: str) -> List[str]:
        """Check for over-engineering"""
        issues = []
        
        # Check for unnecessary abstractions
        if 'abstract' in code.lower() and len(code.split('\n')) < 100:
            issues.append("Unnecessary abstraction for simple code")
        
        # Check for over-complex patterns
        if 'factory' in code.lower() and 'pattern' in code.lower():
            issues.append("Over-complex pattern for simple functionality")
        
        return issues
    
    async def _check_complexity(self, code: str) -> List[str]:
        """Check code complexity"""
        issues = []
        
        # Check cyclomatic complexity
        complexity = len(re.findall(r'\b(if|elif|for|while|except|and|or)\b', code))
        if complexity > self.complexity_thresholds["cyclomatic_complexity"]:
            issues.append(f"High cyclomatic complexity: {complexity}")
        
        # Check nesting depth
        max_nesting = 0
        current_nesting = 0
        for char in code:
            if char in '{[(':
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif char in '}])':
                current_nesting -= 1
        
        if max_nesting > self.complexity_thresholds["nesting_depth"]:
            issues.append(f"High nesting depth: {max_nesting}")
        
        return issues
    
    async def _generate_simplification_suggestions(self, code: str) -> List[str]:
        """Generate simplification suggestions"""
        suggestions = []
        
        # Suggest simpler alternatives
        if 'class ' in code and len(code.split('\n')) < 50:
            suggestions.append("Consider using functions instead of classes for simple functionality")
        
        # Suggest removing unnecessary complexity
        if 'try:' in code and 'except:' in code:
            suggestions.append("Consider simplifying error handling")
        
        return suggestions

