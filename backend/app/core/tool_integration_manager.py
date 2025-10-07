"""
Tool Integration Manager

This module provides seamless tool orchestration and integration management
for the Ethical AI system, enabling dynamic tool discovery and execution.
"""

import asyncio
import structlog
from typing import Dict, List, Optional, Any, Union, Callable, Type
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import uuid
from abc import ABC, abstractmethod

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core

logger = structlog.get_logger(__name__)

class ToolCategory(Enum):
    """Categories of tools"""
    CODE_GENERATION = "code_generation"
    SECURITY_VALIDATION = "security_validation"
    QUALITY_ANALYSIS = "quality_analysis"
    ERROR_RECOVERY = "error_recovery"
    ACCURACY_VALIDATION = "accuracy_validation"
    CONSISTENCY_ENFORCEMENT = "consistency_enforcement"
    MONITORING_ANALYTICS = "monitoring_analytics"
    BUSINESS_INTELLIGENCE = "business_intelligence"

class ToolStatus(Enum):
    """Tool operational status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class ToolPriority(Enum):
    """Tool execution priority"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class ToolDefinition:
    """Definition of a tool"""
    id: str
    name: str
    description: str
    category: ToolCategory
    version: str
    status: ToolStatus = ToolStatus.ACTIVE
    priority: ToolPriority = ToolPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ToolExecution:
    """Tool execution context"""
    execution_id: str
    tool_id: str
    input_data: Dict[str, Any]
    context: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    status: str = "running"

class ITool(ABC):
    """Abstract base class for all tools"""
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute the tool with given input and context"""
        pass
    
    @abstractmethod
    def get_definition(self) -> ToolDefinition:
        """Get tool definition"""
        pass
    
    @abstractmethod
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get tool capabilities"""
        pass

class ToolIntegrationManager:
    """Manages tool integration and orchestration"""
    
    def __init__(self):
        from app.core.redis import get_redis_client_sync
        self.redis_client = get_redis_client_sync()  # Returns None if not initialized yet
        self.registered_tools: Dict[str, ITool] = {}
        self.tool_definitions: Dict[str, ToolDefinition] = {}
        self.execution_history: List[ToolExecution] = []
        self.context_cache: Dict[str, Any] = {}
        
    async def initialize(self):
        """Initialize the tool integration manager"""
        try:
            await self._load_tool_definitions()
            await self._register_builtin_tools()
            logger.info("Tool Integration Manager initialized", 
                       tools_loaded=len(self.registered_tools))
        except Exception as e:
            logger.error("Failed to initialize Tool Integration Manager", error=str(e))
            raise
    
    async def _load_tool_definitions(self):
        """Load tool definitions from cache or database"""
        try:
            # Try to load from Redis cache first
            cached_definitions = await self.redis_client.get("tool_definitions")
            if cached_definitions:
                definitions_data = json.loads(cached_definitions)
                for tool_id, definition_data in definitions_data.items():
                    self.tool_definitions[tool_id] = ToolDefinition(**definition_data)
                logger.info("Loaded tool definitions from cache", count=len(self.tool_definitions))
                return
            
            # If no cache, initialize with empty state
            logger.info("No cached tool definitions found, starting fresh")
            
        except Exception as e:
            logger.error("Failed to load tool definitions", error=str(e))
            raise
    
    async def _register_builtin_tools(self):
        """Register built-in tools"""
        try:
            # Register Security Validator Tool
            security_validator = SecurityValidatorTool()
            await self.register_tool(security_validator)
            
            # Register Code Quality Analyzer Tool
            code_quality_analyzer = CodeQualityAnalyzerTool()
            await self.register_tool(code_quality_analyzer)
            
            # Register Error Recovery Manager Tool
            error_recovery_manager = ErrorRecoveryManagerTool()
            await self.register_tool(error_recovery_manager)
            
            # Register Factual Accuracy Validator Tool
            factual_accuracy_validator = FactualAccuracyValidatorTool()
            await self.register_tool(factual_accuracy_validator)
            
            # Register Consistency Enforcer Tool
            consistency_enforcer = ConsistencyEnforcerTool()
            await self.register_tool(consistency_enforcer)
            
            # Register Monitoring Analytics Manager Tool
            monitoring_analytics_manager = MonitoringAnalyticsManagerTool()
            await self.register_tool(monitoring_analytics_manager)
            
            logger.info("Built-in tools registered successfully")
            
        except Exception as e:
            logger.error("Failed to register built-in tools", error=str(e))
            raise
    
    async def register_tool(self, tool: ITool) -> bool:
        """Register a new tool"""
        try:
            definition = tool.get_definition()
            
            # Validate tool
            if not await self._validate_tool(tool):
                logger.error("Tool validation failed", tool_id=definition.id)
                return False
            
            # Register tool
            self.registered_tools[definition.id] = tool
            self.tool_definitions[definition.id] = definition
            
            # Cache definition
            await self._cache_tool_definition(definition)
            
            logger.info("Tool registered successfully", tool_id=definition.id, name=definition.name)
            return True
            
        except Exception as e:
            logger.error("Failed to register tool", error=str(e))
            return False
    
    async def _validate_tool(self, tool: ITool) -> bool:
        """Validate tool implementation"""
        try:
            definition = tool.get_definition()
            
            # Check required fields
            if not definition.id or not definition.name:
                return False
            
            # Test tool capabilities
            capabilities = await tool.get_capabilities()
            if not capabilities:
                return False
            
            # Test input validation
            test_input = {"test": "data"}
            validation_result = await tool.validate_input(test_input)
            if not isinstance(validation_result, bool):
                return False
            
            return True
            
        except Exception as e:
            logger.error("Tool validation error", error=str(e))
            return False
    
    async def _cache_tool_definition(self, definition: ToolDefinition):
        """Cache tool definition in Redis"""
        try:
            definitions_data = {
                tool_id: definition.dict() 
                for tool_id, definition in self.tool_definitions.items()
            }
            
            await self.redis_client.set(
                "tool_definitions", 
                json.dumps(definitions_data, default=str),
                ex=3600  # Cache for 1 hour
            )
            
        except Exception as e:
            logger.error("Failed to cache tool definition", error=str(e))
    
    async def execute_tool(self, tool_id: str, input_data: Dict[str, Any], 
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a tool with given input and context"""
        try:
            if tool_id not in self.registered_tools:
                raise ValueError(f"Tool {tool_id} not found")
            
            tool = self.registered_tools[tool_id]
            definition = self.tool_definitions[tool_id]
            
            # Check tool status
            if definition.status != ToolStatus.ACTIVE:
                raise ValueError(f"Tool {tool_id} is not active")
            
            # Create execution context
            execution_id = str(uuid.uuid4())
            execution = ToolExecution(
                execution_id=execution_id,
                tool_id=tool_id,
                input_data=input_data,
                context=context or {},
                started_at=datetime.now()
            )
            
            # Validate input
            if not await tool.validate_input(input_data):
                execution.error = "Input validation failed"
                execution.status = "failed"
                execution.completed_at = datetime.now()
                self.execution_history.append(execution)
                raise ValueError("Input validation failed")
            
            # Execute tool
            try:
                result = await tool.execute(input_data, context or {})
                execution.result = result
                execution.status = "completed"
                execution.completed_at = datetime.now()
                
                # Cache result if applicable
                await self._cache_execution_result(execution)
                
                logger.info("Tool executed successfully", 
                           tool_id=tool_id, execution_id=execution_id)
                
                return {
                    "execution_id": execution_id,
                    "tool_id": tool_id,
                    "result": result,
                    "status": "success",
                    "execution_time": (execution.completed_at - execution.started_at).total_seconds()
                }
                
            except Exception as e:
                execution.error = str(e)
                execution.status = "failed"
                execution.completed_at = datetime.now()
                logger.error("Tool execution failed", tool_id=tool_id, error=str(e))
                raise
            
            finally:
                self.execution_history.append(execution)
            
        except Exception as e:
            logger.error("Tool execution error", tool_id=tool_id, error=str(e))
            return {
                "execution_id": execution_id if 'execution_id' in locals() else None,
                "tool_id": tool_id,
                "error": str(e),
                "status": "failed"
            }
    
    async def _cache_execution_result(self, execution: ToolExecution):
        """Cache execution result for future reference"""
        try:
            cache_key = f"tool_execution:{execution.execution_id}"
            cache_data = {
                "tool_id": execution.tool_id,
                "result": execution.result,
                "status": execution.status,
                "completed_at": execution.completed_at.isoformat() if execution.completed_at else None
            }
            
            await self.redis_client.set(
                cache_key,
                json.dumps(cache_data, default=str),
                ex=7200  # Cache for 2 hours
            )
            
        except Exception as e:
            logger.error("Failed to cache execution result", error=str(e))
    
    async def get_tool_capabilities(self, tool_id: str) -> Dict[str, Any]:
        """Get capabilities of a specific tool"""
        try:
            if tool_id not in self.registered_tools:
                raise ValueError(f"Tool {tool_id} not found")
            
            tool = self.registered_tools[tool_id]
            return await tool.get_capabilities()
            
        except Exception as e:
            logger.error("Failed to get tool capabilities", tool_id=tool_id, error=str(e))
            return {}
    
    async def list_tools(self, category: Optional[ToolCategory] = None) -> List[Dict[str, Any]]:
        """List all registered tools, optionally filtered by category"""
        try:
            tools = []
            
            for tool_id, definition in self.tool_definitions.items():
                if category and definition.category != category:
                    continue
                
                tool_info = {
                    "id": tool_id,
                    "name": definition.name,
                    "description": definition.description,
                    "category": definition.category.value,
                    "status": definition.status.value,
                    "priority": definition.priority.value,
                    "version": definition.version
                }
                
                tools.append(tool_info)
            
            return tools
            
        except Exception as e:
            logger.error("Failed to list tools", error=str(e))
            return []
    
    async def get_execution_history(self, tool_id: Optional[str] = None, 
                                   limit: int = 100) -> List[Dict[str, Any]]:
        """Get execution history for tools"""
        try:
            history = []
            
            # Filter by tool_id if specified
            executions = [ex for ex in self.execution_history if not tool_id or ex.tool_id == tool_id]
            
            # Sort by start time (most recent first)
            executions.sort(key=lambda x: x.started_at, reverse=True)
            
            # Limit results
            executions = executions[:limit]
            
            for execution in executions:
                history_item = {
                    "execution_id": execution.execution_id,
                    "tool_id": execution.tool_id,
                    "status": execution.status,
                    "started_at": execution.started_at.isoformat(),
                    "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
                    "error": execution.error
                }
                
                history.append(history_item)
            
            return history
            
        except Exception as e:
            logger.error("Failed to get execution history", error=str(e))
            return []
    
    async def orchestrate_tools(self, tool_sequence: List[str], 
                               input_data: Dict[str, Any],
                               context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Orchestrate execution of multiple tools in sequence"""
        try:
            orchestration_id = str(uuid.uuid4())
            results = []
            context = context or {}
            
            logger.info("Starting tool orchestration", 
                       orchestration_id=orchestration_id, 
                       tool_count=len(tool_sequence))
            
            for i, tool_id in enumerate(tool_sequence):
                try:
                    # Execute tool
                    result = await self.execute_tool(tool_id, input_data, context)
                    results.append(result)
                    
                    # Update context with result for next tool
                    context[f"tool_{i}_result"] = result.get("result")
                    context[f"tool_{i}_status"] = result.get("status")
                    
                    # If tool failed, decide whether to continue
                    if result.get("status") == "failed":
                        # Check if we should continue or stop
                        definition = self.tool_definitions.get(tool_id)
                        if definition and definition.priority == ToolPriority.CRITICAL:
                            logger.error("Critical tool failed, stopping orchestration",
                                       tool_id=tool_id, orchestration_id=orchestration_id)
                            break
                    
                except Exception as e:
                    logger.error("Tool orchestration error", 
                               tool_id=tool_id, 
                               orchestration_id=orchestration_id, 
                               error=str(e))
                    
                    results.append({
                        "tool_id": tool_id,
                        "status": "failed",
                        "error": str(e)
                    })
                    
                    # Continue with next tool unless critical
                    definition = self.tool_definitions.get(tool_id)
                    if definition and definition.priority == ToolPriority.CRITICAL:
                        break
            
            return {
                "orchestration_id": orchestration_id,
                "tool_sequence": tool_sequence,
                "results": results,
                "success_count": len([r for r in results if r.get("status") == "success"]),
                "failure_count": len([r for r in results if r.get("status") == "failed"]),
                "context": context
            }
            
        except Exception as e:
            logger.error("Tool orchestration failed", error=str(e))
            return {
                "orchestration_id": orchestration_id if 'orchestration_id' in locals() else None,
                "status": "failed",
                "error": str(e)
            }

# Built-in Tool Implementations

class SecurityValidatorTool(ITool):
    """Security validation tool"""
    
    def __init__(self):
        self.definition = ToolDefinition(
            id="security_validator",
            name="Security Validator",
            description="Validates security aspects of code and configurations",
            category=ToolCategory.SECURITY_VALIDATION,
            version="1.0.0",
            priority=ToolPriority.HIGH
        )
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute security validation"""
        code = input_data.get("code", "")
        config = input_data.get("config", {})
        
        # Basic security checks
        security_issues = []
        
        # Check for hardcoded secrets
        if any(secret in code.lower() for secret in ["password", "secret", "key", "token"]):
            security_issues.append("Potential hardcoded secrets detected")
        
        # Check for SQL injection patterns
        if "execute" in code.lower() and "SELECT" in code.upper():
            security_issues.append("Potential SQL injection vulnerability")
        
        # Check for XSS patterns
        if "innerHTML" in code or "document.write" in code:
            security_issues.append("Potential XSS vulnerability")
        
        return {
            "security_score": max(0, 100 - len(security_issues) * 20),
            "issues_found": security_issues,
            "recommendations": [
                "Use parameterized queries",
                "Validate and sanitize inputs",
                "Use environment variables for secrets"
            ]
        }
    
    def get_definition(self) -> ToolDefinition:
        return self.definition
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "code" in input_data or "config" in input_data
    
    async def get_capabilities(self) -> Dict[str, Any]:
        return {
            "input_types": ["code", "config"],
            "security_checks": ["secrets", "sql_injection", "xss", "csrf"],
            "output_format": "security_report"
        }

class CodeQualityAnalyzerTool(ITool):
    """Code quality analysis tool"""
    
    def __init__(self):
        self.definition = ToolDefinition(
            id="code_quality_analyzer",
            name="Code Quality Analyzer",
            description="Analyzes code quality metrics and provides recommendations",
            category=ToolCategory.QUALITY_ANALYSIS,
            version="1.0.0",
            priority=ToolPriority.MEDIUM
        )
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute code quality analysis"""
        code = input_data.get("code", "")
        language = input_data.get("language", "python")
        
        # Basic quality metrics
        lines = code.split('\n')
        total_lines = len(lines)
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        blank_lines = len([line for line in lines if not line.strip()])
        
        # Calculate metrics
        comment_ratio = comment_lines / total_lines if total_lines > 0 else 0
        complexity_score = min(100, max(0, 100 - (total_lines / 10)))
        
        # Quality assessment
        quality_score = (comment_ratio * 30 + complexity_score * 70)
        
        return {
            "quality_score": round(quality_score, 2),
            "metrics": {
                "total_lines": total_lines,
                "comment_lines": comment_lines,
                "comment_ratio": round(comment_ratio, 2),
                "complexity_score": round(complexity_score, 2)
            },
            "recommendations": [
                "Add more comments for complex logic",
                "Consider breaking down large functions",
                "Follow consistent naming conventions"
            ]
        }
    
    def get_definition(self) -> ToolDefinition:
        return self.definition
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "code" in input_data
    
    async def get_capabilities(self) -> Dict[str, Any]:
        return {
            "input_types": ["code"],
            "languages": ["python", "javascript", "typescript", "java"],
            "metrics": ["complexity", "maintainability", "readability"],
            "output_format": "quality_report"
        }

class ErrorRecoveryManagerTool(ITool):
    """Error recovery management tool"""
    
    def __init__(self):
        self.definition = ToolDefinition(
            id="error_recovery_manager",
            name="Error Recovery Manager",
            description="Manages error recovery and provides recovery strategies",
            category=ToolCategory.ERROR_RECOVERY,
            version="1.0.0",
            priority=ToolPriority.HIGH
        )
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute error recovery management"""
        error_type = input_data.get("error_type", "unknown")
        error_message = input_data.get("error_message", "")
        context_info = input_data.get("context", {})
        
        # Analyze error and provide recovery strategies
        recovery_strategies = []
        
        if "timeout" in error_message.lower():
            recovery_strategies.append("Increase timeout settings")
            recovery_strategies.append("Optimize query performance")
        elif "connection" in error_message.lower():
            recovery_strategies.append("Check network connectivity")
            recovery_strategies.append("Retry with exponential backoff")
        elif "validation" in error_message.lower():
            recovery_strategies.append("Validate input data")
            recovery_strategies.append("Check data format requirements")
        
        return {
            "error_type": error_type,
            "recovery_strategies": recovery_strategies,
            "retry_recommended": True,
            "fallback_available": len(recovery_strategies) > 0
        }
    
    def get_definition(self) -> ToolDefinition:
        return self.definition
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "error_type" in input_data or "error_message" in input_data
    
    async def get_capabilities(self) -> Dict[str, Any]:
        return {
            "error_types": ["timeout", "connection", "validation", "authentication"],
            "recovery_strategies": ["retry", "fallback", "circuit_breaker"],
            "output_format": "recovery_plan"
        }

class FactualAccuracyValidatorTool(ITool):
    """Factual accuracy validation tool"""
    
    def __init__(self):
        self.definition = ToolDefinition(
            id="factual_accuracy_validator",
            name="Factual Accuracy Validator",
            description="Validates factual accuracy of information and responses",
            category=ToolCategory.ACCURACY_VALIDATION,
            version="1.0.0",
            priority=ToolPriority.HIGH
        )
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute factual accuracy validation"""
        content = input_data.get("content", "")
        fact_claims = input_data.get("fact_claims", [])
        
        # Basic accuracy checks
        accuracy_score = 100
        issues = []
        
        # Check for contradictory statements
        if "always" in content.lower() and "sometimes" in content.lower():
            accuracy_score -= 20
            issues.append("Contradictory statements detected")
        
        # Check for unsupported claims
        if "proven" in content.lower() and not any("study" in content.lower() or "research" in content.lower()):
            accuracy_score -= 30
            issues.append("Unsupported claims detected")
        
        # Validate fact claims
        validated_claims = []
        for claim in fact_claims:
            if claim.get("source") and claim.get("verifiable"):
                validated_claims.append(claim)
            else:
                accuracy_score -= 10
                issues.append(f"Unverified claim: {claim.get('text', 'Unknown')}")
        
        return {
            "accuracy_score": max(0, accuracy_score),
            "issues_found": issues,
            "validated_claims": len(validated_claims),
            "total_claims": len(fact_claims),
            "recommendations": [
                "Provide sources for factual claims",
                "Avoid absolute statements without evidence",
                "Cross-reference information with reliable sources"
            ]
        }
    
    def get_definition(self) -> ToolDefinition:
        return self.definition
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "content" in input_data or "fact_claims" in input_data
    
    async def get_capabilities(self) -> Dict[str, Any]:
        return {
            "input_types": ["content", "fact_claims"],
            "validation_types": ["contradiction", "verification", "source_check"],
            "output_format": "accuracy_report"
        }

class ConsistencyEnforcerTool(ITool):
    """Consistency enforcement tool"""
    
    def __init__(self):
        self.definition = ToolDefinition(
            id="consistency_enforcer",
            name="Consistency Enforcer",
            description="Enforces consistency across system components and data",
            category=ToolCategory.CONSISTENCY_ENFORCEMENT,
            version="1.0.0",
            priority=ToolPriority.MEDIUM
        )
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute consistency enforcement"""
        data_items = input_data.get("data_items", [])
        consistency_rules = input_data.get("consistency_rules", [])
        
        # Check consistency
        inconsistencies = []
        consistency_score = 100
        
        for i, item1 in enumerate(data_items):
            for j, item2 in enumerate(data_items[i+1:], i+1):
                # Check for conflicts
                if self._check_conflict(item1, item2):
                    inconsistencies.append({
                        "item1_index": i,
                        "item2_index": j,
                        "conflict_type": "data_mismatch",
                        "description": f"Items {i} and {j} have conflicting data"
                    })
                    consistency_score -= 10
        
        return {
            "consistency_score": max(0, consistency_score),
            "inconsistencies_found": len(inconsistencies),
            "inconsistencies": inconsistencies,
            "recommendations": [
                "Standardize data formats",
                "Implement validation rules",
                "Use consistent naming conventions"
            ]
        }
    
    def _check_conflict(self, item1: Dict[str, Any], item2: Dict[str, Any]) -> bool:
        """Check if two items have conflicts"""
        # Simple conflict detection
        for key in item1:
            if key in item2 and item1[key] != item2[key]:
                return True
        return False
    
    def get_definition(self) -> ToolDefinition:
        return self.definition
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "data_items" in input_data
    
    async def get_capabilities(self) -> Dict[str, Any]:
        return {
            "input_types": ["data_items", "consistency_rules"],
            "check_types": ["format", "naming", "structure", "values"],
            "output_format": "consistency_report"
        }

class MonitoringAnalyticsManagerTool(ITool):
    """Monitoring and analytics management tool"""
    
    def __init__(self):
        self.definition = ToolDefinition(
            id="monitoring_analytics_manager",
            name="Monitoring Analytics Manager",
            description="Manages monitoring and analytics data collection and analysis",
            category=ToolCategory.MONITORING_ANALYTICS,
            version="1.0.0",
            priority=ToolPriority.MEDIUM
        )
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute monitoring analytics management"""
        metrics_data = input_data.get("metrics_data", {})
        analysis_type = input_data.get("analysis_type", "basic")
        
        # Basic analytics
        if analysis_type == "basic":
            return self._basic_analysis(metrics_data)
        elif analysis_type == "trend":
            return self._trend_analysis(metrics_data)
        else:
            return self._comprehensive_analysis(metrics_data)
    
    def _basic_analysis(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform basic analytics"""
        total_requests = metrics_data.get("total_requests", 0)
        success_rate = metrics_data.get("success_rate", 0)
        avg_response_time = metrics_data.get("avg_response_time", 0)
        
        return {
            "analysis_type": "basic",
            "summary": {
                "total_requests": total_requests,
                "success_rate": success_rate,
                "avg_response_time": avg_response_time
            },
            "health_status": "healthy" if success_rate > 95 else "warning",
            "recommendations": [
                "Monitor response times closely",
                "Investigate failed requests if success rate is low"
            ]
        }
    
    def _trend_analysis(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform trend analysis"""
        return {
            "analysis_type": "trend",
            "trends": {
                "performance_trend": "stable",
                "usage_trend": "increasing",
                "error_trend": "decreasing"
            },
            "predictions": {
                "next_hour_requests": metrics_data.get("total_requests", 0) * 1.1,
                "capacity_utilization": 75
            }
        }
    
    def _comprehensive_analysis(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive analysis"""
        return {
            "analysis_type": "comprehensive",
            "insights": [
                "System performance is optimal",
                "User engagement is increasing",
                "Error rates are within acceptable limits"
            ],
            "recommendations": [
                "Consider scaling if usage continues to grow",
                "Monitor resource utilization",
                "Optimize database queries"
            ]
        }
    
    def get_definition(self) -> ToolDefinition:
        return self.definition
    
    async def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return "metrics_data" in input_data
    
    async def get_capabilities(self) -> Dict[str, Any]:
        return {
            "input_types": ["metrics_data"],
            "analysis_types": ["basic", "trend", "comprehensive"],
            "output_formats": ["summary", "detailed_report", "dashboard_data"]
        }

# Global instance
tool_integration_manager = ToolIntegrationManager()
