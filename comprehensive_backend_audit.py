#!/usr/bin/env python3
"""Comprehensive backend audit - identify ALL remaining issues"""
import asyncio
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, 'backend')

from app.services.reality_check_dna import reality_check_dna

async def comprehensive_audit():
    """Complete audit of backend - identify all remaining issues"""
    
    services_dir = Path("backend/app/services")
    service_files = list(services_dir.glob("*.py"))
    
    print(f"{'='*80}")
    print(f"🔍 COMPREHENSIVE BACKEND AUDIT")
    print(f"{'='*80}\n")
    print(f"Scanning {len(service_files)} files...\n")
    
    # Categories
    perfect_files = []  # 1.00
    excellent_files = []  # 0.95-0.99
    very_good_files = []  # 0.90-0.94
    good_files = []  # 0.85-0.89
    acceptable_files = []  # 0.80-0.84
    needs_review = []  # < 0.80
    
    # Issue tracking
    all_critical = []
    all_high = []
    pattern_count = defaultdict(int)
    
    for file_path in service_files:
        try:
            result = await reality_check_dna.check_file(str(file_path))
            
            # Categorize by score
            file_info = {
                'name': file_path.name,
                'score': result.reality_score,
                'total_issues': result.total_issues,
                'is_real': result.is_real
            }
            
            # Get critical and high issues
            critical = [h for h in result.hallucinations if h.severity.value == 'critical']
            high = [h for h in result.hallucinations if h.severity.value == 'high']
            
            if critical:
                all_critical.append({
                    'file': file_path.name,
                    'issues': critical
                })
            
            if high:
                all_high.append({
                    'file': file_path.name,
                    'issues': high
                })
            
            # Count patterns
            for h in result.hallucinations:
                pattern_count[h.pattern.value] += 1
            
            # Categorize
            score = result.reality_score
            if score == 1.0:
                perfect_files.append(file_info)
            elif score >= 0.95:
                excellent_files.append(file_info)
            elif score >= 0.90:
                very_good_files.append(file_info)
            elif score >= 0.85:
                good_files.append(file_info)
            elif score >= 0.80:
                acceptable_files.append(file_info)
            else:
                needs_review.append(file_info)
        
        except Exception as e:
            print(f"❌ Error scanning {file_path.name}: {e}")
    
    # Calculate stats
    total_files = len(service_files)
    avg_score = sum(f['score'] for files in [perfect_files, excellent_files, very_good_files, 
                                               good_files, acceptable_files, needs_review] 
                    for f in files) / total_files if total_files > 0 else 0
    
    # RESULTS
    print(f"{'='*80}")
    print(f"📊 AUDIT RESULTS")
    print(f"{'='*80}\n")
    
    print(f"Total Files Scanned:      {total_files}")
    print(f"Average Reality Score:    {avg_score:.2f} ({get_grade(avg_score)})")
    print(f"\n")
    
    print(f"{'='*80}")
    print(f"📈 QUALITY DISTRIBUTION")
    print(f"{'='*80}\n")
    
    print(f"Perfect (1.00):           {len(perfect_files):>3} files ({len(perfect_files)/total_files*100:>5.1f}%)")
    print(f"Excellent (0.95-0.99):    {len(excellent_files):>3} files ({len(excellent_files)/total_files*100:>5.1f}%)")
    print(f"Very Good (0.90-0.94):    {len(very_good_files):>3} files ({len(very_good_files)/total_files*100:>5.1f}%)")
    print(f"Good (0.85-0.89):         {len(good_files):>3} files ({len(good_files)/total_files*100:>5.1f}%)")
    print(f"Acceptable (0.80-0.84):   {len(acceptable_files):>3} files ({len(acceptable_files)/total_files*100:>5.1f}%)")
    print(f"Needs Review (<0.80):     {len(needs_review):>3} files ({len(needs_review)/total_files*100:>5.1f}%)")
    print()
    
    # Issue Summary
    print(f"{'='*80}")
    print(f"🔴 ISSUE SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"Critical Issues:          {len(all_critical)} files")
    print(f"High-Severity Issues:     {len(all_high)} files")
    print(f"Total Issue Patterns:     {len(pattern_count)}")
    print()
    
    # Top patterns
    if pattern_count:
        print(f"{'='*80}")
        print(f"📋 TOP ISSUE PATTERNS")
        print(f"{'='*80}\n")
        
        sorted_patterns = sorted(pattern_count.items(), key=lambda x: x[1], reverse=True)
        for i, (pattern, count) in enumerate(sorted_patterns[:10], 1):
            print(f"{i:>2}. {pattern:<30} {count:>4} occurrences")
        print()
    
    # Critical Issues Detail
    if all_critical:
        print(f"{'='*80}")
        print(f"🔴 CRITICAL ISSUES (NEED IMMEDIATE ATTENTION)")
        print(f"{'='*80}\n")
        
        for item in all_critical[:10]:
            print(f"📄 {item['file']}")
            for issue in item['issues'][:2]:
                print(f"   Line {issue.line_number}: {issue.pattern.value}")
                print(f"   → {issue.explanation}")
            print()
    else:
        print(f"{'='*80}")
        print(f"✅ NO CRITICAL ISSUES!")
        print(f"{'='*80}\n")
    
    # Files Needing Review
    if needs_review:
        print(f"{'='*80}")
        print(f"⚠️  FILES NEEDING REVIEW (Score < 0.80)")
        print(f"{'='*80}\n")
        
        # Sort by score
        needs_review.sort(key=lambda x: x['score'])
        
        for i, f in enumerate(needs_review[:15], 1):
            status = "❌ FAKE" if not f['is_real'] else "⚠️  LOW"
            print(f"{i:>2}. {f['name']:<45} {f['score']:.2f}  {status}  ({f['total_issues']} issues)")
        
        if len(needs_review) > 15:
            print(f"\n... and {len(needs_review) - 15} more files\n")
    else:
        print(f"{'='*80}")
        print(f"✅ ALL FILES SCORE >= 0.80!")
        print(f"{'='*80}\n")
    
    # Recommendations
    print(f"{'='*80}")
    print(f"💡 RECOMMENDATIONS")
    print(f"{'='*80}\n")
    
    if len(all_critical) > 0:
        print(f"🔴 URGENT: Fix {len(all_critical)} files with critical issues")
    elif len(needs_review) > 5:
        print(f"⚠️  CONSIDER: Review {len(needs_review)} files with scores < 0.80")
    elif len(needs_review) > 0:
        print(f"📝 OPTIONAL: {len(needs_review)} files could be improved (low priority)")
    else:
        print(f"✅ ALL CLEAR: Backend is in excellent shape!")
    
    if 'perfect_structure_no_impl' in pattern_count and pattern_count['perfect_structure_no_impl'] > 50:
        print(f"📝 INFO: {pattern_count['perfect_structure_no_impl']} unused imports (cleanup recommended)")
    
    print()
    
    # Summary
    print(f"{'='*80}")
    print(f"🎯 BACKEND HEALTH SUMMARY")
    print(f"{'='*80}\n")
    
    health_score = avg_score * 100
    if health_score >= 95:
        status = "🟢 EXCELLENT"
    elif health_score >= 90:
        status = "🟢 VERY GOOD"
    elif health_score >= 85:
        status = "🟡 GOOD"
    elif health_score >= 80:
        status = "🟡 ACCEPTABLE"
    else:
        status = "🔴 NEEDS WORK"
    
    print(f"Overall Health:           {status}")
    print(f"Average Score:            {avg_score:.2f} ({get_grade(avg_score)})")
    print(f"Files >= 0.80:            {total_files - len(needs_review)} / {total_files} ({(total_files-len(needs_review))/total_files*100:.1f}%)")
    print(f"Critical Issues:          {len(all_critical)}")
    print(f"High-Severity Issues:     {len(all_high)}")
    
    if len(all_critical) == 0 and avg_score >= 0.85:
        print(f"\n✅ PRODUCTION-READY: Backend can be deployed!")
    elif len(all_critical) == 0:
        print(f"\n⚠️  ACCEPTABLE: Backend works, but could be improved")
    else:
        print(f"\n🔴 NOT READY: Fix critical issues before deployment")
    
    print()
    print(f"{'='*80}")
    
    return {
        'total_files': total_files,
        'avg_score': avg_score,
        'critical': len(all_critical),
        'high': len(all_high),
        'needs_review': len(needs_review)
    }

def get_grade(score):
    """Convert score to letter grade"""
    if score >= 0.97:
        return "A+"
    elif score >= 0.93:
        return "A"
    elif score >= 0.90:
        return "A-"
    elif score >= 0.87:
        return "B+"
    elif score >= 0.83:
        return "B"
    elif score >= 0.80:
        return "B-"
    elif score >= 0.77:
        return "C+"
    elif score >= 0.70:
        return "C"
    else:
        return "D"

if __name__ == "__main__":
    results = asyncio.run(comprehensive_audit())
    sys.exit(results['critical'])  # Exit code = number of critical issues

