#!/usr/bin/env python3
"""
Variable Consistency Validation Script
Validates that all environment variables are consistently named across the codebase
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class VariableConsistencyValidator:
    def __init__(self):
        self.backend_config_vars = set()
        self.template_vars = set()
        self.service_code_vars = set()
        self.issues = []
        
    def load_backend_config_variables(self) -> Set[str]:
        """Load variables defined in backend config"""
        config_file = Path("app/core/config.py")
        if not config_file.exists():
            return set()
            
        with open(config_file, 'r') as f:
            content = f.read()
            
        # Extract variable names from class attributes
        var_pattern = r'^\s*([A-Z_][A-Z0-9_]*):\s*'
        variables = set()
        
        for line in content.split('\n'):
            match = re.match(var_pattern, line)
            if match:
                variables.add(match.group(1))
                
        return variables
    
    def load_template_variables(self) -> Set[str]:
        """Load variables from environment templates"""
        template_files = [
            "ENHANCED_ENV_TEMPLATE.md",
            "ENVIRONMENT_TEMPLATE.md"
        ]
        
        variables = set()
        for template_file in template_files:
            if Path(template_file).exists():
                with open(template_file, 'r') as f:
                    content = f.read()
                    
                # Extract variable names from bash comments
                var_pattern = r'^([A-Z_][A-Z0-9_]*)='
                for line in content.split('\n'):
                    match = re.match(var_pattern, line)
                    if match:
                        variables.add(match.group(1))
                        
        return variables
    
    def load_service_code_variables(self) -> Dict[str, List[str]]:
        """Load variables used in service code"""
        service_files = [
            "app/services/smart_coding_ai_optimized.py",
            "app/services/auth_service.py",
            "app/core/database.py",
            "app/core/redis.py"
        ]
        
        variables = {}
        for service_file in service_files:
            file_path = Path(service_file)
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Extract os.getenv calls
                getenv_pattern = r'os\.getenv\(["\']([^"\']+)["\']'
                file_vars = re.findall(getenv_pattern, content)
                
                # Extract settings.* references
                settings_pattern = r'settings\.([A-Z_][A-Z0-9_]*)'
                settings_vars = re.findall(settings_pattern, content)
                
                variables[service_file] = list(set(file_vars + settings_vars))
                
        return variables
    
    def validate_jwt_secret_consistency(self) -> List[str]:
        """Validate JWT secret variable naming"""
        issues = []
        
        # Check if JWT_SECRET_KEY still exists in templates
        template_files = ["ENHANCED_ENV_TEMPLATE.md", "ENVIRONMENT_TEMPLATE.md"]
        for template_file in template_files:
            if Path(template_file).exists():
                with open(template_file, 'r') as f:
                    content = f.read()
                    
                if "JWT_SECRET_KEY" in content:
                    issues.append(f"ERROR: {template_file} still contains JWT_SECRET_KEY (should be JWT_SECRET)")
                    
        # Check if JWT_SECRET exists in backend config
        config_file = Path("app/core/config.py")
        if config_file.exists():
            with open(config_file, 'r') as f:
                content = f.read()
                
            if "JWT_SECRET:" not in content:
                issues.append("ERROR: Backend config missing JWT_SECRET definition")
            else:
                issues.append("SUCCESS: JWT_SECRET properly defined in backend config")
                
        return issues
    
    def validate_frontend_variables(self) -> List[str]:
        """Validate frontend NEXT_PUBLIC_* variables"""
        issues = []
        required_frontend_vars = [
            "NEXT_PUBLIC_SUPABASE_URL",
            "NEXT_PUBLIC_SUPABASE_ANON_KEY", 
            "NEXT_PUBLIC_API_URL",
            "NEXT_PUBLIC_APP_URL"
        ]
        
        template_files = ["ENHANCED_ENV_TEMPLATE.md", "ENVIRONMENT_TEMPLATE.md"]
        for template_file in template_files:
            if Path(template_file).exists():
                with open(template_file, 'r') as f:
                    content = f.read()
                    
                for var in required_frontend_vars:
                    if var in content:
                        issues.append(f"SUCCESS: {var} found in {template_file}")
                    else:
                        issues.append(f"ERROR: {var} missing from {template_file}")
                        
        return issues
    
    def validate_redis_consistency(self) -> List[str]:
        """Validate Redis URL variable consistency"""
        issues = []
        
        # Check service code uses UPSTASH_REDIS_REST_URL
        service_file = Path("app/services/smart_coding_ai_optimized.py")
        if service_file.exists():
            with open(service_file, 'r') as f:
                content = f.read()
                
            if 'os.getenv("REDIS_URL"' in content:
                issues.append("ERROR: Service code still uses REDIS_URL (should use UPSTASH_REDIS_REST_URL)")
            elif 'os.getenv("UPSTASH_REDIS_REST_URL"' in content:
                issues.append("SUCCESS: Service code correctly uses UPSTASH_REDIS_REST_URL")
            else:
                issues.append("WARNING: No Redis URL usage found in service code")
                
        return issues
    
    def run_validation(self) -> Dict[str, List[str]]:
        """Run complete validation"""
        results = {
            "jwt_secret": self.validate_jwt_secret_consistency(),
            "frontend_variables": self.validate_frontend_variables(),
            "redis_consistency": self.validate_redis_consistency()
        }
        
        return results
    
    def print_results(self, results: Dict[str, List[str]]):
        """Print validation results"""
        print("Variable Consistency Validation Results")
        print("=" * 50)
        
        for category, issues in results.items():
            print(f"\n{category.upper().replace('_', ' ')}")
            print("-" * 30)
            
            for issue in issues:
                print(f"  {issue}")
                
        # Summary
        total_issues = sum(len([i for i in issues if i.startswith("ERROR:")]) for issues in results.values())
        total_checks = sum(len(issues) for issues in results.values())
        
        print(f"\nSUMMARY")
        print("-" * 20)
        print(f"Total Issues: {total_issues}")
        print(f"Total Checks: {total_checks}")
        
        if total_issues == 0:
            print("SUCCESS: All variable consistency checks passed!")
        else:
            print(f"ERROR: {total_issues} issues need to be resolved")

def main():
    """Main validation function"""
    validator = VariableConsistencyValidator()
    results = validator.run_validation()
    validator.print_results(results)
    
    # Return exit code based on results
    total_issues = sum(len([i for i in issues if i.startswith("❌")]) for issues in results.values())
    return 0 if total_issues == 0 else 1

if __name__ == "__main__":
    exit(main())
