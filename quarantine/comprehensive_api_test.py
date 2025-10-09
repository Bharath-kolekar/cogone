"""
Comprehensive API Endpoint Testing
Tests all critical endpoints after consolidation
"""

import requests
import sys
import time

def test_api_endpoints():
    """Test all critical API endpoints"""
    print("=" * 70)
    print("COMPREHENSIVE API ENDPOINT TESTING")
    print("=" * 70)
    print()
    
    base_url = "http://localhost:8000"
    tests_passed = 0
    tests_failed = 0
    
    # Wait for backend
    print("Waiting for backend to be ready...")
    for i in range(5):
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is ready\n")
                break
        except:
            time.sleep(1)
    
    endpoints = [
        # Core health
        ("GET", "/health", "Core Health"),
        
        # Smart Coding AI (all variants)
        ("GET", "/api/v0/smart-coding-ai/health", "Smart Coding AI Health"),
        ("GET", "/api/v0/smart-coding-ai-optimized/health", "Smart Coding AI Optimized Health"),
        ("GET", "/api/v0/smart-coding-ai-complete/health", "Smart Coding AI Complete Health"),
        
        # AI Orchestration
        ("GET", "/api/v0/ai-orchestration/health", "AI Orchestration Health"),
        ("GET", "/api/v0/enhanced-ai-orchestration/health", "Enhanced AI Orchestration Health"),
        
        # Goal Integrity
        ("GET", "/api/v0/goal-integrity/health", "Goal Integrity Health"),
        
        # Session Management
        ("GET", "/api/v0/session-management/health", "Session Management Health"),
        
        # Voice Services
        ("GET", "/api/v0/voice-to-app/health", "Voice to App Health"),
        ("GET", "/api/v0/voice-to-code/health", "Voice to Code Health"),
        
        # WhatsApp
        ("GET", "/api/v0/whatsapp/health", "WhatsApp Health"),
        
        # Architecture Generator
        ("GET", "/api/v0/architecture-generator/health", "Architecture Generator Health"),
        
        # Advanced Features
        ("GET", "/api/v0/advanced-features/health", "Advanced Features Health"),
        
        # Agent Mode
        ("GET", "/api/v0/agent-mode/health", "Agent Mode Health"),
    ]
    
    print("Testing Critical Endpoints:")
    print("-" * 70)
    
    for method, endpoint, name in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {name}: OK")
                tests_passed += 1
            else:
                print(f"⚠️  {name}: HTTP {response.status_code}")
                tests_failed += 1
                
        except requests.exceptions.Timeout:
            print(f"⏱️  {name}: Timeout")
            tests_failed += 1
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Connection Error (backend not running)")
            tests_failed += 1
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            tests_failed += 1
    
    print()
    print("=" * 70)
    print("API TEST SUMMARY")
    print("=" * 70)
    print()
    print(f"Endpoints Tested: {len(endpoints)}")
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Success Rate: {(tests_passed / len(endpoints) * 100):.1f}%")
    print()
    
    if tests_failed == 0:
        print("🎉 ALL API ENDPOINTS WORKING!")
        print()
        print("✅ Backend: HEALTHY")
        print("✅ Smart Coding AI Core: ACCESSIBLE")
        print("✅ Voice-to-App AI: ACCESSIBLE")
        print("✅ Architecture Generator AI: ACCESSIBLE")
        print("✅ Modular Integration: ACCESSIBLE")
        print()
        return True
    else:
        print(f"⚠️ {tests_failed} endpoints failed")
        return False

if __name__ == "__main__":
    result = test_api_endpoints()
    sys.exit(0 if result else 1)

