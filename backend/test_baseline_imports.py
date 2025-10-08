"""
Baseline Import Test - Run this before and after each refactoring step
If this fails, revert immediately!
"""

import sys

def test_main_import():
    """Test that app.main can be imported"""
    try:
        from app.main import app
        return True, "[PASS] app.main imports successfully"
    except Exception as e:
        return False, f"[FAIL] app.main import failed: {e}"

def test_smart_coding_ai():
    """Test that smart_coding_ai_optimized can be imported"""
    try:
        from app.services.smart_coding_ai_optimized import SmartCodingAIOptimized
        return True, "[PASS] SmartCodingAIOptimized imports successfully"
    except Exception as e:
        return False, f"[FAIL] SmartCodingAIOptimized import failed: {e}"

def test_ai_orchestration():
    """Test that ai_orchestration_layer can be imported"""
    try:
        from app.services.ai_orchestration_layer import AIOrchestrationLayer
        return True, "[PASS] AIOrchestrationLayer imports successfully"
    except Exception as e:
        return False, f"[FAIL] AIOrchestrationLayer import failed: {e}"

def run_all_tests():
    """Run all baseline tests"""
    tests = [
        test_main_import,
        test_smart_coding_ai,
        test_ai_orchestration
    ]
    
    print("\n" + "="*60)
    print("BASELINE IMPORT TEST")
    print("="*60 + "\n")
    
    all_passed = True
    for test in tests:
        passed, message = test()
        print(message)
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("RESULT: ALL TESTS PASSED")
    else:
        print("RESULT: SOME TESTS FAILED")
        print("DO NOT PROCEED WITH REFACTORING!")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

