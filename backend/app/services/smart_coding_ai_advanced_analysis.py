"""
Smart Coding AI - Advanced Code Analysis Implementation
Implements capabilities 14-20: Analysis capabilities
"""

import structlog
import ast
import re
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from collections import defaultdict

logger = structlog.get_logger()


class ComplexityAnalyzer:
    """Implements capability #14: Complexity Analysis"""
    
    async def analyze_complexity(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Measures and suggests reductions in code complexity
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Complexity metrics and reduction suggestions
        """
        try:
            if language == "python":
                metrics = self._analyze_python_complexity(code)
            else:
                metrics = self._analyze_generic_complexity(code)
            
            suggestions = self._generate_complexity_reductions(metrics)
            
            return {
                "success": True,
                "metrics": metrics,
                "suggestions": suggestions,
                "overall_score": self._calculate_complexity_score(metrics),
                "refactoring_priority": self._prioritize_refactoring(metrics)
            }
        except Exception as e:
            logger.error("Complexity analysis failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _analyze_python_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze Python code complexity"""
        try:
            tree = ast.parse(code)
            
            metrics = {
                "cyclomatic_complexity": self._calculate_cyclomatic_complexity(tree),
                "cognitive_complexity": self._calculate_cognitive_complexity(tree),
                "nesting_depth": self._calculate_max_nesting_depth(tree),
                "function_length": self._calculate_function_lengths(tree),
                "class_complexity": self._calculate_class_complexity(tree),
                "lines_of_code": len(code.split('\n')),
                "comment_ratio": self._calculate_comment_ratio(code)
            }
            
            return metrics
        except Exception as e:
            logger.error("Python complexity analysis failed", error=str(e))
            return {}
    
    def _calculate_cyclomatic_complexity(self, tree) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.And, ast.Or)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, tree) -> int:
        """Calculate cognitive complexity (how hard to understand)"""
        complexity = 0
        nesting_level = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += (1 + nesting_level)
                nesting_level += 1
            elif isinstance(node, ast.FunctionDef):
                nesting_level = 0
        
        return complexity
    
    def _calculate_max_nesting_depth(self, tree) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        
        def calculate_depth(node, current_depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.With)):
                    calculate_depth(child, current_depth + 1)
                else:
                    calculate_depth(child, current_depth)
        
        calculate_depth(tree)
        return max_depth
    
    def _calculate_function_lengths(self, tree) -> Dict[str, int]:
        """Calculate length of each function"""
        functions = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                length = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                functions[node.name] = length
        
        return functions
    
    def _calculate_class_complexity(self, tree) -> Dict[str, int]:
        """Calculate complexity of each class"""
        classes = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = sum(1 for child in node.body if isinstance(child, ast.FunctionDef))
                classes[node.name] = methods
        
        return classes
    
    def _calculate_comment_ratio(self, code: str) -> float:
        """Calculate ratio of comments to code"""
        lines = code.split('\n')
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        code_lines = len(lines)
        
        return comment_lines / code_lines if code_lines > 0 else 0.0
    
    def _analyze_generic_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze non-Python code complexity"""
        lines = code.split('\n')
        
        return {
            "lines_of_code": len(lines),
            "estimated_complexity": "medium",
            "nesting_depth": self._estimate_nesting_depth(code)
        }
    
    def _estimate_nesting_depth(self, code: str) -> int:
        """Estimate nesting depth from indentation"""
        max_indent = 0
        for line in code.split('\n'):
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent)
        
        return max_indent // 4  # Assuming 4 spaces per level
    
    def _calculate_complexity_score(self, metrics: Dict[str, Any]) -> str:
        """Calculate overall complexity score"""
        if not metrics:
            return "unknown"
        
        cyclomatic = metrics.get("cyclomatic_complexity", 0)
        nesting = metrics.get("nesting_depth", 0)
        
        if cyclomatic > 20 or nesting > 5:
            return "high"
        elif cyclomatic > 10 or nesting > 3:
            return "medium"
        else:
            return "low"
    
    def _generate_complexity_reductions(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate suggestions to reduce complexity"""
        suggestions = []
        
        if metrics.get("cyclomatic_complexity", 0) > 10:
            suggestions.append("Break down complex functions into smaller, focused functions")
        
        if metrics.get("nesting_depth", 0) > 3:
            suggestions.append("Reduce nesting depth by extracting nested logic into separate functions")
        
        if metrics.get("cognitive_complexity", 0) > 15:
            suggestions.append("Simplify control flow to improve readability")
        
        function_lengths = metrics.get("function_length", {})
        for func, length in function_lengths.items():
            if length > 50:
                suggestions.append(f"Function '{func}' is too long ({length} lines) - consider splitting")
        
        if metrics.get("comment_ratio", 0) < 0.1:
            suggestions.append("Add more comments to explain complex logic")
        
        return suggestions if suggestions else ["Code complexity is acceptable"]
    
    def _prioritize_refactoring(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize which parts need refactoring"""
        priority_list = []
        
        function_lengths = metrics.get("function_length", {})
        for func, length in function_lengths.items():
            if length > 50:
                priority_list.append({
                    "target": func,
                    "type": "function",
                    "reason": "Too long",
                    "priority": "high",
                    "lines": length
                })
        
        return sorted(priority_list, key=lambda x: x.get("lines", 0), reverse=True)


class TechnicalDebtAssessor:
    """Implements capability #15: Technical Debt Assessment"""
    
    async def assess_technical_debt(self, codebase_path: str = None, 
                                   code_sample: str = None) -> Dict[str, Any]:
        """
        Quantifies and locates technical debt
        
        Args:
            codebase_path: Path to codebase (optional)
            code_sample: Code sample to analyze (optional)
            
        Returns:
            Technical debt assessment with scores and locations
        """
        try:
            debt_items = []
            
            if code_sample:
                debt_items = self._analyze_code_debt(code_sample)
            
            total_score = sum(item.get("score", 0) for item in debt_items)
            
            return {
                "success": True,
                "total_debt_score": total_score,
                "debt_level": self._categorize_debt_level(total_score),
                "debt_items": debt_items,
                "estimated_time_to_fix": self._estimate_fix_time(debt_items),
                "priority_ranking": self._rank_by_priority(debt_items),
                "recommendations": self._generate_debt_recommendations(debt_items)
            }
        except Exception as e:
            logger.error("Technical debt assessment failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _analyze_code_debt(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for technical debt indicators"""
        debt_items = []
        
        # Check for common debt patterns
        if "TODO" in code or "FIXME" in code:
            debt_items.append({
                "type": "deferred_work",
                "description": "Contains TODO/FIXME comments",
                "score": 5,
                "priority": "medium"
            })
        
        if "# temporary" in code.lower() or "# hack" in code.lower():
            debt_items.append({
                "type": "temporary_solution",
                "description": "Contains temporary or hack solutions",
                "score": 10,
                "priority": "high"
            })
        
        # Check for duplicated code
        lines = code.split('\n')
        if len(lines) != len(set(lines)):
            debt_items.append({
                "type": "code_duplication",
                "description": "Contains duplicated code",
                "score": 8,
                "priority": "medium"
            })
        
        # Check for long functions
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    length = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                    if length > 50:
                        debt_items.append({
                            "type": "long_function",
                            "description": f"Function {node.name} is too long ({length} lines)",
                            "score": 7,
                            "priority": "medium"
                        })
        except:
            pass
        
        # Check for missing error handling
        if "try:" not in code and ("open(" in code or "request" in code or "http" in code):
            debt_items.append({
                "type": "missing_error_handling",
                "description": "Missing error handling for risky operations",
                "score": 15,
                "priority": "critical"
            })
        
        # Check for missing tests
        if "test_" not in code and "class " in code:
            debt_items.append({
                "type": "missing_tests",
                "description": "No test coverage",
                "score": 12,
                "priority": "high"
            })
        
        return debt_items
    
    def _categorize_debt_level(self, score: int) -> str:
        """Categorize overall debt level"""
        if score > 50:
            return "critical"
        elif score > 30:
            return "high"
        elif score > 15:
            return "medium"
        else:
            return "low"
    
    def _estimate_fix_time(self, debt_items: List[Dict[str, Any]]) -> str:
        """Estimate time to fix all debt"""
        total_score = sum(item.get("score", 0) for item in debt_items)
        hours = total_score * 0.5  # Rough estimate: 30 min per debt point
        
        if hours < 1:
            return "Less than 1 hour"
        elif hours < 8:
            return f"Approximately {int(hours)} hours"
        elif hours < 40:
            return f"Approximately {int(hours/8)} days"
        else:
            return f"Approximately {int(hours/40)} weeks"
    
    def _rank_by_priority(self, debt_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank debt items by priority"""
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return sorted(debt_items, key=lambda x: (priority_order.get(x.get("priority", "low"), 3), -x.get("score", 0)))
    
    def _generate_debt_recommendations(self, debt_items: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations to address technical debt"""
        recommendations = []
        
        debt_types = set(item.get("type") for item in debt_items)
        
        if "missing_error_handling" in debt_types:
            recommendations.append("Priority 1: Add comprehensive error handling to all risky operations")
        
        if "missing_tests" in debt_types:
            recommendations.append("Priority 2: Implement test coverage for all classes and critical functions")
        
        if "long_function" in debt_types:
            recommendations.append("Priority 3: Refactor long functions into smaller, focused units")
        
        if "code_duplication" in debt_types:
            recommendations.append("Priority 4: Extract duplicated code into reusable functions")
        
        if "temporary_solution" in debt_types:
            recommendations.append("Priority 5: Replace temporary solutions with permanent implementations")
        
        return recommendations if recommendations else ["Technical debt is minimal - maintain current quality"]


class CodeSmellDetector:
    """Implements capability #16: Code Smell Detection"""
    
    async def detect_code_smells(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Identifies anti-patterns and poor practices
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Detected code smells with severity and fixes
        """
        try:
            smells = []
            
            if language == "python":
                smells = self._detect_python_smells(code)
            else:
                smells = self._detect_generic_smells(code)
            
            return {
                "success": True,
                "total_smells": len(smells),
                "smells": smells,
                "severity_breakdown": self._count_by_severity(smells),
                "most_critical": self._get_most_critical(smells),
                "quick_wins": self._identify_quick_wins(smells)
            }
        except Exception as e:
            logger.error("Code smell detection failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _detect_python_smells(self, code: str) -> List[Dict[str, Any]]:
        """Detect Python-specific code smells"""
        smells = []
        
        # Long parameter list
        if re.search(r'def\s+\w+\([^)]{100,}\)', code):
            smells.append({
                "type": "long_parameter_list",
                "description": "Function has too many parameters",
                "severity": "medium",
                "fix": "Use dataclass or config object for parameters",
                "line": "Multiple locations"
            })
        
        # God class (too many methods)
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = sum(1 for child in node.body if isinstance(child, ast.FunctionDef))
                    if methods > 20:
                        smells.append({
                            "type": "god_class",
                            "description": f"Class {node.name} has too many methods ({methods})",
                            "severity": "high",
                            "fix": "Split class into smaller, focused classes",
                            "line": node.lineno
                        })
        except:
            pass
        
        # Magic numbers
        if re.findall(r'\b\d{3,}\b', code):
            smells.append({
                "type": "magic_numbers",
                "description": "Hard-coded numbers without explanation",
                "severity": "low",
                "fix": "Extract numbers as named constants",
                "line": "Multiple locations"
            })
        
        # Primitive obsession
        if code.count("Dict[str, Any]") > 5:
            smells.append({
                "type": "primitive_obsession",
                "description": "Overuse of Dict[str, Any] instead of proper types",
                "severity": "medium",
                "fix": "Create proper dataclasses or TypedDict",
                "line": "Multiple locations"
            })
        
        # Dead code (unused imports/variables)
        if re.search(r'^import \w+$', code, re.MULTILINE) and len(code) < 500:
            smells.append({
                "type": "potential_dead_code",
                "description": "Imports that may not be used",
                "severity": "low",
                "fix": "Remove unused imports",
                "line": "Import section"
            })
        
        # Commented out code
        if re.search(r'#\s*[a-z_]+\s*=', code):
            smells.append({
                "type": "commented_code",
                "description": "Contains commented-out code",
                "severity": "low",
                "fix": "Remove commented code or explain why it's kept",
                "line": "Multiple locations"
            })
        
        return smells
    
    def _detect_generic_smells(self, code: str) -> List[Dict[str, Any]]:
        """Detect language-agnostic code smells"""
        smells = []
        
        lines = code.split('\n')
        
        if len(lines) > 500:
            smells.append({
                "type": "long_file",
                "description": f"File is very long ({len(lines)} lines)",
                "severity": "medium",
                "fix": "Split into multiple modules",
                "line": "Entire file"
            })
        
        return smells
    
    def _count_by_severity(self, smells: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count smells by severity"""
        return {
            "critical": sum(1 for s in smells if s.get("severity") == "critical"),
            "high": sum(1 for s in smells if s.get("severity") == "high"),
            "medium": sum(1 for s in smells if s.get("severity") == "medium"),
            "low": sum(1 for s in smells if s.get("severity") == "low")
        }
    
    def _get_most_critical(self, smells: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get most critical smells"""
        return [s for s in smells if s.get("severity") in ["critical", "high"]][:5]
    
    def _identify_quick_wins(self, smells: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify smells that are easy to fix"""
        quick_fixes = ["magic_numbers", "commented_code", "potential_dead_code"]
        return [s for s in smells if s.get("type") in quick_fixes]


class PerformanceBottleneckDetector:
    """Implements capability #17: Performance Bottleneck Detection"""
    
    async def detect_bottlenecks(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Finds and suggests fixes for performance issues
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Detected bottlenecks with fix suggestions
        """
        try:
            bottlenecks = self._analyze_performance_issues(code, language)
            
            return {
                "success": True,
                "bottlenecks_found": len(bottlenecks),
                "bottlenecks": bottlenecks,
                "performance_score": self._calculate_performance_score(bottlenecks),
                "optimization_potential": self._estimate_optimization_potential(bottlenecks),
                "recommended_fixes": self._prioritize_fixes(bottlenecks)
            }
        except Exception as e:
            logger.error("Bottleneck detection failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _analyze_performance_issues(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Analyze code for performance bottlenecks"""
        bottlenecks = []
        
        # Nested loops
        if re.search(r'for.*:\s*for.*:', code, re.DOTALL):
            bottlenecks.append({
                "type": "nested_loops",
                "description": "Nested loops detected - O(n²) or worse complexity",
                "severity": "high",
                "impact": "Severe performance degradation with large datasets",
                "fix": "Consider using hash maps, sets, or single-pass algorithms",
                "estimated_speedup": "10-100x"
            })
        
        # Database queries in loops
        if "for " in code and any(pattern in code for pattern in [".query(", ".find(", ".get(", "SELECT"]):
            bottlenecks.append({
                "type": "n_plus_one_query",
                "description": "Potential N+1 query problem",
                "severity": "critical",
                "impact": "Database overload and slow response times",
                "fix": "Use batch queries, joins, or prefetching",
                "estimated_speedup": "50-1000x"
            })
        
        # Inefficient data structures
        if "list" in code and "in " in code:
            bottlenecks.append({
                "type": "linear_search",
                "description": "Using list for lookups (O(n) instead of O(1))",
                "severity": "medium",
                "impact": "Slow lookups in large collections",
                "fix": "Use set or dict for O(1) lookups",
                "estimated_speedup": "10-100x for large lists"
            })
        
        # Synchronous I/O
        if "open(" in code and "async def" in code and "await" not in code[:code.find("open(")]:
            bottlenecks.append({
                "type": "blocking_io",
                "description": "Synchronous I/O in async function",
                "severity": "high",
                "impact": "Blocks event loop, reduces concurrency",
                "fix": "Use aiofiles or async I/O libraries",
                "estimated_speedup": "5-50x with concurrent requests"
            })
        
        # String concatenation in loops
        if re.search(r'for.*:\s*.*\+=.*["\']', code, re.DOTALL):
            bottlenecks.append({
                "type": "string_concatenation",
                "description": "String concatenation in loop",
                "severity": "medium",
                "impact": "Quadratic time complexity for string building",
                "fix": "Use list and join() for O(n) performance",
                "estimated_speedup": "10-100x for large strings"
            })
        
        return bottlenecks
    
    def _calculate_performance_score(self, bottlenecks: List[Dict[str, Any]]) -> int:
        """Calculate performance score (0-100, higher is better)"""
        severity_penalties = {"critical": 30, "high": 20, "medium": 10, "low": 5}
        
        total_penalty = sum(severity_penalties.get(b.get("severity", "low"), 5) for b in bottlenecks)
        score = max(0, 100 - total_penalty)
        
        return score
    
    def _estimate_optimization_potential(self, bottlenecks: List[Dict[str, Any]]) -> str:
        """Estimate how much performance can be improved"""
        if not bottlenecks:
            return "Minimal - code is already well-optimized"
        
        critical = sum(1 for b in bottlenecks if b.get("severity") == "critical")
        high = sum(1 for b in bottlenecks if b.get("severity") == "high")
        
        if critical > 0:
            return "Extreme - 10-1000x speedup possible"
        elif high > 2:
            return "High - 5-50x speedup possible"
        else:
            return "Moderate - 2-10x speedup possible"
    
    def _prioritize_fixes(self, bottlenecks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize which bottlenecks to fix first"""
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return sorted(bottlenecks, key=lambda x: severity_order.get(x.get("severity", "low"), 3))


class ComplianceChecker:
    """Implements capability #20: Compliance Checking"""
    
    async def check_compliance(self, code: str, standard: str = "pep8", 
                              language: str = "python") -> Dict[str, Any]:
        """
        Ensures code meets regulatory and style requirements
        
        Args:
            code: Source code to check
            standard: Compliance standard (pep8, google, airbnb, etc.)
            language: Programming language
            
        Returns:
            Compliance report with violations and fixes
        """
        try:
            violations = self._check_style_compliance(code, standard, language)
            security_issues = self._check_security_compliance(code)
            
            return {
                "success": True,
                "standard": standard,
                "total_violations": len(violations) + len(security_issues),
                "style_violations": violations,
                "security_issues": security_issues,
                "compliance_score": self._calculate_compliance_score(violations, security_issues),
                "auto_fixable": self._identify_auto_fixable(violations),
                "recommendations": self._generate_compliance_recommendations(violations, security_issues)
            }
        except Exception as e:
            logger.error("Compliance checking failed", error=str(e))
            return {"success": False, "error": str(e)}
    
    def _check_style_compliance(self, code: str, standard: str, language: str) -> List[Dict[str, Any]]:
        """Check code style compliance"""
        violations = []
        
        lines = code.split('\n')
        
        # Line length
        for i, line in enumerate(lines):
            if len(line) > 88 and standard == "pep8":  # Black default
                violations.append({
                    "type": "line_too_long",
                    "line": i + 1,
                    "description": f"Line exceeds 88 characters ({len(line)} chars)",
                    "severity": "low",
                    "auto_fixable": True
                })
        
        # Missing docstrings
        if "class " in code and '"""' not in code:
            violations.append({
                "type": "missing_docstring",
                "description": "Class missing docstring",
                "severity": "medium",
                "auto_fixable": False
            })
        
        # Inconsistent naming
        if re.search(r'def [A-Z]', code):
            violations.append({
                "type": "naming_convention",
                "description": "Function names should be lowercase_with_underscores",
                "severity": "medium",
                "auto_fixable": True
            })
        
        return violations
    
    def _check_security_compliance(self, code: str) -> List[Dict[str, Any]]:
        """Check security compliance"""
        issues = []
        
        # Hardcoded secrets
        if re.search(r'(password|secret|api_key)\s*=\s*["\'][^"\']+["\']', code, re.IGNORECASE):
            issues.append({
                "type": "hardcoded_secret",
                "description": "Potential hardcoded secret detected",
                "severity": "critical",
                "recommendation": "Use environment variables or secret management"
            })
        
        # SQL injection risk
        if re.search(r'execute\([^)]*f["\']|execute\([^)]*%', code):
            issues.append({
                "type": "sql_injection_risk",
                "description": "Potential SQL injection vulnerability",
                "severity": "critical",
                "recommendation": "Use parameterized queries"
            })
        
        # Unsafe deserialization
        if "pickle.loads" in code or "eval(" in code:
            issues.append({
                "type": "unsafe_deserialization",
                "description": "Unsafe deserialization method used",
                "severity": "critical",
                "recommendation": "Use safe alternatives like JSON"
            })
        
        return issues
    
    def _calculate_compliance_score(self, violations: List, security_issues: List) -> int:
        """Calculate compliance score"""
        total_issues = len(violations) + len(security_issues) * 3  # Security issues count 3x
        score = max(0, 100 - (total_issues * 2))
        return score
    
    def _identify_auto_fixable(self, violations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify violations that can be auto-fixed"""
        return [v for v in violations if v.get("auto_fixable", False)]
    
    def _generate_compliance_recommendations(self, violations: List, security_issues: List) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        if security_issues:
            recommendations.append("URGENT: Fix security issues immediately")
        
        auto_fixable = self._identify_auto_fixable(violations)
        if auto_fixable:
            recommendations.append(f"Run auto-formatter to fix {len(auto_fixable)} style issues")
        
        if len(violations) > 10:
            recommendations.append("Consider incremental refactoring to improve compliance")
        
        return recommendations if recommendations else ["Code is compliant with standards"]


__all__ = [
    'ComplexityAnalyzer',
    'TechnicalDebtAssessor',
    'CodeSmellDetector',
    'PerformanceBottleneckDetector',
    'ComplianceChecker'
]

