"""
Run all refactoring tests to verify complete success
"""

import sys
import os
import asyncio
import subprocess

def run_test(test_file):
    """Run a test file and return results"""
    print(f"\nRunning {test_file}...")
    print("-" * 60)
    
    result = subprocess.run(
        [sys.executable, test_file],
        cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        capture_output=False
    )
    
    return result.returncode == 0


def main():
    print("\n" + "="*60)
    print("RUNNING ALL REFACTORING TESTS")
    print("="*60)
    
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    tests = [
        os.path.join(test_dir, "test_chunk_a_models.py"),
        os.path.join(test_dir, "test_chunk_b_core.py"),
        os.path.join(test_dir, "test_chunk_c_analyzers.py"),
        os.path.join(test_dir, "test_chunk_d_managers.py"),
        os.path.join(test_dir, "test_chunk_e_infrastructure.py")
    ]
    
    results = {}
    
    for test in tests:
        test_name = os.path.basename(test)
        passed = run_test(test)
        results[test_name] = passed
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("SUCCESS: All refactoring tests passed!")
        print("Refactoring complete and verified!")
        print("="*60)
        return 0
    else:
        print("FAILURE: Some tests failed")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
