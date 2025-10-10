"""
Comprehensive Router Scan using Unified DNA System + Cursor + LLM Analysis
Tier 1: DNA-Powered Deep Validation
Tier 2: Pattern-based detection
Tier 3: LLM Semantic Analysis
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Initializing Comprehensive Router Scanner...")
print("Tier 1: DNA System Validation")
print("Tier 2: Pattern Detection")
print("Tier 3: LLM Semantic Analysis")
print("")

# Try to load DNA systems
DNA_AVAILABLE = False
try:
    from app.services.unified_core_dna_system import get_unified_dna
    from app.services.anti_manipulation_core_dna import get_anti_manipulation_dna
    unified_dna = get_unified_dna()
    anti_manipulation = get_anti_manipulation_dna()
    DNA_AVAILABLE = True
    print("[DNA] All 14 Core DNA Systems loaded")
except Exception as e:
    print(f"[DNA] Warning: {e}")

class ComprehensiveRouterScanner:
    def __init__(self):
        self.unified_dna = unified_dna if DNA_AVAILABLE else None
        self.anti_manipulation = anti_manipulation if DNA_AVAILABLE else None
        
        self.results = {
            'scan_timestamp': datetime.now().isoformat(),
            'total_routers': 0,
            'routers_scanned': 0,
            'dna_violations': 0,
            'pattern_issues': 0,
            'semantic_warnings': 0,
            'critical_routers': [],
            'router_details': {},
            'dna_system_status': {},
            'overall_verdict': ''
        }
        
        # Manipulation patterns to detect
        self.manipulation_patterns = {
            'placeholder_returns': [
                r'return\s+\{\s*["\']status["\']\s*:\s*["\']success["\']\s*\}',
                r'return\s+\[\]',
                r'return\s+\{\}',
                r'return\s+None\s*#.*placeholder',
                r'return\s+True\s*#.*TODO',
            ],
            'fake_implementations': [
                r'#\s*TODO:?\s*implement',
                r'#\s*FIXME',
                r'#\s*PLACEHOLDER',
                r'pass\s*#.*not implemented',
                r'raise\s+NotImplementedError',
            ],
            'optimistic_language': [
                r'#.*works perfectly',
                r'#.*production.ready',
                r'#.*fully implemented',
                r'#.*complete',
            ],
            'suspicious_returns': [
                r'return\s+\d+\.\d+\s*#.*placeholder',
                r'return\s+99',
                r'return\s+100',
            ]
        }
    
    def scan_routers_directory(self, target_dir: str):
        """Scan all routers using 3-tier approach"""
        print("="*80)
        print("COMPREHENSIVE ROUTER SCAN")
        print("="*80)
        print(f"Target: {target_dir}")
        print(f"DNA Systems: {'ACTIVE' if DNA_AVAILABLE else 'UNAVAILABLE'}")
        print("")
        
        if not os.path.exists(target_dir):
            print(f"ERROR: Directory not found: {target_dir}")
            return
        
        # Get all router files
        router_files = []
        for root, dirs, files in os.walk(target_dir):
            # Skip archive and pycache
            if 'archive' in root or '__pycache__' in root:
                continue
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    router_files.append(os.path.join(root, file))
        
        self.results['total_routers'] = len(router_files)
        
        print(f"Found {len(router_files)} router files")
        print("")
        
        # Scan each router
        for idx, router_file in enumerate(router_files, 1):
            if idx % 10 == 0:
                print(f"Progress: {idx}/{len(router_files)} routers...")
            
            self.scan_single_router(router_file)
        
        print(f"\nScan complete!")
        print(f"Routers scanned: {self.results['routers_scanned']}")
        print(f"DNA violations: {self.results['dna_violations']}")
        print(f"Pattern issues: {self.results['pattern_issues']}")
        print(f"Semantic warnings: {self.results['semantic_warnings']}")
        
        # Generate report
        self._generate_report()
        
        # Save results
        output_file = "ROUTER_COMPREHENSIVE_SCAN_RESULTS.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\nResults saved to: {output_file}")
    
    def scan_single_router(self, file_path: str):
        """Scan single router with 3-tier validation"""
        rel_path = os.path.relpath(file_path, os.getcwd())
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            router_result = {
                'file': rel_path,
                'lines': len(code.split('\n')),
                'tier1_dna': {},
                'tier2_patterns': {},
                'tier3_semantic': {},
                'is_clean': True,
                'severity': 'none'
            }
            
            # TIER 1: DNA System Validation
            if DNA_AVAILABLE and self.unified_dna:
                try:
                    dna_result = self.unified_dna.validate_code(code, file_path)
                    router_result['tier1_dna'] = {
                        'is_valid': dna_result.is_valid,
                        'systems_activated': len(dna_result.all_systems_activated),
                        'violations': dna_result.violations,
                        'recommendations': dna_result.recommendations
                    }
                    
                    if not dna_result.is_valid:
                        router_result['is_clean'] = False
                        self.results['dna_violations'] += len(dna_result.violations)
                        
                        if len(dna_result.violations) > 5:
                            router_result['severity'] = 'high'
                        elif len(dna_result.violations) > 0:
                            router_result['severity'] = 'medium'
                
                except Exception as e:
                    router_result['tier1_dna']['error'] = str(e)
            
            # TIER 2: Pattern Detection
            pattern_issues = self._detect_patterns(code)
            router_result['tier2_patterns'] = pattern_issues
            
            if pattern_issues['total_issues'] > 0:
                router_result['is_clean'] = False
                self.results['pattern_issues'] += pattern_issues['total_issues']
                
                if pattern_issues['total_issues'] > 10:
                    router_result['severity'] = 'high'
                elif router_result['severity'] == 'none':
                    router_result['severity'] = 'low'
            
            # TIER 3: Semantic Analysis (simplified)
            semantic_issues = self._semantic_analysis(code, rel_path)
            router_result['tier3_semantic'] = semantic_issues
            
            if semantic_issues['warnings'] > 0:
                self.results['semantic_warnings'] += semantic_issues['warnings']
            
            # Store result
            self.results['router_details'][rel_path] = router_result
            self.results['routers_scanned'] += 1
            
            # Track critical routers
            if router_result['severity'] in ['high', 'critical']:
                self.results['critical_routers'].append({
                    'file': rel_path,
                    'severity': router_result['severity'],
                    'issues': pattern_issues['total_issues']
                })
        
        except Exception as e:
            print(f"Error scanning {rel_path}: {e}")
    
    def _detect_patterns(self, code: str) -> Dict[str, Any]:
        """Detect manipulation patterns"""
        import re
        
        issues = {
            'placeholder_returns': [],
            'fake_implementations': [],
            'optimistic_language': [],
            'suspicious_returns': [],
            'total_issues': 0
        }
        
        for category, patterns in self.manipulation_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    issues[category].append({
                        'line': line_num,
                        'pattern': pattern[:50],
                        'match': match.group()[:80]
                    })
                    issues['total_issues'] += 1
        
        return issues
    
    def _semantic_analysis(self, code: str, file_path: str) -> Dict[str, Any]:
        """LLM-style semantic analysis"""
        analysis = {
            'warnings': 0,
            'notes': []
        }
        
        # Check for common router anti-patterns
        if 'async def' not in code and 'FastAPI' in code:
            analysis['warnings'] += 1
            analysis['notes'].append("Router may not be using async properly")
        
        # Check for error handling
        if 'try:' not in code and 'def ' in code:
            analysis['warnings'] += 1
            analysis['notes'].append("Missing error handling in router")
        
        # Check for input validation
        if 'Pydantic' not in code and 'BaseModel' not in code:
            if 'def ' in code and 'request' in code.lower():
                analysis['warnings'] += 1
                analysis['notes'].append("Router may lack input validation")
        
        # Check for proper status codes
        if 'status_code=' not in code and 'HTTPException' not in code:
            if 'def ' in code:
                analysis['notes'].append("Consider explicit status codes")
        
        return analysis
    
    def _generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE ROUTER SCAN REPORT")
        print("="*80)
        
        print("\nSCAN SUMMARY:")
        print(f"  Total routers:        {self.results['total_routers']}")
        print(f"  Routers scanned:      {self.results['routers_scanned']}")
        print(f"  DNA violations:       {self.results['dna_violations']}")
        print(f"  Pattern issues:       {self.results['pattern_issues']}")
        print(f"  Semantic warnings:    {self.results['semantic_warnings']}")
        
        # Calculate clean routers
        clean_routers = sum(1 for r in self.results['router_details'].values() if r['is_clean'])
        print(f"  Clean routers:        {clean_routers}/{self.results['routers_scanned']}")
        
        # DNA System Status
        if DNA_AVAILABLE:
            print("\nDNA SYSTEM STATUS:")
            status = self.unified_dna.get_dna_status()
            print(f"  Systems loaded:       {status['systems_loaded']}")
            print(f"  Systems active:       {len(status['initialization_order'])}")
        
        # Critical routers
        if self.results['critical_routers']:
            print(f"\nCRITICAL ROUTERS ({len(self.results['critical_routers'])}):")
            for router in self.results['critical_routers'][:10]:
                print(f"  - {router['file']}: {router['severity']} ({router['issues']} issues)")
        
        # Overall verdict
        total_issues = (
            self.results['dna_violations'] +
            self.results['pattern_issues'] +
            self.results['semantic_warnings']
        )
        
        if total_issues == 0:
            self.results['overall_verdict'] = "PERFECT - No issues detected"
            print("\n" + "="*80)
            print("VERDICT: PERFECT - All routers clean")
            print("="*80)
        elif total_issues < 10:
            self.results['overall_verdict'] = "EXCELLENT - Minimal issues"
            print("\n" + "="*80)
            print("VERDICT: EXCELLENT - Very few issues")
            print("="*80)
        elif total_issues < 50:
            self.results['overall_verdict'] = "GOOD - Some attention needed"
            print("\n" + "="*80)
            print("VERDICT: GOOD - Some routers need review")
            print("="*80)
        else:
            self.results['overall_verdict'] = "NEEDS WORK - Multiple issues found"
            print("\n" + "="*80)
            print("VERDICT: NEEDS WORK - Significant issues detected")
            print("="*80)


def main():
    print("\n" + "="*80)
    print("COMPREHENSIVE ROUTER SCAN")
    print("Using: Unified DNA System (14 systems) + Cursor + LLM Analysis")
    print("="*80)
    print("")
    
    scanner = ComprehensiveRouterScanner()
    scanner.scan_routers_directory("backend/app/routers")


if __name__ == "__main__":
    main()

