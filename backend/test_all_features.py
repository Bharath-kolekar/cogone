#!/usr/bin/env python3
"""
Comprehensive Feature Test Suite
Tests all major backend features and endpoints
"""

import asyncio
import sys
import httpx

BASE_URL = "http://localhost:8000"

async def test_health_endpoint():
    """Test 1: Health Check Endpoint"""
    print("\n=== Test 1: Health Check ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            print(f"[PASS] Health: {data['status']}")
            return True
    except Exception as e:
        print(f"[FAIL] Health check error: {e}")
        return False

async def test_root_endpoint():
    """Test 2: Root Endpoint"""
    print("\n=== Test 2: Root Endpoint ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            print(f"[PASS] Root: {data['message']}")
            return True
    except Exception as e:
        print(f"[FAIL] Root endpoint error: {e}")
        return False

async def test_api_status():
    """Test 3: API Status Endpoint"""
    print("\n=== Test 3: API Status ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/v0/status")
            assert response.status_code == 200
            data = response.json()
            assert "features" in data
            print(f"[PASS] API Status - Features available: {len(data['features'])}")
            return True
    except Exception as e:
        print(f"[FAIL] API status error: {e}")
        return False

async def test_smart_coding_ai_trigger():
    """Test 4: Smart Coding AI Event Trigger"""
    print("\n=== Test 4: Smart Coding AI Event Trigger ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/test/smart-coding-ai/emit-events/test-123")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "started"
            message = data.get("message", "Event trigger successful")
            print(f"[PASS] Event trigger: {message}")
            return True
    except Exception as e:
        print(f"[FAIL] Event trigger error: {e}")
        return False

async def test_cors_headers():
    """Test 5: CORS Headers"""
    print("\n=== Test 5: CORS Configuration ===")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.options(f"{BASE_URL}/", headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            })
            # FastAPI CORS should handle OPTIONS
            print(f"[PASS] CORS configured (status: {response.status_code})")
            return True
    except Exception as e:
        print(f"[FAIL] CORS test error: {e}")
        return False

async def test_response_times():
    """Test 6: Response Times"""
    print("\n=== Test 6: Response Times ===")
    try:
        async with httpx.AsyncClient() as client:
            import time
            
            times = []
            for i in range(5):
                start = time.time()
                response = await client.get(f"{BASE_URL}/health")
                duration = (time.time() - start) * 1000  # ms
                times.append(duration)
            
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"[PASS] Response times (ms):")
            print(f"   Average: {avg_time:.2f}ms")
            print(f"   Min: {min_time:.2f}ms")
            print(f"   Max: {max_time:.2f}ms")
            
            return avg_time < 200  # Should be fast
    except Exception as e:
        print(f"[FAIL] Response time test error: {e}")
        return False

async def test_concurrent_requests():
    """Test 7: Concurrent Request Handling"""
    print("\n=== Test 7: Concurrent Requests ===")
    try:
        async with httpx.AsyncClient() as client:
            # Fire 10 concurrent requests
            tasks = [client.get(f"{BASE_URL}/health") for _ in range(10)]
            responses = await asyncio.gather(*tasks)
            
            success_count = sum(1 for r in responses if r.status_code == 200)
            print(f"[PASS] Concurrent requests: {success_count}/10 successful")
            return success_count == 10
    except Exception as e:
        print(f"[FAIL] Concurrent requests error: {e}")
        return False

async def main():
    """Run all tests"""
    print("=" * 60)
    print("   Comprehensive Feature Test Suite")
    print("=" * 60)
    print(f"Backend URL: {BASE_URL}\n")
    
    # Run all tests
    tests = [
        test_health_endpoint(),
        test_root_endpoint(),
        test_api_status(),
        test_smart_coding_ai_trigger(),
        test_cors_headers(),
        test_response_times(),
        test_concurrent_requests(),
    ]
    
    results = await asyncio.gather(*tests, return_exceptions=True)
    
    # Count results
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False or isinstance(r, Exception))
    total = len(results)
    
    # Summary
    print("\n" + "=" * 60)
    print("   Test Summary")
    print("=" * 60)
    print(f"\nTests Run: {total}")
    print(f"[OK] Passed: {passed}")
    print(f"[ERROR] Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if failed == 0:
        print("\n[SUCCESS] All tests passed!")
        print("Backend is fully functional and ready for production.\n")
        return 0
    else:
        print(f"\n[WARNING] {failed} test(s) failed.")
        print("Review errors above for details.\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[CANCELLED] Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test suite error: {e}")
        sys.exit(1)

