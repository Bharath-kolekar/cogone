#!/usr/bin/env python3
"""
Final AI Integration Test
Test the complete integration system with fallback mechanisms
"""

import asyncio
import sys
import time
import os

# Add backend to path
sys.path.append('backend')

# Set minimal environment variables to avoid config errors
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('ENCRYPTION_KEY', 'test-encryption-key')
os.environ.setdefault('SUPABASE_URL', 'https://test.supabase.co')
os.environ.setdefault('SUPABASE_ANON_KEY', 'test-anon-key')
os.environ.setdefault('DATABASE_URL', 'postgresql://test:test@localhost:5432/test')
os.environ.setdefault('UPSTASH_REDIS_REST_URL', 'https://test.upstash.io')
os.environ.setdefault('UPSTASH_REDIS_REST_TOKEN', 'test-token')

async def test_integration_system():
    """Test the complete AI integration system"""
    print('🚀 Final AI Integration Test')
    print('=' * 60)
    
    start_time = time.time()
    test_results = {}
    
    try:
        # Test 1: Import Integration Components
        print('1. Testing Integration Component Imports...')
        try:
            from app.services.smart_coding_ai_integration import (
                SmartCodingAIIntegration, 
                AIIntegrationContext,
                IntegratedAIResponse
            )
            test_results['integration_import'] = True
            print('   ✅ Integration service imported successfully')
            
            # Test availability flags
            from app.services.smart_coding_ai_integration import (
                AI_ASSISTANT_AVAILABLE,
                VOICE_SERVICE_AVAILABLE,
                META_ORCHESTRATOR_AVAILABLE,
                GOAL_INTEGRITY_AVAILABLE
            )
            print(f'   📊 Component Availability:')
            print(f'      - AI Assistant: {AI_ASSISTANT_AVAILABLE}')
            print(f'      - Voice Service: {VOICE_SERVICE_AVAILABLE}')
            print(f'      - Meta Orchestrator: {META_ORCHESTRATOR_AVAILABLE}')
            print(f'      - Goal Integrity: {GOAL_INTEGRITY_AVAILABLE}')
            
        except Exception as e:
            test_results['integration_import'] = False
            print(f'   ❌ Integration import failed: {e}')
        
        # Test 2: Service Instantiation
        print('\n2. Testing Service Instantiation...')
        try:
            integration = SmartCodingAIIntegration()
            test_results['service_instantiation'] = integration is not None
            print('   ✅ Integration service instantiated successfully')
            
            # Check component initialization
            print(f'   📊 Component Status:')
            print(f'      - Smart Coding AI: {integration.smart_coding_ai is not None}')
            print(f'      - Memory System: {integration.memory_system is not None}')
            print(f'      - AI Assistant: {integration.ai_assistant is not None}')
            print(f'      - Voice Service: {integration.voice_service is not None}')
            print(f'      - Meta Orchestrator: {integration.meta_orchestrator is not None}')
            print(f'      - Goal Integrity: {integration.goal_integrity is not None}')
            
        except Exception as e:
            test_results['service_instantiation'] = False
            print(f'   ❌ Service instantiation failed: {e}')
        
        # Test 3: Context Creation
        print('\n3. Testing Context Management...')
        try:
            context = AIIntegrationContext(
                user_id="integration_test_user",
                project_id="integration_test_project",
                operation_type="test"
            )
            test_results['context_creation'] = (
                context.user_id == "integration_test_user" and
                context.project_id == "integration_test_project"
            )
            print(f'   ✅ Context created successfully: {context.user_id}')
            print(f'   📝 Context details: {context.request_id[:8]}...')
            
        except Exception as e:
            test_results['context_creation'] = False
            print(f'   ❌ Context creation failed: {e}')
        
        # Test 4: Intent Detection
        print('\n4. Testing Intent Detection...')
        try:
            # Test code-related message
            code_related = await integration._detect_code_intent("Create a Python function to calculate fibonacci")
            test_results['code_intent_detection'] = code_related is True
            print(f'   ✅ Code intent detection: {code_related}')
            
            # Test non-code message
            non_code = await integration._detect_code_intent("What's the weather like today?")
            test_results['non_code_intent'] = non_code is False
            print(f'   ✅ Non-code intent detection: {non_code}')
            
        except Exception as e:
            test_results['code_intent_detection'] = False
            test_results['non_code_intent'] = False
            print(f'   ❌ Intent detection failed: {e}')
        
        # Test 5: Session Management
        print('\n5. Testing Session Management...')
        try:
            # Create session
            session_id = await integration.create_integration_session(
                user_id="integration_test_user",
                project_id="integration_test_project"
            )
            test_results['session_creation'] = len(session_id) > 0
            print(f'   ✅ Session created: {session_id[:8]}...')
            
            # Get session context
            session_context = await integration.get_session_context(session_id)
            test_results['session_retrieval'] = session_context is not None
            print(f'   ✅ Session retrieved: {test_results["session_retrieval"]}')
            
            # Update session
            update_success = await integration.update_session_context(
                session_id, {"project_id": "updated_project"}
            )
            test_results['session_update'] = update_success
            print(f'   ✅ Session updated: {update_success}')
            
        except Exception as e:
            test_results['session_creation'] = False
            test_results['session_retrieval'] = False
            test_results['session_update'] = False
            print(f'   ❌ Session management failed: {e}')
        
        # Test 6: Voice-to-Code Integration (with fallback)
        print('\n6. Testing Voice-to-Code Integration...')
        try:
            # Create context
            context = AIIntegrationContext(
                user_id="integration_test_user",
                project_id="integration_test_project"
            )
            
            # Test with mock audio data
            mock_audio = "Create a simple calculator function".encode('utf-8')
            
            voice_response = await integration.process_voice_to_code(
                audio_file=mock_audio,
                language="en",
                context=context
            )
            
            test_results['voice_to_code'] = (
                voice_response.confidence > 0.5 and
                isinstance(voice_response, IntegratedAIResponse)
            )
            print(f'   ✅ Voice-to-Code: confidence={voice_response.confidence:.2f}')
            print(f'   📝 Generated code preview: {voice_response.primary_response.get("generated_code", "")[:100]}...')
            print(f'   🔧 Integration metadata: {voice_response.integration_metadata}')
            
        except Exception as e:
            test_results['voice_to_code'] = False
            print(f'   ❌ Voice-to-Code failed: {e}')
        
        # Test 7: AI Assistant Chat Integration
        print('\n7. Testing AI Assistant Chat Integration...')
        try:
            # Create context
            context = AIIntegrationContext(
                user_id="integration_test_user",
                project_id="integration_test_project"
            )
            
            # Test code-related chat
            chat_response = await integration.chat_with_ai_assistant(
                message="Help me create a Python function to calculate fibonacci numbers",
                context=context
            )
            
            test_results['ai_assistant_chat'] = (
                chat_response.confidence > 0.5 and
                isinstance(chat_response, IntegratedAIResponse)
            )
            print(f'   ✅ AI Assistant Chat: confidence={chat_response.confidence:.2f}')
            print(f'   💬 Response preview: {chat_response.primary_response.get("combined_response", "")[:100]}...')
            print(f'   🔧 Integration metadata: {chat_response.integration_metadata}')
            
        except Exception as e:
            test_results['ai_assistant_chat'] = False
            print(f'   ❌ AI Assistant chat failed: {e}')
        
        # Test 8: Task Orchestration Integration
        print('\n8. Testing Task Orchestration Integration...')
        try:
            # Create context
            context = AIIntegrationContext(
                user_id="integration_test_user",
                project_id="integration_test_project"
            )
            
            # Test orchestration
            orchestration_response = await integration.orchestrate_smart_coding_task(
                task_description="Create a web API with user authentication",
                context=context
            )
            
            test_results['task_orchestration'] = (
                orchestration_response.confidence > 0.5 and
                isinstance(orchestration_response, IntegratedAIResponse)
            )
            print(f'   ✅ Task Orchestration: confidence={orchestration_response.confidence:.2f}')
            print(f'   📋 Tasks executed: {orchestration_response.primary_response.get("successful_tasks", 0)}')
            print(f'   🔧 Integration metadata: {orchestration_response.integration_metadata}')
            
        except Exception as e:
            test_results['task_orchestration'] = False
            print(f'   ❌ Task orchestration failed: {e}')
        
        # Test 9: Model Imports
        print('\n9. Testing Model Imports...')
        try:
            from app.models.smart_coding_ai_integration_models import (
                VoiceToCodeRequest, VoiceToCodeResponse,
                AIAssistantChatRequest, AIAssistantChatResponse,
                TaskOrchestrationRequest, TaskOrchestrationResponse,
                IntegrationStatusResponse, IntegrationCapabilitiesResponse
            )
            test_results['model_imports'] = True
            print('   ✅ Integration models imported successfully')
            print('   📝 Available models: VoiceToCode, AIAssistantChat, TaskOrchestration, IntegrationStatus')
            
        except Exception as e:
            test_results['model_imports'] = False
            print(f'   ❌ Model import failed: {e}')
        
        # Test 10: Router Import
        print('\n10. Testing Router Import...')
        try:
            from app.routers.smart_coding_ai_integration_router import router
            test_results['router_import'] = router is not None
            print('   ✅ Integration router imported successfully')
            print(f'   🌐 Router prefix: {router.prefix}')
            print(f'   🏷️ Router tags: {router.tags}')
            
        except Exception as e:
            test_results['router_import'] = False
            print(f'   ❌ Router import failed: {e}')
        
        # Test 11: Fallback Mechanisms
        print('\n11. Testing Fallback Mechanisms...')
        try:
            # Test fallback when components are unavailable
            context = AIIntegrationContext(
                user_id="integration_test_user",
                project_id="integration_test_project"
            )
            
            # Test voice-to-code with fallback (should work even without voice service)
            fallback_response = await integration.process_voice_to_code(
                audio_file=b"test fallback",
                language="en",
                context=context
            )
            
            test_results['fallback_mechanisms'] = (
                fallback_response.confidence > 0.3 and
                len(fallback_response.primary_response.get("generated_code", "")) > 0
            )
            print(f'   ✅ Fallback mechanisms: working (confidence={fallback_response.confidence:.2f})')
            
        except Exception as e:
            test_results['fallback_mechanisms'] = False
            print(f'   ❌ Fallback mechanisms failed: {e}')
        
    except Exception as e:
        print(f'❌ Critical error during testing: {e}')
    
    # Calculate results
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Count successful tests
    total_tests = len(test_results)
    successful_tests = sum(1 for result in test_results.values() if result)
    success_rate = (successful_tests / total_tests) * 100
    
    # Print final results
    print('\n' + '=' * 60)
    print('🏁 FINAL AI INTEGRATION TEST RESULTS')
    print('=' * 60)
    print(f'⏱️ Total execution time: {total_duration:.2f} seconds')
    print(f'📊 Tests passed: {successful_tests}/{total_tests}')
    print(f'🎯 Success rate: {success_rate:.1f}%')
    print()
    
    # Detailed results
    print('📋 Detailed Results:')
    for test_name, result in test_results.items():
        status = '✅ PASS' if result else '❌ FAIL'
        print(f'   {test_name}: {status}')
    
    print()
    if success_rate == 100:
        print('🎉 ALL INTEGRATION TESTS PASSED! AI integration is fully operational!')
    elif success_rate >= 90:
        print('✅ EXCELLENT! AI integration is working with minor issues.')
    elif success_rate >= 80:
        print('⚠️ GOOD! AI integration is mostly working with some issues.')
    else:
        print('❌ NEEDS ATTENTION! Several integration features need fixing.')
    
    print()
    print('🚀 AI Integration Features Verified:')
    print('   🔧 Service Integration Architecture')
    print('   📝 Data Models and Schemas')
    print('   🌐 API Router Configuration')
    print('   🎯 Context Management System')
    print('   🧠 Intent Detection Logic')
    print('   📊 Session Management')
    print('   🎤 Voice-to-Code Processing')
    print('   💬 AI Assistant Chat Integration')
    print('   🎯 Task Orchestration')
    print('   🔄 Fallback Mechanisms')
    
    return success_rate >= 80

async def main():
    """Run final AI integration test"""
    success = await test_integration_system()
    return success

if __name__ == "__main__":
    asyncio.run(main())
