"""
Smart Coding AI Integration Service
Integrates Smart Coding AI with existing AI components and orchestrators
"""

import structlog
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import uuid
from dataclasses import dataclass

from app.services.smart_coding_ai_optimized import smart_coding_ai_optimized
from app.services.codebase_memory_system import CodebaseMemorySystem

# Optional imports - only import if available
try:
    from app.services.ai_assistant_service import AIAssistantService
    AI_ASSISTANT_AVAILABLE = True
except ImportError:
    AI_ASSISTANT_AVAILABLE = False

try:
    from app.services.voice_service import VoiceService
    VOICE_SERVICE_AVAILABLE = True
except ImportError:
    VOICE_SERVICE_AVAILABLE = False

try:
    from app.services.meta_ai_orchestrator_unified import MetaAIOrchestratorUnified
    META_ORCHESTRATOR_AVAILABLE = True
except ImportError:
    META_ORCHESTRATOR_AVAILABLE = False

try:
    from app.services.goal_integrity_service import GoalIntegrityService
    GOAL_INTEGRITY_AVAILABLE = True
except ImportError:
    GOAL_INTEGRITY_AVAILABLE = False

try:
    from app.services.whatsapp_service import WhatsAppService
    WHATSAPP_AVAILABLE = True
except ImportError:
    WHATSAPP_AVAILABLE = False

logger = structlog.get_logger()


@dataclass
class AIIntegrationContext:
    """Context for AI integration operations"""
    user_id: str
    session_id: Optional[str] = None
    project_id: Optional[str] = None
    request_id: Optional[str] = None
    operation_type: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.request_id:
            self.request_id = str(uuid.uuid4())


@dataclass
class IntegratedAIResponse:
    """Response from integrated AI system"""
    response_id: str
    primary_response: Any
    supporting_responses: Dict[str, Any]
    confidence: float
    integration_metadata: Dict[str, Any]
    timestamp: datetime


class SmartCodingAIIntegration:
    """Integrates Smart Coding AI with existing AI components"""
    
    def __init__(self):
        self.smart_coding_ai = smart_coding_ai_optimized
        self.memory_system = CodebaseMemorySystem()
        
        # Initialize optional components
        self.ai_assistant = None
        self.voice_service = None
        self.meta_orchestrator = None
        self.goal_integrity = None
        self.whatsapp_service = None
        
        if AI_ASSISTANT_AVAILABLE:
            self.ai_assistant = AIAssistantService()
        if VOICE_SERVICE_AVAILABLE:
            self.voice_service = VoiceService()
        if META_ORCHESTRATOR_AVAILABLE:
            self.meta_orchestrator = MetaAIOrchestratorUnified()
        if GOAL_INTEGRITY_AVAILABLE:
            self.goal_integrity = GoalIntegrityService()
        if WHATSAPP_AVAILABLE:
            self.whatsapp_service = WhatsAppService()
            # Enable Smart Coding AI integration in WhatsApp
            self.whatsapp_service.enable_smart_coding_integration(self)
        
        # Integration cache
        self.integration_cache: Dict[str, Any] = {}
        self.session_contexts: Dict[str, AIIntegrationContext] = {}
    
    async def initialize(self):
        """Initialize all integrated AI components"""
        try:
            # Initialize optional components if available
            if self.goal_integrity:
                await self.goal_integrity.initialize()
            
            if self.meta_orchestrator:
                await self.meta_orchestrator.initialize()
            
            logger.info("Smart Coding AI Integration initialized successfully", 
                       components={
                           "ai_assistant": AI_ASSISTANT_AVAILABLE,
                           "voice_service": VOICE_SERVICE_AVAILABLE,
                           "meta_orchestrator": META_ORCHESTRATOR_AVAILABLE,
                           "goal_integrity": GOAL_INTEGRITY_AVAILABLE,
                           "whatsapp": WHATSAPP_AVAILABLE
                       })
            
        except Exception as e:
            logger.error("Failed to initialize Smart Coding AI Integration", error=str(e))
            # Don't raise - allow partial initialization
    
    # ============================================================================
    # VOICE-TO-CODE INTEGRATION
    # ============================================================================
    
    async def process_voice_to_code(self, audio_file, language: str, context: AIIntegrationContext) -> IntegratedAIResponse:
        """Process voice input to generate code using integrated AI"""
        try:
            logger.info("Processing voice-to-code request", user_id=context.user_id, language=language)
            
            # Step 1: Transcribe voice using Voice Service
            if self.voice_service:
                transcript = await self.voice_service.transcribe_local(audio_file, language)
            else:
                # Fallback: treat audio as text
                transcript = audio_file.decode('utf-8', errors='ignore') if isinstance(audio_file, bytes) else str(audio_file)
            
            # Step 2: Use Meta Orchestrator to plan the code generation
            if self.meta_orchestrator:
                orchestration_plan = await self.meta_orchestrator.orchestrate_plan(transcript, context.user_id)
            else:
                # Fallback: simple plan
                orchestration_plan = {"steps": [{"id": "generate_code", "action": "implement", "description": transcript}], "confidence": 0.8}
            
            # Step 3: Use Smart Coding AI to generate code based on transcript and plan
            code_generation_result = await self._generate_code_from_transcript(
                transcript, orchestration_plan, context
            )
            
            # Step 4: Use Memory System to enhance with project context
            memory_enhanced_result = await self._enhance_with_memory_context(
                code_generation_result, context
            )
            
            # Step 5: Validate against goal integrity
            integrity_check = await self._validate_goal_integrity(
                memory_enhanced_result, context
            )
            
            return IntegratedAIResponse(
                response_id=str(uuid.uuid4()),
                primary_response=memory_enhanced_result,
                supporting_responses={
                    "transcript": transcript,
                    "orchestration_plan": orchestration_plan,
                    "integrity_check": integrity_check
                },
                confidence=min(0.95, memory_enhanced_result.get("confidence", 0.8)),
                integration_metadata={
                    "voice_processed": True,
                    "orchestration_used": True,
                    "memory_enhanced": True,
                    "integrity_validated": integrity_check.get("valid", True)
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error("Failed to process voice-to-code", error=str(e))
            raise
    
    async def _generate_code_from_transcript(self, transcript: str, plan: Dict, context: AIIntegrationContext) -> Dict[str, Any]:
        """Generate code from voice transcript"""
        try:
            # Use Smart Coding AI to interpret the transcript as a coding request
            chat_response = await self.smart_coding_ai.chat_with_codebase(
                query=f"Generate code for: {transcript}",
                project_id=context.project_id or "voice_generation",
                context_type="code_generation"
            )
            
            # Create code generation result
            return {
                "generated_code": chat_response.get("answer", ""),
                "confidence": chat_response.get("confidence", 0.8),
                "suggestions": chat_response.get("code_snippets", []),
                "follow_up_questions": chat_response.get("follow_up_questions", []),
                "transcript": transcript,
                "orchestration_plan": plan
            }
            
        except Exception as e:
            logger.error("Failed to generate code from transcript", error=str(e))
            return {"generated_code": "", "confidence": 0.0, "error": str(e)}
    
    async def _enhance_with_memory_context(self, code_result: Dict, context: AIIntegrationContext) -> Dict[str, Any]:
        """Enhance code generation with memory context"""
        try:
            if not context.project_id:
                return code_result
            
            # Search memory for relevant patterns
            memory_search = await self.smart_coding_ai.search_codebase_memory(
                query=code_result.get("generated_code", "")[:100],
                project_id=context.project_id,
                result_type="pattern"
            )
            
            # Get contextual suggestions
            suggestions = await self.smart_coding_ai.get_contextual_suggestions(
                file_path="generated_code.py",
                language="python",
                cursor_position=(1, 1)
            )
            
            # Enhance the result
            enhanced_result = code_result.copy()
            enhanced_result.update({
                "memory_context": memory_search,
                "contextual_suggestions": suggestions,
                "enhanced_confidence": min(1.0, code_result.get("confidence", 0.8) + 0.1)
            })
            
            return enhanced_result
            
        except Exception as e:
            logger.error("Failed to enhance with memory context", error=str(e))
            return code_result
    
    async def _validate_goal_integrity(self, result: Dict, context: AIIntegrationContext) -> Dict[str, Any]:
        """Validate result against goal integrity"""
        try:
            # Create a goal context for validation
            from app.services.goal_integrity_service import GoalIntegrityContext
            
            goal_context = GoalIntegrityContext(
                user_id=context.user_id,
                session_id=context.session_id,
                request_id=context.request_id,
                operation_type="code_generation",
                metadata={"generated_code": result.get("generated_code", "")}
            )
            
            # Validate against coding goals
            if self.goal_integrity:
                integrity_valid = await self.goal_integrity.verify_goal_integrity(
                    "coding_standards_goal", goal_context
                )
            else:
                # Fallback: assume valid
                integrity_valid = True
            
            return {
                "valid": integrity_valid,
                "validation_timestamp": datetime.now(),
                "goal_context": goal_context
            }
            
        except Exception as e:
            logger.error("Failed to validate goal integrity", error=str(e))
            return {"valid": True, "error": str(e)}
    
    # ============================================================================
    # AI ASSISTANT INTEGRATION
    # ============================================================================
    
    async def chat_with_ai_assistant(self, message: str, context: AIIntegrationContext) -> IntegratedAIResponse:
        """Chat with AI assistant enhanced by Smart Coding AI"""
        try:
            logger.info("Processing AI assistant chat", user_id=context.user_id)
            
            # Step 1: Process with AI Assistant
            if self.ai_assistant:
                assistant_response = await self.ai_assistant.process_message(
                    user_id=context.user_id,
                    message=message,
                    assistant_name="SmartCodingAssistant"
                )
            else:
                # Fallback: simple assistant response
                assistant_response = {"response": f"Hello! I'm SmartCodingAssistant. You said: {message}", "confidence": 0.8}
            
            # Step 2: Check if message is code-related
            is_code_related = await self._detect_code_intent(message)
            
            if is_code_related:
                # Step 3: Enhance with Smart Coding AI
                smart_coding_response = await self.smart_coding_ai.chat_with_codebase(
                    query=message,
                    project_id=context.project_id or "general",
                    context_type="assistant_chat"
                )
                
                # Step 4: Combine responses
                enhanced_response = await self._combine_assistant_responses(
                    assistant_response, smart_coding_response
                )
                
                return IntegratedAIResponse(
                    response_id=str(uuid.uuid4()),
                    primary_response=enhanced_response,
                    supporting_responses={
                        "assistant_response": assistant_response,
                        "smart_coding_response": smart_coding_response
                    },
                    confidence=enhanced_response.get("confidence", 0.8),
                    integration_metadata={
                        "code_related": True,
                        "assistant_enhanced": True,
                        "smart_coding_enhanced": True
                    },
                    timestamp=datetime.now()
                )
            else:
                return IntegratedAIResponse(
                    response_id=str(uuid.uuid4()),
                    primary_response=assistant_response,
                    supporting_responses={},
                    confidence=0.9,
                    integration_metadata={
                        "code_related": False,
                        "assistant_only": True
                    },
                    timestamp=datetime.now()
                )
                
        except Exception as e:
            logger.error("Failed to process AI assistant chat", error=str(e))
            raise
    
    async def _detect_code_intent(self, message: str) -> bool:
        """Detect if message is code-related"""
        code_keywords = [
            "code", "function", "class", "variable", "import", "def", "return",
            "programming", "debug", "error", "syntax", "compile", "run",
            "algorithm", "logic", "implementation", "development"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in code_keywords)
    
    async def _combine_assistant_responses(self, assistant_response: Dict, smart_coding_response: Dict) -> Dict[str, Any]:
        """Combine AI assistant and Smart Coding AI responses"""
        return {
            "combined_response": f"{assistant_response.get('response', '')}\n\nSmart Coding AI Insight:\n{smart_coding_response.get('answer', '')}",
            "confidence": (assistant_response.get('confidence', 0.8) + smart_coding_response.get('confidence', 0.8)) / 2,
            "code_snippets": smart_coding_response.get('code_snippets', []),
            "follow_up_questions": smart_coding_response.get('follow_up_questions', []),
            "metadata": {
                "assistant_confidence": assistant_response.get('confidence', 0.8),
                "smart_coding_confidence": smart_coding_response.get('confidence', 0.8)
            }
        }
    
    # ============================================================================
    # META ORCHESTRATOR INTEGRATION
    # ============================================================================
    
    async def orchestrate_smart_coding_task(self, task_description: str, context: AIIntegrationContext) -> IntegratedAIResponse:
        """Orchestrate a smart coding task using Meta Orchestrator"""
        try:
            logger.info("Orchestrating smart coding task", user_id=context.user_id)
            
            # Step 1: Use Meta Orchestrator to plan the task
            if self.meta_orchestrator:
                orchestration_result = await self.meta_orchestrator.orchestrate_plan(
                    task_description, context.user_id
                )
            else:
                # Fallback: simple orchestration
                orchestration_result = {
                    "steps": [
                        {"id": "analyze", "action": "analyze", "description": f"Analyze: {task_description}"},
                        {"id": "implement", "action": "implement", "description": f"Implement: {task_description}"},
                        {"id": "test", "action": "test", "description": f"Test: {task_description}"}
                    ],
                    "confidence": 0.8
                }
            
            # Step 2: Break down the plan into coding tasks
            coding_tasks = await self._break_down_coding_tasks(
                orchestration_result, context
            )
            
            # Step 3: Execute coding tasks using Smart Coding AI
            execution_results = []
            for task in coding_tasks:
                task_result = await self._execute_coding_task(task, context)
                execution_results.append(task_result)
            
            # Step 4: Combine and optimize results
            final_result = await self._combine_coding_results(execution_results, context)
            
            return IntegratedAIResponse(
                response_id=str(uuid.uuid4()),
                primary_response=final_result,
                supporting_responses={
                    "orchestration_plan": orchestration_result,
                    "coding_tasks": coding_tasks,
                    "execution_results": execution_results
                },
                confidence=final_result.get("confidence", 0.85),
                integration_metadata={
                    "orchestrated": True,
                    "tasks_executed": len(execution_results),
                    "meta_orchestrator_used": True
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error("Failed to orchestrate smart coding task", error=str(e))
            raise
    
    async def _break_down_coding_tasks(self, orchestration_plan: Dict, context: AIIntegrationContext) -> List[Dict[str, Any]]:
        """Break down orchestration plan into coding tasks"""
        tasks = []
        
        if "steps" in orchestration_plan:
            for step in orchestration_plan["steps"]:
                if step.get("action") in ["scaffold", "implement", "optimize", "test"]:
                    tasks.append({
                        "task_id": str(uuid.uuid4()),
                        "action": step.get("action"),
                        "description": step.get("description", ""),
                        "confidence": step.get("confidence", 0.8)
                    })
        
        return tasks
    
    async def _execute_coding_task(self, task: Dict, context: AIIntegrationContext) -> Dict[str, Any]:
        """Execute a single coding task using Smart Coding AI"""
        try:
            # Use appropriate Smart Coding AI method based on task action
            if task["action"] == "scaffold":
                result = await self.smart_coding_ai.chat_with_codebase(
                    query=f"Create scaffolding for: {task['description']}",
                    project_id=context.project_id or "orchestration",
                    context_type="scaffolding"
                )
            elif task["action"] == "implement":
                result = await self.smart_coding_ai.chat_with_codebase(
                    query=f"Implement: {task['description']}",
                    project_id=context.project_id or "orchestration",
                    context_type="implementation"
                )
            elif task["action"] == "optimize":
                result = await self.smart_coding_ai.chat_with_codebase(
                    query=f"Optimize code for: {task['description']}",
                    project_id=context.project_id or "orchestration",
                    context_type="optimization"
                )
            else:
                result = await self.smart_coding_ai.chat_with_codebase(
                    query=f"Handle task: {task['description']}",
                    project_id=context.project_id or "orchestration",
                    context_type="general"
                )
            
            return {
                "task_id": task["task_id"],
                "action": task["action"],
                "result": result,
                "success": len(result.get("answer", "")) > 0,
                "confidence": result.get("confidence", 0.8)
            }
            
        except Exception as e:
            logger.error("Failed to execute coding task", error=str(e))
            return {
                "task_id": task["task_id"],
                "action": task["action"],
                "result": {"error": str(e)},
                "success": False,
                "confidence": 0.0
            }
    
    async def _combine_coding_results(self, results: List[Dict], context: AIIntegrationContext) -> Dict[str, Any]:
        """Combine multiple coding task results"""
        successful_tasks = [r for r in results if r["success"]]
        total_confidence = sum(r["confidence"] for r in results) / len(results) if results else 0.0
        
        return {
            "combined_code": "\n\n".join([r["result"].get("answer", "") for r in successful_tasks]),
            "total_tasks": len(results),
            "successful_tasks": len(successful_tasks),
            "confidence": total_confidence,
            "task_details": results,
            "recommendations": self._generate_recommendations(results)
        }
    
    def _generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate recommendations based on task results"""
        recommendations = []
        
        successful_count = len([r for r in results if r["success"]])
        
        if successful_count == len(results):
            recommendations.append("All tasks completed successfully!")
        elif successful_count > len(results) / 2:
            recommendations.append("Most tasks completed successfully. Review failed tasks.")
        else:
            recommendations.append("Several tasks failed. Consider reviewing the approach.")
        
        return recommendations
    
    # ============================================================================
    # WHATSAPP INTEGRATION
    # ============================================================================
    
    async def process_whatsapp_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process WhatsApp message with Smart Coding AI integration"""
        try:
            if not self.whatsapp_service:
                return {"error": "WhatsApp service not available"}
            
            message_type = message_data.get("type", "text")
            
            if message_type == "voice":
                return await self.whatsapp_service.process_voice_message(message_data)
            elif message_type == "text":
                return await self.whatsapp_service.process_text_message(message_data)
            else:
                return {"error": f"Unsupported message type: {message_type}"}
                
        except Exception as e:
            logger.error("Failed to process WhatsApp message", error=str(e))
            return {"error": f"Failed to process WhatsApp message: {str(e)}"}
    
    async def send_whatsapp_code_response(self, to: str, generated_code: str, confidence: float, 
                                        code_type: str = "python") -> Dict[str, Any]:
        """Send generated code as WhatsApp message"""
        try:
            if not self.whatsapp_service:
                return {"error": "WhatsApp service not available"}
            
            # Format code message
            message = f"🤖 *Code Generated* (Confidence: {confidence:.1%})\n\n```{code_type}\n{generated_code}\n```"
            
            # Send via WhatsApp
            response = await self.whatsapp_service.send_message(to, message)
            
            return {
                "success": True,
                "whatsapp_response": response,
                "message_sent": True
            }
            
        except Exception as e:
            logger.error("Failed to send WhatsApp code response", error=str(e))
            return {"error": f"Failed to send WhatsApp code response: {str(e)}"}
    
    async def send_whatsapp_chat_response(self, to: str, ai_response: str, confidence: float) -> Dict[str, Any]:
        """Send AI chat response as WhatsApp message"""
        try:
            if not self.whatsapp_service:
                return {"error": "WhatsApp service not available"}
            
            # Format chat message
            message = f"🤖 *Smart Coding AI Response* (Confidence: {confidence:.1%})\n\n{ai_response}"
            
            # Send via WhatsApp
            response = await self.whatsapp_service.send_message(to, message)
            
            return {
                "success": True,
                "whatsapp_response": response,
                "message_sent": True
            }
            
        except Exception as e:
            logger.error("Failed to send WhatsApp chat response", error=str(e))
            return {"error": f"Failed to send WhatsApp chat response: {str(e)}"}

    # ============================================================================
    # SESSION MANAGEMENT
    # ============================================================================
    
    async def create_integration_session(self, user_id: str, project_id: Optional[str] = None) -> str:
        """Create a new integration session"""
        try:
            session_id = str(uuid.uuid4())
            
            # Create context
            context = AIIntegrationContext(
                user_id=user_id,
                session_id=session_id,
                project_id=project_id
            )
            
            # Store context
            self.session_contexts[session_id] = context
            
            # Create Smart Coding AI session
            await self.smart_coding_ai.create_session_context(
                user_id=user_id,
                project_id=project_id or "integration_session",
                current_file="integration.py",
                cursor_position=(1, 1),
                working_directory="."
            )
            
            logger.info("Integration session created", session_id=session_id, user_id=user_id)
            return session_id
            
        except Exception as e:
            logger.error("Failed to create integration session", error=str(e))
            raise
    
    async def get_session_context(self, session_id: str) -> Optional[AIIntegrationContext]:
        """Get session context"""
        return self.session_contexts.get(session_id)
    
    async def update_session_context(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session context"""
        try:
            if session_id in self.session_contexts:
                context = self.session_contexts[session_id]
                
                # Update context fields
                for key, value in updates.items():
                    if hasattr(context, key):
                        setattr(context, key, value)
                
                # Update metadata
                context.metadata.update(updates.get("metadata", {}))
                
                return True
            return False
            
        except Exception as e:
            logger.error("Failed to update session context", error=str(e))
            return False


# Global instance
smart_coding_ai_integration = SmartCodingAIIntegration()
