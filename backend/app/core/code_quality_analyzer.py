"""
Code Quality Analyzer

This module provides comprehensive code quality analysis for the Ethical AI system,
including code metrics, complexity analysis, maintainability assessment, and quality recommendations.
"""

import ast
import re
import structlog
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import math

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core

logger = structlog.get_logger(__name__)

class QualityLevel(Enum):
    """Code quality levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"

class ComplexityLevel(Enum):
    """Code complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"

class QualityMetric(Enum):
    """Quality metrics"""
    CYCLOMATIC_COMPLEXITY = "cyclomatic_complexity"
    COGNITIVE_COMPLEXITY = "cognitive_complexity"
    MAINTAINABILITY_INDEX = "maintainability_index"
    TECHNICAL_DEBT = "technical_debt"
    CODE_COVERAGE = "code_coverage"
    DUPLICATION_RATIO = "duplication_ratio"
    DOCUMENTATION_COVERAGE = "documentation_coverage"

@dataclass
class QualityIssue:
    """Code quality issue representation"""
    issue_id: str
    metric_type: QualityMetric
    severity: QualityLevel
    description: str
    location: Optional[str] = None
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    recommendation: Optional[str] = None
    impact_score: float = 1.0

@dataclass
class QualityMetrics:
    """Code quality metrics"""
    lines_of_code: int
    comment_lines: int
    blank_lines: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    maintainability_index: float
    technical_debt_ratio: float
    duplication_ratio: float
    documentation_coverage: float
    function_count: int
    class_count: int
    average_function_length: float
    average_class_length: float

@dataclass
class QualityReport:
    """Code quality analysis report"""
    report_id: str
    timestamp: datetime
    overall_quality_score: float
    quality_level: QualityLevel
    complexity_level: ComplexityLevel
    metrics: QualityMetrics
    issues_found: List[QualityIssue]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

class CodeQualityAnalyzer:
    """Comprehensive code quality analysis system"""
    
    def __init__(self):
        from app.core.redis import get_redis_client_sync
        self.redis_client = get_redis_client_sync()  # Returns None if not initialized yet
        self.quality_thresholds = self._initialize_quality_thresholds()
        self.complexity_thresholds = self._initialize_complexity_thresholds()
        self.analysis_cache: Dict[str, QualityReport] = {}
        
    def _initialize_quality_thresholds(self) -> Dict[str, Tuple[float, float]]:
        """Initialize quality thresholds (min, max)"""
        return {
            "maintainability_index": (20.0, 100.0),
            "technical_debt_ratio": (0.0, 0.3),
            "duplication_ratio": (0.0, 0.1),
            "documentation_coverage": (0.3, 1.0),
            "cyclomatic_complexity": (1, 10),
            "cognitive_complexity": (1, 15),
            "average_function_length": (5, 50),
            "average_class_length": (10, 200)
        }
    
    def _initialize_complexity_thresholds(self) -> Dict[int, ComplexityLevel]:
        """Initialize complexity level thresholds"""
        return {
            1: ComplexityLevel.LOW,
            5: ComplexityLevel.MEDIUM,
            10: ComplexityLevel.HIGH,
            20: ComplexityLevel.VERY_HIGH,
            50: ComplexityLevel.EXTREME
        }
    
    async def analyze_code_quality(self, code: str, language: str = "python") -> QualityReport:
        """Analyze code quality comprehensively"""
        try:
            report_id = f"quality_{hash(code).__hash__() % 10000000:08d}"
            
            # Check cache first
            cache_key = f"quality_analysis:{report_id}"
            cached_result = await self.redis_client.get(cache_key)
            if cached_result:
                cached_data = json.loads(cached_result)
                return QualityReport(**cached_data)
            
            # Parse code based on language
            if language.lower() == "python":
                tree = ast.parse(code)
                metrics = await self._analyze_python_code(code, tree)
            else:
                metrics = await self._analyze_generic_code(code)
            
            # Analyze quality issues
            issues_found = await self._analyze_quality_issues(code, metrics, language)
            
            # Calculate overall quality score
            overall_quality_score = self._calculate_quality_score(metrics, issues_found)
            
            # Determine quality and complexity levels
            quality_level = self._determine_quality_level(overall_quality_score)
            complexity_level = self._determine_complexity_level(metrics.cyclomatic_complexity)
            
            # Generate recommendations
            recommendations = self._generate_quality_recommendations(issues_found, metrics)
            
            # Create report
            report = QualityReport(
                report_id=report_id,
                timestamp=datetime.now(),
                overall_quality_score=overall_quality_score,
                quality_level=quality_level,
                complexity_level=complexity_level,
                metrics=metrics,
                issues_found=issues_found,
                recommendations=recommendations,
                metadata={
                    "language": language,
                    "code_length": len(code),
                    "lines_analyzed": len(code.split('\n'))
                }
            )
            
            # Cache result
            await self._cache_quality_report(cache_key, report)
            
            logger.info("Code quality analysis completed", 
                       report_id=report_id,
                       overall_score=overall_quality_score,
                       quality_level=quality_level.value,
                       complexity_level=complexity_level.value)
            
            return report
            
        except Exception as e:
            logger.error("Code quality analysis failed", error=str(e))
            raise
    
    async def _analyze_python_code(self, code: str, tree: ast.AST) -> QualityMetrics:
        """Analyze Python code specifically"""
        lines = code.split('\n')
        
        # Basic metrics
        lines_of_code = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        blank_lines = len([line for line in lines if not line.strip()])
        
        # AST-based analysis
        function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        
        # Calculate cyclomatic complexity
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(tree)
        
        # Calculate cognitive complexity
        cognitive_complexity = self._calculate_cognitive_complexity(tree)
        
        # Calculate maintainability index
        maintainability_index = self._calculate_maintainability_index(
            lines_of_code, cyclomatic_complexity, comment_lines
        )
        
        # Calculate technical debt ratio
        technical_debt_ratio = self._calculate_technical_debt_ratio(
            cyclomatic_complexity, lines_of_code, function_count
        )
        
        # Calculate duplication ratio
        duplication_ratio = self._calculate_duplication_ratio(lines)
        
        # Calculate documentation coverage
        documentation_coverage = self._calculate_documentation_coverage(lines, function_count, class_count)
        
        # Calculate average lengths
        average_function_length = lines_of_code / function_count if function_count > 0 else 0
        average_class_length = lines_of_code / class_count if class_count > 0 else 0
        
        return QualityMetrics(
            lines_of_code=lines_of_code,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            cyclomatic_complexity=cyclomatic_complexity,
            cognitive_complexity=cognitive_complexity,
            maintainability_index=maintainability_index,
            technical_debt_ratio=technical_debt_ratio,
            duplication_ratio=duplication_ratio,
            documentation_coverage=documentation_coverage,
            function_count=function_count,
            class_count=class_count,
            average_function_length=average_function_length,
            average_class_length=average_class_length
        )
    
    async def _analyze_generic_code(self, code: str) -> QualityMetrics:
        """Analyze generic code (non-Python)"""
        lines = code.split('\n')
        
        # Basic metrics
        lines_of_code = len([line for line in lines if line.strip() and not line.strip().startswith('//')])
        comment_lines = len([line for line in lines if line.strip().startswith('//') or '/*' in line])
        blank_lines = len([line for line in lines if not line.strip()])
        
        # Estimate function and class counts based on patterns
        function_count = len(re.findall(r'\b(function|def|public\s+\w+\s+\w+\s*\(|private\s+\w+\s+\w+\s*\()', code))
        class_count = len(re.findall(r'\b(class|interface|struct)\s+\w+', code))
        
        # Estimate complexity based on control structures
        cyclomatic_complexity = self._estimate_cyclomatic_complexity(code)
        cognitive_complexity = self._estimate_cognitive_complexity(code)
        
        # Calculate other metrics
        maintainability_index = self._calculate_maintainability_index(
            lines_of_code, cyclomatic_complexity, comment_lines
        )
        
        technical_debt_ratio = self._calculate_technical_debt_ratio(
            cyclomatic_complexity, lines_of_code, function_count
        )
        
        duplication_ratio = self._calculate_duplication_ratio(lines)
        documentation_coverage = self._calculate_documentation_coverage(lines, function_count, class_count)
        
        average_function_length = lines_of_code / function_count if function_count > 0 else 0
        average_class_length = lines_of_code / class_count if class_count > 0 else 0
        
        return QualityMetrics(
            lines_of_code=lines_of_code,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            cyclomatic_complexity=cyclomatic_complexity,
            cognitive_complexity=cognitive_complexity,
            maintainability_index=maintainability_index,
            technical_debt_ratio=technical_debt_ratio,
            duplication_ratio=duplication_ratio,
            documentation_coverage=documentation_coverage,
            function_count=function_count,
            class_count=class_count,
            average_function_length=average_function_length,
            average_class_length=average_class_length
        )
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for Python AST"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, tree: ast.AST) -> int:
        """Calculate cognitive complexity for Python AST"""
        complexity = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                complexity += 1
                # Nested conditions add extra complexity
                complexity += self._count_nested_conditions(node)
            elif isinstance(node, ast.While):
                complexity += 2  # Loops are more complex than conditions
            elif isinstance(node, ast.For):
                complexity += 1
            elif isinstance(node, ast.AsyncFor):
                complexity += 2
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _count_nested_conditions(self, node: ast.If) -> int:
        """Count nested conditions in an if statement"""
        nested = 0
        for child in ast.walk(node):
            if isinstance(child, ast.If) and child != node:
                nested += 1
        return nested
    
    def _estimate_cyclomatic_complexity(self, code: str) -> int:
        """Estimate cyclomatic complexity for generic code"""
        complexity = 1
        
        # Count control structures
        patterns = [
            r'\bif\s*\(',
            r'\bwhile\s*\(',
            r'\bfor\s*\(',
            r'\bswitch\s*\(',
            r'\bcase\s+',
            r'\bcatch\s*\(',
            r'\?\s*.*\s*:',
            r'\b&&|\|\|'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            complexity += len(matches)
        
        return complexity
    
    def _estimate_cognitive_complexity(self, code: str) -> int:
        """Estimate cognitive complexity for generic code"""
        complexity = 0
        
        # Count different types of control structures with weights
        if_pattern = re.findall(r'\bif\s*\(', code, re.IGNORECASE)
        complexity += len(if_pattern)
        
        loop_patterns = [
            r'\bwhile\s*\(',
            r'\bfor\s*\(',
            r'\bdo\s*\{'
        ]
        
        for pattern in loop_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            complexity += len(matches) * 2  # Loops are more complex
        
        return complexity
    
    def _calculate_maintainability_index(self, lines_of_code: int, complexity: int, comment_lines: int) -> float:
        """Calculate maintainability index"""
        # Simplified maintainability index calculation
        # Real implementation would use more sophisticated metrics
        
        # Volume (Halstead volume approximation)
        volume = lines_of_code * math.log2(max(lines_of_code, 1))
        
        # Complexity factor
        complexity_factor = max(1, complexity / 10)
        
        # Comment factor
        comment_factor = max(0.1, comment_lines / max(lines_of_code, 1))
        
        # Calculate index (higher is better, max 100)
        maintainability_index = max(0, 100 - (volume / 100) - (complexity_factor * 10) + (comment_factor * 20))
        
        return min(100, maintainability_index)
    
    def _calculate_technical_debt_ratio(self, complexity: int, lines_of_code: int, function_count: int) -> float:
        """Calculate technical debt ratio"""
        if lines_of_code == 0:
            return 0.0
        
        # Estimate technical debt based on complexity and code size
        complexity_debt = max(0, (complexity - 10) / 100)
        size_debt = max(0, (lines_of_code - 1000) / 10000)
        function_debt = max(0, (function_count - 20) / 100)
        
        return min(1.0, complexity_debt + size_debt + function_debt)
    
    def _calculate_duplication_ratio(self, lines: List[str]) -> float:
        """Calculate code duplication ratio"""
        if len(lines) < 2:
            return 0.0
        
        # Simple duplication detection based on identical lines
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped:
                line_counts[stripped] = line_counts.get(stripped, 0) + 1
        
        duplicated_lines = sum(count - 1 for count in line_counts.values() if count > 1)
        total_lines = len([line for line in lines if line.strip()])
        
        return duplicated_lines / total_lines if total_lines > 0 else 0.0
    
    def _calculate_documentation_coverage(self, lines: List[str], function_count: int, class_count: int) -> float:
        """Calculate documentation coverage"""
        doc_patterns = [
            r'"""',
            r"'''",
            r'/\*\*',
            r'//\s*@',
            r'/\*',
            r'//.*[Ff]unction|//.*[Mm]ethod|//.*[Cc]lass'
        ]
        
        doc_lines = 0
        for line in lines:
            for pattern in doc_patterns:
                if re.search(pattern, line):
                    doc_lines += 1
                    break
        
        # Estimate documentation coverage
        expected_docs = function_count + class_count
        if expected_docs == 0:
            return 1.0
        
        coverage = min(1.0, doc_lines / expected_docs)
        return coverage
    
    async def _analyze_quality_issues(self, code: str, metrics: QualityMetrics, language: str) -> List[QualityIssue]:
        """Analyze code for quality issues"""
        issues = []
        
        # Check cyclomatic complexity
        if metrics.cyclomatic_complexity > self.quality_thresholds["cyclomatic_complexity"][1]:
            issues.append(QualityIssue(
                issue_id="high_cyclomatic_complexity",
                metric_type=QualityMetric.CYCLOMATIC_COMPLEXITY,
                severity=QualityLevel.POOR if metrics.cyclomatic_complexity > 20 else QualityLevel.FAIR,
                description=f"High cyclomatic complexity: {metrics.cyclomatic_complexity}",
                recommendation="Break down complex functions into smaller, simpler functions"
            ))
        
        # Check cognitive complexity
        if metrics.cognitive_complexity > self.quality_thresholds["cognitive_complexity"][1]:
            issues.append(QualityIssue(
                issue_id="high_cognitive_complexity",
                metric_type=QualityMetric.COGNITIVE_COMPLEXITY,
                severity=QualityLevel.POOR if metrics.cognitive_complexity > 30 else QualityLevel.FAIR,
                description=f"High cognitive complexity: {metrics.cognitive_complexity}",
                recommendation="Simplify control flow and reduce nesting levels"
            ))
        
        # Check maintainability index
        if metrics.maintainability_index < self.quality_thresholds["maintainability_index"][0]:
            issues.append(QualityIssue(
                issue_id="low_maintainability",
                metric_type=QualityMetric.MAINTAINABILITY_INDEX,
                severity=QualityLevel.POOR if metrics.maintainability_index < 10 else QualityLevel.FAIR,
                description=f"Low maintainability index: {metrics.maintainability_index:.2f}",
                recommendation="Improve code structure, add comments, and reduce complexity"
            ))
        
        # Check technical debt
        if metrics.technical_debt_ratio > self.quality_thresholds["technical_debt_ratio"][1]:
            issues.append(QualityIssue(
                issue_id="high_technical_debt",
                metric_type=QualityMetric.TECHNICAL_DEBT,
                severity=QualityLevel.POOR if metrics.technical_debt_ratio > 0.5 else QualityLevel.FAIR,
                description=f"High technical debt ratio: {metrics.technical_debt_ratio:.2f}",
                recommendation="Refactor code to reduce complexity and improve maintainability"
            ))
        
        # Check duplication
        if metrics.duplication_ratio > self.quality_thresholds["duplication_ratio"][1]:
            issues.append(QualityIssue(
                issue_id="high_duplication",
                metric_type=QualityMetric.DUPLICATION_RATIO,
                severity=QualityLevel.FAIR,
                description=f"High code duplication: {metrics.duplication_ratio:.2f}",
                recommendation="Extract common code into reusable functions or classes"
            ))
        
        # Check documentation coverage
        if metrics.documentation_coverage < self.quality_thresholds["documentation_coverage"][0]:
            issues.append(QualityIssue(
                issue_id="low_documentation",
                metric_type=QualityMetric.DOCUMENTATION_COVERAGE,
                severity=QualityLevel.FAIR,
                description=f"Low documentation coverage: {metrics.documentation_coverage:.2f}",
                recommendation="Add documentation for functions, classes, and complex logic"
            ))
        
        # Check function length
        if metrics.average_function_length > self.quality_thresholds["average_function_length"][1]:
            issues.append(QualityIssue(
                issue_id="long_functions",
                metric_type=QualityMetric.MAINTAINABILITY_INDEX,
                severity=QualityLevel.FAIR,
                description=f"Functions are too long on average: {metrics.average_function_length:.1f} lines",
                recommendation="Break down long functions into smaller, focused functions"
            ))
        
        # Check class length
        if metrics.average_class_length > self.quality_thresholds["average_class_length"][1]:
            issues.append(QualityIssue(
                issue_id="long_classes",
                metric_type=QualityMetric.MAINTAINABILITY_INDEX,
                severity=QualityLevel.FAIR,
                description=f"Classes are too long on average: {metrics.average_class_length:.1f} lines",
                recommendation="Split large classes into smaller, more focused classes"
            ))
        
        return issues
    
    def _calculate_quality_score(self, metrics: QualityMetrics, issues: List[QualityIssue]) -> float:
        """Calculate overall quality score"""
        base_score = 100.0
        
        # Deduct points based on metrics
        if metrics.cyclomatic_complexity > 10:
            base_score -= min(30, (metrics.cyclomatic_complexity - 10) * 2)
        
        if metrics.cognitive_complexity > 15:
            base_score -= min(25, (metrics.cognitive_complexity - 15) * 1.5)
        
        if metrics.maintainability_index < 50:
            base_score -= (50 - metrics.maintainability_index) * 0.5
        
        if metrics.technical_debt_ratio > 0.3:
            base_score -= min(20, metrics.technical_debt_ratio * 50)
        
        if metrics.duplication_ratio > 0.1:
            base_score -= min(15, metrics.duplication_ratio * 100)
        
        if metrics.documentation_coverage < 0.3:
            base_score -= (0.3 - metrics.documentation_coverage) * 30
        
        # Deduct points for issues
        for issue in issues:
            if issue.severity == QualityLevel.CRITICAL:
                base_score -= 20
            elif issue.severity == QualityLevel.POOR:
                base_score -= 10
            elif issue.severity == QualityLevel.FAIR:
                base_score -= 5
        
        return max(0.0, base_score)
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """Determine quality level based on score"""
        if score >= 90:
            return QualityLevel.EXCELLENT
        elif score >= 75:
            return QualityLevel.GOOD
        elif score >= 60:
            return QualityLevel.FAIR
        elif score >= 40:
            return QualityLevel.POOR
        else:
            return QualityLevel.CRITICAL
    
    def _determine_complexity_level(self, complexity: int) -> ComplexityLevel:
        """Determine complexity level based on cyclomatic complexity"""
        if complexity <= 5:
            return ComplexityLevel.LOW
        elif complexity <= 10:
            return ComplexityLevel.MEDIUM
        elif complexity <= 20:
            return ComplexityLevel.HIGH
        elif complexity <= 50:
            return ComplexityLevel.VERY_HIGH
        else:
            return ComplexityLevel.EXTREME
    
    def _generate_quality_recommendations(self, issues: List[QualityIssue], metrics: QualityMetrics) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        # Issue-specific recommendations
        for issue in issues:
            if issue.recommendation and issue.recommendation not in recommendations:
                recommendations.append(issue.recommendation)
        
        # General recommendations based on metrics
        if metrics.cyclomatic_complexity > 10:
            recommendations.append("Consider using design patterns to reduce complexity")
        
        if metrics.function_count > 50:
            recommendations.append("Consider splitting the code into multiple modules")
        
        if metrics.documentation_coverage < 0.5:
            recommendations.append("Add comprehensive documentation and comments")
        
        if metrics.duplication_ratio > 0.05:
            recommendations.append("Identify and extract common functionality")
        
        # Add general best practices
        recommendations.extend([
            "Follow consistent coding standards and naming conventions",
            "Implement automated testing to ensure code quality",
            "Use static analysis tools in your development workflow",
            "Regularly refactor code to maintain high quality",
            "Consider code reviews to catch quality issues early"
        ])
        
        return list(set(recommendations))  # Remove duplicates
    
    async def _cache_quality_report(self, cache_key: str, report: QualityReport):
        """Cache quality report in Redis"""
        try:
            cache_data = {
                "report_id": report.report_id,
                "timestamp": report.timestamp.isoformat(),
                "overall_quality_score": report.overall_quality_score,
                "quality_level": report.quality_level.value,
                "complexity_level": report.complexity_level.value,
                "metrics": {
                    "lines_of_code": report.metrics.lines_of_code,
                    "comment_lines": report.metrics.comment_lines,
                    "blank_lines": report.metrics.blank_lines,
                    "cyclomatic_complexity": report.metrics.cyclomatic_complexity,
                    "cognitive_complexity": report.metrics.cognitive_complexity,
                    "maintainability_index": report.metrics.maintainability_index,
                    "technical_debt_ratio": report.metrics.technical_debt_ratio,
                    "duplication_ratio": report.metrics.duplication_ratio,
                    "documentation_coverage": report.metrics.documentation_coverage,
                    "function_count": report.metrics.function_count,
                    "class_count": report.metrics.class_count,
                    "average_function_length": report.metrics.average_function_length,
                    "average_class_length": report.metrics.average_class_length
                },
                "issues_found": [
                    {
                        "issue_id": issue.issue_id,
                        "metric_type": issue.metric_type.value,
                        "severity": issue.severity.value,
                        "description": issue.description,
                        "location": issue.location,
                        "line_number": issue.line_number,
                        "recommendation": issue.recommendation,
                        "impact_score": issue.impact_score
                    }
                    for issue in report.issues_found
                ],
                "recommendations": report.recommendations,
                "metadata": report.metadata
            }
            
            await self.redis_client.set(
                cache_key,
                json.dumps(cache_data, default=str),
                ex=3600  # Cache for 1 hour
            )
            
        except Exception as e:
            logger.error("Failed to cache quality report", error=str(e))
    
    async def get_quality_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of quality analysis metrics"""
        try:
            # Get cached quality reports
            cache_keys = await self.redis_client.keys("quality_analysis:*")
            
            total_analyses = len(cache_keys)
            if total_analyses == 0:
                return {"message": "No quality analyses available"}
            
            quality_levels = {}
            complexity_levels = {}
            avg_scores = []
            
            for key in cache_keys:
                cached_data = await self.redis_client.get(key)
                if cached_data:
                    data = json.loads(cached_data)
                    
                    # Count quality levels
                    quality_level = data.get("quality_level", "unknown")
                    quality_levels[quality_level] = quality_levels.get(quality_level, 0) + 1
                    
                    # Count complexity levels
                    complexity_level = data.get("complexity_level", "unknown")
                    complexity_levels[complexity_level] = complexity_levels.get(complexity_level, 0) + 1
                    
                    # Collect scores
                    score = data.get("overall_quality_score", 0)
                    avg_scores.append(score)
            
            return {
                "total_analyses": total_analyses,
                "average_quality_score": sum(avg_scores) / len(avg_scores) if avg_scores else 0,
                "quality_level_distribution": quality_levels,
                "complexity_level_distribution": complexity_levels,
                "summary": {
                    "excellent_code": quality_levels.get("excellent", 0),
                    "good_code": quality_levels.get("good", 0),
                    "fair_code": quality_levels.get("fair", 0),
                    "poor_code": quality_levels.get("poor", 0),
                    "critical_code": quality_levels.get("critical", 0)
                }
            }
            
        except Exception as e:
            logger.error("Failed to get quality metrics summary", error=str(e))
            return {}

# Global instance
code_quality_analyzer = CodeQualityAnalyzer()
