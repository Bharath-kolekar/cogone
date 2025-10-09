"""
Comprehensive Phase 2 Testing
Tests all modules, imports, endpoints, and functionality
"""

import asyncio
import sys

print("="*70)
print("COMPREHENSIVE PHASE 2 TESTING")
print("="*70)
print()

# Track results
tests_passed = 0
tests_failed = 0
errors = []

def test_result(name, passed, error=None):
    global tests_passed, tests_failed, errors
    if passed:
        print(f"✓ {name}")
        tests_passed += 1
    else:
        print(f"✗ {name}: {error}")
        tests_failed += 1
        errors.append(f"{name}: {error}")

# ============================================================================
# TEST 1: Module Imports
# ============================================================================
print("TEST 1: Individual Module Imports")
print("-" * 70)

try:
    from app.services.smart_coding_ai.whatsapp_integration import WhatsAppIntegration
    test_result("whatsapp_integration.py import", True)
except Exception as e:
    test_result("whatsapp_integration.py import", False, str(e))

try:
    from app.services.smart_coding_ai.session_manager import SessionManager
    test_result("session_manager.py import", True)
except Exception as e:
    test_result("session_manager.py import", False, str(e))

try:
    from app.services.smart_coding_ai.voice_to_code import VoiceToCodeProcessor
    test_result("voice_to_code.py import", True)
except Exception as e:
    test_result("voice_to_code.py import", False, str(e))

try:
    from app.services.smart_coding_ai.chat_assistant import ChatAssistantIntegration
    test_result("chat_assistant.py import", True)
except Exception as e:
    test_result("chat_assistant.py import", False, str(e))

try:
    from app.services.smart_coding_ai.task_orchestration import TaskOrchestrator
    test_result("task_orchestration.py import", True)
except Exception as e:
    test_result("task_orchestration.py import", False, str(e))

try:
    from app.services.smart_coding_ai.core_orchestrators import CoreOrchestratorsIntegration
    test_result("core_orchestrators.py import", True)
except Exception as e:
    test_result("core_orchestrators.py import", False, str(e))

try:
    from app.services.smart_coding_ai.advanced_orchestrators import AdvancedOrchestratorsIntegration
    test_result("advanced_orchestrators.py import", True)
except Exception as e:
    test_result("advanced_orchestrators.py import", False, str(e))

try:
    from app.services.smart_coding_ai.specialized_orchestrators import SpecializedOrchestratorsIntegration
    test_result("specialized_orchestrators.py import", True)
except Exception as e:
    test_result("specialized_orchestrators.py import", False, str(e))

try:
    from app.services.smart_coding_ai.core import SmartCodingAIIntegration
    test_result("core.py import", True)
except Exception as e:
    test_result("core.py import", False, str(e))

print()

# ============================================================================
# TEST 2: Backward Compatibility
# ============================================================================
print("TEST 2: Backward Compatibility")
print("-" * 70)

try:
    from app.services.smart_coding_ai_integration import SmartCodingAIIntegration as OldImport
    test_result("OLD import path (smart_coding_ai_integration)", True)
except Exception as e:
    test_result("OLD import path", False, str(e))

try:
    from app.services.smart_coding_ai import SmartCodingAIIntegration as NewImport
    test_result("NEW import path (smart_coding_ai)", True)
except Exception as e:
    test_result("NEW import path", False, str(e))

try:
    from app.services.smart_coding_ai_integration import AIIntegrationContext
    test_result("AIIntegrationContext from OLD path", True)
except Exception as e:
    test_result("AIIntegrationContext from OLD path", False, str(e))

try:
    from app.services.ai_integration_types import AIIntegrationContext
    test_result("AIIntegrationContext from types module", True)
except Exception as e:
    test_result("AIIntegrationContext from types", False, str(e))

print()

# ============================================================================
# TEST 3: Module Instantiation
# ============================================================================
print("TEST 3: Module Instantiation")
print("-" * 70)

try:
    from app.services.smart_coding_ai.whatsapp_integration import WhatsAppIntegration
    w = WhatsAppIntegration()
    test_result("WhatsAppIntegration() instantiation", True)
except Exception as e:
    test_result("WhatsAppIntegration() instantiation", False, str(e))

try:
    from app.services.smart_coding_ai.session_manager import SessionManager
    s = SessionManager()
    test_result("SessionManager() instantiation", True)
except Exception as e:
    test_result("SessionManager() instantiation", False, str(e))

try:
    class MockAI:
        async def chat_with_codebase(self, **kw): return {}
        async def search_codebase_memory(self, **kw): return {}
        async def get_contextual_suggestions(self, **kw): return []
    
    from app.services.smart_coding_ai.voice_to_code import VoiceToCodeProcessor
    v = VoiceToCodeProcessor(smart_coding_ai=MockAI())
    test_result("VoiceToCodeProcessor() instantiation", True)
except Exception as e:
    test_result("VoiceToCodeProcessor() instantiation", False, str(e))

try:
    from app.services.smart_coding_ai.chat_assistant import ChatAssistantIntegration
    c = ChatAssistantIntegration(smart_coding_ai=MockAI())
    test_result("ChatAssistantIntegration() instantiation", True)
except Exception as e:
    test_result("ChatAssistantIntegration() instantiation", False, str(e))

try:
    from app.services.smart_coding_ai.task_orchestration import TaskOrchestrator
    t = TaskOrchestrator(smart_coding_ai=MockAI())
    test_result("TaskOrchestrator() instantiation", True)
except Exception as e:
    test_result("TaskOrchestrator() instantiation", False, str(e))

print()

# ============================================================================
# TEST 4: Main Integration Class
# ============================================================================
print("TEST 4: Main Integration Class")
print("-" * 70)

try:
    from app.services.smart_coding_ai import smart_coding_ai_integration
    test_result("Global instance available", smart_coding_ai_integration is not None)
except Exception as e:
    test_result("Global instance", False, str(e))

try:
    from app.services.smart_coding_ai import SmartCodingAIIntegration
    integration = SmartCodingAIIntegration()
    test_result("SmartCodingAIIntegration() creation", True)
except Exception as e:
    test_result("SmartCodingAIIntegration() creation", False, str(e))

# Check methods exist
try:
    from app.services.smart_coding_ai import smart_coding_ai_integration
    methods = [
        'process_voice_to_code',
        'chat_with_ai_assistant',
        'orchestrate_smart_coding_task',
        'integrate_with_core_orchestrators',
        'integrate_with_advanced_ai_systems',
        'process_whatsapp_message',
        'create_integration_session',
        'get_session_context',
        'get_integrated_components_status'
    ]
    
    all_exist = all(hasattr(smart_coding_ai_integration, m) for m in methods)
    test_result("All public methods exist", all_exist)
except Exception as e:
    test_result("Public methods check", False, str(e))

print()

# ============================================================================
# TEST 5: Session Management
# ============================================================================
print("TEST 5: Session Management Functionality")
print("-" * 70)

async def test_session():
    try:
        from app.services.smart_coding_ai.session_manager import SessionManager
        manager = SessionManager()
        
        # Create session
        session_id = await manager.create_session('test_user', 'test_project')
        test_result("Session creation", session_id is not None)
        
        # Get context
        context = await manager.get_context(session_id)
        test_result("Session context retrieval", context is not None and context.user_id == 'test_user')
        
        # Update context
        updated = await manager.update_context(session_id, {'operation_type': 'test'})
        test_result("Session context update", updated == True)
        
        # Get status
        status = manager.get_status()
        test_result("Session manager status", status['active_sessions'] == 1)
        
    except Exception as e:
        test_result("Session management tests", False, str(e))

asyncio.run(test_session())

print()

# ============================================================================
# TEST 6: No Circular Dependencies
# ============================================================================
print("TEST 6: Circular Dependency Check")
print("-" * 70)

try:
    # Import in different orders
    from app.services.smart_coding_ai import SmartCodingAIIntegration as A1
    from app.services.smart_coding_ai.core import SmartCodingAIIntegration as A2
    from app.services.smart_coding_ai_integration import SmartCodingAIIntegration as A3
    test_result("No circular import errors", True)
except Exception as e:
    test_result("No circular import errors", False, str(e))

print()

# ============================================================================
# TEST 7: Endpoint Accessibility
# ============================================================================
print("TEST 7: Endpoint Accessibility")
print("-" * 70)

try:
    import requests
    
    # Test health endpoint
    response = requests.get("http://localhost:8000/health", timeout=5)
    test_result("Main health endpoint", response.status_code == 200)
    
    # Test integration health endpoint
    response = requests.get("http://localhost:8000/api/v1/smart-coding-ai/integration/health", timeout=5)
    data = response.json()
    test_result("Integration health endpoint", data.get("status") == "healthy")
    test_result("Service version 2.0.0", data.get("version") == "2.0.0")
    test_result("Modules reported in health", "whatsapp" in data.get("modules", {}))
    
except Exception as e:
    test_result("Endpoint tests", False, str(e))

print()

# ============================================================================
# FINAL RESULTS
# ============================================================================
print("="*70)
print("FINAL TEST RESULTS")
print("="*70)
print(f"Tests Passed: {tests_passed}")
print(f"Tests Failed: {tests_failed}")
print(f"Success Rate: {(tests_passed/(tests_passed+tests_failed)*100):.1f}%")
print()

if tests_failed == 0:
    print("✅ ALL TESTS PASSED! Phase 2 is production-ready!")
    sys.exit(0)
else:
    print("⚠ Some tests failed:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

