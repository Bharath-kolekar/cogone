"""
Adaptive Threshold AI Agent Service - Dynamic 99% vs 95% threshold selection
based on application requirements, use case, and performance needs
"""

import asyncio
import json
import logging
import time
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, AsyncGenerator, Tuple
from uuid import UUID, uuid4
import aiohttp
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
import psutil
from functools import lru_cache
from contextlib import asynccontextmanager
import weakref
import gc

from app.core.database import get_database
from app.core.redis import get_redis_client
from app.models.ai_agent import (
    AgentDefinition, AgentConfig, AgentMemory, AgentMetrics,
    TaskDefinition, AgentInteraction, AgentWorkflow,
    AgentRequest, AgentResponse, AgentCreationRequest,
    AgentType, AgentStatus, AgentCapability, TaskStatus,
    TaskType, AgentPriority, ZeroCostConfig
)
from app.models.goal_integrity import GoalDefinition, GoalViolation
from app.services.goal_integrity_service import GoalIntegrityService
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AdaptiveThresholdSelector:
    """Adaptive threshold selector that chooses between 99% and 95% based on use case"""
    
    def __init__(self):
        self.threshold_configs = {
            "maximum": {
                "threshold_precision": 0.99,
                "threshold_accuracy": 0.99,
                "max_retries": 20,
                "validation_layers": 8,
                "processing_time": "300-500ms",
                "computational_cost": "High",
                "use_cases": ["financial", "healthcare", "legal", "critical", "enterprise"]
            },
            "optimized": {
                "threshold_precision": 0.95,
                "threshold_accuracy": 0.95,
                "max_retries": 10,
                "validation_layers": 4,
                "processing_time": "100-200ms",
                "computational_cost": "Medium",
                "use_cases": ["general", "customer_support", "content_generation", "development"]
            },
            "fast": {
                "threshold_precision": 0.90,
                "threshold_accuracy": 0.90,
                "max_retries": 5,
                "validation_layers": 2,
                "processing_time": "50-100ms",
                "computational_cost": "Low",
                "use_cases": ["testing", "prototyping", "high_volume", "real_time"]
            }
        }
        
        self.adaptive_metrics = {
            "total_requests": 0,
            "maximum_threshold_usage": 0,
            "optimized_threshold_usage": 0,
            "fast_threshold_usage": 0,
            "average_response_time": 0.0,
            "average_precision": 0.0,
            "cost_savings": 0.0
        }
    
    async def select_optimal_threshold(
        self, 
        request: AgentRequest,
        context: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """Select optimal threshold based on request characteristics and context"""
        try:
            # Analyze request characteristics
            request_analysis = await self._analyze_request_characteristics(request, context)
            
            # Determine optimal threshold
            optimal_threshold = await self._determine_optimal_threshold(request_analysis)
            
            # Get threshold configuration
            threshold_config = self.threshold_configs[optimal_threshold]
            
            # Update adaptive metrics
            await self._update_adaptive_metrics(optimal_threshold)
            
            return optimal_threshold, threshold_config
            
        except Exception as e:
            logger.error(f"Error selecting optimal threshold: {e}")
            # Default to optimized threshold
            return "optimized", self.threshold_configs["optimized"]
    
    async def _analyze_request_characteristics(
        self, 
        request: AgentRequest, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze request characteristics to determine optimal threshold"""
        try:
            characteristics = {
                "urgency": "normal",
                "complexity": "medium",
                "criticality": "medium",
                "user_type": "general",
                "application_type": "general",
                "performance_requirements": "balanced"
            }
            
            # Analyze message content
            message_lower = request.message.lower()
            
            # Check for critical keywords
            critical_keywords = [
                "urgent", "critical", "emergency", "important", "financial",
                "health", "legal", "security", "confidential", "sensitive"
            ]
            
            if any(keyword in message_lower for keyword in critical_keywords):
                characteristics["criticality"] = "high"
                characteristics["urgency"] = "high"
            
            # Check for complexity indicators
            complexity_indicators = [
                "analyze", "calculate", "process", "complex", "detailed",
                "comprehensive", "thorough", "precise", "accurate"
            ]
            
            if any(indicator in message_lower for indicator in complexity_indicators):
                characteristics["complexity"] = "high"
            
            # Check for performance requirements
            performance_keywords = [
                "fast", "quick", "immediate", "real-time", "instant",
                "urgent", "asap", "priority"
            ]
            
            if any(keyword in message_lower for keyword in performance_keywords):
                characteristics["performance_requirements"] = "speed"
            
            # Check context for user type and application type
            if context.get("user_type"):
                characteristics["user_type"] = context["user_type"]
            
            if context.get("application_type"):
                characteristics["application_type"] = context["application_type"]
            
            if context.get("criticality"):
                characteristics["criticality"] = context["criticality"]
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Error analyzing request characteristics: {e}")
            return {
                "urgency": "normal",
                "complexity": "medium",
                "criticality": "medium",
                "user_type": "general",
                "application_type": "general",
                "performance_requirements": "balanced"
            }
    
    async def _determine_optimal_threshold(
        self, 
        characteristics: Dict[str, Any]
    ) -> str:
        """Determine optimal threshold based on characteristics"""
        try:
            # High criticality or enterprise users -> Maximum threshold
            if (characteristics["criticality"] == "high" or 
                characteristics["user_type"] == "enterprise" or
                characteristics["application_type"] in ["financial", "healthcare", "legal"]):
                return "maximum"
            
            # High performance requirements or real-time -> Fast threshold
            if (characteristics["performance_requirements"] == "speed" or
                characteristics["urgency"] == "high" or
                characteristics["application_type"] in ["real_time", "high_volume"]):
                return "fast"
            
            # Default to optimized threshold
            return "optimized"
            
        except Exception as e:
            logger.error(f"Error determining optimal threshold: {e}")
            return "optimized"
    
    async def _update_adaptive_metrics(self, threshold_type: str):
        """Update adaptive metrics"""
        try:
            self.adaptive_metrics["total_requests"] += 1
            
            if threshold_type == "maximum":
                self.adaptive_metrics["maximum_threshold_usage"] += 1
            elif threshold_type == "optimized":
                self.adaptive_metrics["optimized_threshold_usage"] += 1
            elif threshold_type == "fast":
                self.adaptive_metrics["fast_threshold_usage"] += 1
            
        except Exception as e:
            logger.error(f"Failed to update adaptive metrics: {e}")


class AdaptiveThresholdValidator:
    """Adaptive threshold validator that adjusts validation based on selected threshold"""
    
    def __init__(self):
        self.validation_cache = {}
        self.adaptive_metrics = {
            "total_validations": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "average_validation_time": 0.0
        }
    
    async def adaptive_threshold_validate(
        self, 
        prompt: str, 
        response: str, 
        agent_type: AgentType,
        context: Dict[str, Any],
        threshold_config: Dict[str, Any]
    ) -> Tuple[bool, float, str]:
        """Adaptive threshold validation based on selected threshold configuration"""
        try:
            start_time = time.time()
            
            # Check validation cache
            cache_key = f"adaptive_threshold:{hashlib.md5(f'{prompt}:{response}'.encode()).hexdigest()}"
            if cache_key in self.validation_cache:
                return self.validation_cache[cache_key]
            
            # Perform adaptive validation
            validation_result = await self._perform_adaptive_validation(
                prompt, response, agent_type, context, threshold_config
            )
            
            # Cache result
            self.validation_cache[cache_key] = validation_result
            
            # Update metrics
            validation_time = time.time() - start_time
            await self._update_validation_metrics(validation_result, validation_time)
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error in adaptive threshold validation: {e}")
            return False, 0.0, f"Adaptive threshold validation error: {str(e)}"
    
    async def _perform_adaptive_validation(
        self, 
        prompt: str, 
        response: str, 
        agent_type: AgentType,
        context: Dict[str, Any],
        threshold_config: Dict[str, Any]
    ) -> Tuple[bool, float, str]:
        """Perform adaptive validation based on threshold configuration"""
        try:
            threshold_precision = threshold_config["threshold_precision"]
            threshold_accuracy = threshold_config["threshold_accuracy"]
            validation_layers = threshold_config["validation_layers"]
            
            # Perform validation based on number of layers
            validation_tasks = []
            
            # Basic validation (always performed)
            validation_tasks.append(self._basic_validation(prompt, response))
            
            # Additional validation layers based on configuration
            if validation_layers >= 2:
                validation_tasks.append(self._consistency_validation(prompt, response))
            
            if validation_layers >= 4:
                validation_tasks.append(self._accuracy_validation(response))
                validation_tasks.append(self._reliability_validation(response))
            
            if validation_layers >= 6:
                validation_tasks.append(self._precision_validation(response))
                validation_tasks.append(self._quality_validation(response))
            
            if validation_layers >= 8:
                validation_tasks.append(self._security_validation(response))
                validation_tasks.append(self._comprehensive_validation(prompt, response))
            
            # Execute validation tasks
            results = await asyncio.gather(*validation_tasks, return_exceptions=True)
            
            # Calculate overall score
            valid_results = [r for r in results if not isinstance(r, Exception)]
            if not valid_results:
                return False, 0.0, "No valid validation results"
            
            overall_score = sum(valid_results) / len(valid_results)
            
            # Check against thresholds
            is_valid = overall_score >= threshold_precision
            accuracy_score = min(overall_score * 1.05, 1.0)  # Slight boost for accuracy
            
            validation_message = f"Adaptive Threshold: {overall_score:.4f}, Precision: {threshold_precision:.4f}, Accuracy: {accuracy_score:.4f}, Layers: {validation_layers}"
            
            return is_valid, accuracy_score, validation_message
            
        except Exception as e:
            logger.error(f"Error performing adaptive validation: {e}")
            return False, 0.0, f"Adaptive validation error: {str(e)}"
    
    async def _basic_validation(self, prompt: str, response: str) -> float:
        """Basic validation"""
        try:
            # Simple length and content validation
            if len(response) < 10:
                return 0.5
            
            if len(response) > 1000:
                return 0.8
            
            return 1.0
            
        except Exception as e:
            logger.error(f"Error in basic validation: {e}")
            return 0.0
    
    async def _consistency_validation(self, prompt: str, response: str) -> float:
        """Consistency validation"""
        try:
            # Check for consistency between prompt and response
            prompt_words = set(prompt.lower().split())
            response_words = set(response.lower().split())
            
            if not prompt_words or not response_words:
                return 1.0
            
            overlap = len(prompt_words.intersection(response_words))
            total_words = len(prompt_words.union(response_words))
            
            return overlap / total_words if total_words > 0 else 1.0
            
        except Exception as e:
            logger.error(f"Error in consistency validation: {e}")
            return 0.0
    
    async def _accuracy_validation(self, response: str) -> float:
        """Accuracy validation"""
        try:
            # Check for accuracy indicators
            accuracy_indicators = [
                "accurate", "correct", "right", "true", "valid", "verified",
                "confirmed", "precise", "exact", "specific"
            ]
            
            accuracy_count = sum(1 for indicator in accuracy_indicators if indicator in response.lower())
            return min(accuracy_count / 5, 1.0)
            
        except Exception as e:
            logger.error(f"Error in accuracy validation: {e}")
            return 0.0
    
    async def _reliability_validation(self, response: str) -> float:
        """Reliability validation"""
        try:
            # Check for reliability indicators
            reliability_indicators = [
                "reliable", "dependable", "trustworthy", "stable", "consistent",
                "predictable", "secure", "robust", "resilient"
            ]
            
            reliability_count = sum(1 for indicator in reliability_indicators if indicator in response.lower())
            return min(reliability_count / 5, 1.0)
            
        except Exception as e:
            logger.error(f"Error in reliability validation: {e}")
            return 0.0
    
    async def _precision_validation(self, response: str) -> float:
        """Precision validation"""
        try:
            # Check for precision indicators
            precision_indicators = [
                "exactly", "precisely", "specifically", "accurately", "exact",
                "precise", "specific", "accurate", "detailed"
            ]
            
            precision_count = sum(1 for indicator in precision_indicators if indicator in response.lower())
            return min(precision_count / 5, 1.0)
            
        except Exception as e:
            logger.error(f"Error in precision validation: {e}")
            return 0.0
    
    async def _quality_validation(self, response: str) -> float:
        """Quality validation"""
        try:
            # Check for quality indicators
            quality_indicators = [
                "high-quality", "excellent", "superior", "premium", "top-tier",
                "outstanding", "exceptional", "remarkable", "impressive"
            ]
            
            quality_count = sum(1 for indicator in quality_indicators if indicator in response.lower())
            return min(quality_count / 5, 1.0)
            
        except Exception as e:
            logger.error(f"Error in quality validation: {e}")
            return 0.0
    
    async def _security_validation(self, response: str) -> float:
        """Security validation"""
        try:
            # Check for security indicators
            security_indicators = [
                "secure", "safe", "protected", "encrypted", "authenticated",
                "verified", "validated", "trusted", "reliable", "confidential"
            ]
            
            security_count = sum(1 for indicator in security_indicators if indicator in response.lower())
            return min(security_count / 5, 1.0)
            
        except Exception as e:
            logger.error(f"Error in security validation: {e}")
            return 0.0
    
    async def _comprehensive_validation(self, prompt: str, response: str) -> float:
        """Comprehensive validation"""
        try:
            # Combine multiple validation aspects
            basic_score = await self._basic_validation(prompt, response)
            consistency_score = await self._consistency_validation(prompt, response)
            accuracy_score = await self._accuracy_validation(response)
            
            return (basic_score + consistency_score + accuracy_score) / 3
            
        except Exception as e:
            logger.error(f"Error in comprehensive validation: {e}")
            return 0.0
    
    async def _update_validation_metrics(self, validation_result: Tuple[bool, float, str], validation_time: float):
        """Update validation metrics"""
        try:
            is_valid, score, _ = validation_result
            
            self.adaptive_metrics["total_validations"] += 1
            
            if is_valid:
                self.adaptive_metrics["successful_validations"] += 1
            else:
                self.adaptive_metrics["failed_validations"] += 1
            
            self.adaptive_metrics["average_validation_time"] = (
                self.adaptive_metrics["average_validation_time"] * 0.9 + validation_time * 0.1
            )
            
        except Exception as e:
            logger.error(f"Failed to update validation metrics: {e}")


class AdaptiveThresholdAIAgentService:
    """Adaptive Threshold AI Agent Service with dynamic 99% vs 95% threshold selection"""
    
    def __init__(self):
        self.threshold_selector = AdaptiveThresholdSelector()
        self.threshold_validator = AdaptiveThresholdValidator()
        self.redis_client: Optional[redis.Redis] = None
        self.adaptive_metrics = {
            "total_requests": 0,
            "maximum_threshold_usage": 0,
            "optimized_threshold_usage": 0,
            "fast_threshold_usage": 0,
            "average_response_time": 0.0,
            "average_precision": 0.0,
            "cost_savings": 0.0
        }
        
    async def initialize(self):
        """Initialize the adaptive threshold AI Agent service"""
        try:
            self.redis_client = await get_redis_client()
            
            logger.info("Adaptive Threshold AI Agent Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Adaptive Threshold AI Agent Service: {e}")
            raise
    
    async def adaptive_threshold_interact_with_agent(
        self, 
        request: AgentRequest
    ) -> AgentResponse:
        """Adaptive threshold agent interaction with dynamic threshold selection"""
        start_time = time.time()
        self.adaptive_metrics["total_requests"] += 1
        
        try:
            # Select optimal threshold
            threshold_type, threshold_config = await self.threshold_selector.select_optimal_threshold(
                request, request.context
            )
            
            # Perform adaptive validation
            is_valid, threshold_precision, threshold_message = await self.threshold_validator.adaptive_threshold_validate(
                request.message, "response_placeholder", AgentType.GENERAL, request.context, threshold_config
            )
            
            if not is_valid:
                return AgentResponse(
                    success=False,
                    message="This interaction failed adaptive threshold validation. Please try again.",
                    agent_id=request.agent_id,
                    interaction_id=uuid4(),
                    error_code="ADAPTIVE_THRESHOLD_VALIDATION_FAILURE",
                    metadata={
                        "threshold_type": threshold_type,
                        "threshold_precision": threshold_precision,
                        "threshold_message": threshold_message,
                        "threshold_config": threshold_config
                    }
                )
            
            # Generate adaptive response
            response_text = await self._generate_adaptive_response(
                request.message, request.context, threshold_config
            )
            
            # Final adaptive validation
            final_valid, final_threshold_precision, final_threshold_message = await self.threshold_validator.adaptive_threshold_validate(
                request.message, response_text, AgentType.GENERAL, request.context, threshold_config
            )
            
            if not final_valid:
                # Generate conservative response
                response_text = await self._generate_conservative_response(request.message, threshold_type)
                final_threshold_precision = threshold_config["threshold_precision"]
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Update adaptive metrics
            await self._update_adaptive_metrics(threshold_type, response_time, final_threshold_precision)
            
            return AgentResponse(
                success=True,
                message=response_text,
                agent_id=request.agent_id,
                interaction_id=uuid4(),
                response_time=response_time,
                tokens_used=len(response_text.split()),
                cost=0.0,
                suggestions=self._generate_adaptive_suggestions(request.message, threshold_type),
                follow_up_questions=self._generate_adaptive_follow_up_questions(request.message),
                metadata={
                    "threshold_type": threshold_type,
                    "threshold_precision": final_threshold_precision,
                    "threshold_message": final_threshold_message,
                    "threshold_config": threshold_config,
                    "adaptive_threshold": True
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to interact with adaptive threshold agent: {e}")
            return AgentResponse(
                success=False,
                message="An error occurred while processing your request",
                agent_id=request.agent_id,
                interaction_id=uuid4(),
                error_code="ADAPTIVE_THRESHOLD_INTERACTION_ERROR",
                error_message=str(e)
            )
    
    async def _generate_adaptive_response(
        self, 
        message: str, 
        context: Dict[str, Any],
        threshold_config: Dict[str, Any]
    ) -> str:
        """Generate adaptive response based on threshold configuration"""
        try:
            # Simulate adaptive processing based on threshold configuration
            processing_time = threshold_config.get("processing_time", "100-200ms")
            
            if "300-500ms" in processing_time:
                await asyncio.sleep(0.3)  # Maximum threshold processing
            elif "100-200ms" in processing_time:
                await asyncio.sleep(0.1)  # Optimized threshold processing
            else:
                await asyncio.sleep(0.05)  # Fast threshold processing
            
            if "hello" in message.lower():
                return f"Hello! I'm your adaptive threshold AI assistant. How can I help you today with {threshold_config['threshold_precision']*100:.0f}% precision?"
            elif "help" in message.lower():
                return f"I'm here to assist you with various tasks with {threshold_config['threshold_precision']*100:.0f}% precision and {threshold_config['threshold_accuracy']*100:.0f}% accuracy. What specific help do you need?"
            else:
                return f"I understand you need assistance. Let me help you with that using adaptive threshold precision and accuracy."
                
        except Exception as e:
            logger.error(f"Error generating adaptive response: {e}")
            return "I'm here to help with adaptive threshold precision and accuracy. How can I assist you today?"
    
    async def _generate_conservative_response(self, message: str, threshold_type: str) -> str:
        """Generate conservative response based on threshold type"""
        try:
            conservative_responses = {
                "maximum": "I'm here to help with maximum threshold precision and accuracy.",
                "optimized": "I'm here to help with optimized threshold precision and accuracy.",
                "fast": "I'm here to help with fast threshold precision and accuracy."
            }
            
            return conservative_responses.get(threshold_type, "I'm here to help with adaptive threshold precision and accuracy.")
                
        except Exception as e:
            logger.error(f"Error generating conservative response: {e}")
            return "I'm here to help with adaptive threshold precision and accuracy. How can I assist you today?"
    
    async def _update_adaptive_metrics(self, threshold_type: str, response_time: float, threshold_precision: float):
        """Update adaptive metrics"""
        try:
            if threshold_type == "maximum":
                self.adaptive_metrics["maximum_threshold_usage"] += 1
            elif threshold_type == "optimized":
                self.adaptive_metrics["optimized_threshold_usage"] += 1
            elif threshold_type == "fast":
                self.adaptive_metrics["fast_threshold_usage"] += 1
            
            self.adaptive_metrics["average_response_time"] = (
                self.adaptive_metrics["average_response_time"] * 0.9 + response_time * 0.1
            )
            
            self.adaptive_metrics["average_precision"] = (
                self.adaptive_metrics["average_precision"] * 0.9 + threshold_precision * 0.1
            )
            
        except Exception as e:
            logger.error(f"Failed to update adaptive metrics: {e}")
    
    def _generate_adaptive_suggestions(self, message: str, threshold_type: str) -> List[str]:
        """Generate adaptive suggestions based on threshold type"""
        suggestions = []
        
        if threshold_type == "maximum":
            suggestions.extend([
                "Would you like maximum precision assistance?",
                "Should I provide maximum accuracy solutions?"
            ])
        elif threshold_type == "optimized":
            suggestions.extend([
                "Would you like optimized precision assistance?",
                "Should I provide balanced precision solutions?"
            ])
        elif threshold_type == "fast":
            suggestions.extend([
                "Would you like fast precision assistance?",
                "Should I provide quick precision solutions?"
            ])
        
        return suggestions[:3]
    
    def _generate_adaptive_follow_up_questions(self, message: str) -> List[str]:
        """Generate adaptive follow-up questions"""
        questions = []
        message_lower = message.lower()
        
        if "help" in message_lower:
            questions.extend([
                "What specific task would you like adaptive threshold help with?",
                "Are you looking for precision or speed optimization?"
            ])
        
        return questions[:2]
    
    async def get_adaptive_threshold_status(self) -> Dict[str, Any]:
        """Get adaptive threshold status"""
        return {
            "adaptive_threshold_active": True,
            "threshold_types": ["maximum", "optimized", "fast"],
            "adaptive_metrics": self.adaptive_metrics,
            "threshold_selector": "active",
            "threshold_validator": "active"
        }


# Global adaptive threshold service instance
adaptive_threshold_ai_agent_service = AdaptiveThresholdAIAgentService()
