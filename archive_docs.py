"""
Archive non-essential documentation files
Keep only 18 essential files in root directory
"""

import os
import shutil
from pathlib import Path

# Essential files to keep
ESSENTIAL_FILES = {
    # Existing documentation
    'README.md',
    
    # New CTO review documents
    'CTO_REVIEW_REPORT.md',
    'ARCHITECTURE_IMPROVEMENT_PLAN.md',
    'EXECUTIVE_SUMMARY.md',
    
    # Essential docs (create if missing)
    'ARCHITECTURE.md',
    'API_DOCUMENTATION.md',
    'DEVELOPMENT_GUIDE.md',
    'DEPLOYMENT_GUIDE.md',
    'TESTING_GUIDE.md',
    'CONTRIBUTING.md',
    'CHANGELOG.md',
    'SECURITY.md',
    'DATABASE_SCHEMA.md',
    'CONFIGURATION.md',
    'TROUBLESHOOTING.md',
    'MIGRATION_GUIDE.md',
    'CODE_STYLE.md',
    'ROADMAP.md',
}

def main():
    # Create archive directory
    archive_dir = Path('archive/documentation_archive_2025_10_10')
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all markdown files in root
    root_dir = Path('.')
    md_files = list(root_dir.glob('*.md'))
    
    print(f"Found {len(md_files)} markdown files in root directory")
    print(f"Essential files to keep: {len(ESSENTIAL_FILES)}")
    
    # Move non-essential files to archive
    moved_count = 0
    kept_count = 0
    
    for md_file in md_files:
        if md_file.name in ESSENTIAL_FILES:
            print(f"✓ Keeping: {md_file.name}")
            kept_count += 1
        else:
            try:
                dest = archive_dir / md_file.name
                shutil.move(str(md_file), str(dest))
                print(f"→ Archived: {md_file.name}")
                moved_count += 1
            except Exception as e:
                print(f"✗ Error moving {md_file.name}: {e}")
    
    print("\n" + "="*60)
    print("ARCHIVING COMPLETE")
    print("="*60)
    print(f"Files kept in root:    {kept_count}")
    print(f"Files archived:        {moved_count}")
    print(f"Archive location:      {archive_dir}")
    print("\nEssential files kept:")
    
    # List what we kept
    remaining_files = sorted(root_dir.glob('*.md'))
    for f in remaining_files:
        print(f"  - {f.name}")
    
    # Check for missing essential files
    existing_files = {f.name for f in remaining_files}
    missing_files = ESSENTIAL_FILES - existing_files
    if missing_files:
        print(f"\nMissing essential files (need to create):")
        for f in sorted(missing_files):
            print(f"  - {f}")

if __name__ == '__main__':
    main()

