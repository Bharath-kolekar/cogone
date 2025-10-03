"""
AI Assistant service with naming, wake word, and chat consolidation features
"""

import structlog
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
import json
from dataclasses import dataclass
from enum import Enum

logger = structlog.get_logger()


class ChatStatus(str, Enum):
    """Chat status options"""
    ACTIVE = "active"
    CONSOLIDATED = "consolidated"
    ARCHIVED = "archived"


@dataclass
class ChatMessage:
    """Chat message model"""
    id: str
    user_id: str
    content: str
    role: str  # "user" or "assistant"
    timestamp: datetime
    metadata: Dict[str, Any] = None


@dataclass
class ChatSession:
    """Chat session model"""
    id: str
    user_id: str
    assistant_name: str
    wake_word: str
    messages: List[ChatMessage]
    status: ChatStatus
    created_at: datetime
    last_activity: datetime
    consolidated_at: Optional[datetime] = None
    summary: Optional[str] = None


@dataclass
class AssistantConfig:
    """AI Assistant configuration"""
    name: str = "Vihaan"
    wake_word: str = "Hey Vihaan"
    personality: str = "helpful, friendly, and professional"
    response_style: str = "conversational"
    max_context_length: int = 4000
    consolidation_threshold: int = 20  # Consolidate after 20 messages
    consolidation_enabled: bool = True


class AIAssistantService:
    """AI Assistant service with advanced features"""
    
    def __init__(self):
        self.assistant_config = AssistantConfig()
        self.active_sessions: Dict[str, ChatSession] = {}
        self.consolidated_sessions: Dict[str, ChatSession] = {}
        self.user_preferences: Dict[str, Dict[str, Any]] = {}
    
    async def create_chat_session(self, user_id: str, assistant_name: str = None, wake_word: str = None) -> ChatSession:
        """Create new chat session"""
        try:
            # Get user preferences
            user_prefs = self.user_preferences.get(user_id, {})
            
            session = ChatSession(
                id=f"chat_{user_id}_{datetime.now().timestamp()}",
                user_id=user_id,
                assistant_name=assistant_name or user_prefs.get("assistant_name", self.assistant_config.name),
                wake_word=wake_word or user_prefs.get("wake_word", self.assistant_config.wake_word),
                messages=[],
                status=ChatStatus.ACTIVE,
                created_at=datetime.now(),
                last_activity=datetime.now()
            )
            
            self.active_sessions[session.id] = session
            
            logger.info(
                "Chat session created",
                session_id=session.id,
                user_id=user_id,
                assistant_name=session.assistant_name,
                wake_word=session.wake_word
            )
            
            return session
            
        except Exception as e:
            logger.error("Failed to create chat session", error=str(e))
            raise e
    
    async def add_message(self, session_id: str, content: str, role: str, metadata: Dict[str, Any] = None) -> ChatMessage:
        """Add message to chat session"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.active_sessions[session_id]
            
            message = ChatMessage(
                id=f"msg_{session_id}_{datetime.now().timestamp()}",
                user_id=session.user_id,
                content=content,
                role=role,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            
            session.messages.append(message)
            session.last_activity = datetime.now()
            
            # Check if consolidation is needed
            if self.assistant_config.consolidation_enabled and len(session.messages) >= self.assistant_config.consolidation_threshold:
                await self._consolidate_chat_session(session)
            
            logger.info(
                "Message added to session",
                session_id=session_id,
                message_id=message.id,
                role=role,
                content_length=len(content)
            )
            
            return message
            
        except Exception as e:
            logger.error("Failed to add message", error=str(e))
            raise e
    
    async def _consolidate_chat_session(self, session: ChatSession):
        """Consolidate chat session to save space"""
        try:
            # Generate summary of conversation
            summary = await self._generate_chat_summary(session)
            
            # Keep only recent messages (last 5)
            recent_messages = session.messages[-5:] if len(session.messages) > 5 else session.messages
            
            # Create consolidated session
            consolidated_session = ChatSession(
                id=f"consolidated_{session.id}",
                user_id=session.user_id,
                assistant_name=session.assistant_name,
                wake_word=session.wake_word,
                messages=recent_messages,
                status=ChatStatus.CONSOLIDATED,
                created_at=session.created_at,
                last_activity=datetime.now(),
                consolidated_at=datetime.now(),
                summary=summary
            )
            
            # Store consolidated session
            self.consolidated_sessions[consolidated_session.id] = consolidated_session
            
            # Update original session
            session.status = ChatStatus.CONSOLIDATED
            session.consolidated_at = datetime.now()
            session.summary = summary
            session.messages = recent_messages
            
            logger.info(
                "Chat session consolidated",
                session_id=session.id,
                original_messages=len(session.messages),
                summary_length=len(summary)
            )
            
        except Exception as e:
            logger.error("Failed to consolidate chat session", error=str(e))
    
    async def _generate_chat_summary(self, session: ChatSession) -> str:
        """Generate summary of chat conversation"""
        try:
            # Extract key topics and decisions from conversation
            topics = []
            decisions = []
            questions = []
            
            for message in session.messages:
                if message.role == "user":
                    if "?" in message.content:
                        questions.append(message.content)
                    elif any(word in message.content.lower() for word in ["decide", "choose", "select", "pick"]):
                        decisions.append(message.content)
                    else:
                        topics.append(message.content)
            
            # Generate summary
            summary_parts = []
            
            if topics:
                summary_parts.append(f"Topics discussed: {', '.join(topics[:3])}")
            
            if decisions:
                summary_parts.append(f"Decisions made: {', '.join(decisions[:2])}")
            
            if questions:
                summary_parts.append(f"Questions asked: {len(questions)}")
            
            summary = f"Chat with {session.assistant_name} - " + "; ".join(summary_parts)
            
            return summary
            
        except Exception as e:
            logger.error("Failed to generate chat summary", error=str(e))
            return f"Chat session with {session.assistant_name} - {len(session.messages)} messages"
    
    async def get_chat_history(self, user_id: str, include_consolidated: bool = True) -> List[ChatSession]:
        """Get chat history for user"""
        try:
            sessions = []
            
            # Get active sessions
            for session in self.active_sessions.values():
                if session.user_id == user_id:
                    sessions.append(session)
            
            # Get consolidated sessions if requested
            if include_consolidated:
                for session in self.consolidated_sessions.values():
                    if session.user_id == user_id:
                        sessions.append(session)
            
            # Sort by last activity
            sessions.sort(key=lambda x: x.last_activity, reverse=True)
            
            return sessions
            
        except Exception as e:
            logger.error("Failed to get chat history", error=str(e))
            return []
    
    async def update_assistant_config(self, user_id: str, name: str = None, wake_word: str = None, personality: str = None):
        """Update assistant configuration for user"""
        try:
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = {}
            
            if name:
                self.user_preferences[user_id]["assistant_name"] = name
                self.assistant_config.name = name
            
            if wake_word:
                self.user_preferences[user_id]["wake_word"] = wake_word
                self.assistant_config.wake_word = wake_word
            
            if personality:
                self.user_preferences[user_id]["personality"] = personality
                self.assistant_config.personality = personality
            
            logger.info(
                "Assistant configuration updated",
                user_id=user_id,
                name=name,
                wake_word=wake_word,
                personality=personality
            )
            
        except Exception as e:
            logger.error("Failed to update assistant configuration", error=str(e))
            raise e
    
    async def get_assistant_config(self, user_id: str) -> Dict[str, Any]:
        """Get assistant configuration for user"""
        user_prefs = self.user_preferences.get(user_id, {})
        
        return {
            "name": user_prefs.get("assistant_name", self.assistant_config.name),
            "wake_word": user_prefs.get("wake_word", self.assistant_config.wake_word),
            "personality": user_prefs.get("personality", self.assistant_config.personality),
            "response_style": self.assistant_config.response_style,
            "max_context_length": self.assistant_config.max_context_length,
            "consolidation_enabled": self.assistant_config.consolidation_enabled
        }
    
    async def process_wake_word(self, user_id: str, audio_text: str) -> bool:
        """Process wake word detection"""
        try:
            user_prefs = self.user_preferences.get(user_id, {})
            wake_word = user_prefs.get("wake_word", self.assistant_config.wake_word)
            
            # Simple wake word detection (can be enhanced with NLP)
            wake_word_lower = wake_word.lower()
            audio_text_lower = audio_text.lower()
            
            is_wake_word = wake_word_lower in audio_text_lower
            
            if is_wake_word:
                logger.info(
                    "Wake word detected",
                    user_id=user_id,
                    wake_word=wake_word,
                    audio_text=audio_text
                )
            
            return is_wake_word
            
        except Exception as e:
            logger.error("Failed to process wake word", error=str(e))
            return False
    
    async def generate_response(self, session_id: str, user_message: str) -> str:
        """Generate AI assistant response"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError(f"Session {session_id} not found")
            
            session = self.active_sessions[session_id]
            
            # Get context from recent messages
            context = self._build_context(session)
            
            # Generate response based on assistant personality and context
            response = await self._generate_contextual_response(
                user_message=user_message,
                context=context,
                assistant_name=session.assistant_name,
                personality=session.assistant_name
            )
            
            # Add response to session
            await self.add_message(session_id, response, "assistant")
            
            logger.info(
                "Response generated",
                session_id=session_id,
                response_length=len(response)
            )
            
            return response
            
        except Exception as e:
            logger.error("Failed to generate response", error=str(e))
            return "I apologize, but I'm having trouble processing your request right now. Please try again."
    
    def _build_context(self, session: ChatSession) -> str:
        """Build context from recent messages"""
        recent_messages = session.messages[-10:]  # Last 10 messages
        
        context_parts = []
        for message in recent_messages:
            role_label = "User" if message.role == "user" else session.assistant_name
            context_parts.append(f"{role_label}: {message.content}")
        
        return "\n".join(context_parts)
    
    async def _generate_contextual_response(self, user_message: str, context: str, assistant_name: str, personality: str) -> str:
        """Generate contextual response using AI"""
        try:
            # This would integrate with GROQ, Together AI, or local models
            # For now, return a simple response
            
            response = f"Hello! I'm {assistant_name}. I understand you said: '{user_message}'. "
            response += "I'm here to help you with your questions and tasks. "
            response += "How can I assist you today?"
            
            return response
            
        except Exception as e:
            logger.error("Failed to generate contextual response", error=str(e))
            return "I'm here to help! What can I do for you today?"
    
    async def get_session_stats(self, user_id: str) -> Dict[str, Any]:
        """Get session statistics for user"""
        try:
            active_sessions = sum(1 for s in self.active_sessions.values() if s.user_id == user_id)
            consolidated_sessions = sum(1 for s in self.consolidated_sessions.values() if s.user_id == user_id)
            
            total_messages = 0
            for session in self.active_sessions.values():
                if session.user_id == user_id:
                    total_messages += len(session.messages)
            
            return {
                "active_sessions": active_sessions,
                "consolidated_sessions": consolidated_sessions,
                "total_messages": total_messages,
                "assistant_name": self.user_preferences.get(user_id, {}).get("assistant_name", self.assistant_config.name),
                "wake_word": self.user_preferences.get(user_id, {}).get("wake_word", self.assistant_config.wake_word)
            }
            
        except Exception as e:
            logger.error("Failed to get session stats", error=str(e))
            return {}
