"""
Performance Optimizer for AI Orchestration
Optimizes code performance and prevents performance issues
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class PerformanceOptimizer:
    """Optimizes code performance and prevents performance issues"""
    
    def __init__(self):
        self.performance_patterns = self._load_performance_patterns()
        self.optimization_rules = self._load_optimization_rules()
        
    def _load_performance_patterns(self) -> Dict[str, List[str]]:
        """Load performance anti-patterns"""
        return {
            "memory_leaks": [
                r'global\s+\w+',
                r'class\s+\w+.*:\s*$',
                r'def\s+\w+.*:\s*$'
            ],
            "slow_queries": [
                r'SELECT\s+\*\s+FROM',
                r'WHERE\s+\w+\s+IN\s*\(',
                r'ORDER\s+BY\s+\w+\s+DESC'
            ],
            "inefficient_loops": [
                r'for\s+\w+\s+in\s+range\s*\(',
                r'while\s+True:',
                r'for\s+\w+\s+in\s+\w+\.keys\s*\('
            ]
        }
    
    def _load_optimization_rules(self) -> Dict[str, Any]:
        """Load optimization rules"""
        return {
            "max_function_complexity": 10,
            "max_nesting_depth": 5,
            "max_parameters": 5,
            "max_line_length": 88,
            "max_file_size": 1000
        }
    
    async def optimize_performance(self, code: str) -> Dict[str, Any]:
        """Optimize code performance"""
        try:
            optimization_result = {
                "is_optimized": True,
                "performance_issues": [],
                "optimizations": [],
                "metrics": {}
            }
            
            # Check for performance issues
            performance_issues = await self._check_performance_issues(code)
            optimization_result["performance_issues"].extend(performance_issues)
            
            # Suggest optimizations
            optimizations = await self._suggest_optimizations(code)
            optimization_result["optimizations"].extend(optimizations)
            
            # Calculate performance metrics
            metrics = await self._calculate_performance_metrics(code)
            optimization_result["metrics"] = metrics
            
            # Update optimization status
            optimization_result["is_optimized"] = len(optimization_result["performance_issues"]) == 0
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Error optimizing performance: {e}")
            return {"is_optimized": False, "performance_issues": [f"Performance error: {str(e)}"]}
    
    async def _check_performance_issues(self, code: str) -> List[str]:
        """Check for performance issues"""
        issues = []
        
        # Check for memory leaks
        for pattern in self.performance_patterns["memory_leaks"]:
            if re.search(pattern, code):
                issues.append(f"Potential memory leak: {pattern}")
        
        # Check for slow queries
        for pattern in self.performance_patterns["slow_queries"]:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(f"Slow query detected: {pattern}")
        
        # Check for inefficient loops
        for pattern in self.performance_patterns["inefficient_loops"]:
            if re.search(pattern, code):
                issues.append(f"Inefficient loop: {pattern}")
        
        return issues
    
    async def _suggest_optimizations(self, code: str) -> List[str]:
        """Suggest performance optimizations"""
        suggestions = []
        
        # Suggest list comprehensions
        if 'for ' in code and ' in ' in code:
            suggestions.append("Consider using list comprehensions for better performance")
        
        # Suggest async/await
        if 'def ' in code and 'await' not in code:
            suggestions.append("Consider using async/await for I/O operations")
        
        # Suggest caching
        if 'def ' in code and 'cache' not in code.lower():
            suggestions.append("Consider adding caching for expensive operations")
        
        return suggestions
    
    async def _calculate_performance_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate performance metrics"""
        metrics = {
            "cyclomatic_complexity": 0,
            "nesting_depth": 0,
            "function_count": 0,
            "class_count": 0,
            "import_count": 0
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
        
        # Count functions and classes
        metrics["function_count"] = len(re.findall(r'def\s+\w+', code))
        metrics["class_count"] = len(re.findall(r'class\s+\w+', code))
        metrics["import_count"] = len(re.findall(r'import\s+\w+|from\s+\w+\s+import', code))
        
        return metrics

