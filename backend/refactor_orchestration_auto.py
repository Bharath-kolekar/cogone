"""
Automated Refactoring Script for ai_orchestration_layer.py
Uses AST parsing to extract remaining classes and create modular structure

This script will:
1. Parse ai_orchestration_layer.py with AST
2. Extract all remaining classes (excluding already extracted validators)
3. Organize into proper directories (strategies, monitoring, engines, managers)
4. Create module files with proper imports
5. Generate __init__.py files
6. Preserve all functionality
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import re

class OrchestrationRefactorer:
    """Automated refactoring for ai_orchestration_layer.py"""
    
    def __init__(self, source_file: str, target_base: str):
        self.source_file = source_file
        self.target_base = target_base
        self.source_code = None
        self.tree = None
        self.classes = []
        
        # Already extracted validators
        self.extracted_validators = {
            'FactualAccuracyValidator',
            'ContextAwarenessManager',
            'ConsistencyEnforcer',
            'PracticalityValidator',
            'SecurityValidator',
            'MaintainabilityEnforcer',
            'PerformanceOptimizer',
            'CodeQualityAnalyzer',
            'ArchitectureValidator',
            'BusinessLogicValidator',
            'IntegrationValidator'
        }
        
        # Already extracted core classes
        self.extracted_core = {
            'AIOrchestrationLayer',
            'AutonomousAIOrchestrationLayer',
            'EnhancedAutonomousAIOrchestrationLayer'
        }
        
        # Already extracted coordination
        self.extracted_coordination = {
            'IntelligentTaskDecomposer',
            'MultiAgentCoordinator'
        }
        
        # Class categories for organization
        self.categories = {
            'engines': [
                'AutonomousLearningEngine',
                'AutonomousOptimizationEngine',
                'AutonomousHealingEngine',
                'AutonomousMonitoringEngine',
                'AutonomousDecisionEngine',
                'AutonomousStrategyEngine',
                'AutonomousAdaptationEngine',
                'AutonomousCreativeEngine',
                'AutonomousInnovationEngine'
            ],
            'managers': [
                'WorkflowManager',
                'QualityAssuranceManager',
                'StateManager',
                'ToolIntegrationManager',
                'ErrorRecoveryManager',
                'ContinuousLearningManager',
                'ExternalIntegrationManager',
                'MonitoringAnalyticsManager'
            ],
            'validators_maximum': [
                'MaximumAccuracyValidator',
                'MaximumConsistencyValidator',
                'MaximumThresholdValidator',
                'ResourceOptimizedValidator'
            ]
        }
    
    def parse_file(self):
        """Parse the source file with AST"""
        print(f" Reading {self.source_file}...")
        with open(self.source_file, 'r', encoding='utf-8') as f:
            self.source_code = f.read()
        
        print(" Parsing with AST...")
        self.tree = ast.parse(self.source_code)
        print(" File parsed successfully!")
    
    def extract_classes(self):
        """Extract all class definitions"""
        print("\n Extracting classes...")
        
        source_lines = self.source_code.split('\n')
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                # Skip already extracted classes
                if (class_name in self.extracted_validators or 
                    class_name in self.extracted_core or
                    class_name in self.extracted_coordination):
                    print(f"    Skipping {class_name} (already extracted)")
                    continue
                
                # Get source code for this class
                start_line = node.lineno - 1
                end_line = node.end_lineno
                
                class_source_lines = source_lines[start_line:end_line]
                class_source = '\n'.join(class_source_lines)
                
                # Extract imports needed for this class
                imports = self._extract_imports_for_class(class_source)
                
                # Categorize the class
                category = self._categorize_class(class_name)
                
                self.classes.append({
                    'name': class_name,
                    'source': class_source,
                    'imports': imports,
                    'category': category,
                    'start_line': start_line + 1,
                    'end_line': end_line,
                    'lines': end_line - start_line
                })
                
                print(f"   {class_name} ({end_line - start_line} lines)  {category}")
        
        print(f"\n Total classes to extract: {len(self.classes)}")
        return self.classes
    
    def _extract_imports_for_class(self, class_source: str) -> List[str]:
        """Extract necessary imports for a class"""
        imports = []
        
        # Common imports needed
        base_imports = [
            'import asyncio',
            'import logging',
            'from typing import Dict, List, Optional, Any, Tuple',
            'from datetime import datetime, timedelta',
            'from uuid import uuid4',
        ]
        
        # Check what imports are needed based on code content
        if 're.' in class_source or 'import re' in class_source:
            base_imports.append('import re')
        
        if 'json.' in class_source or 'import json' in class_source:
            base_imports.append('import json')
        
        if 'uuid4' in class_source:
            base_imports.append('from uuid import uuid4')
        
        return base_imports
    
    def _categorize_class(self, class_name: str) -> str:
        """Categorize class into appropriate directory"""
        for category, classes in self.categories.items():
            if class_name in classes:
                return category
        
        # Default categorization
        if 'Engine' in class_name:
            return 'engines'
        elif 'Manager' in class_name:
            return 'managers'
        elif 'Validator' in class_name:
            return 'validators_maximum'
        else:
            return 'other'
    
    def create_modules(self):
        """Create module files for each class"""
        print("\n Creating module files...")
        
        created_files = {}
        
        for cls in self.classes:
            category = cls['category']
            class_name = cls['name']
            
            # Create directory
            target_dir = os.path.join(self.target_base, category)
            os.makedirs(target_dir, exist_ok=True)
            
            # Create filename (snake_case)
            filename = self._to_snake_case(class_name) + '.py'
            filepath = os.path.join(target_dir, filename)
            
            # Create module content
            content = self._create_module_content(cls)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   Created {filepath}")
            
            if category not in created_files:
                created_files[category] = []
            created_files[category].append({
                'filename': filename,
                'class_name': class_name,
                'filepath': filepath
            })
        
        return created_files
    
    def _to_snake_case(self, name: str) -> str:
        """Convert CamelCase to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _create_module_content(self, cls: Dict) -> str:
        """Create complete module content with imports and class"""
        imports = '\n'.join(cls['imports'])
        
        content = f'''"""
{cls['name']} for AI Orchestration
Extracted from ai_orchestration_layer.py
"""

{imports}

logger = logging.getLogger(__name__)


{cls['source']}
'''
        return content
    
    def create_init_files(self, created_files: Dict):
        """Create __init__.py files for each category"""
        print("\n Creating __init__.py files...")
        
        for category, files in created_files.items():
            target_dir = os.path.join(self.target_base, category)
            init_file = os.path.join(target_dir, '__init__.py')
            
            # Create imports
            imports = []
            exports = []
            
            for file_info in files:
                module_name = file_info['filename'].replace('.py', '')
                class_name = file_info['class_name']
                imports.append(f"from .{module_name} import {class_name}")
                exports.append(f"    '{class_name}'")
            
            content = f'''"""
{category.replace('_', ' ').title()} for AI Orchestration
"""

{chr(10).join(imports)}

__all__ = [
{chr(10).join(exports)}
]
'''
            
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   Created {init_file}")
    
    def generate_report(self):
        """Generate refactoring report"""
        print("\n" + "="*70)
        print(" REFACTORING REPORT")
        print("="*70)
        
        # Group by category
        by_category = {}
        for cls in self.classes:
            category = cls['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(cls)
        
        total_lines = 0
        for category, classes in sorted(by_category.items()):
            lines = sum(c['lines'] for c in classes)
            total_lines += lines
            print(f"\n{category.upper()}: {len(classes)} classes, {lines} lines")
            for cls in sorted(classes, key=lambda x: x['name']):
                print(f"  - {cls['name']}: {cls['lines']} lines")
        
        print(f"\n{'='*70}")
        print(f"TOTAL: {len(self.classes)} classes, {total_lines} lines extracted")
        print(f"{'='*70}\n")
    
    def run(self):
        """Execute the refactoring"""
        print(" Starting Automated Refactoring")
        print("="*70)
        
        try:
            # Step 1: Parse file
            self.parse_file()
            
            # Step 2: Extract classes
            self.extract_classes()
            
            # Step 3: Create modules
            created_files = self.create_modules()
            
            # Step 4: Create __init__ files
            self.create_init_files(created_files)
            
            # Step 5: Generate report
            self.generate_report()
            
            print(" Automated refactoring complete!")
            print("\n Next steps:")
            print("  1. Review generated files")
            print("  2. Update main __init__.py to export new classes")
            print("  3. Run tests to verify")
            print("  4. Move original file to quarantine")
            
            return True
            
        except Exception as e:
            print(f"\n Error during refactoring: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point"""
    # Configuration
    source_file = "app/services/ai_orchestration_layer.py"
    target_base = "app/services/ai_orchestration"
    
    print("\n" + "="*70)
    print(" HYBRID REFACTORING: Automated Script + Manual Verification")
    print("="*70)
    print(f"\nSource: {source_file}")
    print(f"Target: {target_base}/")
    print()
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print(f" Error: Source file not found: {source_file}")
        print("Please run this script from the backend/ directory")
        return 1
    
    # Create refactorer
    refactorer = OrchestrationRefactorer(source_file, target_base)
    
    # Run refactoring
    success = refactorer.run()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

