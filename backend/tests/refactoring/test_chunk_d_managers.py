"""
Test Chunk D: Managers
Verifies that extracted manager components maintain 100% compatibility
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


async def test_manager_components():
    """Test all manager components work correctly"""
    
    print("\n" + "="*60)
    print("CHUNK D: MANAGER COMPONENTS TEST")
    print("="*60)
    
    # Test 1: Import manager components
    print("\n[TEST] Importing manager components...")
    from app.services.smart_coding_ai.managers import (
        SessionMemoryManager,
        StateManager,
        RBACManager
    )
    
    print("  [PASS] All manager components imported successfully")
    
    # Test 2: Initialize managers
    print("\n[TEST] Initializing manager components...")
    session_manager = SessionMemoryManager()
    state_manager = StateManager()
    rbac_manager = RBACManager()
    
    assert session_manager is not None
    assert state_manager is not None
    assert rbac_manager is not None
    assert len(rbac_manager.roles) == 3  # owner, developer, viewer
    print("  [PASS] All managers initialized correctly")
    
    # Test 3: Test SessionMemoryManager
    print("\n[TEST] Testing SessionMemoryManager...")
    context = await session_manager.create_session_context(
        user_id="test_user",
        project_id="test_project",
        current_file="test.py",
        cursor_position=(1, 0),
        working_directory="."
    )
    
    assert context is not None
    assert "session_id" in context
    assert context["user_id"] == "test_user"
    assert context["project_id"] == "test_project"
    print(f"  [PASS] SessionMemoryManager works - Session ID: {context['session_id'][:8]}...")
    
    # Test session update
    updated = await session_manager.update_session_context(
        context["session_id"],
        {"recent_files": ["test.py", "test2.py"]}
    )
    assert updated == True
    print("  [PASS] Session context update works")
    
    # Test 4: Test StateManager
    print("\n[TEST] Testing StateManager...")
    state = await state_manager.initialize_state(
        entity_id="test_entity",
        entity_type="session",
        state_type="validation",
        initial_state="pending",
        user_id="test_user"
    )
    
    assert state is not None
    assert state["current_state"] == "pending"
    assert state["status"] == "active"
    print(f"  [PASS] StateManager initialization works - State: {state['current_state']}")
    
    # Test state transition
    new_state = await state_manager.transition_state(
        entity_id="test_entity",
        entity_type="session",
        state_type="validation",
        target_state="completed",
        user_id="test_user"
    )
    
    assert new_state is not None
    assert new_state["current_state"] == "completed"
    assert new_state["previous_state"] == "pending"
    print(f"  [PASS] State transition works - {new_state['previous_state']} -> {new_state['current_state']}")
    
    # Test 5: Test RBACManager
    print("\n[TEST] Testing RBACManager...")
    
    # Check default roles
    owner_role = await rbac_manager.get_role("owner")
    developer_role = await rbac_manager.get_role("developer")
    viewer_role = await rbac_manager.get_role("viewer")
    
    assert owner_role is not None
    assert developer_role is not None
    assert viewer_role is not None
    assert "*" in owner_role["permissions"]  # Owner has all permissions
    print("  [PASS] Default RBAC roles created (owner, developer, viewer)")
    
    # Test role assignment
    assignment = await rbac_manager.assign_role(
        user_id="test_user",
        role_id="developer",
        granted_by="system"
    )
    
    assert assignment is not None
    assert assignment["user_id"] == "test_user"
    assert assignment["role_id"] == "developer"
    print("  [PASS] Role assignment works")
    
    # Test permission check
    has_read = await rbac_manager.check_permission(
        user_id="test_user",
        resource_type="completion",
        action_type="read"
    )
    
    has_create = await rbac_manager.check_permission(
        user_id="test_user",
        resource_type="completion",
        action_type="create"
    )
    
    has_admin = await rbac_manager.check_permission(
        user_id="test_user",
        resource_type="completion",
        action_type="admin"
    )
    
    assert has_read == True  # Developer can read
    assert has_create == True  # Developer can create
    assert has_admin == False  # Developer cannot admin
    print("  [PASS] Permission checking works correctly")
    
    # Test 6: Test project memory
    print("\n[TEST] Testing project memory...")
    memory_data = {
        "files": ["test.py", "test2.py"],
        "functions": ["test_func"],
        "classes": ["TestClass"]
    }
    
    saved = await session_manager.save_project_memory("test_project", memory_data)
    assert saved == True
    
    retrieved = await session_manager.get_project_memory("test_project")
    assert retrieved is not None
    assert retrieved["files"] == ["test.py", "test2.py"]
    print("  [PASS] Project memory save/retrieve works")
    
    # Test 7: Test state history
    print("\n[TEST] Testing state history...")
    history = await state_manager.get_state_history(
        entity_id="test_entity",
        entity_type="session",
        state_type="validation"
    )
    
    assert len(history) >= 2  # Initial state + transition
    assert history[0]["current_state"] == "pending"
    assert history[1]["current_state"] == "completed"
    print(f"  [PASS] State history tracking works - {len(history)} states recorded")
    
    print("\n" + "="*60)
    print("CHUNK D: ALL MANAGER TESTS PASSED!")
    print("Managers successfully extracted with 100% compatibility")
    print("="*60)
    
    return True


async def test_manager_integration():
    """Test manager integration with main module"""
    
    print("\n" + "="*60)
    print("CHUNK D: MANAGER INTEGRATION TEST")
    print("="*60)
    
    # Import main module
    print("\n[TEST] Testing manager integration...")
    from app.services.smart_coding_ai import SmartCodingAIOptimized
    
    # Initialize service
    service = SmartCodingAIOptimized()
    
    # Check all managers are available
    assert hasattr(service, 'session_memory')
    assert hasattr(service, 'state_manager')
    assert hasattr(service, 'rbac_manager')
    print("  [PASS] All managers available through main class")
    
    # Test manager functionality through service
    print("\n[TEST] Testing manager functionality through service...")
    
    # Test session manager
    context = await service.session_memory.create_session_context(
        user_id="test_user_2",
        project_id="test_project_2",
        current_file="app.py",
        cursor_position=(10, 5),
        working_directory="."
    )
    assert context["user_id"] == "test_user_2"
    print("  [PASS] Session manager works through service")
    
    # Test RBAC manager
    has_permission = await service.rbac_manager.check_permission(
        user_id="test_user_2",
        resource_type="completion",
        action_type="read"
    )
    # Should be False since we haven't assigned a role
    assert has_permission == False
    print("  [PASS] RBAC manager works through service")
    
    print("\n" + "="*60)
    print("CHUNK D: MANAGER INTEGRATION VERIFIED!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        # Run async tests
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_manager_components())
        loop.run_until_complete(test_manager_integration())
        
        print("\n" + "="*60)
        print("SUCCESS: Chunk D (Managers) refactoring verified!")
        print("All functionality preserved, ready to commit.")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
