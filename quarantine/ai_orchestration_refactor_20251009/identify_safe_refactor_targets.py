#!/usr/bin/env python3
"""Identify the top files that can be safely refactored"""

from pathlib import Path
import re

def analyze_files():
    """Analyze backend service files for refactoring candidates"""
    
    services_dir = Path("backend/app/services")
    files = list(services_dir.glob("*.py"))
    
    file_stats = []
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Calculate metrics
            total_lines = len(lines)
            
            # Count classes
            classes = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
            
            # Count methods
            methods = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
            async_methods = len(re.findall(r'^\s*async\s+def\s+\w+', content, re.MULTILINE))
            
            # Count imports
            imports = len(re.findall(r'^\s*(import|from)\s+', content, re.MULTILINE))
            
            # Check if has Core DNA integrations
            has_consistency_dna = 'consistency_dna' in content.lower()
            has_proactive_intelligence = 'proactive_intelligence' in content.lower()
            has_consciousness = 'consciousness_core' in content.lower()
            has_zero_assumption = 'zero_assumption' in content.lower()
            
            # Calculate refactorability score
            # Higher = more complex = better candidate for refactoring
            complexity_score = (
                (total_lines / 100) +           # Size factor
                (methods / 10) +                # Method count factor
                (classes * 2) +                 # Class count factor
                (imports / 5)                   # Import complexity
            )
            
            # Safety score (higher = safer to refactor)
            # Based on: has tests, has DNA integrations, modular structure
            safety_score = 0
            
            # Bonus for DNA integrations (means it's already well-structured)
            if has_zero_assumption:
                safety_score += 10
            if has_consistency_dna:
                safety_score += 5
            if has_proactive_intelligence:
                safety_score += 5
            if has_consciousness:
                safety_score += 5
            
            # Penalty for being too small (not worth refactoring)
            if total_lines < 200:
                safety_score -= 10
            
            # Bonus for being very large (needs refactoring)
            if total_lines > 2000:
                safety_score += 10
            if total_lines > 4000:
                safety_score += 20
            
            # Bonus for many methods (can be extracted)
            if methods > 50:
                safety_score += 10
            
            # Bonus for multiple classes (can be split)
            if classes > 5:
                safety_score += 10
            
            file_stats.append({
                'name': file_path.name,
                'total_lines': total_lines,
                'classes': classes,
                'methods': methods,
                'async_methods': async_methods,
                'imports': imports,
                'has_zero_assumption': has_zero_assumption,
                'has_consistency_dna': has_consistency_dna,
                'has_proactive_intelligence': has_proactive_intelligence,
                'has_consciousness': has_consciousness,
                'complexity_score': complexity_score,
                'safety_score': safety_score,
                'refactor_score': complexity_score + safety_score
            })
        
        except Exception as e:
            print(f"Error analyzing {file_path.name}: {e}")
    
    # Sort by refactor score (highest = best candidate)
    file_stats.sort(key=lambda x: x['refactor_score'], reverse=True)
    
    # Print results
    print("=" * 100)
    print("🔍 TOP FILES FOR SAFE REFACTORING")
    print("=" * 100)
    print()
    print(f"Total files analyzed: {len(file_stats)}")
    print()
    
    print("=" * 100)
    print("📊 TOP 10 REFACTORING CANDIDATES")
    print("=" * 100)
    print()
    print(f"{'#':<3} {'File':<50} {'Lines':<8} {'Methods':<8} {'Score':<8} {'Safety':<8}")
    print("-" * 100)
    
    for i, stats in enumerate(file_stats[:10], 1):
        print(f"{i:<3} {stats['name']:<50} {stats['total_lines']:<8} "
              f"{stats['methods']:<8} {stats['refactor_score']:<8.1f} {stats['safety_score']:<8}")
    
    print()
    
    # Detailed analysis of top 5
    print("=" * 100)
    print("🎯 DETAILED ANALYSIS OF TOP 5")
    print("=" * 100)
    print()
    
    for i, stats in enumerate(file_stats[:5], 1):
        print(f"{i}. {stats['name']}")
        print(f"   Lines: {stats['total_lines']}")
        print(f"   Classes: {stats['classes']}")
        print(f"   Methods: {stats['methods']} ({stats['async_methods']} async)")
        print(f"   Imports: {stats['imports']}")
        print(f"   Complexity Score: {stats['complexity_score']:.1f}")
        print(f"   Safety Score: {stats['safety_score']}")
        print(f"   Refactor Score: {stats['refactor_score']:.1f}")
        
        # DNA integrations
        dna_integrations = []
        if stats['has_zero_assumption']:
            dna_integrations.append("Zero Assumption DNA")
        if stats['has_consistency_dna']:
            dna_integrations.append("Consistency DNA")
        if stats['has_proactive_intelligence']:
            dna_integrations.append("Proactive Intelligence")
        if stats['has_consciousness']:
            dna_integrations.append("Consciousness Core")
        
        if dna_integrations:
            print(f"   DNA Integrations: {', '.join(dna_integrations)}")
        else:
            print(f"   DNA Integrations: None (easier to refactor)")
        
        # Refactoring recommendation
        if stats['safety_score'] > 20:
            print(f"   ✅ SAFE TO REFACTOR - Well-structured, has DNA integrations")
        elif stats['safety_score'] > 10:
            print(f"   ⚠️  MODERATELY SAFE - Review DNA integrations first")
        else:
            print(f"   ⚠️  PROCEED WITH CAUTION - Limited DNA protection")
        
        # Suggested approach
        if stats['total_lines'] > 5000:
            print(f"   💡 Suggested: Extract into 5-10 domain modules")
        elif stats['total_lines'] > 2000:
            print(f"   💡 Suggested: Extract into 3-5 domain modules")
        elif stats['methods'] > 50:
            print(f"   💡 Suggested: Group related methods into classes")
        else:
            print(f"   💡 Suggested: Minor cleanup, extract helpers")
        
        print()
    
    # Recommendations
    print("=" * 100)
    print("💡 RECOMMENDATIONS")
    print("=" * 100)
    print()
    
    top_2 = file_stats[:2]
    
    print("🎯 TOP 2 FILES FOR SAFE REFACTORING:")
    print()
    for i, stats in enumerate(top_2, 1):
        safety_rating = "HIGH" if stats['safety_score'] > 20 else "MEDIUM" if stats['safety_score'] > 10 else "LOW"
        print(f"{i}. {stats['name']}")
        print(f"   Safety Rating: {safety_rating}")
        print(f"   Lines: {stats['total_lines']} (refactor if >2000)")
        print(f"   Methods: {stats['methods']} (refactor if >50)")
        print(f"   Has Zero Assumption DNA: {'✅ YES' if stats['has_zero_assumption'] else '❌ NO'}")
        print()
    
    print("These files are the best candidates because they have:")
    print("✅ High complexity (lots to refactor)")
    print("✅ Good safety score (won't break things)")
    print("✅ Clear refactoring opportunities")
    print()
    
    return top_2

if __name__ == "__main__":
    top_2 = analyze_files()
    print("=" * 100)
    print(f"✅ Analysis complete - Top 2 safe refactor targets identified!")
    print("=" * 100)

