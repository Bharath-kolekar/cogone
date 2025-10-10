"""
🧬 DNA-Powered Manipulation Detection

Uses the Unified Core DNA System (all 9 DNA systems) to identify:
- All 14 manipulation types (Anti-Trick DNA)
- All 7 manipulation tricks (Anti-Manipulation DNA)
- Placeholder patterns (Precision DNA)
- Quality issues (Reality Check DNA)
- Consistency problems (Consistency DNA)

This is the REAL way to scan - activate ONE DNA, ALL activate.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, List, Any

# Add backend to path
sys.path.insert(0, 'backend')

try:
    from app.services.unified_core_dna_system import (
        get_unified_dna,
        DNASystem,
        DNAValidationResult
    )
    from app.services.anti_manipulation_core_dna import (
        get_anti_manipulation_dna,
        ManipulationTrick
    )
    DNA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  DNA systems not available: {e}")
    print("Running in fallback mode...")
    DNA_AVAILABLE = False


class DNAPoweredManipulationScanner:
    """
    🧬 Scan using Unified Core DNA System
    
    When we call validate_code(), ALL 9 DNA systems activate:
    1. Immutable DNA - Core principles
    2. Zero Assumption DNA - Input validation
    3. Precision DNA - Completeness checks
    4. Reality Check DNA - Quality validation
    5. Reality-Focused DNA - No manipulation
    6. Anti-Trick DNA - 14 manipulation types
    7. Anti-Manipulation DNA - 7 tricks
    8. Consistency DNA - Pattern enforcement
    9. Autonomous DNA - Recommendations
    """
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        
        if DNA_AVAILABLE:
            self.unified_dna = get_unified_dna()
            self.anti_manipulation = get_anti_manipulation_dna()
        else:
            self.unified_dna = None
            self.anti_manipulation = None
        
        self.results = {
            'files_scanned': 0,
            'files_with_violations': 0,
            'total_violations': 0,
            'manipulation_files': [],
            'critical_files': [],
            'by_dna_system': {
                'immutable': [],
                'zero_assumption': [],
                'precision': [],
                'reality_check': [],
                'reality_focused': [],
                'anti_trick': [],
                'anti_manipulation': [],
                'consistency': [],
                'autonomous': []
            },
            'by_violation_type': {}
        }
    
    def scan_directory(self, target_dir: str = "backend/app"):
        """
        Scan directory using Unified Core DNA System
        
        Each file goes through ALL 9 DNA systems automatically
        """
        print("🧬" * 40)
        print("DNA-POWERED MANIPULATION DETECTION")
        print("🧬" * 40)
        print("")
        print("🔬 Using: Unified Core DNA System")
        print("📊 DNA Systems: 9 (activate one, activate all)")
        print(f"📁 Target: {target_dir}")
        print("")
        
        if not DNA_AVAILABLE:
            print("❌ ERROR: DNA systems not available")
            print("Please ensure backend imports are working")
            return
        
        target_path = Path(target_dir)
        if not target_path.exists():
            print(f"❌ ERROR: Directory not found: {target_dir}")
            return
        
        # Find Python files in our code (not venv)
        python_files = []
        for pattern in ["*.py"]:
            for file in target_path.rglob(pattern):
                # Skip venv, node_modules, __pycache__
                if any(skip in str(file) for skip in ['.venv', 'node_modules', '__pycache__', '.git']):
                    continue
                python_files.append(file)
        
        total_files = len(python_files)
        print(f"📊 Found {total_files} Python files to scan")
        print("")
        
        # Scan each file with DNA systems
        for i, file_path in enumerate(python_files, 1):
            self._scan_file_with_dna(file_path, i, total_files)
        
        print(f"\n✅ Scan complete!")
        print(f"📊 Files scanned: {self.results['files_scanned']}")
        print(f"⚠️  Files with violations: {self.results['files_with_violations']}")
        print(f"🚨 Total violations: {self.results['total_violations']}")
        
        # Save results
        self._save_results()
        
        # Print comprehensive report
        self._print_report()
    
    def _scan_file_with_dna(self, file_path: Path, index: int, total: int):
        """
        Scan a single file using Unified Core DNA System
        
        This triggers ALL 9 DNA systems automatically
        """
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            if not code.strip():
                return
            
            relative_path = file_path.relative_to(self.root_path)
            
            # Progress
            if index % 10 == 0:
                print(f"Progress: {index}/{total} files...")
            
            # 🧬 UNIFIED DNA VALIDATION
            # This ONE call activates ALL 9 DNA systems
            result = self.unified_dna.validate_code(
                code=code,
                file_path=str(relative_path)
            )
            
            self.results['files_scanned'] += 1
            
            # Check if file has violations
            if not result.is_valid or len(result.violations) > 0:
                self.results['files_with_violations'] += 1
                self.results['total_violations'] += len(result.violations)
                
                file_result = {
                    'file': str(relative_path),
                    'violations': result.violations,
                    'recommendations': result.recommendations,
                    'systems_activated': [s.value for s in result.all_systems_activated],
                    'is_valid': result.is_valid,
                    'execution_time_ms': result.execution_time_ms
                }
                
                self.results['manipulation_files'].append(file_result)
                
                # Categorize by DNA system
                for validation_key, validation_data in result.validations.items():
                    if validation_data and isinstance(validation_data, dict):
                        if not validation_data.get('compliant', True) or validation_data.get('violations'):
                            self.results['by_dna_system'][validation_key].append({
                                'file': str(relative_path),
                                'data': validation_data
                            })
                
                # Categorize by violation type
                for violation in result.violations:
                    v_type = violation.get('type', 'unknown')
                    if v_type not in self.results['by_violation_type']:
                        self.results['by_violation_type'][v_type] = []
                    self.results['by_violation_type'][v_type].append({
                        'file': str(relative_path),
                        'violation': violation
                    })
                
                # Mark as critical if many violations
                if len(result.violations) >= 3:
                    self.results['critical_files'].append({
                        'file': str(relative_path),
                        'violation_count': len(result.violations),
                        'types': list(set(v.get('type') for v in result.violations))
                    })
        
        except Exception as e:
            print(f"Error scanning {file_path}: {str(e)[:100]}")
    
    def _save_results(self):
        """Save comprehensive results"""
        output_file = Path("DNA_MANIPULATION_SCAN_RESULTS.json")
        
        output_data = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'root_path': str(self.root_path.absolute()),
                'dna_systems_used': 9,
                'scanner': 'DNAPoweredManipulationScanner'
            },
            'summary': {
                'files_scanned': self.results['files_scanned'],
                'files_with_violations': self.results['files_with_violations'],
                'total_violations': self.results['total_violations'],
                'manipulation_rate': (
                    self.results['files_with_violations'] / self.results['files_scanned'] * 100
                    if self.results['files_scanned'] > 0 else 0
                )
            },
            'detailed_results': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
    
    def _print_report(self):
        """Print comprehensive DNA-powered report"""
        print("\n" + "="*80)
        print("🧬 DNA-POWERED MANIPULATION DETECTION REPORT")
        print("="*80)
        
        print("\n📊 SCAN SUMMARY:")
        print(f"  Files scanned:           {self.results['files_scanned']}")
        print(f"  Files with violations:   {self.results['files_with_violations']} ⚠️")
        print(f"  Clean files:             {self.results['files_scanned'] - self.results['files_with_violations']} ✅")
        
        if self.results['files_scanned'] > 0:
            manipulation_rate = self.results['files_with_violations'] / self.results['files_scanned'] * 100
            print(f"  Manipulation rate:       {manipulation_rate:.1f}%")
        
        print(f"\n⚠️  TOTAL VIOLATIONS: {self.results['total_violations']}")
        
        # Violations by type
        if self.results['by_violation_type']:
            print("\n📋 VIOLATIONS BY TYPE:")
            sorted_types = sorted(
                self.results['by_violation_type'].items(),
                key=lambda x: len(x[1]),
                reverse=True
            )
            for v_type, violations in sorted_types[:10]:
                print(f"  {v_type:25} {len(violations):5} occurrences")
        
        # By DNA system
        print("\n🧬 VIOLATIONS BY DNA SYSTEM:")
        for dna_name, issues in self.results['by_dna_system'].items():
            if issues:
                print(f"  {dna_name:25} {len(issues):5} files flagged")
        
        # Critical files
        if self.results['critical_files']:
            print(f"\n🚨 CRITICAL FILES (Top 20):")
            sorted_critical = sorted(
                self.results['critical_files'],
                key=lambda x: x['violation_count'],
                reverse=True
            )
            
            for i, file_info in enumerate(sorted_critical[:20], 1):
                print(f"\n  {i}. {file_info['file']}")
                print(f"     Violations: {file_info['violation_count']}")
                print(f"     Types: {', '.join(file_info['types'])}")
        
        # Sample violations
        if self.results['manipulation_files']:
            print(f"\n📝 SAMPLE VIOLATIONS (First 5 files):")
            for file_result in self.results['manipulation_files'][:5]:
                print(f"\n  File: {file_result['file']}")
                print(f"  Violations: {len(file_result['violations'])}")
                for v in file_result['violations'][:3]:
                    print(f"    - Type: {v.get('type', 'unknown')}")
                    if 'reason' in v:
                        print(f"      Reason: {v['reason'][:100]}")
                    if 'code' in v:
                        print(f"      Code: {v['code'][:80]}")
        
        print("\n" + "="*80)
        
        # Verdict
        manipulation_rate = (
            self.results['files_with_violations'] / self.results['files_scanned'] * 100
            if self.results['files_scanned'] > 0 else 0
        )
        
        if manipulation_rate == 0:
            print("✅ VERDICT: PERFECT - No manipulation detected by DNA systems")
        elif manipulation_rate < 5:
            print("✅ VERDICT: EXCELLENT - Minimal issues detected")
        elif manipulation_rate < 15:
            print("⚠️  VERDICT: GOOD - Some files need attention")
        elif manipulation_rate < 30:
            print("⚠️  VERDICT: NEEDS WORK - Significant manipulation detected")
        else:
            print("❌ VERDICT: CRITICAL - Major manipulation issues")
        
        print("="*80)
        
        # DNA System Status
        if DNA_AVAILABLE:
            status = self.unified_dna.get_dna_status()
            print("\n🧬 DNA SYSTEM STATUS:")
            print(f"  Systems loaded: {status['systems_loaded']}/9")
            print(f"  Initialization order: {', '.join(status['initialization_order'])}")


def main():
    print("\n" + "🧬"*40)
    print("UNIFIED CORE DNA SYSTEM - MANIPULATION DETECTION")
    print("🧬"*40)
    print("")
    print("This scan uses the UNIFIED CORE DNA SYSTEM")
    print("")
    print("DNA Systems (9 total):")
    print("  1. Immutable DNA         - Core principles")
    print("  2. Zero Assumption DNA   - Input validation")
    print("  3. Precision DNA         - Completeness checks")
    print("  4. Reality Check DNA     - Quality validation")
    print("  5. Reality-Focused DNA   - No manipulation")
    print("  6. Anti-Trick DNA        - 14 manipulation types")
    print("  7. Anti-Manipulation DNA - 7 tricks")
    print("  8. Consistency DNA       - Pattern enforcement")
    print("  9. Autonomous DNA        - Recommendations")
    print("")
    print("🔬 Principle: ACTIVATE ONE → ACTIVATE ALL")
    print("")
    
    scanner = DNAPoweredManipulationScanner()
    scanner.scan_directory("backend/app")


if __name__ == "__main__":
    main()

