"""
WhatsApp service for free messaging using WhatsApp Business API
Integrated with Smart Coding AI for voice-to-code and chat functionality
"""

import structlog
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
import aiohttp
import json
import base64
from app.core.config import settings

logger = structlog.get_logger()


class WhatsAppService:
    """WhatsApp service for free messaging"""
    
    def __init__(self):
        self.webhook_url = settings.WHATSAPP_WEBHOOK_URL
        self.verify_token = settings.WHATSAPP_VERIFY_TOKEN
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.business_account_id = settings.WHATSAPP_BUSINESS_ACCOUNT_ID
        self.base_url = "https://graph.facebook.com/v18.0"
        self.webhook_secret = settings.WHATSAPP_WEBHOOK_SECRET
        
        # Smart Coding AI Integration
        self.smart_coding_ai = None
        self.integration_enabled = False
    
    def enable_smart_coding_integration(self, smart_coding_ai_service):
        """Enable Smart Coding AI integration"""
        self.smart_coding_ai = smart_coding_ai_service
        self.integration_enabled = True
        logger.info("WhatsApp Smart Coding AI integration enabled")
    
    async def process_voice_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process voice message for code generation"""
        try:
            if not self.integration_enabled or not self.smart_coding_ai:
                return {"error": "Smart Coding AI integration not enabled"}
            
            # Extract voice data from WhatsApp message
            voice_data = message_data.get("voice", {})
            if not voice_data:
                return {"error": "No voice data found"}
            
            # Get voice media URL
            media_id = voice_data.get("id")
            if not media_id:
                return {"error": "No voice media ID found"}
            
            # Download voice file
            voice_file = await self._download_media(media_id)
            if not voice_file:
                return {"error": "Failed to download voice file"}
            
            # Get user info
            from_number = message_data.get("from", "")
            user_id = f"whatsapp_{from_number}"
            
            # Process with Smart Coding AI
            from app.services.smart_coding_ai_integration import AIIntegrationContext
            context = AIIntegrationContext(
                user_id=user_id,
                project_id=f"whatsapp_project_{from_number}",
                operation_type="voice_to_code"
            )
            
            # Use Smart Coding AI integration
            response = await self.smart_coding_ai.process_voice_to_code(
                audio_file=voice_file,
                language="en",
                context=context
            )
            
            # Format response for WhatsApp
            generated_code = response.primary_response.get("generated_code", "")
            confidence = response.confidence
            
            if generated_code:
                message = f"🤖 *Code Generated* (Confidence: {confidence:.1%})\n\n```python\n{generated_code}\n```"
            else:
                message = f"🤖 I couldn't generate code from your voice message. Confidence: {confidence:.1%}"
            
            return {
                "success": True,
                "message": message,
                "generated_code": generated_code,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error("Failed to process voice message", error=str(e))
            return {"error": f"Failed to process voice message: {str(e)}"}
    
    async def process_text_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process text message for Smart Coding AI chat"""
        try:
            if not self.integration_enabled or not self.smart_coding_ai:
                return {"error": "Smart Coding AI integration not enabled"}
            
            # Extract text from WhatsApp message
            text = message_data.get("text", {}).get("body", "")
            if not text:
                return {"error": "No text found in message"}
            
            # Get user info
            from_number = message_data.get("from", "")
            user_id = f"whatsapp_{from_number}"
            
            # Check if it's a code-related query
            code_keywords = ["code", "function", "class", "variable", "import", "programming", "debug", "error"]
            is_code_related = any(keyword in text.lower() for keyword in code_keywords)
            
            if is_code_related:
                # Process with Smart Coding AI
                from app.services.smart_coding_ai_integration import AIIntegrationContext
                context = AIIntegrationContext(
                    user_id=user_id,
                    project_id=f"whatsapp_project_{from_number}",
                    operation_type="ai_assistant_chat"
                )
                
                # Use Smart Coding AI integration
                response = await self.smart_coding_ai.chat_with_ai_assistant(
                    message=text,
                    context=context
                )
                
                # Format response for WhatsApp
                ai_response = response.primary_response.get("combined_response", response.primary_response)
                confidence = response.confidence
                
                message = f"🤖 *Smart Coding AI Response* (Confidence: {confidence:.1%})\n\n{ai_response}"
                
                # Add code snippets if available
                code_snippets = response.primary_response.get("code_snippets", [])
                if code_snippets:
                    for snippet in code_snippets[:2]:  # Limit to 2 snippets
                        message += f"\n\n```python\n{snippet.get('content', '')}\n```"
                
                return {
                    "success": True,
                    "message": message,
                    "confidence": confidence,
                    "code_related": True
                }
            else:
                # Regular WhatsApp response
                return {
                    "success": True,
                    "message": f"👋 Hello! I received your message: {text}\n\nFor code-related questions, use keywords like 'code', 'function', 'debug', etc.",
                    "confidence": 1.0,
                    "code_related": False
                }
            
        except Exception as e:
            logger.error("Failed to process text message", error=str(e))
            return {"error": f"Failed to process text message: {str(e)}"}
    
    async def _download_media(self, media_id: str) -> Optional[bytes]:
        """Download media from WhatsApp API"""
        try:
            url = f"{self.base_url}/{media_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        media_url = data.get("url")
                        
                        if media_url:
                            async with session.get(media_url, headers=headers) as media_response:
                                if media_response.status == 200:
                                    return await media_response.read()
            
            return None
            
        except Exception as e:
            logger.error("Failed to download media", error=str(e))
            return None
    
    async def send_message(self, to: str, message: str, message_type: str = "text") -> Dict[str, Any]:
        """Send WhatsApp message"""
        try:
            if not self.access_token or not self.phone_number_id:
                raise ValueError("WhatsApp not configured properly")
            
            url = f"{self.base_url}/{self.phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": message_type,
                "text": {
                    "body": message
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info("WhatsApp message sent successfully", to=to, message_id=result.get("messages", [{}])[0].get("id"))
                        return result
                    else:
                        error_text = await response.text()
                        logger.error("Failed to send WhatsApp message", status=response.status, error=error_text)
                        raise Exception(f"Failed to send message: {error_text}")
            
        except Exception as e:
            logger.error("WhatsApp message sending failed", error=str(e))
            raise e
    
    async def send_template_message(self, to: str, template_name: str, language_code: str = "en", parameters: List[str] = None) -> Dict[str, Any]:
        """Send WhatsApp template message"""
        try:
            if not self.access_token or not self.phone_number_id:
                raise ValueError("WhatsApp not configured properly")
            
            url = f"{self.base_url}/{self.phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    },
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": param} for param in (parameters or [])
                            ]
                        }
                    ]
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info("WhatsApp template message sent", to=to, template=template_name)
                        return result
                    else:
                        error_text = await response.text()
                        logger.error("Failed to send WhatsApp template", status=response.status, error=error_text)
                        raise Exception(f"Failed to send template: {error_text}")
            
        except Exception as e:
            logger.error("WhatsApp template sending failed", error=str(e))
            raise e
    
    async def send_usage_alert(self, phone_number: str, service_name: str, usage_percentage: float, alert_level: str) -> Dict[str, Any]:
        """Send usage alert via WhatsApp"""
        try:
            emoji = "🚨" if alert_level == "critical" else "⚠️"
            message = f"{emoji} {alert_level.upper()} ALERT\n\n"
            message += f"Service: {service_name}\n"
            message += f"Usage: {usage_percentage:.1f}% of free tier limit\n\n"
            message += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            message += "Please check your admin dashboard for details."
            
            return await self.send_message(phone_number, message)
            
        except Exception as e:
            logger.error("Failed to send usage alert via WhatsApp", error=str(e))
            raise e
    
    async def send_otp(self, phone_number: str, otp_code: str) -> Dict[str, Any]:
        """Send OTP via WhatsApp"""
        try:
            message = f"🔐 Your OTP for Cognomega AI is: {otp_code}\n\n"
            message += "This code will expire in 10 minutes.\n\n"
            message += "If you didn't request this code, please ignore this message."
            
            return await self.send_message(phone_number, message)
            
        except Exception as e:
            logger.error("Failed to send OTP via WhatsApp", error=str(e))
            raise e
    
    async def send_welcome_message(self, phone_number: str, user_name: str = None) -> Dict[str, Any]:
        """Send welcome message via WhatsApp"""
        try:
            name = user_name or "User"
            message = f"🎉 Welcome to Cognomega AI, {name}!\n\n"
            message += "I'm Vihaan, your AI assistant. You can:\n"
            message += "• Ask me questions\n"
            message += "• Get help with tasks\n"
            message += "• Use voice commands\n\n"
            message += "Just say 'Hey Vihaan' to get started!\n\n"
            message += "How can I help you today?"
            
            return await self.send_message(phone_number, message)
            
        except Exception as e:
            logger.error("Failed to send welcome message via WhatsApp", error=str(e))
            raise e
    
    async def verify_webhook(self, mode: str, token: str, challenge: str) -> str:
        """Verify WhatsApp webhook"""
        try:
            if mode == "subscribe" and token == self.verify_token:
                logger.info("WhatsApp webhook verified successfully")
                return challenge
            else:
                logger.warning("WhatsApp webhook verification failed", mode=mode, token=token)
                raise ValueError("Webhook verification failed")
                
        except Exception as e:
            logger.error("WhatsApp webhook verification error", error=str(e))
            raise e
    
    async def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming WhatsApp webhook"""
        try:
            if "entry" not in webhook_data:
                return {"status": "ignored", "reason": "No entry data"}
            
            for entry in webhook_data["entry"]:
                if "changes" not in entry:
                    continue
                
                for change in entry["changes"]:
                    if change["field"] == "messages":
                        await self._process_messages(change["value"])
            
            return {"status": "processed"}
            
        except Exception as e:
            logger.error("Failed to process WhatsApp webhook", error=str(e))
            return {"status": "error", "error": str(e)}
    
    async def _process_messages(self, messages_data: Dict[str, Any]):
        """Process incoming messages"""
        try:
            if "messages" not in messages_data:
                return
            
            for message in messages_data["messages"]:
                sender = message["from"]
                message_id = message["id"]
                timestamp = message["timestamp"]
                
                if "text" in message:
                    text_content = message["text"]["body"]
                    logger.info("Received WhatsApp text message", sender=sender, content=text_content)
                    
                    # Process the message (could trigger AI response, etc.)
                    await self._handle_text_message(sender, text_content, message_id)
                
                elif "button" in message:
                    button_text = message["button"]["text"]
                    logger.info("Received WhatsApp button response", sender=sender, button=button_text)
                    
                    # Process button response
                    await self._handle_button_response(sender, button_text, message_id)
            
        except Exception as e:
            logger.error("Failed to process messages", error=str(e))
    
    async def _handle_text_message(self, sender: str, content: str, message_id: str):
        """Handle incoming text message"""
        try:
            # Check for wake word
            if "hey vihaan" in content.lower() or "hey vihaan" in content.lower():
                response = "Hello! I'm Vihaan, your AI assistant. How can I help you today?"
                await self.send_message(sender, response)
            
            # Process other messages
            else:
                # This could integrate with AI assistant service
                response = f"Thanks for your message: '{content}'. I'm here to help!"
                await self.send_message(sender, response)
            
        except Exception as e:
            logger.error("Failed to handle text message", error=str(e))
    
    async def _handle_button_response(self, sender: str, button_text: str, message_id: str):
        """Handle button response"""
        try:
            if button_text == "Get Help":
                help_message = "🆘 Help Center\n\n"
                help_message += "• Type 'Hey Vihaan' to start a conversation\n"
                help_message += "• Ask me any question\n"
                help_message += "• I can help with various tasks\n\n"
                help_message += "What would you like to know?"
                
                await self.send_message(sender, help_message)
            
            elif button_text == "Contact Support":
                support_message = "📞 Support Information\n\n"
                support_message += "Email: vihaan@cognomega.com\n"
                support_message += "Website: https://cognomega.com\n\n"
                support_message += "We'll get back to you soon!"
                
                await self.send_message(sender, support_message)
            
        except Exception as e:
            logger.error("Failed to handle button response", error=str(e))
    
    async def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """Get message delivery status"""
        try:
            if not self.access_token:
                raise ValueError("WhatsApp not configured")
            
            url = f"{self.base_url}/{message_id}"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error("Failed to get message status", status=response.status, error=error_text)
                        raise Exception(f"Failed to get status: {error_text}")
            
        except Exception as e:
            logger.error("Failed to get message status", error=str(e))
            raise e
    
    async def create_template(self, name: str, category: str, language: str, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create WhatsApp template"""
        try:
            if not self.access_token:
                raise ValueError("WhatsApp not configured")
            
            url = f"{self.base_url}/{self.phone_number_id}/message_templates"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "name": name,
                "category": category,
                "language": language,
                "components": components
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info("WhatsApp template created", name=name)
                        return result
                    else:
                        error_text = await response.text()
                        logger.error("Failed to create template", status=response.status, error=error_text)
                        raise Exception(f"Failed to create template: {error_text}")
            
        except Exception as e:
            logger.error("Failed to create WhatsApp template", error=str(e))
            raise e
