"""
Architecture Compliance System

This module implements standard architecture principles compliance
including SOLID principles, design patterns, and architectural best practices.
"""

import asyncio
import inspect
import ast
import importlib
from typing import Dict, List, Optional, Any, Type, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import structlog
from abc import ABC, abstractmethod
import weakref
from collections import defaultdict
from functools import wraps
import sys
import os

logger = structlog.get_logger(__name__)

class ComplianceLevel(Enum):
    """Architecture compliance levels"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    ENTERPRISE = "enterprise"

class PrincipleType(Enum):
    """SOLID principles types"""
    SINGLE_RESPONSIBILITY = "single_responsibility"
    OPEN_CLOSED = "open_closed"
    LISKOV_SUBSTITUTION = "liskov_substitution"
    INTERFACE_SEGREGATION = "interface_segregation"
    DEPENDENCY_INVERSION = "dependency_inversion"

class DesignPatternType(Enum):
    """Design pattern types"""
    REPOSITORY = "repository"
    STRATEGY = "strategy"
    COMMAND = "command"
    OBSERVER = "observer"
    FACTORY = "factory"
    SINGLETON = "singleton"
    ADAPTER = "adapter"
    DECORATOR = "decorator"
    FACADE = "facade"
    PROXY = "proxy"

@dataclass
class ComplianceViolation:
    """Architecture compliance violation"""
    principle: PrincipleType
    violation_type: str
    severity: str  # low, medium, high, critical
    description: str
    file_path: str
    line_number: int
    class_name: Optional[str] = None
    function_name: Optional[str] = None
    suggestion: Optional[str] = None

@dataclass
class ComplianceReport:
    """Architecture compliance report"""
    overall_score: float
    principle_scores: Dict[PrincipleType, float]
    violations: List[ComplianceViolation]
    recommendations: List[str]
    design_patterns_used: List[DesignPatternType]
    compliance_level: ComplianceLevel

class ArchitectureAnalyzer:
    """Architecture analysis engine"""
    
    def __init__(self):
        self.analyzed_files: Dict[str, ast.AST] = {}
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)
        self.interface_registry: Dict[str, List[str]] = defaultdict(list)
        
    def analyze_file(self, file_path: str) -> ast.AST:
        """Analyze Python file and return AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=file_path)
            self.analyzed_files[file_path] = tree
            return tree
        except Exception as e:
            logger.error("Failed to analyze file", file=file_path, error=str(e))
            return None
    
    def analyze_directory(self, directory: str) -> Dict[str, ast.AST]:
        """Analyze all Python files in directory"""
        trees = {}
        
        for root, dirs, files in os.walk(directory):
            # Skip heavy directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.venv', '.tox', '.mypy_cache', '.pytest_cache'}]
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    tree = self.analyze_file(file_path)
                    if tree:
                        trees[file_path] = tree
        
        return trees
    
    def extract_classes(self, tree: ast.AST) -> List[ast.ClassDef]:
        """Extract class definitions from AST"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node)
        return classes
    
    def extract_functions(self, tree: ast.AST) -> List[ast.FunctionDef]:
        """Extract function definitions from AST"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
        return functions
    
    def extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements from AST"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports

class SOLIDPrinciplesChecker:
    """SOLID principles compliance checker"""
    
    def __init__(self, analyzer: ArchitectureAnalyzer):
        self.analyzer = analyzer
        self.violations: List[ComplianceViolation] = []
    
    def check_single_responsibility(self, tree: ast.AST, file_path: str) -> List[ComplianceViolation]:
        """Check Single Responsibility Principle compliance"""
        violations = []
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            # Check if class has too many methods (indicating multiple responsibilities)
            methods = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
            if len(methods) > 10:
                violations.append(ComplianceViolation(
                    principle=PrincipleType.SINGLE_RESPONSIBILITY,
                    violation_type="too_many_methods",
                    severity="medium",
                    description=f"Class {class_def.name} has {len(methods)} methods, suggesting multiple responsibilities",
                    file_path=file_path,
                    line_number=class_def.lineno,
                    class_name=class_def.name,
                    suggestion="Consider splitting into smaller, focused classes"
                ))
            
            # Check for mixed concerns in method names
            method_names = [method.name for method in methods]
            concerns = set()
            
            for name in method_names:
                if any(keyword in name.lower() for keyword in ['auth', 'login', 'password']):
                    concerns.add('authentication')
                if any(keyword in name.lower() for keyword in ['user', 'profile', 'account']):
                    concerns.add('user_management')
                if any(keyword in name.lower() for keyword in ['email', 'notification', 'send']):
                    concerns.add('notification')
                if any(keyword in name.lower() for keyword in ['database', 'save', 'load']):
                    concerns.add('data_persistence')
            
            if len(concerns) > 2:
                violations.append(ComplianceViolation(
                    principle=PrincipleType.SINGLE_RESPONSIBILITY,
                    violation_type="mixed_concerns",
                    severity="high",
                    description=f"Class {class_def.name} handles multiple concerns: {', '.join(concerns)}",
                    file_path=file_path,
                    line_number=class_def.lineno,
                    class_name=class_def.name,
                    suggestion="Separate concerns into different classes"
                ))
        
        return violations
    
    def check_open_closed(self, tree: ast.AST, file_path: str) -> List[ComplianceViolation]:
        """Check Open/Closed Principle compliance"""
        violations = []
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            # Check for hard-coded type checks (violates open/closed)
            for node in ast.walk(class_def):
                if isinstance(node, ast.If):
                    # Check for isinstance checks
                    if isinstance(node.test, ast.Call):
                        if isinstance(node.test.func, ast.Name) and node.test.func.id == 'isinstance':
                            violations.append(ComplianceViolation(
                                principle=PrincipleType.OPEN_CLOSED,
                                violation_type="hard_coded_type_check",
                                severity="medium",
                                description="Hard-coded type checking violates open/closed principle",
                                file_path=file_path,
                                line_number=node.lineno,
                                class_name=class_def.name,
                                suggestion="Use polymorphism or strategy pattern instead"
                            ))
                
                # Check for switch-like if-elif chains
                elif isinstance(node, ast.If):
                    if_count = 0
                    current = node
                    while isinstance(current, ast.If):
                        if_count += 1
                        current = current.orelse[0] if current.orelse else None
                    
                    if if_count > 3:
                        violations.append(ComplianceViolation(
                            principle=PrincipleType.OPEN_CLOSED,
                            violation_type="long_if_chain",
                            severity="low",
                            description=f"Long if-elif chain ({if_count} conditions) may violate open/closed principle",
                            file_path=file_path,
                            line_number=node.lineno,
                            class_name=class_def.name,
                            suggestion="Consider using strategy pattern or polymorphism"
                        ))
        
        return violations
    
    def check_liskov_substitution(self, tree: ast.AST, file_path: str) -> List[ComplianceViolation]:
        """Check Liskov Substitution Principle compliance"""
        violations = []
        classes = self.analyzer.extract_classes(tree)
        
        # Find base classes and their subclasses
        inheritance_map = {}
        for class_def in classes:
            for base in class_def.bases:
                if isinstance(base, ast.Name):
                    base_name = base.id
                    if base_name not in inheritance_map:
                        inheritance_map[base_name] = []
                    inheritance_map[base_name].append(class_def.name)
        
        # Check for method signature changes in subclasses
        for base_class, subclasses in inheritance_map.items():
            base_methods = self._get_class_methods(tree, base_class)
            
            for subclass_name in subclasses:
                subclass_methods = self._get_class_methods(tree, subclass_name)
                
                for base_method in base_methods:
                    if base_method in subclass_methods:
                        # Check if method signature was changed
                        base_args = self._get_method_args(tree, base_class, base_method)
                        sub_args = self._get_method_args(tree, subclass_name, base_method)
                        
                        if base_args != sub_args:
                            violations.append(ComplianceViolation(
                                principle=PrincipleType.LISKOV_SUBSTITUTION,
                                violation_type="method_signature_change",
                                severity="high",
                                description=f"Method {base_method} signature changed in subclass {subclass_name}",
                                file_path=file_path,
                                line_number=0,  # Would need more complex tracking
                                class_name=subclass_name,
                                function_name=base_method,
                                suggestion="Maintain the same method signature in subclasses"
                            ))
        
        return violations
    
    def check_interface_segregation(self, tree: ast.AST, file_path: str) -> List[ComplianceViolation]:
        """Check Interface Segregation Principle compliance"""
        violations = []
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            methods = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
            
            # Check for large interfaces (too many methods)
            if len(methods) > 8:
                violations.append(ComplianceViolation(
                    principle=PrincipleType.INTERFACE_SEGREGATION,
                    violation_type="large_interface",
                    severity="medium",
                    description=f"Class {class_def.name} has {len(methods)} methods, creating a large interface",
                    file_path=file_path,
                    line_number=class_def.lineno,
                    class_name=class_def.name,
                    suggestion="Split into smaller, more focused interfaces"
                ))
            
            # Check for unused methods (clients forced to depend on unused methods)
            # This would require more complex analysis of method usage
            for method in methods:
                if method.name.startswith('_') and not method.name.startswith('__'):
                    # Private methods are okay
                    continue
                
                # Check if method is used within the class
                method_used = False
                for other_method in methods:
                    if method != other_method:
                        for node in ast.walk(other_method):
                            if isinstance(node, ast.Call):
                                if isinstance(node.func, ast.Name) and node.func.id == method.name:
                                    method_used = True
                                    break
                
                if not method_used and len(methods) > 5:
                    violations.append(ComplianceViolation(
                        principle=PrincipleType.INTERFACE_SEGREGATION,
                        violation_type="potentially_unused_method",
                        severity="low",
                        description=f"Method {method.name} may not be used, forcing clients to depend on unused methods",
                        file_path=file_path,
                        line_number=method.lineno,
                        class_name=class_def.name,
                        function_name=method.name,
                        suggestion="Consider removing unused methods or making them optional"
                    ))
        
        return violations
    
    def check_dependency_inversion(self, tree: ast.AST, file_path: str) -> List[ComplianceViolation]:
        """Check Dependency Inversion Principle compliance"""
        violations = []
        
        # Check for direct instantiations of concrete classes
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    # Check for direct instantiation of concrete classes
                    class_name = node.func.id
                    if class_name[0].isupper():  # Likely a class name
                        violations.append(ComplianceViolation(
                            principle=PrincipleType.DEPENDENCY_INVERSION,
                            violation_type="direct_instantiation",
                            severity="medium",
                            description=f"Direct instantiation of concrete class {class_name}",
                            file_path=file_path,
                            line_number=node.lineno,
                            suggestion="Use dependency injection or factory pattern"
                        ))
        
        # Check for imports of concrete implementations instead of abstractions
        imports = self.analyzer.extract_imports(tree)
        for import_name in imports:
            if any(concrete in import_name.lower() for concrete in ['mysql', 'postgres', 'sqlite']):
                violations.append(ComplianceViolation(
                    principle=PrincipleType.DEPENDENCY_INVERSION,
                    violation_type="concrete_import",
                    severity="medium",
                    description=f"Importing concrete implementation: {import_name}",
                    file_path=file_path,
                    line_number=0,
                    suggestion="Import abstractions instead of concrete implementations"
                ))
        
        return violations
    
    def _get_class_methods(self, tree: ast.AST, class_name: str) -> List[str]:
        """Get methods of a specific class"""
        methods = []
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            if class_def.name == class_name:
                for node in class_def.body:
                    if isinstance(node, ast.FunctionDef):
                        methods.append(node.name)
                break
        
        return methods
    
    def _get_method_args(self, tree: ast.AST, class_name: str, method_name: str) -> List[str]:
        """Get method arguments"""
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            if class_def.name == class_name:
                for node in class_def.body:
                    if isinstance(node, ast.FunctionDef) and node.name == method_name:
                        return [arg.arg for arg in node.args.args]
        
        return []

class DesignPatternDetector:
    """Design pattern detection system"""
    
    def __init__(self, analyzer: ArchitectureAnalyzer):
        self.analyzer = analyzer
        self.detected_patterns: Dict[DesignPatternType, List[str]] = defaultdict(list)
    
    def detect_patterns(self, tree: ast.AST, file_path: str) -> Dict[DesignPatternType, List[str]]:
        """Detect design patterns in the code"""
        patterns = defaultdict(list)
        
        # Detect Repository Pattern
        if self._detect_repository_pattern(tree):
            patterns[DesignPatternType.REPOSITORY].append(file_path)
        
        # Detect Strategy Pattern
        if self._detect_strategy_pattern(tree):
            patterns[DesignPatternType.STRATEGY].append(file_path)
        
        # Detect Command Pattern
        if self._detect_command_pattern(tree):
            patterns[DesignPatternType.COMMAND].append(file_path)
        
        # Detect Observer Pattern
        if self._detect_observer_pattern(tree):
            patterns[DesignPatternType.OBSERVER].append(file_path)
        
        # Detect Factory Pattern
        if self._detect_factory_pattern(tree):
            patterns[DesignPatternType.FACTORY].append(file_path)
        
        # Detect Singleton Pattern
        if self._detect_singleton_pattern(tree):
            patterns[DesignPatternType.SINGLETON].append(file_path)
        
        return patterns
    
    def _detect_repository_pattern(self, tree: ast.AST) -> bool:
        """Detect Repository pattern"""
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            class_name = class_def.name.lower()
            if 'repository' in class_name:
                # Check for typical repository methods
                methods = [node.name for node in class_def.body if isinstance(node, ast.FunctionDef)]
                repo_methods = ['get', 'create', 'update', 'delete', 'find', 'save']
                
                if any(method in methods for method in repo_methods):
                    return True
        
        return False
    
    def _detect_strategy_pattern(self, tree: ast.AST) -> bool:
        """Detect Strategy pattern"""
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            # Look for strategy-like methods
            methods = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
            for method in methods:
                if method.name in ['execute', 'process', 'handle', 'algorithm']:
                    return True
        
        return False
    
    def _detect_command_pattern(self, tree: ast.AST) -> bool:
        """Detect Command pattern"""
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            class_name = class_def.name.lower()
            if 'command' in class_name:
                methods = [node.name for node in class_def.body if isinstance(node, ast.FunctionDef)]
                if 'execute' in methods and 'undo' in methods:
                    return True
        
        return False
    
    def _detect_observer_pattern(self, tree: ast.AST) -> bool:
        """Detect Observer pattern"""
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            methods = [node.name for node in class_def.body if isinstance(node, ast.FunctionDef)]
            observer_methods = ['attach', 'detach', 'notify', 'update', 'subscribe', 'unsubscribe']
            
            if any(method in methods for method in observer_methods):
                return True
        
        return False
    
    def _detect_factory_pattern(self, tree: ast.AST) -> bool:
        """Detect Factory pattern"""
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            class_name = class_def.name.lower()
            if 'factory' in class_name:
                methods = [node.name for node in class_def.body if isinstance(node, ast.FunctionDef)]
                factory_methods = ['create', 'make', 'build', 'get_instance']
                
                if any(method in methods for method in factory_methods):
                    return True
        
        return False
    
    def _detect_singleton_pattern(self, tree: ast.AST) -> bool:
        """Detect Singleton pattern"""
        classes = self.analyzer.extract_classes(tree)
        
        for class_def in classes:
            methods = [node for node in class_def.body if isinstance(node, ast.FunctionDef)]
            
            # Look for __new__ method or get_instance method
            for method in methods:
                if method.name in ['__new__', 'get_instance']:
                    return True
        
        return False

class ArchitectureComplianceEngine:
    """Main architecture compliance engine"""
    
    def __init__(self, compliance_level: ComplianceLevel = ComplianceLevel.ADVANCED):
        self.compliance_level = compliance_level
        self.analyzer = ArchitectureAnalyzer()
        self.solid_checker = SOLIDPrinciplesChecker(self.analyzer)
        self.pattern_detector = DesignPatternDetector(self.analyzer)
        
    async def analyze_codebase(self, directory: str) -> ComplianceReport:
        """Analyze entire codebase for architecture compliance"""
        logger.info("Starting architecture compliance analysis", directory=directory)
        
        # Analyze all Python files
        trees = self.analyzer.analyze_directory(directory)
        
        all_violations = []
        all_patterns = defaultdict(list)
        
        for file_path, tree in trees.items():
            if tree:
                # Check SOLID principles
                violations = []
                violations.extend(self.solid_checker.check_single_responsibility(tree, file_path))
                violations.extend(self.solid_checker.check_open_closed(tree, file_path))
                violations.extend(self.solid_checker.check_liskov_substitution(tree, file_path))
                violations.extend(self.solid_checker.check_interface_segregation(tree, file_path))
                violations.extend(self.solid_checker.check_dependency_inversion(tree, file_path))
                
                all_violations.extend(violations)
                
                # Detect design patterns
                patterns = self.pattern_detector.detect_patterns(tree, file_path)
                for pattern_type, files in patterns.items():
                    all_patterns[pattern_type].extend(files)
        
        # Calculate scores
        principle_scores = self._calculate_principle_scores(all_violations)
        overall_score = sum(principle_scores.values()) / len(principle_scores)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(all_violations, all_patterns)
        
        # Create report
        report = ComplianceReport(
            overall_score=overall_score,
            principle_scores=principle_scores,
            violations=all_violations,
            recommendations=recommendations,
            design_patterns_used=list(all_patterns.keys()),
            compliance_level=self.compliance_level
        )
        
        logger.info("Architecture compliance analysis completed", 
                   score=overall_score, 
                   violations=len(all_violations))
        
        return report
    
    def _calculate_principle_scores(self, violations: List[ComplianceViolation]) -> Dict[PrincipleType, float]:
        """Calculate compliance scores for each principle"""
        scores = {}
        
        for principle in PrincipleType:
            principle_violations = [v for v in violations if v.principle == principle]
            
            # Weight violations by severity
            total_weight = 0
            for violation in principle_violations:
                if violation.severity == 'critical':
                    total_weight += 4
                elif violation.severity == 'high':
                    total_weight += 3
                elif violation.severity == 'medium':
                    total_weight += 2
                else:  # low
                    total_weight += 1
            
            # Calculate score (100 - weighted violations)
            score = max(0, 100 - total_weight)
            scores[principle] = score
        
        return scores
    
    def _generate_recommendations(self, violations: List[ComplianceViolation], 
                                patterns: Dict[DesignPatternType, List[str]]) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Group violations by principle
        violations_by_principle = defaultdict(list)
        for violation in violations:
            violations_by_principle[violation.principle].append(violation)
        
        # Generate recommendations for each principle
        if violations_by_principle.get(PrincipleType.SINGLE_RESPONSIBILITY):
            recommendations.append("Implement Single Responsibility Principle by splitting large classes into smaller, focused classes")
        
        if violations_by_principle.get(PrincipleType.OPEN_CLOSED):
            recommendations.append("Use polymorphism and strategy patterns to make code open for extension but closed for modification")
        
        if violations_by_principle.get(PrincipleType.DEPENDENCY_INVERSION):
            recommendations.append("Implement dependency injection to depend on abstractions rather than concrete implementations")
        
        if violations_by_principle.get(PrincipleType.INTERFACE_SEGREGATION):
            recommendations.append("Create smaller, more focused interfaces to avoid forcing clients to depend on unused methods")
        
        # Design pattern recommendations
        if DesignPatternType.REPOSITORY not in patterns:
            recommendations.append("Consider implementing Repository pattern for data access abstraction")
        
        if DesignPatternType.STRATEGY not in patterns:
            recommendations.append("Consider implementing Strategy pattern for interchangeable algorithms")
        
        return recommendations
    
    async def get_compliance_status(self, directory: str) -> Dict[str, Any]:
        """Get current compliance status"""
        report = await self.analyze_codebase(directory)
        
        return {
            "overall_score": report.overall_score,
            "compliance_level": report.compliance_level.value,
            "principle_scores": {p.value: s for p, s in report.principle_scores.items()},
            "violations_count": len(report.violations),
            "critical_violations": len([v for v in report.violations if v.severity == 'critical']),
            "design_patterns_used": [p.value for p in report.design_patterns_used],
            "recommendations_count": len(report.recommendations),
            "status": "compliant" if report.overall_score >= 80 else "needs_improvement"
        }

# Global compliance engine instance
compliance_engine = ArchitectureComplianceEngine()

# Compliance decorators
def ensure_compliance(principle: PrincipleType):
    """Decorator to ensure method compliance with specific principle"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # This would perform runtime compliance checks
            # For now, just log the compliance check
            logger.debug("Checking compliance", principle=principle.value, function=func.__name__)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def design_pattern(pattern_type: DesignPatternType):
    """Decorator to mark design pattern usage"""
    def decorator(cls):
        # Mark class as implementing specific pattern
        cls._design_pattern = pattern_type
        return cls
    return decorator
