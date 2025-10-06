"""
Smarty Agent Integration Service

This module integrates AI Agents with Smarty (SmartCodingAIOptimized),
providing intelligent agents with enhanced code generation capabilities
and ethical validation.
"""

import structlog
import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Tuple, Union, AsyncGenerator
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid

# Import existing services
from .ai_agent_consolidated_service import ConsolidatedAIAgentServices
from .smart_coding_ai_optimized import SmartCodingAIOptimized
from .smarty_ethical_integration import SmartyEthicalIntegration

# Import AI Agent models
from app.models.ai_agent import (
    AgentDefinition, AgentConfig, AgentMemory, AgentMetrics,
    TaskDefinition, AgentInteraction, AgentWorkflow,
    AgentRequest, AgentResponse, AgentCreationRequest,
    AgentType, AgentStatus, AgentCapability, TaskStatus,
    TaskType, AgentPriority
)

# Import Ethical AI Components
from app.core.ethical_ai_core import ethical_ai_core
from app.core.tool_integration_manager import tool_integration_manager
from app.core.security_validator import security_validator
from app.core.code_quality_analyzer import code_quality_analyzer
from app.services.goal_integrity_service import goal_integrity_service
from app.core.error_recovery_manager import error_recovery_manager
from app.core.factual_accuracy_validator import factual_accuracy_validator
from app.core.consistency_enforcer import consistency_enforcer
from app.core.enhanced_context_sharing import enhanced_context_sharing, ContextType, ContextPriority, ContextAccess
from app.core.enhanced_monitoring_analytics import enhanced_monitoring_analytics, MetricType, AlertSeverity, ComponentStatus

logger = structlog.get_logger(__name__)

class AgentSmartyMode(Enum):
    """Agent-Smarty integration modes"""
    CODE_GENERATION_ASSISTANT = "code_generation_assistant"
    CODE_REVIEW_ASSISTANT = "code_review_assistant"
    DEBUGGING_ASSISTANT = "debugging_assistant"
    TESTING_ASSISTANT = "testing_assistant"
    DOCUMENTATION_ASSISTANT = "documentation_assistant"
    ARCHITECTURE_ASSISTANT = "architecture_assistant"
    OPTIMIZATION_ASSISTANT = "optimization_assistant"
    SECURITY_ASSISTANT = "security_assistant"

class AgentCodeCapability(Enum):
    """Agent code generation capabilities"""
    BASIC_CODE = "basic_code"
    ADVANCED_CODE = "advanced_code"
    ARCHITECTURAL_CODE = "architectural_code"
    OPTIMIZED_CODE = "optimized_code"
    SECURE_CODE = "secure_code"
    TESTED_CODE = "tested_code"
    DOCUMENTED_CODE = "documented_code"

@dataclass
class AgentSmartyConfig:
    """Configuration for Agent-Smarty integration"""
    agent_id: str
    smarty_mode: AgentSmartyMode
    code_capability: AgentCodeCapability
    ethical_validation_level: str = "standard"
    quality_threshold: float = 0.8
    security_threshold: float = 0.9
    consistency_threshold: float = 0.85
    enable_real_time_validation: bool = True
    enable_context_sharing: bool = True
    enable_monitoring: bool = True

@dataclass
class AgentCodeGenerationRequest:
    """Request for agent code generation"""
    agent_id: str
    user_id: str
    prompt: str
    context: Dict[str, Any] = field(default_factory=dict)
    code_type: str = "general"
    complexity_level: str = "medium"
    requirements: Dict[str, Any] = field(default_factory=dict)
    ethical_constraints: List[str] = field(default_factory=list)
    quality_requirements: List[str] = field(default_factory=list)

@dataclass
class AgentCodeGenerationResponse:
    """Response from agent code generation"""
    agent_id: str
    user_id: str
    generated_code: str
    validation_results: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    ethical_compliance: Dict[str, Any]
    security_assessment: Dict[str, Any]
    recommendations: List[str]
    execution_time: float
    confidence_score: float

class SmartyAgentIntegration:
    """Enhanced AI Agent integration with Smarty capabilities"""
    
    def __init__(self):
        self.agent_services = ConsolidatedAIAgentServices()
        self.smarty_service = SmartCodingAIOptimized()
        self.ethical_smarty = SmartyEthicalIntegration()
        
        # Agent-Smarty configurations
        self.agent_configs: Dict[str, AgentSmartyConfig] = {}
        self.agent_interactions: Dict[str, List[AgentInteraction]] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        
        # Performance tracking
        self.integration_metrics: Dict[str, Any] = {
            "total_agent_interactions": 0,
            "successful_code_generations": 0,
            "failed_code_generations": 0,
            "average_quality_score": 0.0,
            "average_security_score": 0.0,
            "average_ethical_compliance": 0.0,
            "average_response_time": 0.0
        }
        
        logger.info("SmartyAgentIntegration initialized with enhanced capabilities")

    async def create_smarty_agent(self, 
                                agent_creation_request: AgentCreationRequest,
                                smarty_mode: AgentSmartyMode,
                                code_capability: AgentCodeCapability,
                                ethical_validation_level: str = "standard") -> AgentDefinition:
        """Create an AI agent with Smarty integration capabilities"""
        try:
            logger.info(f"Creating Smarty-enabled agent", 
                       agent_type=agent_creation_request.agent_type.value,
                       smarty_mode=smarty_mode.value,
                       code_capability=code_capability.value)
            
            # Create base agent
            base_agent = await self.agent_services.create_agent(agent_creation_request)
            
            # Create Agent-Smarty configuration
            agent_config = AgentSmartyConfig(
                agent_id=str(base_agent.agent_id),
                smarty_mode=smarty_mode,
                code_capability=code_capability,
                ethical_validation_level=ethical_validation_level
            )
            
            # Store configuration
            self.agent_configs[str(base_agent.agent_id)] = agent_config
            
            # Initialize agent metrics
            self.agent_metrics[str(base_agent.agent_id)] = AgentMetrics(
                agent_id=base_agent.agent_id,
                total_interactions=0,
                successful_interactions=0,
                average_response_time=0.0,
                average_confidence=0.0,
                total_cost=0.0,
                performance_score=0.0
            )
            
            # Initialize interaction history
            self.agent_interactions[str(base_agent.agent_id)] = []
            
            # Enhance agent definition with Smarty capabilities
            enhanced_agent = AgentDefinition(
                agent_id=base_agent.agent_id,
                name=f"{base_agent.name} (Smarty-Enhanced)",
                description=f"{base_agent.description} - Enhanced with Smarty code generation capabilities",
                agent_type=base_agent.agent_type,
                capabilities=self._enhance_capabilities_with_smarty(base_agent.capabilities, smarty_mode, code_capability),
                config=base_agent.config,
                memory=base_agent.memory,
                status=base_agent.status,
                created_at=base_agent.created_at,
                updated_at=datetime.now()
            )
            
            logger.info(f"Smarty-enabled agent created successfully", 
                       agent_id=str(base_agent.agent_id),
                       enhanced_capabilities=len(enhanced_agent.capabilities))
            
            return enhanced_agent
            
        except Exception as e:
            logger.error(f"Smarty agent creation failed", error=str(e))
            raise

    async def interact_with_smarty_agent(self, 
                                       request: AgentCodeGenerationRequest) -> AgentCodeGenerationResponse:
        """Interact with a Smarty-enhanced agent for code generation"""
        try:
            start_time = time.time()
            agent_id = request.agent_id
            
            logger.info(f"Starting Smarty agent interaction", 
                       agent_id=agent_id,
                       user_id=request.user_id,
                       code_type=request.code_type)
            
            # Get agent configuration
            agent_config = self.agent_configs.get(agent_id)
            if not agent_config:
                raise ValueError(f"Agent configuration not found for agent {agent_id}")
            
            # Create base agent interaction request
            base_request = AgentRequest(
                agent_id=uuid.UUID(agent_id),
                message=request.prompt,
                context=request.context,
                user_id=uuid.UUID(request.user_id)
            )
            
            # Get base agent response
            base_response = await self.agent_services.interact_with_agent(base_request)
            
            # Enhance with Smarty code generation
            smarty_enhanced_response = await self._enhance_with_smarty_generation(
                base_response, request, agent_config
            )
            
            # Validate generated code
            validation_results = await self._validate_agent_generated_code(
                smarty_enhanced_response['generated_code'], agent_config
            )
            
            # Calculate quality metrics
            quality_metrics = await self._calculate_agent_quality_metrics(
                smarty_enhanced_response, validation_results
            )
            
            # Create final response
            response = AgentCodeGenerationResponse(
                agent_id=agent_id,
                user_id=request.user_id,
                generated_code=smarty_enhanced_response['generated_code'],
                validation_results=validation_results,
                quality_metrics=quality_metrics,
                ethical_compliance=validation_results.get('ethical_validation', {}),
                security_assessment=validation_results.get('security_validation', {}),
                recommendations=smarty_enhanced_response.get('recommendations', []),
                execution_time=time.time() - start_time,
                confidence_score=smarty_enhanced_response.get('confidence_score', 0.0)
            )
            
            # Update metrics
            await self._update_agent_metrics(agent_id, response)
            
            # Store interaction
            await self._store_agent_interaction(agent_id, request, response)
            
            logger.info(f"Smarty agent interaction completed", 
                       agent_id=agent_id,
                       execution_time=response.execution_time,
                       confidence_score=response.confidence_score,
                       quality_score=quality_metrics.get('overall_quality_score', 0.0))
            
            return response
            
        except Exception as e:
            logger.error(f"Smarty agent interaction failed", 
                        error=str(e), 
                        agent_id=request.agent_id,
                        user_id=request.user_id)
            raise

    async def _enhance_with_smarty_generation(self, 
                                            base_response: AgentResponse,
                                            request: AgentCodeGenerationRequest,
                                            agent_config: AgentSmartyConfig) -> Dict[str, Any]:
        """Enhance base agent response with Smarty code generation"""
        try:
            # Prepare enhanced prompt for Smarty
            enhanced_prompt = self._create_smarty_prompt(
                base_response, request, agent_config
            )
            
            # Generate code using appropriate Smarty service
            if agent_config.ethical_validation_level in ["strict", "maximum"]:
                # Use ethical Smarty for high validation levels
                code_result = await self.ethical_smarty.generate_ethical_code(
                    prompt=enhanced_prompt,
                    context=request.context,
                    mode="ethical_development"
                )
                generated_code = code_result.get('code', '')
                confidence_score = code_result.get('confidence_score', 0.0)
                recommendations = code_result.get('recommendations', [])
            else:
                # Use regular Smarty for standard validation
                code_result = await self.smarty_service.generate_code(
                    prompt=enhanced_prompt,
                    context=request.context
                )
                generated_code = code_result.get('generated_code', '')
                confidence_score = code_result.get('confidence', 0.0)
                recommendations = []
            
            # Combine base agent insights with generated code
            enhanced_response = {
                'agent_response': base_response.message,
                'generated_code': generated_code,
                'confidence_score': confidence_score,
                'recommendations': recommendations,
                'agent_insights': {
                    'reasoning': base_response.message,
                    'confidence': base_response.confidence,
                    'context_understanding': base_response.context_understanding
                },
                'smarty_enhancements': {
                    'code_generation_mode': agent_config.smarty_mode.value,
                    'code_capability': agent_config.code_capability.value,
                    'ethical_validation_level': agent_config.ethical_validation_level
                }
            }
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Smarty enhancement failed", error=str(e))
            return {
                'agent_response': base_response.message,
                'generated_code': '',
                'confidence_score': 0.0,
                'recommendations': [],
                'error': str(e)
            }

    def _create_smarty_prompt(self, 
                            base_response: AgentResponse,
                            request: AgentCodeGenerationRequest,
                            agent_config: AgentSmartyConfig) -> str:
        """Create enhanced prompt for Smarty based on agent response"""
        try:
            # Base prompt from agent response
            base_prompt = f"""
Agent Analysis: {base_response.message}

User Request: {request.prompt}
Code Type: {request.code_type}
Complexity Level: {request.complexity_level}
Requirements: {json.dumps(request.requirements, indent=2)}

Smarty Mode: {agent_config.smarty_mode.value}
Code Capability: {agent_config.code_capability.value}
Ethical Constraints: {', '.join(request.ethical_constraints)}
Quality Requirements: {', '.join(request.quality_requirements)}

Please generate high-quality, secure, and ethical code based on the agent's analysis and user requirements.
"""
            
            # Add mode-specific instructions
            mode_instructions = self._get_mode_specific_instructions(agent_config.smarty_mode)
            
            # Add capability-specific instructions
            capability_instructions = self._get_capability_specific_instructions(agent_config.code_capability)
            
            enhanced_prompt = f"{base_prompt}\n\n{mode_instructions}\n\n{capability_instructions}"
            
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"Prompt creation failed", error=str(e))
            return request.prompt

    def _get_mode_specific_instructions(self, mode: AgentSmartyMode) -> str:
        """Get mode-specific instructions for Smarty"""
        instructions = {
            AgentSmartyMode.CODE_GENERATION_ASSISTANT: "Focus on generating clean, maintainable, and well-structured code.",
            AgentSmartyMode.CODE_REVIEW_ASSISTANT: "Focus on code review, best practices, and improvement suggestions.",
            AgentSmartyMode.DEBUGGING_ASSISTANT: "Focus on identifying and fixing bugs, with detailed explanations.",
            AgentSmartyMode.TESTING_ASSISTANT: "Focus on generating comprehensive tests with good coverage.",
            AgentSmartyMode.DOCUMENTATION_ASSISTANT: "Focus on clear documentation and code comments.",
            AgentSmartyMode.ARCHITECTURE_ASSISTANT: "Focus on architectural patterns and design principles.",
            AgentSmartyMode.OPTIMIZATION_ASSISTANT: "Focus on performance optimization and efficiency.",
            AgentSmartyMode.SECURITY_ASSISTANT: "Focus on security best practices and vulnerability prevention."
        }
        return instructions.get(mode, "Generate high-quality code based on the requirements.")

    def _get_capability_specific_instructions(self, capability: AgentCodeCapability) -> str:
        """Get capability-specific instructions for Smarty"""
        instructions = {
            AgentCodeCapability.BASIC_CODE: "Generate basic, functional code that meets the requirements.",
            AgentCodeCapability.ADVANCED_CODE: "Generate advanced code with sophisticated patterns and techniques.",
            AgentCodeCapability.ARCHITECTURAL_CODE: "Generate code following architectural patterns and design principles.",
            AgentCodeCapability.OPTIMIZED_CODE: "Generate highly optimized code for performance and efficiency.",
            AgentCodeCapability.SECURE_CODE: "Generate secure code with proper security measures and validation.",
            AgentCodeCapability.TESTED_CODE: "Generate code with comprehensive test coverage and validation.",
            AgentCodeCapability.DOCUMENTED_CODE: "Generate well-documented code with clear comments and documentation."
        }
        return instructions.get(capability, "Generate high-quality code based on the requirements.")

    async def _validate_agent_generated_code(self, 
                                           generated_code: str,
                                           agent_config: AgentSmartyConfig) -> Dict[str, Any]:
        """Validate code generated by agent using ethical AI components"""
        try:
            validation_results = {
                'security_validation': {},
                'quality_validation': {},
                'ethical_validation': {},
                'consistency_validation': {},
                'overall_score': 0.0
            }
            
            # Security validation
            if generated_code:
                security_results = await security_validator.validate_code_security(generated_code)
                validation_results['security_validation'] = security_results
                
                # Quality validation
                quality_results = await code_quality_analyzer.analyze_code_quality(generated_code)
                validation_results['quality_validation'] = quality_results
                
                # Ethical validation
                ethical_results = await ethical_ai_core.validate_code_ethics(generated_code)
                validation_results['ethical_validation'] = ethical_results
                
                # Consistency validation
                consistency_results = await consistency_enforcer.validate_code_consistency(generated_code)
                validation_results['consistency_validation'] = consistency_results
                
                # Calculate overall score
                validation_results['overall_score'] = await self._calculate_validation_score(validation_results)
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Agent code validation failed", error=str(e))
            return {'overall_score': 0.0, 'error': str(e)}

    async def _calculate_validation_score(self, validation_results: Dict[str, Any]) -> float:
        """Calculate overall validation score for agent-generated code"""
        try:
            scores = []
            
            # Security score
            security_score = validation_results.get('security_validation', {}).get('score', 0.0)
            if security_score > 0:
                scores.append(security_score)
            
            # Quality score
            quality_score = validation_results.get('quality_validation', {}).get('quality_score', 0.0)
            if quality_score > 0:
                scores.append(quality_score)
            
            # Ethical score
            ethical_score = validation_results.get('ethical_validation', {}).get('ethics_score', 0.0)
            if ethical_score > 0:
                scores.append(ethical_score)
            
            # Consistency score
            consistency_score = validation_results.get('consistency_validation', {}).get('consistency_score', 0.0)
            if consistency_score > 0:
                scores.append(consistency_score)
            
            if scores:
                return sum(scores) / len(scores)
            else:
                return 0.0
                
        except Exception as e:
            logger.error(f"Validation score calculation failed", error=str(e))
            return 0.0

    async def _calculate_agent_quality_metrics(self, 
                                             enhanced_response: Dict[str, Any],
                                             validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quality metrics for agent code generation"""
        try:
            quality_metrics = {
                'overall_quality_score': validation_results.get('overall_score', 0.0),
                'code_generation_score': enhanced_response.get('confidence_score', 0.0),
                'agent_insight_score': enhanced_response.get('agent_insights', {}).get('confidence', 0.0),
                'smarty_enhancement_score': 0.0,
                'compliance_scores': {
                    'security': validation_results.get('security_validation', {}).get('score', 0.0),
                    'quality': validation_results.get('quality_validation', {}).get('quality_score', 0.0),
                    'ethics': validation_results.get('ethical_validation', {}).get('ethics_score', 0.0),
                    'consistency': validation_results.get('consistency_validation', {}).get('consistency_score', 0.0)
                },
                'recommendations_count': len(enhanced_response.get('recommendations', [])),
                'code_length': len(enhanced_response.get('generated_code', '')),
                'complexity_indicators': self._analyze_code_complexity(enhanced_response.get('generated_code', ''))
            }
            
            # Calculate Smarty enhancement score
            smarty_enhancements = enhanced_response.get('smarty_enhancements', {})
            if smarty_enhancements:
                quality_metrics['smarty_enhancement_score'] = 0.8  # Base score for Smarty integration
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Quality metrics calculation failed", error=str(e))
            return {'overall_quality_score': 0.0}

    def _analyze_code_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity indicators"""
        try:
            if not code:
                return {'complexity_level': 'none', 'indicators': []}
            
            # Simple complexity analysis
            lines = len(code.split('\n'))
            functions = code.count('def ') + code.count('function ') + code.count('class ')
            imports = code.count('import ') + code.count('from ')
            
            complexity_level = 'low'
            if lines > 100 or functions > 10:
                complexity_level = 'high'
            elif lines > 50 or functions > 5:
                complexity_level = 'medium'
            
            return {
                'complexity_level': complexity_level,
                'lines_of_code': lines,
                'functions_count': functions,
                'imports_count': imports,
                'indicators': ['code_length', 'function_count'] if functions > 0 else ['code_length']
            }
            
        except Exception as e:
            logger.error(f"Code complexity analysis failed", error=str(e))
            return {'complexity_level': 'unknown', 'indicators': []}

    def _enhance_capabilities_with_smarty(self, 
                                        base_capabilities: List[AgentCapability],
                                        smarty_mode: AgentSmartyMode,
                                        code_capability: AgentCodeCapability) -> List[AgentCapability]:
        """Enhance agent capabilities with Smarty-specific capabilities"""
        try:
            enhanced_capabilities = base_capabilities.copy()
            
            # Add Smarty-specific capabilities
            smarty_capabilities = [
                AgentCapability.CODE_GENERATION,
                AgentCapability.CODE_REVIEW,
                AgentCapability.PROBLEM_SOLVING,
                AgentCapability.ANALYSIS,
                AgentCapability.OPTIMIZATION
            ]
            
            # Add mode-specific capabilities
            mode_capabilities = {
                AgentSmartyMode.CODE_GENERATION_ASSISTANT: [AgentCapability.CODE_GENERATION, AgentCapability.CREATIVITY],
                AgentSmartyMode.CODE_REVIEW_ASSISTANT: [AgentCapability.CODE_REVIEW, AgentCapability.ANALYSIS],
                AgentSmartyMode.DEBUGGING_ASSISTANT: [AgentCapability.DEBUGGING, AgentCapability.PROBLEM_SOLVING],
                AgentSmartyMode.TESTING_ASSISTANT: [AgentCapability.TESTING, AgentCapability.VALIDATION],
                AgentSmartyMode.DOCUMENTATION_ASSISTANT: [AgentCapability.DOCUMENTATION, AgentCapability.COMMUNICATION],
                AgentSmartyMode.ARCHITECTURE_ASSISTANT: [AgentCapability.ARCHITECTURE, AgentCapability.DESIGN],
                AgentSmartyMode.OPTIMIZATION_ASSISTANT: [AgentCapability.OPTIMIZATION, AgentCapability.PERFORMANCE],
                AgentSmartyMode.SECURITY_ASSISTANT: [AgentCapability.SECURITY, AgentCapability.VALIDATION]
            }
            
            # Add capabilities based on mode and capability level
            enhanced_capabilities.extend(smarty_capabilities)
            enhanced_capabilities.extend(mode_capabilities.get(smarty_mode, []))
            
            # Remove duplicates
            enhanced_capabilities = list(set(enhanced_capabilities))
            
            return enhanced_capabilities
            
        except Exception as e:
            logger.error(f"Capability enhancement failed", error=str(e))
            return base_capabilities

    async def _update_agent_metrics(self, agent_id: str, response: AgentCodeGenerationResponse):
        """Update agent metrics with interaction results"""
        try:
            if agent_id not in self.agent_metrics:
                return
            
            metrics = self.agent_metrics[agent_id]
            metrics.total_interactions += 1
            
            if response.confidence_score > 0.7:
                metrics.successful_interactions += 1
            
            # Update average response time
            current_avg = metrics.average_response_time
            total_interactions = metrics.total_interactions
            new_avg = ((current_avg * (total_interactions - 1)) + response.execution_time) / total_interactions
            metrics.average_response_time = new_avg
            
            # Update average confidence
            current_confidence = metrics.average_confidence
            new_confidence = ((current_confidence * (total_interactions - 1)) + response.confidence_score) / total_interactions
            metrics.average_confidence = new_confidence
            
            # Update performance score
            quality_score = response.quality_metrics.get('overall_quality_score', 0.0)
            security_score = response.security_assessment.get('score', 0.0)
            ethical_score = response.ethical_compliance.get('ethics_score', 0.0)
            
            performance_score = (quality_score * 0.4) + (security_score * 0.3) + (ethical_score * 0.3)
            metrics.performance_score = performance_score
            
            # Update integration metrics
            self.integration_metrics['total_agent_interactions'] += 1
            if response.confidence_score > 0.7:
                self.integration_metrics['successful_code_generations'] += 1
            else:
                self.integration_metrics['failed_code_generations'] += 1
            
            # Update averages
            total_interactions = self.integration_metrics['total_agent_interactions']
            if total_interactions > 0:
                # Update average quality score
                current_avg_quality = self.integration_metrics['average_quality_score']
                new_avg_quality = ((current_avg_quality * (total_interactions - 1)) + quality_score) / total_interactions
                self.integration_metrics['average_quality_score'] = new_avg_quality
                
                # Update average security score
                current_avg_security = self.integration_metrics['average_security_score']
                new_avg_security = ((current_avg_security * (total_interactions - 1)) + security_score) / total_interactions
                self.integration_metrics['average_security_score'] = new_avg_security
                
                # Update average ethical compliance
                current_avg_ethical = self.integration_metrics['average_ethical_compliance']
                new_avg_ethical = ((current_avg_ethical * (total_interactions - 1)) + ethical_score) / total_interactions
                self.integration_metrics['average_ethical_compliance'] = new_avg_ethical
                
                # Update average response time
                current_avg_time = self.integration_metrics['average_response_time']
                new_avg_time = ((current_avg_time * (total_interactions - 1)) + response.execution_time) / total_interactions
                self.integration_metrics['average_response_time'] = new_avg_time
            
        except Exception as e:
            logger.error(f"Metrics update failed for agent {agent_id}", error=str(e))

    async def _store_agent_interaction(self, 
                                     agent_id: str,
                                     request: AgentCodeGenerationRequest,
                                     response: AgentCodeGenerationResponse):
        """Store agent interaction for history and analysis"""
        try:
            interaction = AgentInteraction(
                interaction_id=uuid.uuid4(),
                agent_id=uuid.UUID(agent_id),
                user_id=uuid.UUID(request.user_id),
                message=request.prompt,
                response=response.generated_code,
                confidence=response.confidence_score,
                context=request.context,
                created_at=datetime.now()
            )
            
            if agent_id not in self.agent_interactions:
                self.agent_interactions[agent_id] = []
            
            self.agent_interactions[agent_id].append(interaction)
            
            # Keep only last 100 interactions per agent
            if len(self.agent_interactions[agent_id]) > 100:
                self.agent_interactions[agent_id] = self.agent_interactions[agent_id][-100:]
            
        except Exception as e:
            logger.error(f"Interaction storage failed for agent {agent_id}", error=str(e))

    async def get_agent_smarty_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get Smarty integration status for an agent"""
        try:
            agent_config = self.agent_configs.get(agent_id)
            if not agent_config:
                return None
            
            metrics = self.agent_metrics.get(agent_id)
            interactions = self.agent_interactions.get(agent_id, [])
            
            return {
                'agent_id': agent_id,
                'smarty_mode': agent_config.smarty_mode.value,
                'code_capability': agent_config.code_capability.value,
                'ethical_validation_level': agent_config.ethical_validation_level,
                'total_interactions': len(interactions),
                'metrics': {
                    'total_interactions': metrics.total_interactions if metrics else 0,
                    'successful_interactions': metrics.successful_interactions if metrics else 0,
                    'average_response_time': metrics.average_response_time if metrics else 0.0,
                    'average_confidence': metrics.average_confidence if metrics else 0.0,
                    'performance_score': metrics.performance_score if metrics else 0.0
                },
                'last_interaction': interactions[-1].created_at.isoformat() if interactions else None,
                'status': 'active'
            }
            
        except Exception as e:
            logger.error(f"Status retrieval failed for agent {agent_id}", error=str(e))
            return None

    async def get_integration_metrics(self) -> Dict[str, Any]:
        """Get overall integration metrics"""
        try:
            return {
                'integration_metrics': self.integration_metrics,
                'active_agents_count': len(self.agent_configs),
                'total_interactions_across_agents': sum(len(interactions) for interactions in self.agent_interactions.values())
            }
            
        except Exception as e:
            logger.error(f"Integration metrics retrieval failed", error=str(e))
            return {}

    async def update_agent_smarty_config(self, 
                                       agent_id: str,
                                       new_config: AgentSmartyConfig) -> bool:
        """Update Smarty configuration for an agent"""
        try:
            if agent_id not in self.agent_configs:
                return False
            
            self.agent_configs[agent_id] = new_config
            logger.info(f"Agent Smarty configuration updated", agent_id=agent_id)
            return True
            
        except Exception as e:
            logger.error(f"Agent configuration update failed", error=str(e))
            return False

    async def remove_smarty_agent(self, agent_id: str) -> bool:
        """Remove Smarty integration from an agent"""
        try:
            removed = False
            
            if agent_id in self.agent_configs:
                del self.agent_configs[agent_id]
                removed = True
            
            if agent_id in self.agent_interactions:
                del self.agent_interactions[agent_id]
            
            if agent_id in self.agent_metrics:
                del self.agent_metrics[agent_id]
            
            if removed:
                logger.info(f"Smarty integration removed from agent", agent_id=agent_id)
            
            return removed
            
        except Exception as e:
            logger.error(f"Agent removal failed", error=str(e))
            return False

# Global instance
smarty_agent_integration = SmartyAgentIntegration()
