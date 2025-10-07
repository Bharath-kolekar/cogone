"""
Code Quality Analyzer for AI Orchestration
Analyzes and improves code quality
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class CodeQualityAnalyzer:
    """Analyzes and improves code quality"""
    
    def __init__(self):
        self.quality_rules = self._load_quality_rules()
        self.anti_patterns = self._load_anti_patterns()
        
    def _load_quality_rules(self) -> Dict[str, Any]:
        """Load code quality rules"""
        return {
            "dead_code": {
                "unused_imports": True,
                "unused_variables": True,
                "unreachable_code": True
            },
            "duplication": {
                "similar_functions": True,
                "copy_paste_code": True,
                "repeated_patterns": True
            },
            "magic_numbers": {
                "hardcoded_values": True,
                "magic_strings": True,
                "configuration_values": True
            }
        }
    
    def _load_anti_patterns(self) -> Dict[str, List[str]]:
        """Load code anti-patterns"""
        return {
            "dead_code": [
                r'import\s+\w+\s*$',
                r'def\s+\w+.*:\s*$',
                r'class\s+\w+.*:\s*$'
            ],
            "duplication": [
                r'def\s+\w+.*:\s*.*def\s+\w+.*:\s*',
                r'class\s+\w+.*:\s*.*class\s+\w+.*:\s*'
            ],
            "magic_numbers": [
                r'\b\d+\b',
                r'"[^"]*"',
                r"'[^']*'"
            ]
        }
    
    async def analyze_code_quality(self, code: str) -> Dict[str, Any]:
        """Analyze code quality"""
        try:
            quality_result = {
                "is_high_quality": True,
                "quality_issues": [],
                "improvements": [],
                "metrics": {}
            }
            
            # Check for dead code
            dead_code_issues = await self._check_dead_code(code)
            quality_result["quality_issues"].extend(dead_code_issues)
            
            # Check for duplication
            duplication_issues = await self._check_duplication(code)
            quality_result["quality_issues"].extend(duplication_issues)
            
            # Check for magic numbers
            magic_number_issues = await self._check_magic_numbers(code)
            quality_result["quality_issues"].extend(magic_number_issues)
            
            # Calculate quality metrics
            metrics = await self._calculate_quality_metrics(code)
            quality_result["metrics"] = metrics
            
            # Update quality status
            quality_result["is_high_quality"] = len(quality_result["quality_issues"]) == 0
            
            return quality_result
            
        except Exception as e:
            logger.error(f"Error analyzing code quality: {e}")
            return {"is_high_quality": False, "quality_issues": [f"Quality analysis error: {str(e)}"]}
    
    async def _check_dead_code(self, code: str) -> List[str]:
        """Check for dead code"""
        issues = []
        
        # Check for unused imports
        imports = re.findall(r'import\s+(\w+)', code)
        for imp in imports:
            if imp not in code.replace(f'import {imp}', ''):
                issues.append(f"Unused import: {imp}")
        
        # Check for unused variables
        variables = re.findall(r'(\w+)\s*=', code)
        for var in variables:
            if var not in code.replace(f'{var} =', ''):
                issues.append(f"Unused variable: {var}")
        
        return issues
    
    async def _check_duplication(self, code: str) -> List[str]:
        """Check for code duplication"""
        issues = []
        
        # Check for similar functions
        functions = re.findall(r'def\s+(\w+).*?:\s*(.*?)(?=\ndef|\nclass|\n$)', code, re.DOTALL)
        for i, (name1, body1) in enumerate(functions):
            for j, (name2, body2) in enumerate(functions[i+1:], i+1):
                if self._calculate_similarity(body1, body2) > 0.8:
                    issues.append(f"Similar functions: {name1} and {name2}")
        
        return issues
    
    async def _check_magic_numbers(self, code: str) -> List[str]:
        """Check for magic numbers"""
        issues = []
        
        # Find magic numbers
        magic_numbers = re.findall(r'\b(\d+)\b', code)
        for num in magic_numbers:
            if int(num) > 10:  # Threshold for magic numbers
                issues.append(f"Magic number: {num}")
        
        return issues
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity"""
        # Simple similarity calculation
        words1 = set(text1.split())
        words2 = set(text2.split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0
    
    async def _calculate_quality_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate quality metrics"""
        metrics = {
            "lines_of_code": len(code.split('\n')),
            "function_count": len(re.findall(r'def\s+\w+', code)),
            "class_count": len(re.findall(r'class\s+\w+', code)),
            "comment_ratio": 0.0,
            "complexity_score": 0
        }
        
        # Calculate comment ratio
        lines = code.split('\n')
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        metrics["comment_ratio"] = comment_lines / len(lines) if lines else 0
        
        # Calculate complexity score
        metrics["complexity_score"] = len(re.findall(r'\b(if|elif|for|while|except|and|or)\b', code))
        
        return metrics

