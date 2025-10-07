"""
Test Chunk F: Orchestration Models
Verifies that orchestration models work correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_orchestration_models():
    """Test all orchestration models work correctly"""
    
    print("\n" + "="*60)
    print("CHUNK F: ORCHESTRATION MODELS TEST")
    print("="*60)
    
    # Test 1: Import models
    print("\n[TEST] Importing orchestration models...")
    from app.services.ai_orchestration.models import (
        OrchestrationMode,
        ValidationLevel,
        OrchestrationPriority,
        EngineType,
        OrchestrationRequest,
        OrchestrationResponse,
        ValidationResult
    )
    
    print("  [PASS] All models imported successfully")
    
    # Test 2: Test enums
    print("\n[TEST] Testing enums...")
    assert OrchestrationMode.HIERARCHICAL.value == "hierarchical"
    assert ValidationLevel.SIX_SIGMA.value == "six_sigma"
    assert OrchestrationPriority.CRITICAL.value == "critical"
    assert EngineType.LEARNING.value == "learning"
    print("  [PASS] All enums work correctly")
    
    # Test 3: Test OrchestrationRequest
    print("\n[TEST] Testing OrchestrationRequest...")
    request = OrchestrationRequest(
        request_id="test-123",
        code="def test(): pass",
        language="python",
        validation_level=ValidationLevel.SIX_SIGMA,
        orchestration_mode=OrchestrationMode.HIERARCHICAL
    )
    
    assert request.request_id == "test-123"
    assert request.validation_level == ValidationLevel.SIX_SIGMA
    assert request.created_at is not None
    print("  [PASS] OrchestrationRequest works with Six Sigma level")
    
    # Test 4: Test OrchestrationResponse
    print("\n[TEST] Testing OrchestrationResponse...")
    response = OrchestrationResponse(
        request_id="test-123",
        validation_results={"passed": True},
        overall_score=0.9999966,  # Six Sigma
        passed=True
    )
    
    assert response.overall_score == 0.9999966
    assert response.passed == True
    assert response.completed_at is not None
    print("  [PASS] OrchestrationResponse works with Six Sigma score")
    
    # Test 5: Test ValidationResult
    print("\n[TEST] Testing ValidationResult...")
    result = ValidationResult(
        category="factual_accuracy",
        passed=True,
        score=0.99,
        issues=[],
        suggestions=[],
        metrics={"accuracy": 99.0},
        processing_time=0.15,
        validator_name="FactualAccuracyValidator"
    )
    
    assert result.category == "factual_accuracy"
    assert result.passed == True
    assert result.timestamp is not None
    print("  [PASS] ValidationResult works")
    
    # Test 6: Test all 9 engine types
    print("\n[TEST] Testing all engine types...")
    engine_types = list(EngineType)
    assert len(engine_types) == 9
    assert EngineType.LEARNING in engine_types
    assert EngineType.INNOVATION in engine_types
    print(f"  [PASS] All {len(engine_types)} engine types defined")
    
    # Test 7: Test all validation levels
    print("\n[TEST] Testing validation levels...")
    validation_levels = list(ValidationLevel)
    assert ValidationLevel.SIX_SIGMA in validation_levels
    assert ValidationLevel.MAXIMUM in validation_levels
    print(f"  [PASS] All {len(validation_levels)} validation levels defined")
    
    # Test 8: Test orchestration modes
    print("\n[TEST] Testing orchestration modes...")
    modes = list(OrchestrationMode)
    assert OrchestrationMode.HIERARCHICAL in modes  # 6 levels preserved
    assert OrchestrationMode.PARALLEL in modes
    print(f"  [PASS] All {len(modes)} orchestration modes defined")
    
    print("\n" + "="*60)
    print("CHUNK F: ALL ORCHESTRATION MODEL TESTS PASSED!")
    print("Models successfully created and verified")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        test_orchestration_models()
        
        print("\n" + "="*60)
        print("SUCCESS: Chunk F (Orchestration Models) verified!")
        print("Ready to proceed with validators extraction.")
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
