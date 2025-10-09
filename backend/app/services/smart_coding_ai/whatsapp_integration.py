"""
WhatsApp Integration Module
Handles WhatsApp messaging for Smart Coding AI

Dependencies: 2 (WhatsAppService, structlog)
Production-grade: Complete implementation with comprehensive error handling
"""

import structlog
from typing import Dict, Any, Optional

logger = structlog.get_logger(__name__)


class WhatsAppIntegration:
    """
    WhatsApp integration for Smart Coding AI
    Handles message processing and response formatting
    """
    
    def __init__(self, whatsapp_service: Optional[Any] = None):
        """
        Initialize WhatsApp integration
        
        Args:
            whatsapp_service: Optional WhatsAppService instance
        """
        self.whatsapp_service = whatsapp_service
        logger.info("WhatsApp integration initialized", 
                   service_available=whatsapp_service is not None)
    
    def set_whatsapp_service(self, whatsapp_service: Any) -> None:
        """
        Set or update the WhatsApp service instance
        
        Args:
            whatsapp_service: WhatsAppService instance
        """
        self.whatsapp_service = whatsapp_service
        logger.info("WhatsApp service updated")
    
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process WhatsApp message with Smart Coding AI integration
        
        Args:
            message_data: WhatsApp message data including type and content
            
        Returns:
            Dict with processing result or error
            
        Raises:
            No exceptions raised - all errors returned in dict
        """
        try:
            # Validate WhatsApp service availability
            if not self.whatsapp_service:
                logger.warning("WhatsApp message received but service not available")
                return {
                    "success": False,
                    "error": "WhatsApp service not available"
                }
            
            # Validate message data
            if not message_data:
                logger.error("Empty message data received")
                return {
                    "success": False,
                    "error": "Invalid message data"
                }
            
            message_type = message_data.get("type", "text")
            logger.info("Processing WhatsApp message", 
                       message_type=message_type,
                       from_number=message_data.get("from", "unknown"))
            
            # Route based on message type
            if message_type == "voice":
                result = await self.whatsapp_service.process_voice_message(message_data)
            elif message_type == "text":
                result = await self.whatsapp_service.process_text_message(message_data)
            else:
                logger.warning("Unsupported message type", message_type=message_type)
                return {
                    "success": False,
                    "error": f"Unsupported message type: {message_type}"
                }
            
            logger.info("WhatsApp message processed successfully", 
                       message_type=message_type,
                       success=result.get("success", False))
            return result
                
        except Exception as e:
            logger.error("Failed to process WhatsApp message", 
                        error=str(e),
                        error_type=type(e).__name__)
            return {
                "success": False,
                "error": f"Failed to process WhatsApp message: {str(e)}"
            }
    
    async def send_code_response(
        self, 
        to: str, 
        generated_code: str, 
        confidence: float,
        code_type: str = "python"
    ) -> Dict[str, Any]:
        """
        Send generated code as WhatsApp message
        
        Args:
            to: Recipient phone number
            generated_code: Generated code to send
            confidence: AI confidence score (0.0 to 1.0)
            code_type: Programming language for syntax highlighting
            
        Returns:
            Dict with send result and metadata
            
        Raises:
            No exceptions raised - all errors returned in dict
        """
        try:
            # Validate WhatsApp service
            if not self.whatsapp_service:
                logger.warning("Attempted to send code but WhatsApp service not available")
                return {
                    "success": False,
                    "error": "WhatsApp service not available"
                }
            
            # Validate inputs
            if not to:
                logger.error("Cannot send WhatsApp message: missing recipient")
                return {
                    "success": False,
                    "error": "Recipient phone number is required"
                }
            
            if not generated_code:
                logger.warning("Attempted to send empty code", to=to)
                return {
                    "success": False,
                    "error": "Cannot send empty code"
                }
            
            # Validate confidence score
            if not (0.0 <= confidence <= 1.0):
                logger.warning("Invalid confidence score", 
                             confidence=confidence,
                             to=to)
                confidence = max(0.0, min(1.0, confidence))  # Clamp to valid range
            
            # Format code message with markdown
            message = (
                f"🤖 *Code Generated* (Confidence: {confidence:.1%})\n\n"
                f"```{code_type}\n{generated_code}\n```"
            )
            
            logger.info("Sending code response via WhatsApp",
                       to=to,
                       code_length=len(generated_code),
                       confidence=confidence,
                       code_type=code_type)
            
            # Send via WhatsApp
            response = await self.whatsapp_service.send_message(to, message)
            
            logger.info("Code response sent successfully", 
                       to=to,
                       message_id=response.get("id"))
            
            return {
                "success": True,
                "whatsapp_response": response,
                "message_sent": True,
                "message_id": response.get("id"),
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error("Failed to send WhatsApp code response",
                        error=str(e),
                        error_type=type(e).__name__,
                        to=to)
            return {
                "success": False,
                "error": f"Failed to send WhatsApp code response: {str(e)}"
            }
    
    async def send_chat_response(
        self, 
        to: str, 
        ai_response: str, 
        confidence: float
    ) -> Dict[str, Any]:
        """
        Send AI chat response as WhatsApp message
        
        Args:
            to: Recipient phone number
            ai_response: AI-generated response text
            confidence: AI confidence score (0.0 to 1.0)
            
        Returns:
            Dict with send result and metadata
            
        Raises:
            No exceptions raised - all errors returned in dict
        """
        try:
            # Validate WhatsApp service
            if not self.whatsapp_service:
                logger.warning("Attempted to send chat but WhatsApp service not available")
                return {
                    "success": False,
                    "error": "WhatsApp service not available"
                }
            
            # Validate inputs
            if not to:
                logger.error("Cannot send WhatsApp message: missing recipient")
                return {
                    "success": False,
                    "error": "Recipient phone number is required"
                }
            
            if not ai_response:
                logger.warning("Attempted to send empty response", to=to)
                return {
                    "success": False,
                    "error": "Cannot send empty response"
                }
            
            # Validate confidence score
            if not (0.0 <= confidence <= 1.0):
                logger.warning("Invalid confidence score", 
                             confidence=confidence,
                             to=to)
                confidence = max(0.0, min(1.0, confidence))  # Clamp to valid range
            
            # Format chat message
            message = (
                f"🤖 *Smart Coding AI Response* (Confidence: {confidence:.1%})\n\n"
                f"{ai_response}"
            )
            
            logger.info("Sending chat response via WhatsApp",
                       to=to,
                       response_length=len(ai_response),
                       confidence=confidence)
            
            # Send via WhatsApp
            response = await self.whatsapp_service.send_message(to, message)
            
            logger.info("Chat response sent successfully", 
                       to=to,
                       message_id=response.get("id"))
            
            return {
                "success": True,
                "whatsapp_response": response,
                "message_sent": True,
                "message_id": response.get("id"),
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error("Failed to send WhatsApp chat response",
                        error=str(e),
                        error_type=type(e).__name__,
                        to=to)
            return {
                "success": False,
                "error": f"Failed to send WhatsApp chat response: {str(e)}"
            }
    
    def is_available(self) -> bool:
        """
        Check if WhatsApp service is available
        
        Returns:
            bool: True if service is configured and available
        """
        return self.whatsapp_service is not None
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get WhatsApp integration status
        
        Returns:
            Dict with status information
        """
        return {
            "available": self.is_available(),
            "service_configured": self.whatsapp_service is not None,
            "module": "whatsapp_integration",
            "version": "1.0.0"
        }

