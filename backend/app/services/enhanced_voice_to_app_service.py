"""
Enhanced Voice-to-App Service with Smarty AI Orchestrator Integration

This service provides complete voice-to-app generation using the Smarty AI Orchestrator
for intelligent orchestration and ethical code generation.
"""

import structlog
import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import uuid
import base64
import io

from app.services.smarty_ai_orchestrator import smarty_ai_orchestrator, OrchestrationMode, CodeGenerationStrategy
from app.services.smarty_agent_integration import smarty_agent_integration, AgentSmartyMode, AgentCodeCapability
from app.core.config import settings

logger = structlog.get_logger(__name__)

class VoiceToAppRequest:
    """Request model for voice-to-app generation"""
    def __init__(self, 
                 audio_data: bytes,
                 user_id: str,
                 language: str = "en",
                 app_type: Optional[str] = None,
                 complexity_level: str = "medium",
                 ethical_validation_level: str = "standard",
                 orchestration_mode: OrchestrationMode = OrchestrationMode.VOICE_TO_APP,
                 code_generation_strategy: CodeGenerationStrategy = CodeGenerationStrategy.ADAPTIVE):
        self.audio_data = audio_data
        self.user_id = user_id
        self.language = language
        self.app_type = app_type
        self.complexity_level = complexity_level
        self.ethical_validation_level = ethical_validation_level
        self.orchestration_mode = orchestration_mode
        self.code_generation_strategy = code_generation_strategy
        self.request_id = str(uuid.uuid4())
        self.created_at = datetime.now()

class VoiceToAppResponse:
    """Response model for voice-to-app generation"""
    def __init__(self):
        self.request_id: str = ""
        self.user_id: str = ""
        self.transcript: str = ""
        self.app_type: str = ""
        self.complexity_level: str = ""
        self.orchestration_plan: Optional[Dict[str, Any]] = None
        self.generated_app: Optional[Dict[str, Any]] = None
        self.deployment_info: Optional[Dict[str, Any]] = None
        self.quality_metrics: Dict[str, Any] = {}
        self.execution_time: float = 0.0
        self.confidence_score: float = 0.0
        self.status: str = "pending"
        self.created_at: datetime = datetime.now()
        self.completed_at: Optional[datetime] = None

class EnhancedVoiceToAppService:
    """Enhanced Voice-to-App service with Smarty AI Orchestrator integration"""
    
    def __init__(self):
        # Voice transcription handled internally (no longer depends on separate VoiceService)
        self.smarty_orchestrator = smarty_ai_orchestrator
        self.smarty_agent_integration = smarty_agent_integration
        
        # Processing state
        self.active_requests: Dict[str, VoiceToAppRequest] = {}
        self.completed_responses: Dict[str, VoiceToAppResponse] = {}
        
        # Performance metrics
        self.metrics = {
            "total_requests": 0,
            "successful_generations": 0,
            "failed_generations": 0,
            "average_execution_time": 0.0,
            "average_confidence_score": 0.0,
            "average_quality_score": 0.0
        }
        
        logger.info("Enhanced Voice-to-App Service initialized with Smarty AI Orchestrator")

    async def generate_app_from_voice(self, request: VoiceToAppRequest) -> VoiceToAppResponse:
        """Generate complete app from voice input using Smarty AI Orchestrator"""
        try:
            start_time = time.time()
            response = VoiceToAppResponse()
            response.request_id = request.request_id
            response.user_id = request.user_id
            response.status = "processing"
            
            logger.info(f"Starting voice-to-app generation", 
                       request_id=request.request_id,
                       user_id=request.user_id,
                       language=request.language)
            
            # Store active request
            self.active_requests[request.request_id] = request
            
            # Step 1: Transcribe voice to text
            transcript = await self._transcribe_voice(request)
            response.transcript = transcript
            
            # Step 2: Analyze and enhance transcript
            enhanced_transcript = await self._enhance_transcript(transcript, request)
            
            # Step 3: Orchestrate app generation using Smarty AI Orchestrator
            orchestration_plan = await self._orchestrate_app_generation(
                enhanced_transcript, request, response
            )
            response.orchestration_plan = orchestration_plan
            
            # Step 4: Generate the actual app
            generated_app = await self._generate_app_from_plan(
                orchestration_plan, request, response
            )
            response.generated_app = generated_app
            
            # Step 5: Deploy the app (if requested)
            deployment_info = await self._deploy_generated_app(
                generated_app, request, response
            )
            response.deployment_info = deployment_info
            
            # Step 6: Calculate quality metrics
            response.quality_metrics = await self._calculate_quality_metrics(
                transcript, orchestration_plan, generated_app
            )
            
            # Step 7: Finalize response
            response.execution_time = time.time() - start_time
            response.confidence_score = orchestration_plan.get('confidence', 0.0)
            response.status = "completed"
            response.completed_at = datetime.now()
            
            # Store completed response
            self.completed_responses[request.request_id] = response
            
            # Update metrics
            self._update_metrics(response)
            
            # Clean up active request
            if request.request_id in self.active_requests:
                del self.active_requests[request.request_id]
            
            logger.info(f"Voice-to-app generation completed", 
                       request_id=request.request_id,
                       execution_time=response.execution_time,
                       confidence_score=response.confidence_score)
            
            return response
            
        except Exception as e:
            logger.error(f"Voice-to-app generation failed", 
                        error=str(e), 
                        request_id=request.request_id,
                        user_id=request.user_id)
            
            # Create error response
            response = VoiceToAppResponse()
            response.request_id = request.request_id
            response.user_id = request.user_id
            response.status = "failed"
            response.completed_at = datetime.now()
            response.execution_time = time.time() - start_time if 'start_time' in locals() else 0.0
            response.quality_metrics = {"error": str(e)}
            
            # Update metrics
            self.metrics["total_requests"] += 1
            self.metrics["failed_generations"] += 1
            
            # Clean up active request
            if request.request_id in self.active_requests:
                del self.active_requests[request.request_id]
            
            return response

    async def _transcribe_audio_inline(self, audio_file, language: str = "en") -> str:
        """Inline audio transcription (migrated from VoiceService)"""
        try:
            # Mock implementation - in production, integrate with Whisper or similar
            mock_transcripts = {
                "en": "Create a todo app with add, edit, and delete functionality",
                "hi": "एक टूडू ऐप बनाएं जिसमें जोड़ने, संपादित करने और हटाने की सुविधा हो",
                "ta": "செய்ய வேண்டியவை பட்டியல் செயலியை உருவாக்குங்கள்",
                "te": "టూడూ యాప్‌ను సృష్టించండి",
                "bn": "একটি টুডু অ্যাপ তৈরি করুন",
            }
            return mock_transcripts.get(language, mock_transcripts["en"])
        except Exception as e:
            logger.error("Audio transcription failed", error=str(e))
            raise

    async def _transcribe_voice(self, request: VoiceToAppRequest) -> str:
        """Transcribe voice audio to text"""
        try:
            logger.info(f"Transcribing voice audio", 
                       request_id=request.request_id,
                       language=request.language)
            
            # Convert bytes to file-like object
            audio_file = io.BytesIO(request.audio_data)
            
            # Transcribe audio inline (mock implementation for now)
            transcript = await self._transcribe_audio_inline(
                audio_file, request.language
            )
            
            logger.info(f"Voice transcription completed", 
                       request_id=request.request_id,
                       transcript_length=len(transcript))
            
            return transcript
            
        except Exception as e:
            logger.error(f"Voice transcription failed", 
                        error=str(e), 
                        request_id=request.request_id)
            raise

    async def _enhance_transcript(self, transcript: str, request: VoiceToAppRequest) -> str:
        """Enhance transcript with additional context and requirements"""
        try:
            logger.info(f"Enhancing transcript", 
                       request_id=request.request_id,
                       original_length=len(transcript))
            
            # Create enhancement prompt
            enhancement_prompt = f"""
            Original voice transcript: "{transcript}"
            
            Please enhance this transcript for app generation with:
            1. Clear technical requirements
            2. Specific functionality details
            3. User interface requirements
            4. Database needs
            5. API requirements
            6. Deployment considerations
            
            Language: {request.language}
            Complexity Level: {request.complexity_level}
            App Type: {request.app_type or 'auto-detect'}
            """
            
            # Use Smarty Agent for transcript enhancement
            enhanced_transcript = await self._enhance_with_smarty_agent(
                enhancement_prompt, request
            )
            
            logger.info(f"Transcript enhancement completed", 
                       request_id=request.request_id,
                       enhanced_length=len(enhanced_transcript))
            
            return enhanced_transcript
            
        except Exception as e:
            logger.error(f"Transcript enhancement failed", 
                        error=str(e), 
                        request_id=request.request_id)
            # Return original transcript if enhancement fails
            return transcript

    async def _enhance_with_smarty_agent(self, prompt: str, request: VoiceToAppRequest) -> str:
        """Enhance transcript using Smarty Agent"""
        try:
            # Create a temporary agent for transcript enhancement
            agent_creation_request = {
                "name": f"Transcript Enhancement Agent - {request.request_id[:8]}",
                "description": "Agent for enhancing voice transcripts for app generation",
                "agent_type": "coding_assistant",
                "capabilities": ["code_generation", "analysis", "documentation"]
            }
            
            # Create agent
            agent = await self.smarty_agent_integration.create_smarty_agent(
                agent_creation_request=agent_creation_request,
                smarty_mode=AgentSmartyMode.DOCUMENTATION_ASSISTANT,
                code_capability=AgentCodeCapability.DOCUMENTED_CODE,
                ethical_validation_level=request.ethical_validation_level
            )
            
            # Use agent for enhancement
            code_request = {
                "agent_id": str(agent.agent_id),
                "user_id": request.user_id,
                "prompt": prompt,
                "context": {
                    "language": request.language,
                    "complexity_level": request.complexity_level,
                    "app_type": request.app_type
                },
                "code_type": "requirements_documentation",
                "complexity_level": request.complexity_level,
                "requirements": {
                    "clarity": "high",
                    "completeness": "high",
                    "technical_detail": "high"
                }
            }
            
            response = await self.smarty_agent_integration.interact_with_smarty_agent(code_request)
            
            # Clean up agent
            await self.smarty_agent_integration.remove_smarty_agent(str(agent.agent_id))
            
            return response.generated_code or prompt
            
        except Exception as e:
            logger.error(f"Smarty agent enhancement failed", error=str(e))
            return prompt

    async def _orchestrate_app_generation(self, 
                                        enhanced_transcript: str, 
                                        request: VoiceToAppRequest,
                                        response: VoiceToAppResponse) -> Dict[str, Any]:
        """Orchestrate app generation using Smarty AI Orchestrator"""
        try:
            logger.info(f"Orchestrating app generation", 
                       request_id=request.request_id,
                       transcript_length=len(enhanced_transcript))
            
            # Use Smarty AI Orchestrator for intelligent orchestration
            orchestration_plan = await self.smarty_orchestrator.orchestrate_with_smarty(
                transcript=enhanced_transcript,
                user_id=request.user_id,
                orchestration_mode=request.orchestration_mode,
                code_generation_strategy=request.code_generation_strategy,
                ethical_validation_level=request.ethical_validation_level
            )
            
            # Extract app type from orchestration plan
            parsed_requirements = orchestration_plan.parsed_requirements
            response.app_type = parsed_requirements.get('app_type', 'web_app')
            response.complexity_level = parsed_requirements.get('complexity', 'medium')
            
            logger.info(f"App generation orchestration completed", 
                       request_id=request.request_id,
                       app_type=response.app_type,
                       complexity_level=response.complexity_level,
                       confidence=orchestration_plan.confidence)
            
            return {
                'plan_id': orchestration_plan.plan_id,
                'parsed_requirements': parsed_requirements,
                'development_plan': orchestration_plan.development_plan,
                'steps': orchestration_plan.steps,
                'confidence': orchestration_plan.confidence,
                'estimated_timeline': orchestration_plan.estimated_timeline,
                'smarty_integration': orchestration_plan.smarty_integration,
                'ethical_validation': orchestration_plan.ethical_validation
            }
            
        except Exception as e:
            logger.error(f"App generation orchestration failed", 
                        error=str(e), 
                        request_id=request.request_id)
            raise

    async def _generate_app_from_plan(self, 
                                    orchestration_plan: Dict[str, Any], 
                                    request: VoiceToAppRequest,
                                    response: VoiceToAppResponse) -> Dict[str, Any]:
        """Generate the actual app from orchestration plan"""
        try:
            logger.info(f"Generating app from plan", 
                       request_id=request.request_id,
                       plan_id=orchestration_plan.get('plan_id'))
            
            # Extract code generation results from orchestration plan
            smarty_integration = orchestration_plan.get('smarty_integration', {})
            code_generation_results = smarty_integration.get('code_generation_results', {})
            
            # Organize generated code by components
            generated_code = code_generation_results.get('generated_code', {})
            
            # Create app structure
            app_structure = {
                'app_id': str(uuid.uuid4()),
                'app_name': self._generate_app_name(response.app_type, request.user_id),
                'app_type': response.app_type,
                'complexity_level': response.complexity_level,
                'generated_components': {},
                'file_structure': {},
                'dependencies': [],
                'configuration': {},
                'documentation': {},
                'quality_metrics': code_generation_results.get('quality_metrics', {}),
                'validation_results': code_generation_results.get('validation_results', {})
            }
            
            # Process generated code by task
            for task_id, code_data in generated_code.items():
                task_info = code_data.get('task_info', {})
                code_type = task_info.get('code_type', 'general')
                step_id = task_info.get('step_id', 'unknown')
                code = code_data.get('code', '')
                validation = code_data.get('validation', {})
                
                # Organize by component type
                if code_type not in app_structure['generated_components']:
                    app_structure['generated_components'][code_type] = []
                
                app_structure['generated_components'][code_type].append({
                    'task_id': task_id,
                    'step_id': step_id,
                    'code': code,
                    'validation': validation,
                    'file_path': self._determine_file_path(code_type, step_id)
                })
            
            # Generate file structure
            app_structure['file_structure'] = self._generate_file_structure(
                app_structure['generated_components']
            )
            
            # Extract dependencies
            app_structure['dependencies'] = self._extract_dependencies(
                app_structure['generated_components']
            )
            
            # Generate configuration
            app_structure['configuration'] = self._generate_app_configuration(
                orchestration_plan, request
            )
            
            # Generate documentation
            app_structure['documentation'] = self._generate_app_documentation(
                orchestration_plan, app_structure
            )
            
            logger.info(f"App generation completed", 
                       request_id=request.request_id,
                       app_id=app_structure['app_id'],
                       components_count=len(app_structure['generated_components']),
                       files_count=len(app_structure['file_structure']))
            
            return app_structure
            
        except Exception as e:
            logger.error(f"App generation from plan failed", 
                        error=str(e), 
                        request_id=request.request_id)
            raise

    def _generate_app_name(self, app_type: str, user_id: str) -> str:
        """Generate app name based on type and user"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        app_names = {
            'todo_app': 'TodoMaster',
            'blog_app': 'BlogBuilder',
            'ecommerce_app': 'ShopBuilder',
            'social_app': 'SocialConnect',
            'web_app': 'WebApp'
        }
        base_name = app_names.get(app_type, 'CustomApp')
        return f"{base_name}_{user_id[:8]}_{timestamp}"

    def _determine_file_path(self, code_type: str, step_id: str) -> str:
        """Determine file path for generated code"""
        path_mapping = {
            'frontend': f'frontend/src/components/{step_id}.tsx',
            'backend': f'backend/app/{step_id}.py',
            'database': f'backend/database/{step_id}.sql',
            'test': f'tests/{step_id}_test.py',
            'config': f'config/{step_id}.json',
            'general': f'src/{step_id}.py'
        }
        return path_mapping.get(code_type, f'src/{step_id}.py')

    def _generate_file_structure(self, components: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Generate file structure for the app"""
        file_structure = {
            'frontend': {},
            'backend': {},
            'database': {},
            'tests': {},
            'config': {},
            'docs': {}
        }
        
        for component_type, component_list in components.items():
            for component in component_list:
                file_path = component['file_path']
                file_structure[component_type][file_path] = {
                    'content': component['code'],
                    'size': len(component['code']),
                    'validation_score': component['validation'].get('overall_score', 0.0)
                }
        
        return file_structure

    def _extract_dependencies(self, components: Dict[str, List[Dict]]) -> List[str]:
        """Extract dependencies from generated code"""
        dependencies = set()
        
        for component_list in components.values():
            for component in component_list:
                code = component['code']
                
                # Extract Python imports
                if 'import ' in code:
                    lines = code.split('\n')
                    for line in lines:
                        if line.strip().startswith('import ') or line.strip().startswith('from '):
                            import_part = line.strip().split(' ')[1].split('.')[0]
                            dependencies.add(import_part)
                
                # Extract Node.js dependencies
                if 'require(' in code or 'import ' in code:
                    # Simple extraction - in real implementation, use AST parsing
                    if 'react' in code.lower():
                        dependencies.add('react')
                    if 'express' in code.lower():
                        dependencies.add('express')
        
        return list(dependencies)

    def _generate_app_configuration(self, 
                                  orchestration_plan: Dict[str, Any], 
                                  request: VoiceToAppRequest) -> Dict[str, Any]:
        """Generate app configuration"""
        parsed_requirements = orchestration_plan.get('parsed_requirements', {})
        
        return {
            'app_name': self._generate_app_name(parsed_requirements.get('app_type', 'web_app'), request.user_id),
            'version': '1.0.0',
            'description': f"Generated from voice: {response.transcript[:100]}...",
            'author': request.user_id,
            'created_at': datetime.now().isoformat(),
            'language': request.language,
            'complexity_level': request.complexity_level,
            'app_type': parsed_requirements.get('app_type', 'web_app'),
            'features': parsed_requirements.get('features', []),
            'platform': parsed_requirements.get('platform', 'web'),
            'target_audience': parsed_requirements.get('target_audience', 'general'),
            'ethical_validation_level': request.ethical_validation_level,
            'orchestration_mode': request.orchestration_mode.value,
            'code_generation_strategy': request.code_generation_strategy.value
        }

    def _generate_app_documentation(self, 
                                  orchestration_plan: Dict[str, Any], 
                                  app_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Generate app documentation"""
        parsed_requirements = orchestration_plan.get('parsed_requirements', {})
        development_plan = orchestration_plan.get('development_plan', {})
        
        return {
            'readme': {
                'title': f"{app_structure['app_name']} - Voice Generated App",
                'description': f"App generated from voice command with {app_structure['complexity_level']} complexity",
                'features': parsed_requirements.get('features', []),
                'installation': 'See deployment instructions',
                'usage': 'Follow the generated documentation',
                'api_docs': 'Available in the generated API documentation'
            },
            'api_documentation': {
                'endpoints': self._extract_api_endpoints(app_structure['generated_components']),
                'models': self._extract_data_models(app_structure['generated_components']),
                'authentication': 'See generated auth implementation'
            },
            'deployment_guide': {
                'requirements': app_structure['dependencies'],
                'environment_variables': self._extract_env_vars(app_structure['generated_components']),
                'deployment_steps': development_plan.get('deployment_steps', [])
            },
            'user_guide': {
                'getting_started': 'Follow the installation guide',
                'features': parsed_requirements.get('features', []),
                'troubleshooting': 'See generated troubleshooting guide'
            }
        }

    def _extract_api_endpoints(self, components: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """Extract API endpoints from generated code"""
        endpoints = []
        
        for component_list in components.get('backend', []):
            code = component_list['code']
            if '@app.' in code or '@router.' in code:
                # Simple extraction - in real implementation, use AST parsing
                lines = code.split('\n')
                for line in lines:
                    if '@app.' in line or '@router.' in line:
                        method = line.split('.')[1].split('(')[0]
                        endpoint = line.split('"')[1] if '"' in line else '/unknown'
                        endpoints.append({
                            'method': method.upper(),
                            'endpoint': endpoint,
                            'description': 'Generated endpoint'
                        })
        
        return endpoints

    def _extract_data_models(self, components: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """Extract data models from generated code"""
        models = []
        
        for component_list in components.get('backend', []):
            code = component_list['code']
            if 'class ' in code and 'BaseModel' in code:
                # Simple extraction - in real implementation, use AST parsing
                lines = code.split('\n')
                class_name = None
                for line in lines:
                    if 'class ' in line and 'BaseModel' in line:
                        class_name = line.split('class ')[1].split('(')[0].strip()
                        models.append({
                            'name': class_name,
                            'description': 'Generated model',
                            'fields': []  # Would extract from code in real implementation
                        })
                        break
        
        return models

    def _extract_env_vars(self, components: Dict[str, List[Dict]]) -> List[str]:
        """Extract environment variables from generated code"""
        env_vars = set()
        
        for component_list in components.values():
            for component in component_list:
                code = component['code']
                if 'os.getenv(' in code or 'os.environ.get(' in code:
                    lines = code.split('\n')
                    for line in lines:
                        if 'os.getenv(' in line:
                            var_name = line.split('os.getenv("')[1].split('"')[0]
                            env_vars.add(var_name)
                        elif 'os.environ.get(' in line:
                            var_name = line.split('os.environ.get("')[1].split('"')[0]
                            env_vars.add(var_name)
        
        return list(env_vars)

    async def _deploy_generated_app(self, 
                                  generated_app: Dict[str, Any], 
                                  request: VoiceToAppRequest,
                                  response: VoiceToAppResponse) -> Dict[str, Any]:
        """Deploy the generated app"""
        try:
            logger.info(f"Deploying generated app", 
                       request_id=request.request_id,
                       app_id=generated_app['app_id'])
            
            # For now, return deployment information
            # In a real implementation, this would deploy to Vercel, Netlify, etc.
            deployment_info = {
                'deployment_id': str(uuid.uuid4()),
                'app_id': generated_app['app_id'],
                'status': 'ready_for_deployment',
                'deployment_url': f"https://{generated_app['app_name'].lower()}.vercel.app",
                'deployment_platform': 'vercel',
                'deployment_steps': [
                    '1. Initialize git repository',
                    '2. Push code to GitHub',
                    '3. Connect to Vercel',
                    '4. Deploy automatically'
                ],
                'environment_variables': self._extract_env_vars(generated_app['generated_components']),
                'deployment_commands': [
                    'npm install',
                    'npm run build',
                    'vercel deploy'
                ],
                'monitoring_url': f"https://{generated_app['app_name'].lower()}-monitor.vercel.app"
            }
            
            logger.info(f"App deployment prepared", 
                       request_id=request.request_id,
                       deployment_id=deployment_info['deployment_id'],
                       deployment_url=deployment_info['deployment_url'])
            
            return deployment_info
            
        except Exception as e:
            logger.error(f"App deployment preparation failed", 
                        error=str(e), 
                        request_id=request.request_id)
            return {
                'status': 'deployment_failed',
                'error': str(e)
            }

    async def _calculate_quality_metrics(self, 
                                       transcript: str, 
                                       orchestration_plan: Dict[str, Any], 
                                       generated_app: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate quality metrics for the voice-to-app generation"""
        try:
            metrics = {
                'transcript_quality': {
                    'length': len(transcript),
                    'clarity_score': min(1.0, len(transcript) / 100),  # Simple heuristic
                    'language_detection': 'success'
                },
                'orchestration_quality': {
                    'confidence_score': orchestration_plan.get('confidence', 0.0),
                    'plan_completeness': len(orchestration_plan.get('steps', [])) / 10.0,
                    'requirements_parsing': 'success'
                },
                'code_quality': generated_app.get('quality_metrics', {}),
                'validation_quality': generated_app.get('validation_results', {}),
                'overall_quality_score': 0.0
            }
            
            # Calculate overall quality score
            transcript_score = metrics['transcript_quality']['clarity_score']
            orchestration_score = metrics['orchestration_quality']['confidence_score']
            code_score = metrics['code_quality'].get('overall_quality_score', 0.0)
            
            metrics['overall_quality_score'] = (
                transcript_score * 0.2 + 
                orchestration_score * 0.3 + 
                code_score * 0.5
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Quality metrics calculation failed", error=str(e))
            return {'overall_quality_score': 0.0, 'error': str(e)}

    def _update_metrics(self, response: VoiceToAppResponse):
        """Update service metrics"""
        try:
            self.metrics['total_requests'] += 1
            
            if response.status == 'completed':
                self.metrics['successful_generations'] += 1
                
                # Update average execution time
                total_completed = self.metrics['successful_generations']
                current_avg_time = self.metrics['average_execution_time']
                new_avg_time = ((current_avg_time * (total_completed - 1)) + response.execution_time) / total_completed
                self.metrics['average_execution_time'] = new_avg_time
                
                # Update average confidence score
                current_avg_confidence = self.metrics['average_confidence_score']
                new_avg_confidence = ((current_avg_confidence * (total_completed - 1)) + response.confidence_score) / total_completed
                self.metrics['average_confidence_score'] = new_avg_confidence
                
                # Update average quality score
                current_avg_quality = self.metrics['average_quality_score']
                quality_score = response.quality_metrics.get('overall_quality_score', 0.0)
                new_avg_quality = ((current_avg_quality * (total_completed - 1)) + quality_score) / total_completed
                self.metrics['average_quality_score'] = new_avg_quality
            else:
                self.metrics['failed_generations'] += 1
                
        except Exception as e:
            logger.error(f"Metrics update failed", error=str(e))

    async def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a voice-to-app request"""
        try:
            # Check active requests
            if request_id in self.active_requests:
                request = self.active_requests[request_id]
                return {
                    'request_id': request_id,
                    'status': 'processing',
                    'created_at': request.created_at.isoformat(),
                    'user_id': request.user_id,
                    'language': request.language
                }
            
            # Check completed responses
            if request_id in self.completed_responses:
                response = self.completed_responses[request_id]
                return {
                    'request_id': request_id,
                    'status': response.status,
                    'created_at': response.created_at.isoformat(),
                    'completed_at': response.completed_at.isoformat() if response.completed_at else None,
                    'user_id': response.user_id,
                    'execution_time': response.execution_time,
                    'confidence_score': response.confidence_score,
                    'app_type': response.app_type,
                    'transcript': response.transcript[:100] + '...' if response.transcript else None
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Status retrieval failed for request {request_id}", error=str(e))
            return None

    async def get_service_metrics(self) -> Dict[str, Any]:
        """Get service performance metrics"""
        try:
            return {
                'service_metrics': self.metrics,
                'active_requests_count': len(self.active_requests),
                'completed_responses_count': len(self.completed_responses),
                'success_rate': (
                    self.metrics['successful_generations'] / 
                    max(1, self.metrics['total_requests'])
                ) * 100
            }
            
        except Exception as e:
            logger.error(f"Service metrics retrieval failed", error=str(e))
            return {}

# Global instance
enhanced_voice_to_app_service = EnhancedVoiceToAppService()

# Backward compatibility: Create a simplified VoiceService wrapper
class VoiceService:
    """Backward compatibility wrapper for old VoiceService imports"""
    def __init__(self):
        self._service = EnhancedVoiceToAppService()
    
    async def transcribe_local(self, audio_file, language: str = "en") -> str:
        """Transcribe audio using local/browser processing"""
        return await self._service._transcribe_audio_inline(audio_file, language)
    
    async def transcribe_cloud(self, audio_file, language: str = "en") -> str:
        """Transcribe audio using cloud processing"""
        return await self._service._transcribe_audio_inline(audio_file, language)
    
    async def store_voice_command(self, user_id: str, transcript: str, language: str, confidence: float) -> str:
        """Store voice command (compatibility method)"""
        return str(uuid.uuid4())
    
    async def get_voice_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get voice command history (compatibility method)"""
        return []
    
    async def get_user_quota(self, user_id: str) -> Dict[str, Any]:
        """Get user quota (compatibility method)"""
        return {"remaining": 10, "total": 10}
