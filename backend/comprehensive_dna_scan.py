"""
🧬 Comprehensive Backend DNA Scan

Scans entire backend using Unified Core DNA System
Provides detailed report on code quality, manipulations, and violations

Usage:
    python backend/comprehensive_dna_scan.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import structlog

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from app.services.unified_core_dna_system import get_unified_dna, DNASystem
except ImportError as e:
    print(f"❌ Error: Could not import Unified DNA System: {e}")
    print("Make sure you're running from project root")
    sys.exit(1)

logger = structlog.get_logger()


class ComprehensiveDNAScan:
    """Comprehensive scanner using Unified Core DNA System"""
    
    def __init__(self, backend_path: str = "backend/app"):
        self.backend_path = Path(backend_path)
        self.unified_dna = get_unified_dna()
        self.results = []
        self.summary = {
            'total_files': 0,
            'files_scanned': 0,
            'files_passed': 0,
            'files_failed': 0,
            'total_violations': 0,
            'violations_by_type': {},
            'dna_activations': {dna.value: 0 for dna in DNASystem},
            'critical_files': [],
            'recommendations': []
        }
        
    def scan_directory(self):
        """Scan entire backend directory"""
        print("🧬 COMPREHENSIVE DNA SCAN STARTING")
        print(f"📁 Target: {self.backend_path}")
        print(f"🔬 Using: Unified Core DNA System (9 systems)")
        print("")
        
        # Find all Python files
        python_files = list(self.backend_path.rglob("*.py"))
        self.summary['total_files'] = len(python_files)
        
        print(f"📊 Found {len(python_files)} Python files")
        print("")
        
        # Scan each file
        for i, file_path in enumerate(python_files, 1):
            self._scan_file(file_path, i, len(python_files))
        
        # Generate summary
        self._generate_summary()
        
        # Save results
        self._save_results()
        
        # Print report
        self._print_report()
    
    def _scan_file(self, file_path: Path, index: int, total: int):
        """Scan a single file with all DNA systems"""
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            if not code.strip():
                return  # Skip empty files
            
            # Progress indicator
            progress = f"[{index}/{total}]"
            relative_path = file_path.relative_to(self.backend_path.parent)
            print(f"{progress} Scanning: {relative_path}", end="")
            
            # Run unified DNA validation
            result = self.unified_dna.validate_code(
                code=code,
                file_path=str(relative_path)
            )
            
            self.summary['files_scanned'] += 1
            
            # Track activations
            for dna in result.all_systems_activated:
                self.summary['dna_activations'][dna.value] += 1
            
            # Check result
            if result.is_valid:
                print(" ✅")
                self.summary['files_passed'] += 1
            else:
                print(f" ❌ ({len(result.violations)} violations)")
                self.summary['files_failed'] += 1
                self.summary['total_violations'] += len(result.violations)
                
                # Track violations by type
                for violation in result.violations:
                    v_type = violation.get('type', 'unknown')
                    self.summary['violations_by_type'][v_type] = \
                        self.summary['violations_by_type'].get(v_type, 0) + 1
                
                # Mark as critical if many violations
                if len(result.violations) >= 5:
                    self.summary['critical_files'].append({
                        'file': str(relative_path),
                        'violations': len(result.violations),
                        'types': list(set(v.get('type') for v in result.violations))
                    })
            
            # Store result
            self.results.append({
                'file': str(relative_path),
                'is_valid': result.is_valid,
                'violations': result.violations,
                'recommendations': result.recommendations,
                'systems_activated': [s.value for s in result.all_systems_activated],
                'execution_time_ms': result.execution_time_ms,
                'timestamp': result.timestamp.isoformat()
            })
            
        except Exception as e:
            print(f" ⚠️  Error: {str(e)[:50]}")
            logger.error(f"Error scanning {file_path}", error=str(e))
    
    def _generate_summary(self):
        """Generate comprehensive summary"""
        # Calculate pass rate
        if self.summary['files_scanned'] > 0:
            self.summary['pass_rate'] = (
                self.summary['files_passed'] / self.summary['files_scanned']
            ) * 100
        else:
            self.summary['pass_rate'] = 0.0
        
        # Sort critical files by violation count
        self.summary['critical_files'].sort(
            key=lambda x: x['violations'],
            reverse=True
        )
        
        # Generate recommendations
        if self.summary['files_failed'] > 0:
            self.summary['recommendations'].append(
                f"Fix {self.summary['files_failed']} files with violations"
            )
        
        if self.summary['critical_files']:
            self.summary['recommendations'].append(
                f"Priority: Fix {len(self.summary['critical_files'])} critical files"
            )
        
        if 'manipulation' in self.summary['violations_by_type']:
            self.summary['recommendations'].append(
                "Critical: Manipulation tricks detected - apply real fixes"
            )
    
    def _save_results(self):
        """Save results to JSON file"""
        output_file = Path("backend/DNA_SCAN_RESULTS.json")
        
        output_data = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'backend_path': str(self.backend_path),
                'unified_dna_systems': 9
            },
            'summary': self.summary,
            'detailed_results': self.results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
    
    def _print_report(self):
        """Print comprehensive report"""
        print("\n" + "="*80)
        print("🧬 COMPREHENSIVE DNA SCAN REPORT")
        print("="*80)
        
        print("\n📊 SCAN STATISTICS:")
        print(f"  Total files found:    {self.summary['total_files']}")
        print(f"  Files scanned:        {self.summary['files_scanned']}")
        print(f"  Files passed:         {self.summary['files_passed']} ✅")
        print(f"  Files failed:         {self.summary['files_failed']} ❌")
        print(f"  Pass rate:            {self.summary['pass_rate']:.1f}%")
        
        print("\n🔬 DNA SYSTEM ACTIVATIONS:")
        for dna_name, count in self.summary['dna_activations'].items():
            if count > 0:
                print(f"  {dna_name:30} {count:5} activations")
        
        print(f"\n⚠️  TOTAL VIOLATIONS: {self.summary['total_violations']}")
        
        if self.summary['violations_by_type']:
            print("\n📋 VIOLATIONS BY TYPE:")
            sorted_violations = sorted(
                self.summary['violations_by_type'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            for v_type, count in sorted_violations:
                print(f"  {v_type:20} {count:5} violations")
        
        if self.summary['critical_files']:
            print(f"\n🚨 CRITICAL FILES (Top 10):")
            for i, file_info in enumerate(self.summary['critical_files'][:10], 1):
                print(f"  {i:2}. {file_info['file']}")
                print(f"      Violations: {file_info['violations']}")
                print(f"      Types: {', '.join(file_info['types'])}")
        
        if self.summary['recommendations']:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(self.summary['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "="*80)
        
        # Overall verdict
        if self.summary['pass_rate'] >= 95:
            print("✅ VERDICT: EXCELLENT - Codebase passes DNA validation")
        elif self.summary['pass_rate'] >= 80:
            print("⚠️  VERDICT: GOOD - Minor issues to fix")
        elif self.summary['pass_rate'] >= 60:
            print("⚠️  VERDICT: NEEDS IMPROVEMENT - Several violations found")
        else:
            print("❌ VERDICT: CRITICAL - Major violations require immediate attention")
        
        print("="*80)


def main():
    """Main execution"""
    print("="*80)
    print("🧬 UNIFIED CORE DNA SYSTEM - COMPREHENSIVE BACKEND SCAN")
    print("="*80)
    print("")
    print("This scan will:")
    print("  ✓ Use all 9 Core DNA Systems")
    print("  ✓ Scan every Python file in backend")
    print("  ✓ Detect manipulations, violations, quality issues")
    print("  ✓ Generate comprehensive report")
    print("")
    
    scanner = ComprehensiveDNAScan()
    scanner.scan_directory()
    
    print("\n✅ Scan complete!")


if __name__ == "__main__":
    main()

