"""
ChangeExecutor Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ChangeExecutor:
    """Executes code changes autonomously"""
    
    def __init__(self):
        self.backup_dir = Path("agent_mode_backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    async def execute_changes(self, changes: List[CodeChange], task_id: str) -> Dict[str, Any]:
        """Execute a list of code changes"""
        try:
            logger.info("Executing changes", task_id=task_id, changes_count=len(changes))
            
            # Create backup
            backup_path = await self._create_backup(task_id)
            
            results = {
                "successful_changes": [],
                "failed_changes": [],
                "backup_path": str(backup_path),
                "total_changes": len(changes)
            }
            
            for change in changes:
                try:
                    await self._execute_change(change)
                    results["successful_changes"].append(change.change_id)
                    logger.info("Change executed successfully", change_id=change.change_id)
                except Exception as e:
                    results["failed_changes"].append({
                        "change_id": change.change_id,
                        "error": str(e)
                    })
                    logger.error("Failed to execute change", change_id=change.change_id, error=str(e))
            
            return results
            
        except Exception as e:
            logger.error("Failed to execute changes", error=str(e))
            raise
    
    async def _create_backup(self, task_id: str) -> Path:
        """Create backup of current state"""
        backup_path = self.backup_dir / f"backup_{task_id}_{int(time.time())}"
        backup_path.mkdir(exist_ok=True)
        
        # Copy all files to backup
        for root, dirs, files in os.walk(Path.cwd()):
            for file in files:
                if not str(Path(root) / file).startswith(str(self.backup_dir)):
                    src = Path(root) / file
                    rel_path = src.relative_to(Path.cwd())
                    dst = backup_path / rel_path
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        import shutil
                        shutil.copy2(src, dst)
                    except:
                        pass
        
        return backup_path
    
    async def _execute_change(self, change: CodeChange):
        """Execute a single change"""
        if change.change_type == ChangeType.CREATE_FILE:
            await self._create_file(change)
        elif change.change_type == ChangeType.MODIFY_FILE:
            await self._modify_file(change)
        elif change.change_type == ChangeType.DELETE_FILE:
            await self._delete_file(change)
        elif change.change_type == ChangeType.ADD_DEPENDENCY:
            await self._add_dependency(change)
        elif change.change_type == ChangeType.ADD_IMPORT:
            await self._add_import(change)
        elif change.change_type == ChangeType.ADD_FUNCTION:
            await self._add_function(change)
        elif change.change_type == ChangeType.ADD_CLASS:
            await self._add_class(change)
    
    async def _create_file(self, change: CodeChange):
        """Create a new file"""
        file_path = Path(change.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(change.new_content)
    
    async def _modify_file(self, change: CodeChange):
        """Modify an existing file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple replacement for now
            if change.old_content and change.new_content:
                content = content.replace(change.old_content, change.new_content)
            elif change.new_content:
                content += "\n" + change.new_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _delete_file(self, change: CodeChange):
        """Delete a file"""
        file_path = Path(change.file_path)
        if file_path.exists():
            file_path.unlink()
    
    async def _add_dependency(self, change: CodeChange):
        """Add a dependency to requirements.txt"""
        requirements_file = Path("requirements.txt")
        
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                content = f.read()
        else:
            content = ""
        
        for dep in change.dependencies:
            if dep not in content:
                content += f"\n{dep}"
        
        with open(requirements_file, 'w') as f:
            f.write(content)
    
    async def _add_import(self, change: CodeChange):
        """Add an import to a file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add import at the top
            imports = change.dependencies
            import_lines = [f"import {imp}" for imp in imports]
            new_imports = "\n".join(import_lines)
            
            # Find the right place to insert imports
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_index = i + 1
                elif line.strip() and not line.strip().startswith('#'):
                    break
            
            lines.insert(insert_index, new_imports)
            content = '\n'.join(lines)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _add_function(self, change: CodeChange):
        """Add a function to a file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add function at the end
            content += "\n\n" + change.new_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _add_class(self, change: CodeChange):
        """Add a class to a file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add class at the end
            content += "\n\n" + change.new_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
