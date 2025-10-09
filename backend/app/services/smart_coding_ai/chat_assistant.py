"""
Chat Assistant Integration Module
Handles AI assistant chat enhanced with Smart Coding AI

Dependencies: 3 (AIAssistantService, smart_coding_ai, ai_integration_types)
Production-grade: Complete implementation with comprehensive error handling
"""

import structlog
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from app.services.ai_integration_types import AIIntegrationContext, IntegratedAIResponse

logger = structlog.get_logger(__name__)


class ChatAssistantIntegration:
    """
    AI assistant chat integration enhanced with Smart Coding AI
    Detects code-related queries and provides enhanced responses
    """
    
    def __init__(
        self,
        smart_coding_ai: Any,
        ai_assistant: Optional[Any] = None
    ):
        """
        Initialize chat assistant integration
        
        Args:
            smart_coding_ai: Smart Coding AI service (required)
            ai_assistant: Optional AI assistant service
        """
        self.smart_coding_ai = smart_coding_ai
        self.ai_assistant = ai_assistant
        
        logger.info("Chat assistant integration initialized",
                   ai_assistant_available=ai_assistant is not None)
    
    async def chat(
        self, 
        message: str, 
        context: AIIntegrationContext
    ) -> IntegratedAIResponse:
        """
        Chat with AI assistant enhanced by Smart Coding AI
        
        Args:
            message: User message
            context: Integration context
            
        Returns:
            IntegratedAIResponse with enhanced chat response
            
        Raises:
            ValueError: If message or context is invalid
            Exception: For critical failures (after logging)
        """
        try:
            # Validate inputs
            if not message or not message.strip():
                raise ValueError("Message cannot be empty")
            
            if not context or not context.user_id:
                raise ValueError("Valid context with user_id is required")
            
            logger.info("Processing AI assistant chat", 
                       user_id=context.user_id,
                       message_length=len(message))
            
            # Step 1: Process with AI Assistant
            assistant_response = await self._get_assistant_response(message, context)
            
            # Step 2: Check if message is code-related
            is_code_related = await self._detect_code_intent(message)
            
            if is_code_related:
                # Step 3: Enhance with Smart Coding AI
                smart_coding_response = await self._get_smart_coding_response(
                    message, context
                )
                
                # Step 4: Combine responses
                enhanced_response = await self._combine_responses(
                    assistant_response, smart_coding_response
                )
                
                return IntegratedAIResponse(
                    response_id=str(uuid.uuid4()),
                    primary_response=enhanced_response,
                    supporting_responses={
                        "assistant_response": assistant_response,
                        "smart_coding_response": smart_coding_response
                    },
                    confidence=min(0.95, enhanced_response.get("confidence", 0.8)),
                    integration_metadata={
                        "code_related": True,
                        "assistant_used": True,
                        "smart_coding_enhanced": True
                    },
                    timestamp=datetime.now()
                )
            else:
                # Return standard assistant response
                return IntegratedAIResponse(
                    response_id=str(uuid.uuid4()),
                    primary_response=assistant_response,
                    supporting_responses={},
                    confidence=assistant_response.get("confidence", 0.8),
                    integration_metadata={
                        "code_related": False,
                        "assistant_used": True,
                        "smart_coding_enhanced": False
                    },
                    timestamp=datetime.now()
                )
                
        except ValueError as e:
            logger.error("Validation error in chat assistant", error=str(e))
            raise
        except Exception as e:
            logger.error("Failed to process AI assistant chat", 
                        error=str(e),
                        error_type=type(e).__name__,
                        user_id=context.user_id if context else "unknown")
            raise
    
    async def _get_assistant_response(
        self, 
        message: str, 
        context: AIIntegrationContext
    ) -> Dict[str, Any]:
        """
        Get response from AI assistant
        
        Args:
            message: User message
            context: Integration context
            
        Returns:
            Assistant response dict
        """
        try:
            if self.ai_assistant:
                logger.debug("Getting AI assistant response")
                response = await self.ai_assistant.process_message(
                    user_id=context.user_id,
                    message=message,
                    assistant_name="SmartCodingAssistant"
                )
                return response
            else:
                # Fallback: simple assistant response
                logger.debug("Using fallback assistant response")
                return {
                    "response": f"Hello! I'm SmartCodingAssistant. You said: {message}",
                    "confidence": 0.8,
                    "fallback": True
                }
                
        except Exception as e:
            logger.error("Failed to get assistant response", error=str(e))
            # Return fallback instead of failing
            return {
                "response": "I'm having trouble processing your message.",
                "confidence": 0.5,
                "error": str(e),
                "fallback": True
            }
    
    async def _detect_code_intent(self, message: str) -> bool:
        """
        Detect if message is code-related
        
        Args:
            message: User message
            
        Returns:
            bool: True if message appears to be code-related
        """
        try:
            if not message:
                return False
            
            message_lower = message.lower()
            
            # Code-related keywords
            code_keywords = [
                "code", "function", "class", "variable", "import", 
                "programming", "debug", "error", "syntax", "compile", 
                "run", "execute", "algorithm", "method", "loop",
                "array", "string", "integer", "boolean", "refactor",
                "optimize", "test", "bug", "fix", "implement"
            ]
            
            # Check for code keywords
            is_code_related = any(keyword in message_lower for keyword in code_keywords)
            
            logger.debug("Code intent detection", 
                        is_code_related=is_code_related,
                        message_length=len(message))
            
            return is_code_related
            
        except Exception as e:
            logger.error("Failed to detect code intent", error=str(e))
            # Default to True to be safe (better to enhance unnecessarily than miss)
            return True
    
    async def _get_smart_coding_response(
        self, 
        message: str, 
        context: AIIntegrationContext
    ) -> Dict[str, Any]:
        """
        Get enhanced response from Smart Coding AI
        
        Args:
            message: User message
            context: Integration context
            
        Returns:
            Smart Coding AI response dict
        """
        try:
            logger.debug("Getting Smart Coding AI enhancement",
                        project_id=context.project_id)
            
            response = await self.smart_coding_ai.chat_with_codebase(
                query=message,
                project_id=context.project_id or "general",
                context_type="assistant_chat"
            )
            
            return response
            
        except Exception as e:
            logger.error("Failed to get Smart Coding AI response", error=str(e))
            # Return empty enhancement rather than failing
            return {
                "answer": "",
                "confidence": 0.0,
                "error": str(e)
            }
    
    async def _combine_responses(
        self, 
        assistant_response: Dict[str, Any], 
        smart_coding_response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Combine assistant and Smart Coding AI responses
        
        Args:
            assistant_response: Response from AI assistant
            smart_coding_response: Response from Smart Coding AI
            
        Returns:
            Combined enhanced response dict
        """
        try:
            # Extract responses
            assistant_text = assistant_response.get("response", "")
            coding_answer = smart_coding_response.get("answer", "")
            
            # Combine confidences (weighted average)
            assistant_confidence = assistant_response.get("confidence", 0.8)
            coding_confidence = smart_coding_response.get("confidence", 0.8)
            combined_confidence = (assistant_confidence * 0.4) + (coding_confidence * 0.6)
            
            # Create combined response
            if coding_answer:
                combined_text = f"{assistant_text}\n\n**Smart Coding AI Enhancement:**\n{coding_answer}"
            else:
                combined_text = assistant_text
            
            combined = {
                "response": combined_text,
                "confidence": combined_confidence,
                "assistant_part": assistant_text,
                "coding_part": coding_answer,
                "code_snippets": smart_coding_response.get("code_snippets", []),
                "follow_up_questions": smart_coding_response.get("follow_up_questions", []),
                "sources": smart_coding_response.get("sources", []),
                "combined": True
            }
            
            logger.info("Responses combined",
                       has_coding_enhancement=bool(coding_answer),
                       combined_confidence=combined_confidence)
            
            return combined
            
        except Exception as e:
            logger.error("Failed to combine responses", error=str(e))
            # Return assistant response as fallback
            return assistant_response
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get chat assistant integration status
        
        Returns:
            Dict with status information
        """
        return {
            "ai_assistant_available": self.ai_assistant is not None,
            "smart_coding_ai_configured": self.smart_coding_ai is not None,
            "module": "chat_assistant",
            "version": "1.0.0"
        }

