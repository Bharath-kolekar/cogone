"""
Tool Integration Manager for CognOmega Platform
Manages external tool integrations with Groq AI as primary service
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import logging
import httpx
from dataclasses import dataclass

from ..models.tool_integration_models import (
    ToolIntegration, ToolType, ToolStatus, ToolPriority, ToolCapability,
    ToolConfiguration, ToolAuthentication, ToolEndpoint, ToolMetadata,
    ToolExecutionRequest, ToolExecutionResult, ToolHealthCheck,
    ToolRegistry, ToolIntegrationStats, AuthenticationType
)

logger = logging.getLogger(__name__)

@dataclass
class GroqConfig:
    """Groq API configuration"""
    api_key: str
    model: str = "llama3-8b-8192"
    max_tokens: int = 8000
    temperature: float = 0.7
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    timeout: int = 30
    base_url: str = "https://api.groq.com/openai/v1"

class ToolIntegrationManager:
    """Manages external tool integrations with intelligent routing"""
    
    def __init__(self, groq_config: Optional[GroqConfig] = None):
        self.registry = ToolRegistry()
        self.execution_history: List[ToolExecutionResult] = []
        self.health_checks: Dict[str, ToolHealthCheck] = {}
        self.groq_config = groq_config
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
        # Performance metrics
        self.total_executions = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self.total_response_time = 0.0
        
        # Initialize with built-in tools
        self._initialize_builtin_tools()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _initialize_builtin_tools(self):
        """Initialize built-in tool integrations"""
        
        # Groq AI Service (Primary)
        if self.groq_config:
            groq_tool = ToolIntegration(
                id="groq-ai-service",
                name="Groq AI Service",
                type=ToolType.AI_SERVICE,
                status=ToolStatus.ACTIVE,
                priority=ToolPriority.CRITICAL,
                configuration=[
                    ToolConfiguration(name="api_key", value=self.groq_config.api_key, encrypted=True),
                    ToolConfiguration(name="model", value=self.groq_config.model),
                    ToolConfiguration(name="max_tokens", value=self.groq_config.max_tokens),
                    ToolConfiguration(name="temperature", value=self.groq_config.temperature),
                    ToolConfiguration(name="base_url", value=self.groq_config.base_url)
                ],
                authentication=ToolAuthentication(
                    auth_type=AuthenticationType.BEARER_TOKEN,
                    credentials={"token": self.groq_config.api_key}
                ),
                endpoints=[
                    ToolEndpoint(
                        name="chat_completions",
                        url=f"{self.groq_config.base_url}/chat/completions",
                        method="POST",
                        timeout=self.groq_config.timeout
                    )
                ],
                capabilities=[
                    ToolCapability.GENERATE,
                    ToolCapability.ANALYZE,
                    ToolCapability.TRANSFORM,
                    ToolCapability.VALIDATE
                ],
                metadata=ToolMetadata(
                    version="1.0.0",
                    description="Groq AI service for fast inference",
                    author="Groq",
                    tags=["ai", "llm", "inference", "groq"]
                )
            )
            self.registry.tools["groq-ai-service"] = groq_tool
        
        # OpenAI Service (Fallback)
        openai_tool = ToolIntegration(
            id="openai-service",
            name="OpenAI Service",
            type=ToolType.AI_SERVICE,
            status=ToolStatus.INACTIVE,
            priority=ToolPriority.HIGH,
            configuration=[
                ToolConfiguration(name="api_key", value="", encrypted=True),
                ToolConfiguration(name="model", value="gpt-4-turbo-preview"),
                ToolConfiguration(name="max_tokens", value=4000),
                ToolConfiguration(name="temperature", value=0.7),
                ToolConfiguration(name="base_url", value="https://api.openai.com/v1")
            ],
            authentication=ToolAuthentication(
                auth_type=AuthenticationType.BEARER_TOKEN,
                credentials={"token": ""}
            ),
            endpoints=[
                ToolEndpoint(
                    name="chat_completions",
                    url="https://api.openai.com/v1/chat/completions",
                    method="POST",
                    timeout=30
                )
            ],
            capabilities=[
                ToolCapability.GENERATE,
                ToolCapability.ANALYZE,
                ToolCapability.TRANSFORM,
                ToolCapability.VALIDATE
            ],
            metadata=ToolMetadata(
                version="1.0.0",
                description="OpenAI service for AI completions",
                author="OpenAI",
                tags=["ai", "llm", "openai", "gpt"]
            )
        )
        self.registry.tools["openai-service"] = openai_tool
        
        # Anthropic Service (Fallback)
        anthropic_tool = ToolIntegration(
            id="anthropic-service",
            name="Anthropic Service",
            type=ToolType.AI_SERVICE,
            status=ToolStatus.INACTIVE,
            priority=ToolPriority.HIGH,
            configuration=[
                ToolConfiguration(name="api_key", value="", encrypted=True),
                ToolConfiguration(name="model", value="claude-3-sonnet-20240229"),
                ToolConfiguration(name="max_tokens", value=4000),
                ToolConfiguration(name="temperature", value=0.7),
                ToolConfiguration(name="base_url", value="https://api.anthropic.com/v1")
            ],
            authentication=ToolAuthentication(
                auth_type=AuthenticationType.API_KEY,
                credentials={"api_key": ""}
            ),
            endpoints=[
                ToolEndpoint(
                    name="messages",
                    url="https://api.anthropic.com/v1/messages",
                    method="POST",
                    timeout=30
                )
            ],
            capabilities=[
                ToolCapability.GENERATE,
                ToolCapability.ANALYZE,
                ToolCapability.TRANSFORM,
                ToolCapability.VALIDATE
            ],
            metadata=ToolMetadata(
                version="1.0.0",
                description="Anthropic Claude service",
                author="Anthropic",
                tags=["ai", "llm", "anthropic", "claude"]
            )
        )
        self.registry.tools["anthropic-service"] = anthropic_tool
        
        # Ollama Local Service (Fallback)
        ollama_tool = ToolIntegration(
            id="ollama-service",
            name="Ollama Local Service",
            type=ToolType.AI_SERVICE,
            status=ToolStatus.INACTIVE,
            priority=ToolPriority.MEDIUM,
            configuration=[
                ToolConfiguration(name="host", value="http://localhost:11434"),
                ToolConfiguration(name="model", value="llama3:8b-instruct-q4_K_M"),
                ToolConfiguration(name="temperature", value=0.7),
                ToolConfiguration(name="timeout", value=120)
            ],
            authentication=ToolAuthentication(auth_type=AuthenticationType.NONE),
            endpoints=[
                ToolEndpoint(
                    name="generate",
                    url="http://localhost:11434/api/generate",
                    method="POST",
                    timeout=120
                )
            ],
            capabilities=[
                ToolCapability.GENERATE,
                ToolCapability.ANALYZE,
                ToolCapability.TRANSFORM,
                ToolCapability.VALIDATE
            ],
            metadata=ToolMetadata(
                version="1.0.0",
                description="Local Ollama service for offline AI",
                author="Ollama",
                tags=["ai", "llm", "local", "ollama", "offline"]
            )
        )
        self.registry.tools["ollama-service"] = ollama_tool
        
        # Update registry categories
        self._update_registry_categories()
    
    def _update_registry_categories(self):
        """Update registry categories and capabilities"""
        self.registry.categories = {}
        self.registry.capabilities = {}
        
        for tool_id, tool in self.registry.tools.items():
            # Group by type
            if tool.type not in self.registry.categories:
                self.registry.categories[tool.type] = []
            self.registry.categories[tool.type].append(tool_id)
            
            # Group by capability
            for capability in tool.capabilities:
                if capability not in self.registry.capabilities:
                    self.registry.capabilities[capability] = []
                self.registry.capabilities[capability].append(tool_id)
        
        self.registry.last_updated = datetime.utcnow()
    
    async def register_tool(self, tool: ToolIntegration) -> bool:
        """Register a new tool integration"""
        try:
            # Validate tool configuration
            if not await self._validate_tool_configuration(tool):
                logger.error(f"Invalid tool configuration for {tool.name}")
                return False
            
            # Add to registry
            self.registry.tools[tool.id] = tool
            self._update_registry_categories()
            
            # Perform initial health check
            await self._perform_health_check(tool.id)
            
            logger.info(f"Successfully registered tool: {tool.name} ({tool.id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register tool {tool.name}: {str(e)}")
            return False
    
    async def unregister_tool(self, tool_id: str) -> bool:
        """Unregister a tool integration"""
        try:
            if tool_id in self.registry.tools:
                tool_name = self.registry.tools[tool_id].name
                del self.registry.tools[tool_id]
                self._update_registry_categories()
                
                # Remove from health checks
                if tool_id in self.health_checks:
                    del self.health_checks[tool_id]
                
                logger.info(f"Successfully unregistered tool: {tool_name} ({tool_id})")
                return True
            else:
                logger.warning(f"Tool {tool_id} not found in registry")
                return False
                
        except Exception as e:
            logger.error(f"Failed to unregister tool {tool_id}: {str(e)}")
            return False
    
    async def execute_tool(self, request: ToolExecutionRequest) -> ToolExecutionResult:
        """Execute a tool operation"""
        start_time = datetime.utcnow()
        execution_id = f"exec_{int(time.time())}_{request.tool_id}"
        
        result = ToolExecutionResult(
            execution_id=execution_id,
            tool_id=request.tool_id,
            operation=request.operation,
            status="running",
            start_time=start_time,
            parameters=request.parameters,
            context=request.context
        )
        
        try:
            # Check if tool exists
            if request.tool_id not in self.registry.tools:
                raise ValueError(f"Tool {request.tool_id} not found")
            
            tool = self.registry.tools[request.tool_id]
            
            # Check if tool is active
            if tool.status != ToolStatus.ACTIVE:
                raise ValueError(f"Tool {request.tool_id} is not active (status: {tool.status})")
            
            # Execute based on tool type
            if tool.type == ToolType.AI_SERVICE:
                result.result = await self._execute_ai_service(tool, request)
            else:
                result.result = await self._execute_generic_tool(tool, request)
            
            # Update success metrics
            result.status = "completed"
            result.end_time = datetime.utcnow()
            result.duration = (result.end_time - result.start_time).total_seconds()
            
            self.successful_executions += 1
            self.total_response_time += result.duration
            
            # Update tool metrics
            tool.usage_count += 1
            tool.last_used = datetime.utcnow()
            
            if tool.avg_response_time is None:
                tool.avg_response_time = result.duration
            else:
                tool.avg_response_time = (tool.avg_response_time + result.duration) / 2
            
            logger.info(f"Tool execution completed: {request.tool_id} - {request.operation} ({result.duration:.2f}s)")
            
        except Exception as e:
            result.status = "failed"
            result.error = str(e)
            result.end_time = datetime.utcnow()
            result.duration = (result.end_time - result.start_time).total_seconds()
            
            self.failed_executions += 1
            
            # Update tool error metrics
            tool.error_count += 1
            
            logger.error(f"Tool execution failed: {request.tool_id} - {request.operation}: {str(e)}")
        
        finally:
            self.total_executions += 1
            self.execution_history.append(result)
            
            # Keep only last 1000 executions
            if len(self.execution_history) > 1000:
                self.execution_history = self.execution_history[-1000:]
        
        return result
    
    async def _execute_ai_service(self, tool: ToolIntegration, request: ToolExecutionRequest) -> Any:
        """Execute AI service tool"""
        if tool.id == "groq-ai-service":
            return await self._execute_groq_service(tool, request)
        elif tool.id == "openai-service":
            return await self._execute_openai_service(tool, request)
        elif tool.id == "anthropic-service":
            return await self._execute_anthropic_service(tool, request)
        elif tool.id == "ollama-service":
            return await self._execute_ollama_service(tool, request)
        else:
            raise ValueError(f"Unknown AI service: {tool.id}")
    
    async def _execute_groq_service(self, tool: ToolIntegration, request: ToolExecutionRequest) -> Any:
        """Execute Groq AI service"""
        try:
            # Get configuration
            config = {c.name: c.value for c in tool.configuration}
            
            # Prepare request
            messages = request.parameters.get("messages", [])
            if not messages:
                messages = [{"role": "user", "content": request.parameters.get("prompt", "")}]
            
            payload = {
                "model": config.get("model", "llama3-8b-8192"),
                "messages": messages,
                "max_tokens": config.get("max_tokens", 8000),
                "temperature": config.get("temperature", 0.7),
                "top_p": config.get("top_p", 0.9),
                "stream": False
            }
            
            # Make request
            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json"
            }
            
            response = await self.http_client.post(
                f"{config['base_url']}/chat/completions",
                json=payload,
                headers=headers,
                timeout=config.get("timeout", 30)
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract content
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise ValueError("No response content from Groq")
                
        except Exception as e:
            logger.error(f"Groq service execution failed: {str(e)}")
            raise
    
    async def _execute_openai_service(self, tool: ToolIntegration, request: ToolExecutionRequest) -> Any:
        """
        Execute OpenAI service
        
        🧬 REAL IMPLEMENTATION: OpenAI Chat Completions API
        """
        try:
            # Get configuration
            config = {c.name: c.value for c in tool.configuration}
            api_key = config.get('api_key', '')
            
            # Prepare request
            payload = {
                "model": config.get("model", "gpt-3.5-turbo"),
                "messages": [
                    {"role": "user", "content": request.parameters.get("prompt", "")}
                ],
                "max_tokens": config.get("max_tokens", 2000),
                "temperature": config.get("temperature", 0.7)
            }
            
            # Make request to OpenAI API
            response = await self.http_client.post(
                f"{config.get('base_url', 'https://api.openai.com/v1')}/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                timeout=config.get("timeout", 30)
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract response
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"OpenAI service execution failed: {str(e)}")
            raise
    
    async def _execute_anthropic_service(self, tool: ToolIntegration, request: ToolExecutionRequest) -> Any:
        """
        Execute Anthropic service
        
        🧬 REAL IMPLEMENTATION: Anthropic Messages API
        """
        try:
            # Get configuration
            config = {c.name: c.value for c in tool.configuration}
            api_key = config.get('api_key', '')
            
            # Prepare request
            payload = {
                "model": config.get("model", "claude-3-sonnet-20240229"),
                "messages": [
                    {"role": "user", "content": request.parameters.get("prompt", "")}
                ],
                "max_tokens": config.get("max_tokens", 4096),
                "temperature": config.get("temperature", 0.7)
            }
            
            # Make request to Anthropic API
            response = await self.http_client.post(
                f"{config.get('base_url', 'https://api.anthropic.com/v1')}/messages",
                json=payload,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                timeout=config.get("timeout", 30)
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract response
            return result['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Anthropic service execution failed: {str(e)}")
            raise
    
    async def _execute_ollama_service(self, tool: ToolIntegration, request: ToolExecutionRequest) -> Any:
        """Execute Ollama local service"""
        try:
            # Get configuration
            config = {c.name: c.value for c in tool.configuration}
            
            # Prepare request
            payload = {
                "model": config.get("model", "llama3:8b-instruct-q4_K_M"),
                "prompt": request.parameters.get("prompt", ""),
                "stream": False,
                "options": {
                    "temperature": config.get("temperature", 0.7)
                }
            }
            
            # Make request
            response = await self.http_client.post(
                f"{config['host']}/api/generate",
                json=payload,
                timeout=config.get("timeout", 120)
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get("response", "")
            
        except Exception as e:
            logger.error(f"Ollama service execution failed: {str(e)}")
            raise
    
    async def _execute_generic_tool(self, tool: ToolIntegration, request: ToolExecutionRequest) -> Any:
        """
        Execute generic tool
        
        🧬 REAL IMPLEMENTATION: Generic HTTP tool executor
        """
        try:
            # Get configuration
            config = {c.name: c.value for c in tool.configuration}
            
            # Get endpoint
            endpoint = tool.endpoints[0] if tool.endpoints else None
            if not endpoint:
                raise ValueError("No endpoint configured for generic tool")
            
            # Prepare headers
            headers = {}
            if tool.authentication:
                auth = tool.authentication
                if auth.auth_type == AuthenticationType.BEARER_TOKEN:
                    headers["Authorization"] = f"Bearer {auth.credentials.get('token', '')}"
                elif auth.auth_type == AuthenticationType.API_KEY:
                    key_name = auth.credentials.get('key_name', 'X-API-Key')
                    headers[key_name] = auth.credentials.get('api_key', '')
                elif auth.auth_type == AuthenticationType.BASIC:
                    import base64
                    username = auth.credentials.get('username', '')
                    password = auth.credentials.get('password', '')
                    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                    headers["Authorization"] = f"Basic {credentials}"
            
            # Prepare request
            method = endpoint.method.upper()
            url = endpoint.url
            
            # Make request
            if method == "GET":
                response = await self.http_client.get(url, headers=headers, params=request.parameters)
            elif method == "POST":
                response = await self.http_client.post(url, headers=headers, json=request.parameters)
            elif method == "PUT":
                response = await self.http_client.put(url, headers=headers, json=request.parameters)
            elif method == "DELETE":
                response = await self.http_client.delete(url, headers=headers, params=request.parameters)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            # Return response based on content type
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return response.json()
            else:
                return response.text
            
        except Exception as e:
            logger.error(f"Generic tool execution failed: {str(e)}")
            raise
    
    async def _validate_tool_configuration(self, tool: ToolIntegration) -> bool:
        """Validate tool configuration"""
        try:
            # Check required fields
            if not tool.name or not tool.type:
                return False
            
            # Validate configuration
            for config in tool.configuration:
                if config.required and not config.value:
                    return False
            
            # Validate endpoints
            for endpoint in tool.endpoints:
                if not endpoint.url or not endpoint.name:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Tool configuration validation failed: {str(e)}")
            return False
    
    async def _perform_health_check(self, tool_id: str) -> ToolHealthCheck:
        """Perform health check for a tool"""
        start_time = time.time()
        
        health_check = ToolHealthCheck(
            tool_id=tool_id,
            status=ToolStatus.ERROR,
            last_check=datetime.utcnow()
        )
        
        try:
            if tool_id not in self.registry.tools:
                health_check.error_message = "Tool not found in registry"
                self.health_checks[tool_id] = health_check
                return health_check
            
            tool = self.registry.tools[tool_id]
            
            # Perform health check based on tool type
            if tool.type == ToolType.AI_SERVICE:
                # Test AI service endpoint
                test_request = ToolExecutionRequest(
                    tool_id=tool_id,
                    operation="health_check",
                    parameters={"prompt": "Hello, are you working?"}
                )
                
                result = await self.execute_tool(test_request)
                if result.status == "completed":
                    health_check.status = ToolStatus.ACTIVE
                    health_check.details = {"test_response": result.result[:100]}
                else:
                    health_check.error_message = result.error
            else:
                # Generic health check
                health_check.status = ToolStatus.ACTIVE
                health_check.details = {"type": "generic_tool"}
            
            health_check.response_time = time.time() - start_time
            
        except Exception as e:
            health_check.error_message = str(e)
            health_check.response_time = time.time() - start_time
        
        self.health_checks[tool_id] = health_check
        return health_check
    
    async def get_tool_by_capability(self, capability: ToolCapability) -> List[ToolIntegration]:
        """Get tools that have a specific capability"""
        if capability in self.registry.capabilities:
            tool_ids = self.registry.capabilities[capability]
            return [self.registry.tools[tool_id] for tool_id in tool_ids if tool_id in self.registry.tools]
        return []
    
    async def get_active_tools(self) -> List[ToolIntegration]:
        """Get all active tools"""
        return [tool for tool in self.registry.tools.values() if tool.status == ToolStatus.ACTIVE]
    
    async def get_tool_stats(self) -> ToolIntegrationStats:
        """Get tool integration statistics"""
        tools = list(self.registry.tools.values())
        
        stats = ToolIntegrationStats(
            total_tools=len(tools),
            active_tools=len([t for t in tools if t.status == ToolStatus.ACTIVE]),
            tools_by_type={},
            tools_by_status={},
            total_executions=self.total_executions,
            successful_executions=self.successful_executions,
            failed_executions=self.failed_executions,
            avg_response_time=self.total_response_time / max(self.total_executions, 1),
            success_rate=(self.successful_executions / max(self.total_executions, 1)) * 100
        )
        
        # Count by type
        for tool in tools:
            tool_type = tool.type.value
            stats.tools_by_type[tool_type] = stats.tools_by_type.get(tool_type, 0) + 1
        
        # Count by status
        for tool in tools:
            tool_status = tool.status.value
            stats.tools_by_status[tool_status] = stats.tools_by_status.get(tool_status, 0) + 1
        
        return stats
    
    def _start_background_tasks(self):
        """
        Start background tasks for health monitoring
        
        🧬 REAL IMPLEMENTATION: Starts async health check task
        """
        import asyncio
        
        try:
            # 🧬 REAL: Create background task for health monitoring
            loop = asyncio.get_event_loop()
            
            async def health_check_loop():
                while True:
                    try:
                        # Check health of all tools
                        for tool_name, tool in self.tools.items():
                            health = await self.check_tool_health(tool_name)
                            if not health.get("is_healthy", False):
                                logger.warning(f"Tool {tool_name} unhealthy: {health}")
                        
                        await asyncio.sleep(300)  # Check every 5 minutes
                    except Exception as e:
                        logger.error(f"Health check loop error: {e}")
                        await asyncio.sleep(60)
            
            # Start the background task
            asyncio.create_task(health_check_loop())
            logger.info("Background health monitoring started")
            
        except Exception as e:
            logger.warning(f"Could not start background tasks: {e}")
    
    async def shutdown(self):
        """Shutdown the tool integration manager"""
        await self.http_client.aclose()
        logger.info("Tool Integration Manager shutdown complete")
