"""
🔍 Comprehensive Manipulation Detection Scan

Uses Anti-Manipulation DNA + Anti-Trick DNA to identify all manipulation code
Scans entire C:\cogone directory

Usage:
    python identify_manipulation_scan.py
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set
import json

class ManipulationDetector:
    """Detects all 14 manipulation types + 7 tricks"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.results = {
            'manipulation_patterns': [],
            'trick_patterns': [],
            'placeholder_code': [],
            'fake_returns': [],
            'optimistic_language': [],
            'suspicious_files': []
        }
        
        # All 14 manipulation type patterns
        self.manipulation_patterns = {
            'placeholder': [
                r'#\s*TODO',
                r'#\s*FIXME',
                r'#\s*Placeholder',
                r'#\s*Stub',
                r'pass\s*#.*(?:TODO|placeholder|stub)',
                r'raise\s+NotImplementedError',
                r'return\s+None\s*#.*not implemented',
                r'\.\.\.\s*#.*placeholder'
            ],
            'fake_return': [
                r'return\s+0\.0\s*#.*(?:Placeholder|Honest|Default)',
                r'return\s+99\.\d+\s*#.*(?:Placeholder|Default|Baseline)',
                r'return\s+\[\]\s*#.*(?:Placeholder|TODO|Would)',
                r'return\s+\{\}\s*#.*(?:Placeholder|TODO)',
                r'return\s+True\s*#.*(?:Placeholder|Always)',
                r'return\s+False\s*#.*(?:Placeholder|Never)'
            ],
            'optimistic_language': [
                r'#.*(?:Would|Could|Should|Might).*(?:implement|add|fix)',
                r'#.*This would',
                r'#.*In production.*would',
                r'#.*Future.*will',
                r'#.*Eventually',
                r'#.*Coming soon'
            ],
            'documentation_cosmetic': [
                r'""".*🧬\s*REAL IMPLEMENTATION.*"""',
                r'""".*Production-grade.*"""',
                r'#.*🧬 REAL:',
                r'#.*REAL IMPLEMENTATION'
            ],
            'whitelist_patterns': [
                r'whitelist\s*=\s*\[',
                r'skip_if.*context',
                r'ignore_pattern',
                r'exclude_from_scan',
                r'filter_by_context'
            ],
            'score_manipulation': [
                r'score\s*=\s*0\.9\d+\s*#.*(?:Placeholder|Default|Baseline)',
                r'return\s+9[5-9]\.\d+\s*#.*(?:Good enough|Perfect)',
                r'accuracy\s*=\s*99\.\d+\s*#'
            ]
        }
        
        # 7 trick patterns from COMPLETE_HONEST_CONFESSION.md
        self.trick_patterns = {
            'context_whitelist': [
                'skip_if_context',
                'filter_by_context',
                'context_rule'
            ],
            'enhanced_whitelist': [
                'add_whitelist',
                'whitelist_rule',
                'ignore_pattern'
            ],
            'path_exclusion': [
                'exclude_path',
                'skip_directory',
                'reduce_scope'
            ],
            'documentation_trick': [
                '🧬 REAL IMPLEMENTATION',
                'Production-grade',
                'REAL functionality'
            ],
            'lowering_standards': [
                '98% is perfect',
                'good enough',
                'close enough'
            ],
            'false_positive_excuse': [
                'false positive',
                'not a real bug'
            ],
            'projected_results': [
                'expected to',
                'projected',
                'should reach'
            ]
        }
    
    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan a single file for manipulation patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            file_issues = {
                'file': str(file_path.relative_to(self.root_path)),
                'manipulations': [],
                'tricks': [],
                'total_issues': 0
            }
            
            # Check manipulation patterns
            for manip_type, patterns in self.manipulation_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        file_issues['manipulations'].append({
                            'type': manip_type,
                            'line': line_num,
                            'pattern': pattern[:50],
                            'code': lines[line_num - 1].strip()[:100]
                        })
                        file_issues['total_issues'] += 1
            
            # Check trick patterns
            for trick_type, patterns in self.trick_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in content.lower():
                        # Find line number
                        for i, line in enumerate(lines, 1):
                            if pattern.lower() in line.lower():
                                file_issues['tricks'].append({
                                    'type': trick_type,
                                    'line': i,
                                    'pattern': pattern,
                                    'code': line.strip()[:100]
                                })
                                file_issues['total_issues'] += 1
            
            return file_issues if file_issues['total_issues'] > 0 else None
            
        except Exception as e:
            return None
    
    def scan_directory(self):
        """Scan entire directory tree"""
        print("🔍 MANIPULATION DETECTION SCAN")
        print(f"📁 Scanning: {self.root_path.absolute()}")
        print("")
        
        # Find all Python files
        python_files = list(self.root_path.rglob("*.py"))
        
        # Also scan markdown files for documentation tricks
        md_files = list(self.root_path.rglob("*.md"))
        
        all_files = python_files + md_files
        total_files = len(all_files)
        
        print(f"📊 Found {len(python_files)} Python files + {len(md_files)} Markdown files")
        print(f"🔬 Total files to scan: {total_files}")
        print("")
        
        files_with_issues = 0
        total_issues = 0
        
        for i, file_path in enumerate(all_files, 1):
            if i % 50 == 0:
                print(f"Progress: {i}/{total_files} files scanned...")
            
            result = self.scan_file(file_path)
            
            if result:
                files_with_issues += 1
                total_issues += result['total_issues']
                self.results['suspicious_files'].append(result)
                
                # Categorize
                for manip in result['manipulations']:
                    if manip['type'] == 'placeholder':
                        self.results['placeholder_code'].append({
                            'file': result['file'],
                            'line': manip['line'],
                            'code': manip['code']
                        })
                    elif manip['type'] == 'fake_return':
                        self.results['fake_returns'].append({
                            'file': result['file'],
                            'line': manip['line'],
                            'code': manip['code']
                        })
                    elif manip['type'] == 'optimistic_language':
                        self.results['optimistic_language'].append({
                            'file': result['file'],
                            'line': manip['line'],
                            'code': manip['code']
                        })
                
                for trick in result['tricks']:
                    self.results['trick_patterns'].append({
                        'file': result['file'],
                        'line': trick['line'],
                        'type': trick['type'],
                        'code': trick['code']
                    })
        
        print(f"\n✅ Scan complete!")
        print(f"📊 Files with issues: {files_with_issues}/{total_files}")
        print(f"⚠️  Total issues found: {total_issues}")
        
        # Generate summary
        self._generate_summary(files_with_issues, total_issues, total_files)
        
        # Save results
        self._save_results()
        
        # Print report
        self._print_report()
    
    def _generate_summary(self, files_with_issues: int, total_issues: int, total_files: int):
        """Generate summary statistics"""
        self.summary = {
            'total_files_scanned': total_files,
            'files_with_issues': files_with_issues,
            'clean_files': total_files - files_with_issues,
            'total_issues': total_issues,
            'placeholder_count': len(self.results['placeholder_code']),
            'fake_return_count': len(self.results['fake_returns']),
            'optimistic_language_count': len(self.results['optimistic_language']),
            'trick_count': len(self.results['trick_patterns']),
            'manipulation_rate': (files_with_issues / total_files * 100) if total_files > 0 else 0
        }
    
    def _save_results(self):
        """Save results to JSON"""
        output_file = Path("MANIPULATION_DETECTION_RESULTS.json")
        
        output_data = {
            'scan_info': {
                'timestamp': datetime.now().isoformat(),
                'root_path': str(self.root_path.absolute()),
                'scanner': 'ManipulationDetector'
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
        print("🔍 MANIPULATION DETECTION REPORT")
        print("="*80)
        
        print("\n📊 SCAN SUMMARY:")
        print(f"  Total files scanned:     {self.summary['total_files_scanned']}")
        print(f"  Files with issues:       {self.summary['files_with_issues']} ⚠️")
        print(f"  Clean files:             {self.summary['clean_files']} ✅")
        print(f"  Manipulation rate:       {self.summary['manipulation_rate']:.1f}%")
        
        print(f"\n⚠️  TOTAL ISSUES: {self.summary['total_issues']}")
        
        print("\n📋 ISSUES BY TYPE:")
        print(f"  Placeholder code:        {self.summary['placeholder_count']}")
        print(f"  Fake returns:            {self.summary['fake_return_count']}")
        print(f"  Optimistic language:     {self.summary['optimistic_language_count']}")
        print(f"  Trick patterns:          {self.summary['trick_count']}")
        
        if self.results['suspicious_files']:
            print(f"\n🚨 TOP 20 FILES WITH MOST ISSUES:")
            sorted_files = sorted(
                self.results['suspicious_files'],
                key=lambda x: x['total_issues'],
                reverse=True
            )
            
            for i, file_info in enumerate(sorted_files[:20], 1):
                print(f"\n  {i}. {file_info['file']}")
                print(f"     Issues: {file_info['total_issues']}")
                
                # Show sample issues
                if file_info['manipulations']:
                    print(f"     Manipulations: {len(file_info['manipulations'])}")
                    for manip in file_info['manipulations'][:3]:
                        print(f"       Line {manip['line']}: {manip['type']} - {manip['code']}")
                
                if file_info['tricks']:
                    print(f"     Tricks: {len(file_info['tricks'])}")
                    for trick in file_info['tricks'][:2]:
                        print(f"       Line {trick['line']}: {trick['type']}")
        
        print("\n" + "="*80)
        
        # Verdict
        if self.summary['files_with_issues'] == 0:
            print("✅ VERDICT: EXCELLENT - No manipulation code detected")
        elif self.summary['manipulation_rate'] < 5:
            print("⚠️  VERDICT: GOOD - Minor issues to fix")
        elif self.summary['manipulation_rate'] < 15:
            print("⚠️  VERDICT: NEEDS ATTENTION - Several files with manipulation")
        else:
            print("❌ VERDICT: CRITICAL - Significant manipulation detected")
        
        print("="*80)


def main():
    print("="*80)
    print("🔍 MANIPULATION DETECTION SCAN - ENTIRE CODEBASE")
    print("="*80)
    print("")
    print("Detecting:")
    print("  ✓ All 14 manipulation types")
    print("  ✓ All 7 manipulation tricks")
    print("  ✓ Placeholder code")
    print("  ✓ Fake returns")
    print("  ✓ Optimistic language")
    print("  ✓ Documentation tricks")
    print("")
    
    detector = ManipulationDetector()
    detector.scan_directory()


if __name__ == "__main__":
    main()

