"""
Command Pattern Implementation
Follows Command Pattern for operation encapsulation and undo/redo functionality
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import structlog
import asyncio

logger = structlog.get_logger()


class CommandStatus(str, Enum):
    """Command execution status"""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CommandType(str, Enum):
    """Command types"""
    CREATE_USER = "create_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    CREATE_AI_AGENT = "create_ai_agent"
    UPDATE_AI_AGENT = "update_ai_agent"
    DELETE_AI_AGENT = "delete_ai_agent"
    GENERATE_APP = "generate_app"
    DEPLOY_APP = "deploy_app"
    SEND_EMAIL = "send_email"
    PROCESS_VOICE = "process_voice"


@dataclass
class CommandResult:
    """Command execution result"""
    command_id: str
    status: CommandStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class Command(ABC):
    """
    Abstract Command interface
    Follows Command Pattern
    """
    
    def __init__(self, command_id: str, command_type: CommandType):
        self.command_id = command_id
        self.command_type = command_type
        self.status = CommandStatus.PENDING
        self.created_at = datetime.utcnow()
        self.executed_at: Optional[datetime] = None
        self.undo_data: Optional[Dict[str, Any]] = None
    
    @abstractmethod
    async def execute(self) -> CommandResult:
        """Execute the command"""
        pass
    
    @abstractmethod
    async def undo(self) -> CommandResult:
        """Undo the command (if supported)"""
        pass
    
    @abstractmethod
    async def can_undo(self) -> bool:
        """Check if command can be undone"""
        pass
    
    def get_execution_time(self) -> Optional[float]:
        """Get command execution time"""
        if self.executed_at:
            return (self.executed_at - self.created_at).total_seconds()
        return None


class CreateUserCommand(Command):
    """Create user command"""
    
    def __init__(
        self, 
        command_id: str, 
        user_data: Dict[str, Any],
        user_service: Any
    ):
        super().__init__(command_id, CommandType.CREATE_USER)
        self.user_data = user_data
        self.user_service = user_service
        self.created_user_id: Optional[str] = None
    
    async def execute(self) -> CommandResult:
        """Execute create user command"""
        start_time = datetime.utcnow()
        
        try:
            self.status = CommandStatus.EXECUTING
            
            # Execute user creation
            user = await self.user_service.create_user(self.user_data)
            self.created_user_id = str(user.id)
            
            self.status = CommandStatus.COMPLETED
            self.executed_at = datetime.utcnow()
            
            execution_time = (self.executed_at - start_time).total_seconds()
            
            logger.info("Create user command executed", 
                       command_id=self.command_id, 
                       user_id=self.created_user_id,
                       execution_time=execution_time)
            
            return CommandResult(
                command_id=self.command_id,
                status=self.status,
                result={"user_id": self.created_user_id, "user": user},
                execution_time=execution_time
            )
            
        except Exception as e:
            self.status = CommandStatus.FAILED
            self.executed_at = datetime.utcnow()
            
            logger.error("Create user command failed", 
                        command_id=self.command_id, 
                        error=str(e))
            
            return CommandResult(
                command_id=self.command_id,
                status=self.status,
                error=str(e),
                execution_time=(self.executed_at - start_time).total_seconds()
            )
    
    async def undo(self) -> CommandResult:
        """Undo create user command"""
        if not self.can_undo():
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.FAILED,
                error="Cannot undo create user command - user may have dependencies"
            )
        
        try:
            if self.created_user_id:
                await self.user_service.delete_user(self.created_user_id)
                
            logger.info("Create user command undone", 
                       command_id=self.command_id, 
                       user_id=self.created_user_id)
            
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.COMPLETED,
                result={"undone": True}
            )
            
        except Exception as e:
            logger.error("Failed to undo create user command", 
                        command_id=self.command_id, 
                        error=str(e))
            
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.FAILED,
                error=str(e)
            )
    
    async def can_undo(self) -> bool:
        """Check if create user command can be undone"""
        # Can only undo if user was created and has no dependencies
        return (self.created_user_id is not None and 
                self.status == CommandStatus.COMPLETED)


class UpdateUserCommand(Command):
    """Update user command"""
    
    def __init__(
        self, 
        command_id: str, 
        user_id: str,
        update_data: Dict[str, Any],
        user_service: Any
    ):
        super().__init__(command_id, CommandType.UPDATE_USER)
        self.user_id = user_id
        self.update_data = update_data
        self.user_service = user_service
        self.original_data: Optional[Dict[str, Any]] = None
    
    async def execute(self) -> CommandResult:
        """Execute update user command"""
        start_time = datetime.utcnow()
        
        try:
            self.status = CommandStatus.EXECUTING
            
            # Get original data for undo
            original_user = await self.user_service.get_user_by_id(self.user_id)
            if original_user:
                self.original_data = original_user.dict() if hasattr(original_user, 'dict') else original_user.__dict__
            
            # Execute user update
            updated_user = await self.user_service.update_user(self.user_id, self.update_data)
            
            self.status = CommandStatus.COMPLETED
            self.executed_at = datetime.utcnow()
            
            execution_time = (self.executed_at - start_time).total_seconds()
            
            logger.info("Update user command executed", 
                       command_id=self.command_id, 
                       user_id=self.user_id,
                       execution_time=execution_time)
            
            return CommandResult(
                command_id=self.command_id,
                status=self.status,
                result={"user_id": self.user_id, "user": updated_user},
                execution_time=execution_time
            )
            
        except Exception as e:
            self.status = CommandStatus.FAILED
            self.executed_at = datetime.utcnow()
            
            logger.error("Update user command failed", 
                        command_id=self.command_id, 
                        user_id=self.user_id,
                        error=str(e))
            
            return CommandResult(
                command_id=self.command_id,
                status=self.status,
                error=str(e),
                execution_time=(self.executed_at - start_time).total_seconds()
            )
    
    async def undo(self) -> CommandResult:
        """Undo update user command"""
        if not self.can_undo():
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.FAILED,
                error="Cannot undo update user command - no original data available"
            )
        
        try:
            if self.original_data:
                await self.user_service.update_user(self.user_id, self.original_data)
                
            logger.info("Update user command undone", 
                       command_id=self.command_id, 
                       user_id=self.user_id)
            
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.COMPLETED,
                result={"undone": True}
            )
            
        except Exception as e:
            logger.error("Failed to undo update user command", 
                        command_id=self.command_id, 
                        user_id=self.user_id,
                        error=str(e))
            
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.FAILED,
                error=str(e)
            )
    
    async def can_undo(self) -> bool:
        """Check if update user command can be undone"""
        return (self.original_data is not None and 
                self.status == CommandStatus.COMPLETED)


class GenerateAppCommand(Command):
    """Generate app command"""
    
    def __init__(
        self, 
        command_id: str, 
        requirements: Dict[str, Any],
        app_service: Any
    ):
        super().__init__(command_id, CommandType.GENERATE_APP)
        self.requirements = requirements
        self.app_service = app_service
        self.generated_app_id: Optional[str] = None
    
    async def execute(self) -> CommandResult:
        """Execute generate app command"""
        start_time = datetime.utcnow()
        
        try:
            self.status = CommandStatus.EXECUTING
            
            # Execute app generation
            app_result = await self.app_service.generate_app(self.requirements)
            self.generated_app_id = app_result.get("app_id")
            
            self.status = CommandStatus.COMPLETED
            self.executed_at = datetime.utcnow()
            
            execution_time = (self.executed_at - start_time).total_seconds()
            
            logger.info("Generate app command executed", 
                       command_id=self.command_id, 
                       app_id=self.generated_app_id,
                       execution_time=execution_time)
            
            return CommandResult(
                command_id=self.command_id,
                status=self.status,
                result=app_result,
                execution_time=execution_time
            )
            
        except Exception as e:
            self.status = CommandStatus.FAILED
            self.executed_at = datetime.utcnow()
            
            logger.error("Generate app command failed", 
                        command_id=self.command_id, 
                        error=str(e))
            
            return CommandResult(
                command_id=self.command_id,
                status=self.status,
                error=str(e),
                execution_time=(self.executed_at - start_time).total_seconds()
            )
    
    async def undo(self) -> CommandResult:
        """Undo generate app command"""
        if not self.can_undo():
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.FAILED,
                error="Cannot undo generate app command - app may be deployed"
            )
        
        try:
            if self.generated_app_id:
                await self.app_service.delete_app(self.generated_app_id)
                
            logger.info("Generate app command undone", 
                       command_id=self.command_id, 
                       app_id=self.generated_app_id)
            
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.COMPLETED,
                result={"undone": True}
            )
            
        except Exception as e:
            logger.error("Failed to undo generate app command", 
                        command_id=self.command_id, 
                        error=str(e))
            
            return CommandResult(
                command_id=self.command_id,
                status=CommandStatus.FAILED,
                error=str(e)
            )
    
    async def can_undo(self) -> bool:
        """Check if generate app command can be undone"""
        return (self.generated_app_id is not None and 
                self.status == CommandStatus.COMPLETED)


class CommandInvoker:
    """
    Command Invoker following Command Pattern
    Manages command execution, history, and undo/redo functionality
    """
    
    def __init__(self):
        self.command_history: List[Command] = []
        self.undo_stack: List[Command] = []
        self.max_history_size = 1000
    
    async def execute_command(self, command: Command) -> CommandResult:
        """Execute a command"""
        try:
            # Execute the command
            result = await command.execute()
            
            # Add to history
            self.command_history.append(command)
            
            # Clear undo stack since we have a new command
            self.undo_stack.clear()
            
            # Maintain history size
            if len(self.command_history) > self.max_history_size:
                self.command_history.pop(0)
            
            logger.info("Command executed", 
                       command_id=command.command_id,
                       command_type=command.command_type.value,
                       status=result.status.value)
            
            return result
            
        except Exception as e:
            logger.error("Command execution error", 
                        command_id=command.command_id,
                        error=str(e))
            
            return CommandResult(
                command_id=command.command_id,
                status=CommandStatus.FAILED,
                error=str(e)
            )
    
    async def undo_last_command(self) -> Optional[CommandResult]:
        """Undo the last executed command"""
        if not self.command_history:
            return None
        
        command = self.command_history.pop()
        
        if await command.can_undo():
            try:
                result = await command.undo()
                self.undo_stack.append(command)
                
                logger.info("Command undone", 
                           command_id=command.command_id,
                           command_type=command.command_type.value)
                
                return result
                
            except Exception as e:
                logger.error("Command undo error", 
                            command_id=command.command_id,
                            error=str(e))
                
                return CommandResult(
                    command_id=command.command_id,
                    status=CommandStatus.FAILED,
                    error=str(e)
                )
        else:
            # Put command back in history if it can't be undone
            self.command_history.append(command)
            return None
    
    async def redo_last_undone_command(self) -> Optional[CommandResult]:
        """Redo the last undone command"""
        if not self.undo_stack:
            return None
        
        command = self.undo_stack.pop()
        
        try:
            result = await command.execute()
            self.command_history.append(command)
            
            logger.info("Command redone", 
                       command_id=command.command_id,
                       command_type=command.command_type.value)
            
            return result
            
        except Exception as e:
            logger.error("Command redo error", 
                        command_id=command.command_id,
                        error=str(e))
            
            return CommandResult(
                command_id=command.command_id,
                status=CommandStatus.FAILED,
                error=str(e)
            )
    
    def get_command_history(self, limit: int = 50) -> List[Command]:
        """Get command history"""
        return self.command_history[-limit:]
    
    def get_undo_stack(self) -> List[Command]:
        """Get undo stack"""
        return self.undo_stack.copy()
    
    def clear_history(self):
        """Clear command history and undo stack"""
        self.command_history.clear()
        self.undo_stack.clear()
        logger.info("Command history cleared")


class CommandFactory:
    """
    Command Factory following Factory Pattern
    Creates command instances based on command type
    """
    
    _command_classes: Dict[CommandType, type] = {
        CommandType.CREATE_USER: CreateUserCommand,
        CommandType.UPDATE_USER: UpdateUserCommand,
        CommandType.GENERATE_APP: GenerateAppCommand,
    }
    
    @classmethod
    def create_command(
        cls, 
        command_type: CommandType, 
        command_id: str, 
        **kwargs
    ) -> Command:
        """Create command instance"""
        if command_type not in cls._command_classes:
            raise ValueError(f"Unsupported command type: {command_type}")
        
        command_class = cls._command_classes[command_type]
        return command_class(command_id, **kwargs)
    
    @classmethod
    def register_command(cls, command_type: CommandType, command_class: type):
        """Register new command class"""
        cls._command_classes[command_type] = command_class
        logger.info("Command class registered", command_type=command_type.value)
    
    @classmethod
    def get_supported_commands(cls) -> List[CommandType]:
        """Get list of supported command types"""
        return list(cls._command_classes.keys())
