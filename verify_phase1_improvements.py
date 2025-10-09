"""
Quick verification of Phase 1 improvements
Tests the specific endpoints we fixed
"""

import requests
import json
from datetime import datetime

def test_health_endpoints():
    """Test newly added health endpoints"""
    base_url = "http://localhost:8000"
    
    # Test a sample of newly added health endpoints
    health_endpoints = [
        "/api/v0/admin/health",
        "/api/v0/auth/health",
        "/api/v0/apps/health",
        "/api/v0/gamification/health",
        "/api/v0/code-processing/health",
        "/api/v0/advanced-analytics/health",
        "/api/v0/ai-agents/health",
        "/api/v0/capabilities/health",
        "/api/v0/data-analytics/health",
        "/api/v0/frontend/health",
        "/api/v0/meta-orchestrator/health",
        "/api/v0/multi-agent-coordinator/health",
        "/api/v0/optimized/services/health",
        "/api/v0/payments/health",
        "/api/v0/performance-architecture/health",
        "/api/v0/profiles/health",
        "/api/v0/super-intelligent-optimization/health",
        "/api/v0/tools-integration/health",
        "/api/v0/transcribe/health",
        "/api/v0/user-preferences/health",
        "/api/v0/webhooks/health",
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("PHASE 1 VERIFICATION - HEALTH ENDPOINTS")
    print("=" * 80)
    print()
    
    for endpoint in health_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint:<60} OK")
                passed += 1
            else:
                print(f"❌ {endpoint:<60} HTTP {response.status_code}")
                failed += 1
        except Exception as e:
            print(f"❌ {endpoint:<60} ERROR")
            failed += 1
    
    print()
    print(f"New Health Endpoints: {passed}/{len(health_endpoints)} working ({passed/len(health_endpoints)*100:.1f}%)")
    print()
    
    return passed, failed

def test_status_endpoints():
    """Test newly added status endpoints"""
    base_url = "http://localhost:8000"
    
    status_endpoints = [
        "/api/v0/consistency-dna/status",
        "/api/v0/unified-autonomous-dna/status",
        "/api/v0/self-modification/status",
        "/api/v0/smart-coding-ai/status",
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("PHASE 1 VERIFICATION - STATUS ENDPOINTS")
    print("=" * 80)
    print()
    
    for endpoint in status_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 503]:  # 200 or 503 both acceptable
                status = "OK" if response.status_code == 200 else "503 (expected)"
                print(f"✅ {endpoint:<60} {status}")
                passed += 1
            else:
                print(f"❌ {endpoint:<60} HTTP {response.status_code}")
                failed += 1
        except Exception as e:
            print(f"❌ {endpoint:<60} ERROR")
            failed += 1
    
    print()
    print(f"New Status Endpoints: {passed}/{len(status_endpoints)} working ({passed/len(status_endpoints)*100:.1f}%)")
    print()
    
    return passed, failed

def test_fixed_method():
    """Test the fixed HTTP method endpoint"""
    base_url = "http://localhost:8000"
    
    print("=" * 80)
    print("PHASE 1 VERIFICATION - HTTP METHOD FIX")
    print("=" * 80)
    print()
    
    endpoint = "/api/v0/agent-mode/health"
    
    try:
        response = requests.get(f"{base_url}{endpoint}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {endpoint:<60} OK (GET now works)")
            print()
            return 1, 0
        else:
            print(f"❌ {endpoint:<60} HTTP {response.status_code}")
            print()
            return 0, 1
    except Exception as e:
        print(f"❌ {endpoint:<60} ERROR: {e}")
        print()
        return 0, 1

def main():
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║         PHASE 1 IMPROVEMENTS VERIFICATION                         ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Test health endpoints
    health_passed, health_failed = test_health_endpoints()
    
    # Test status endpoints
    status_passed, status_failed = test_status_endpoints()
    
    # Test fixed method
    method_passed, method_failed = test_fixed_method()
    
    # Summary
    total_passed = health_passed + status_passed + method_passed
    total_failed = health_failed + status_failed + method_failed
    total = total_passed + total_failed
    
    print("=" * 80)
    print("PHASE 1 VERIFICATION SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Endpoints Tested: {total}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"Success Rate: {total_passed/total*100:.1f}%")
    print()
    
    print("📊 BREAKDOWN:")
    print(f"  • Health Endpoints: {health_passed}/{health_passed+health_failed} ({health_passed/(health_passed+health_failed)*100:.1f}%)")
    print(f"  • Status Endpoints: {status_passed}/{status_passed+status_failed} ({status_passed/(status_passed+status_failed)*100:.1f}%)")
    print(f"  • HTTP Method Fix:  {method_passed}/{method_passed+method_failed} ({method_passed/(method_passed+method_failed)*100:.1f}%)")
    print()
    
    if total_failed == 0:
        print("🎉 ALL PHASE 1 FIXES VERIFIED AND WORKING!")
    elif total_passed >= total * 0.8:
        print(f"✅ Phase 1 mostly successful ({total_passed}/{total} working)")
    else:
        print(f"⚠️  Some Phase 1 fixes need attention ({total_failed} failures)")
    
    print()
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "phase": 1,
        "total_tested": total,
        "passed": total_passed,
        "failed": total_failed,
        "success_rate": f"{total_passed/total*100:.1f}%",
        "breakdown": {
            "health_endpoints": {"passed": health_passed, "failed": health_failed},
            "status_endpoints": {"passed": status_passed, "failed": status_failed},
            "method_fix": {"passed": method_passed, "failed": method_failed}
        }
    }
    
    with open("phase1_verification_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("📄 Results saved to: phase1_verification_results.json")
    print()

if __name__ == "__main__":
    main()

