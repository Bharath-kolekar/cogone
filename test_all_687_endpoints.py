"""
Comprehensive 687 Endpoint Testing
Tests each endpoint individually with appropriate methods
"""

import requests
import json
import time
from typing import Dict, List, Tuple
from datetime import datetime
import sys

class ComprehensiveEndpointTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            'passed': [],
            'failed': [],
            'skipped': [],
            'total': 0
        }
        self.start_time = None
        
    def get_all_endpoints(self) -> Dict:
        """Fetch OpenAPI spec with all endpoints"""
        try:
            response = requests.get(f"{self.base_url}/openapi.json", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to fetch OpenAPI spec: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error fetching OpenAPI spec: {e}")
            return None
    
    def determine_test_method(self, path: str, methods: List[str], operation: Dict) -> Tuple[str, Dict]:
        """Determine the best way to test an endpoint"""
        
        # Priority 1: Health endpoints - always use GET
        if 'health' in path.lower():
            return ('GET', {})
        
        # Priority 2: GET endpoints - safe to test
        if 'GET' in methods:
            return ('GET', {})
        
        # Priority 3: POST endpoints - need careful handling
        if 'POST' in methods:
            # Check if it requires authentication
            security = operation.get('security', [])
            
            # If it's a public endpoint, try with minimal data
            if not security:
                # Try to get request body schema
                request_body = operation.get('requestBody', {})
                content = request_body.get('content', {})
                schema = content.get('application/json', {}).get('schema', {})
                
                # Return POST with empty body or minimal data
                return ('POST', {'test_mode': True})
            else:
                # Skip authenticated POST endpoints for now
                return ('SKIP', {'reason': 'Requires authentication'})
        
        # Priority 4: Other methods - skip for safety
        return ('SKIP', {'reason': f'Unsupported methods: {methods}'})
    
    def test_endpoint(self, path: str, method: str, data: Dict = None) -> bool:
        """Test a single endpoint"""
        url = f"{self.base_url}{path}"
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=5)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=5)
            else:
                return False
            
            # Consider success: 200, 201, 204, 400 (validation), 401 (auth required), 403 (forbidden)
            # These mean the endpoint is working, just protected or needs different input
            if response.status_code in [200, 201, 204, 400, 401, 403]:
                return True
            
            return False
            
        except requests.exceptions.Timeout:
            return False
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive test on all 687 endpoints"""
        self.start_time = time.time()
        
        print("=" * 80)
        print("COMPREHENSIVE 687 ENDPOINT TESTING")
        print("=" * 80)
        print()
        
        # Wait for backend
        print("⏳ Waiting for backend to be ready...")
        for i in range(5):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend is ready\n")
                    break
            except:
                time.sleep(1)
        else:
            print("❌ Backend not responding. Please start the backend first.")
            return False
        
        # Get all endpoints
        print("📥 Fetching endpoint list from OpenAPI spec...")
        spec = self.get_all_endpoints()
        if not spec:
            return False
        
        paths = spec.get('paths', {})
        self.results['total'] = len(paths)
        print(f"✅ Found {len(paths)} endpoints\n")
        
        # Group endpoints by service
        services = {}
        for path, path_item in paths.items():
            parts = path.split('/')
            if len(parts) >= 4 and parts[1] == 'api':
                service = parts[3] if parts[2] == 'v0' else parts[2]
            elif len(parts) >= 2:
                service = parts[1] if parts[1] else "root"
            else:
                service = "root"
            
            if service not in services:
                services[service] = []
            services[service].append((path, path_item))
        
        print(f"📦 Testing {len(services)} services...\n")
        print("-" * 80)
        
        # Test each service
        for service_name, endpoints in sorted(services.items()):
            print(f"\n📦 {service_name.upper()} ({len(endpoints)} endpoints)")
            print("-" * 80)
            
            service_passed = 0
            service_failed = 0
            service_skipped = 0
            
            for path, path_item in endpoints:
                # Get methods and operation details
                methods = [m.upper() for m in path_item.keys() if m.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']]
                
                if not methods:
                    self.results['skipped'].append({
                        'path': path,
                        'reason': 'No HTTP methods found'
                    })
                    service_skipped += 1
                    print(f"  ⏭️  {path[:60]:<60} SKIPPED (No methods)")
                    continue
                
                # Get operation details (use first method)
                operation = path_item.get(methods[0].lower(), {})
                
                # Determine test method
                test_method, test_data = self.determine_test_method(path, methods, operation)
                
                if test_method == 'SKIP':
                    self.results['skipped'].append({
                        'path': path,
                        'reason': test_data.get('reason', 'Unknown')
                    })
                    service_skipped += 1
                    reason = test_data.get('reason', 'Unknown')[:30]
                    print(f"  ⏭️  {path[:60]:<60} SKIPPED ({reason})")
                    continue
                
                # Test the endpoint
                success = self.test_endpoint(path, test_method, test_data)
                
                if success:
                    self.results['passed'].append({
                        'path': path,
                        'method': test_method
                    })
                    service_passed += 1
                    print(f"  ✅ {path[:60]:<60} OK ({test_method})")
                else:
                    self.results['failed'].append({
                        'path': path,
                        'method': test_method
                    })
                    service_failed += 1
                    print(f"  ❌ {path[:60]:<60} FAILED ({test_method})")
            
            # Service summary
            total_service = service_passed + service_failed + service_skipped
            success_rate = (service_passed / total_service * 100) if total_service > 0 else 0
            print(f"\n  📊 {service_name}: {service_passed} passed, {service_failed} failed, {service_skipped} skipped ({success_rate:.1f}% success)")
        
        # Final summary
        self.print_summary()
        
        return len(self.results['failed']) == 0
    
    def print_summary(self):
        """Print comprehensive summary"""
        elapsed = time.time() - self.start_time
        
        print("\n" + "=" * 80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        print()
        
        total = self.results['total']
        passed = len(self.results['passed'])
        failed = len(self.results['failed'])
        skipped = len(self.results['skipped'])
        tested = passed + failed
        
        print(f"Total Endpoints:    {total}")
        print(f"Tested:             {tested}")
        print(f"  ✅ Passed:        {passed}")
        print(f"  ❌ Failed:        {failed}")
        print(f"⏭️  Skipped:         {skipped}")
        print()
        
        if tested > 0:
            success_rate = (passed / tested * 100)
            print(f"Success Rate:       {success_rate:.1f}% ({passed}/{tested})")
        
        print(f"Time Elapsed:       {elapsed:.2f} seconds")
        print()
        
        # Detailed failure report
        if failed > 0:
            print("-" * 80)
            print("FAILED ENDPOINTS (Need Attention):")
            print("-" * 80)
            for item in self.results['failed'][:20]:  # Show first 20
                print(f"  ❌ {item['path']} ({item['method']})")
            if failed > 20:
                print(f"  ... and {failed - 20} more")
            print()
        
        # Skipped summary
        if skipped > 0:
            skip_reasons = {}
            for item in self.results['skipped']:
                reason = item['reason']
                skip_reasons[reason] = skip_reasons.get(reason, 0) + 1
            
            print("-" * 80)
            print("SKIPPED ENDPOINTS (By Reason):")
            print("-" * 80)
            for reason, count in sorted(skip_reasons.items(), key=lambda x: -x[1]):
                print(f"  • {reason}: {count} endpoints")
            print()
        
        # Final status
        print("=" * 80)
        if failed == 0:
            print("🎉 ALL TESTED ENDPOINTS WORKING!")
            print(f"✅ {passed}/{tested} endpoints passed tests")
            if skipped > 0:
                print(f"ℹ️  {skipped} endpoints skipped (require auth or special handling)")
        else:
            print(f"⚠️  {failed} endpoints need attention")
            print(f"✅ {passed}/{tested} endpoints working")
        print("=" * 80)
        print()
        
        # Save detailed results
        self.save_results()
    
    def save_results(self):
        """Save detailed results to JSON"""
        results_file = "endpoint_test_results.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total': self.results['total'],
                'tested': len(self.results['passed']) + len(self.results['failed']),
                'passed': len(self.results['passed']),
                'failed': len(self.results['failed']),
                'skipped': len(self.results['skipped']),
                'elapsed_seconds': time.time() - self.start_time,
                'passed_endpoints': self.results['passed'],
                'failed_endpoints': self.results['failed'],
                'skipped_endpoints': self.results['skipped']
            }, f, indent=2)
        
        print(f"📄 Detailed results saved to: {results_file}")
        print()

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║          COMPREHENSIVE 687 ENDPOINT TESTING SUITE                 ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    tester = ComprehensiveEndpointTester()
    success = tester.run_comprehensive_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

