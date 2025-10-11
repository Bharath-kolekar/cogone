"""
Frontend Assessment Script
Analyzes the quarantined frontend for salvageability
"""

import os
import json
from pathlib import Path
from collections import defaultdict

def assess_frontend():
    """Assess the quarantined frontend"""
    
    frontend_path = Path("quarantine/frontend_corrupted_20251009_081509")
    
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        return
    
    print("="*70)
    print("FRONTEND ASSESSMENT")
    print("="*70)
    print()
    
    # Count files by type
    file_counts = defaultdict(int)
    total_size = 0
    
    # Component analysis
    components = []
    pages = []
    hooks = []
    services = []
    issues = []
    
    for file_path in frontend_path.rglob("*"):
        if file_path.is_file() and "node_modules" not in str(file_path):
            ext = file_path.suffix
            file_counts[ext] += 1
            total_size += file_path.stat().st_size
            
            # Categorize files
            rel_path = str(file_path.relative_to(frontend_path))
            
            if "components" in rel_path and ext in ['.tsx', '.jsx']:
                components.append(rel_path)
            elif "app" in rel_path and ext == '.tsx':
                pages.append(rel_path)
            elif "hooks" in rel_path:
                hooks.append(rel_path)
            elif "services" in rel_path:
                services.append(rel_path)
    
    # Print file statistics
    print("📊 FILE STATISTICS")
    print("-" * 70)
    print(f"Total files (excluding node_modules): {sum(file_counts.values())}")
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    print()
    
    print("File breakdown:")
    for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True):
        if ext and count > 0:
            print(f"  {ext:10s}: {count:4d} files")
    print()
    
    # Component analysis
    print("🎨 COMPONENTS")
    print("-" * 70)
    print(f"Total components: {len(components)}")
    print()
    key_components = [c for c in components if any(x in c.lower() for x in ['dashboard', 'editor', 'voice', 'ai', 'smart'])]
    print(f"Key components identified: {len(key_components)}")
    for comp in key_components[:10]:
        print(f"  ✓ {comp}")
    if len(key_components) > 10:
        print(f"  ... and {len(key_components) - 10} more")
    print()
    
    # Pages analysis
    print("📄 PAGES (App Router)")
    print("-" * 70)
    print(f"Total pages: {len(pages)}")
    for page in sorted(pages):
        print(f"  ✓ {page}")
    print()
    
    # Hooks analysis
    print("🪝 CUSTOM HOOKS")
    print("-" * 70)
    print(f"Total hooks: {len(hooks)}")
    for hook in hooks:
        print(f"  ✓ {hook}")
    print()
    
    # Check key config files
    print("⚙️  CONFIGURATION FILES")
    print("-" * 70)
    
    config_files = {
        "package.json": "Package configuration",
        "tsconfig.json": "TypeScript configuration",
        "next.config.js": "Next.js configuration",
        "tailwind.config.js": "Tailwind CSS configuration"
    }
    
    for filename, description in config_files.items():
        file_path = frontend_path / filename
        if file_path.exists():
            print(f"  ✓ {filename:20s} - {description}")
        else:
            print(f"  ✗ {filename:20s} - MISSING")
            issues.append(f"Missing {filename}")
    print()
    
    # Check dependencies
    print("📦 DEPENDENCIES")
    print("-" * 70)
    
    package_json = frontend_path / "package.json"
    if package_json.exists():
        with open(package_json) as f:
            package_data = json.load(f)
            
        deps = package_data.get('dependencies', {})
        dev_deps = package_data.get('devDependencies', {})
        
        print(f"Dependencies: {len(deps)}")
        print(f"Dev Dependencies: {len(dev_deps)}")
        print()
        
        # Key dependencies
        key_deps = {
            'next': 'Next.js framework',
            'react': 'React library',
            '@tanstack/react-query': 'Data fetching',
            '@trpc/client': 'tRPC client',
            'tailwindcss': 'Tailwind CSS'
        }
        
        print("Key dependencies:")
        for dep, desc in key_deps.items():
            if dep in deps:
                version = deps[dep]
                print(f"  ✓ {dep:30s} {version:10s} - {desc}")
            else:
                print(f"  ✗ {dep:30s} {'MISSING':10s} - {desc}")
                issues.append(f"Missing dependency: {dep}")
    else:
        print("  ✗ package.json not found!")
        issues.append("Missing package.json")
    print()
    
    # Salvageability assessment
    print("="*70)
    print("🎯 SALVAGEABILITY ASSESSMENT")
    print("="*70)
    print()
    
    # Calculate salvageability score
    score = 100
    
    # Deduct points for issues
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  ⚠️  {issue}")
            score -= 5
        print()
    
    # Check structure
    structure_items = [
        ("app/ directory", frontend_path / "app"),
        ("components/ directory", frontend_path / "components"),
        ("lib/ directory", frontend_path / "lib"),
        ("hooks/ directory", frontend_path / "hooks"),
    ]
    
    print("Structure integrity:")
    for name, path in structure_items:
        if path.exists():
            print(f"  ✓ {name}")
        else:
            print(f"  ✗ {name} - MISSING")
            score -= 10
    print()
    
    # Final assessment
    print(f"SALVAGEABILITY SCORE: {score}%")
    print()
    
    if score >= 80:
        print("✅ VERDICT: HIGHLY SALVAGEABLE - Restore and fix")
        print("   Recommendation: Fix issues and restore")
        print("   Estimated effort: 2-3 days")
    elif score >= 60:
        print("⚠️  VERDICT: MODERATELY SALVAGEABLE - Restore with caution")
        print("   Recommendation: Fix critical issues, consider partial rebuild")
        print("   Estimated effort: 3-5 days")
    elif score >= 40:
        print("🟡 VERDICT: MARGINALLY SALVAGEABLE - Consider rebuild")
        print("   Recommendation: Rebuild may be faster")
        print("   Estimated effort: 5-7 days to restore, 4-5 days to rebuild")
    else:
        print("🔴 VERDICT: NOT SALVAGEABLE - Rebuild recommended")
        print("   Recommendation: Clean rebuild from scratch")
        print("   Estimated effort: 5-7 days")
    print()
    
    # Next steps
    print("="*70)
    print("📋 RECOMMENDED NEXT STEPS")
    print("="*70)
    print()
    
    if score >= 60:
        print("1. Copy frontend from quarantine to root")
        print("2. Install dependencies: npm install")
        print("3. Fix TypeScript errors: npm run type-check")
        print("4. Fix linting issues: npm run lint")
        print("5. Test build: npm run build")
        print("6. Test development server: npm run dev")
    else:
        print("1. Create new Next.js app: npx create-next-app@latest frontend")
        print("2. Port salvageable components from quarantine")
        print("3. Rebuild pages with clean structure")
        print("4. Reconnect to backend APIs")
        print("5. Add tests and documentation")
    print()

if __name__ == "__main__":
    assess_frontend()

