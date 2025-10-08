"""
Smart Coding AI Core - DependencyTracker
Extracted from smart_coding_ai_optimized.py
"""

import structlog
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
import ast
import os
from pathlib import Path

logger = structlog.get_logger()


class DependencyTracker:
    """Tracks project dependencies and configurations"""
    
    def __init__(self):
        self.dependency_cache: Dict[str, List[Dict]] = {}
        self.config_cache: Dict[str, Dict] = {}
    
    async def analyze_dependencies(self, project_path: str) -> List[Dict]:
        """Analyze project dependencies"""
        try:
            project_path = Path(project_path)
            dependencies = []
            
            # Python dependencies
            requirements_files = list(project_path.glob("requirements*.txt"))
            for req_file in requirements_files:
                deps = await self._parse_requirements_file(req_file)
                dependencies.extend(deps)
            
            # Node.js dependencies
            package_json = project_path / "package.json"
            if package_json.exists():
                deps = await self._parse_package_json(package_json)
                dependencies.extend(deps)
            
            # PHP dependencies
            composer_json = project_path / "composer.json"
            if composer_json.exists():
                deps = await self._parse_composer_json(composer_json)
                dependencies.extend(deps)
            
            # Rust dependencies
            cargo_toml = project_path / "Cargo.toml"
            if cargo_toml.exists():
                deps = await self._parse_cargo_toml(cargo_toml)
                dependencies.extend(deps)
            
            return dependencies
            
        except Exception as e:
            logger.error(f"Failed to analyze dependencies: {e}")
            return []
    
    async def _parse_requirements_file(self, file_path: Path) -> List[Dict]:
        """Parse Python requirements file"""
        dependencies = []
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        dep_info = await self._parse_python_dependency(line)
                        if dep_info:
                            dep_info.update({
                                "source": str(file_path),
                                "type": "python_package"
                            })
                            dependencies.append(dep_info)
        except Exception as e:
            logger.error(f"Failed to parse requirements file {file_path}: {e}")
        
        return dependencies
    
    async def _parse_package_json(self, file_path: Path) -> List[Dict]:
        """Parse Node.js package.json"""
        dependencies = []
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                # Production dependencies
                for name, version in data.get("dependencies", {}).items():
                    dependencies.append({
                        "dependency_id": str(uuid.uuid4()),
                        "name": name,
                        "version": version,
                        "type": "npm_package",
                        "source": str(file_path),
                        "is_dev_dependency": False
                    })
                
                # Dev dependencies
                for name, version in data.get("devDependencies", {}).items():
                    dependencies.append({
                        "dependency_id": str(uuid.uuid4()),
                        "name": name,
                        "version": version,
                        "type": "npm_package",
                        "source": str(file_path),
                        "is_dev_dependency": True
                    })
        except Exception as e:
            logger.error(f"Failed to parse package.json {file_path}: {e}")
        
        return dependencies
    
    async def _parse_composer_json(self, file_path: Path) -> List[Dict]:
        """Parse PHP composer.json"""
        dependencies = []
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                for name, version in data.get("require", {}).items():
                    dependencies.append({
                        "dependency_id": str(uuid.uuid4()),
                        "name": name,
                        "version": version,
                        "type": "php_package",
                        "source": str(file_path),
                        "is_dev_dependency": False
                    })
                
                for name, version in data.get("require-dev", {}).items():
                    dependencies.append({
                        "dependency_id": str(uuid.uuid4()),
                        "name": name,
                        "version": version,
                        "type": "php_package",
                        "source": str(file_path),
                        "is_dev_dependency": True
                    })
        except Exception as e:
            logger.error(f"Failed to parse composer.json {file_path}: {e}")
        
        return dependencies
    
    async def _parse_cargo_toml(self, file_path: Path) -> List[Dict]:
        """Parse Rust Cargo.toml"""
        dependencies = []
        try:
            # Simple TOML parsing (could be improved with toml library)
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Extract dependencies section
            if "[dependencies]" in content:
                deps_section = content.split("[dependencies]")[1].split("[")[0]
                for line in deps_section.split('\n'):
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        name = line.split('=')[0].strip()
                        version = line.split('=')[1].strip().strip('"\'')
                        dependencies.append({
                            "dependency_id": str(uuid.uuid4()),
                            "name": name,
                            "version": version,
                            "type": "rust_crate",
                            "source": str(file_path),
                            "is_dev_dependency": False
                        })
        except Exception as e:
            logger.error(f"Failed to parse Cargo.toml {file_path}: {e}")
        
        return dependencies
    
    async def _parse_python_dependency(self, line: str) -> Optional[Dict]:
        """Parse individual Python dependency line"""
        try:
            # Handle different formats: package==1.0.0, package>=1.0.0, package~=1.0.0, etc.
            if '==' in line:
                name, version = line.split('==', 1)
                return {
                    "dependency_id": str(uuid.uuid4()),
                    "name": name.strip(),
                    "version": version.strip(),
                    "is_dev_dependency": False
                }
            elif '>=' in line:
                name, version = line.split('>=', 1)
                return {
                    "dependency_id": str(uuid.uuid4()),
                    "name": name.strip(),
                    "version": f">={version.strip()}",
                    "is_dev_dependency": False
                }
            elif '<=' in line:
                name, version = line.split('<=', 1)
                return {
                    "dependency_id": str(uuid.uuid4()),
                    "name": name.strip(),
                    "version": f"<={version.strip()}",
                    "is_dev_dependency": False
                }
            elif '~=' in line:
                name, version = line.split('~=', 1)
                return {
                    "dependency_id": str(uuid.uuid4()),
                    "name": name.strip(),
                    "version": f"~={version.strip()}",
                    "is_dev_dependency": False
                }
            else:
                # Just package name
                return {
                    "dependency_id": str(uuid.uuid4()),
                    "name": line.strip(),
                    "version": "latest",
                    "is_dev_dependency": False
                }
        except Exception as e:
            logger.error(f"Failed to parse Python dependency line '{line}': {e}")
            return None




__all__ = ['DependencyTracker']
