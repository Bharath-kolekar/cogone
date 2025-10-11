# Design Patterns Integration Guide

## Quick Start Guide

### 1. Repository Pattern Usage

```python
from app.core.repositories.user_repository import UserRepository
from app.core.repositories.base_repository import UnitOfWork
from app.core.database import get_db_session

# Using Unit of Work for transaction management
async with UnitOfWork(db_session) as uow:
    user_repo = uow.get_repository("user", User)
    
    # Create user
    user = await user_repo.create(user_data)
    
    # Get user by email
    user = await user_repo.get_by_email("user@example.com")
    
    # Update user
    updated_user = await user_repo.update(user_id, update_data)
    
    # Commit transaction
    await uow.commit()
```

### 2. Strategy Pattern Usage

```python
from app.core.strategies.ai_provider_strategy import AIProviderManager, AIProviderType

# Initialize provider manager
provider_manager = AIProviderManager()

# Add providers
provider_manager.add_provider(
    AIProviderType.OPENAI, 
    api_key="your-openai-key",
    is_primary=True
)

provider_manager.add_provider(
    AIProviderType.LOCAL_LLM,
    api_key="local",
    base_url="http://localhost:11434"
)

# Generate completion with fallback
response = await provider_manager.generate_completion(
    prompt="Generate code for a user service",
    preferred_provider=AIProviderType.OPENAI
)
```

### 3. Command Pattern Usage

```python
from app.core.commands.command_pattern import CommandInvoker, CommandFactory, CommandType

# Initialize command invoker
invoker = CommandInvoker()

# Create command
command = CommandFactory.create_command(
    CommandType.CREATE_USER,
    command_id="create_user_001",
    user_data=user_create_data,
    user_service=user_service
)

# Execute command
result = await invoker.execute_command(command)

# Undo command if needed
if result.status == CommandStatus.COMPLETED:
    undo_result = await invoker.undo_last_command()
```

### 4. Observer Pattern Usage

```python
from app.core.observers.observer_pattern import (
    event_manager, EventType, EventPriority,
    EmailNotificationObserver, AnalyticsObserver
)

# Register observers
event_manager.register_observer(
    EmailNotificationObserver(email_service),
    [EventType.USER_CREATED, EventType.PAYMENT_COMPLETED]
)

event_manager.register_observer(
    AnalyticsObserver(analytics_service),
    [EventType.USER_LOGIN, EventType.AI_AGENT_EXECUTED]
)

# Publish events
await event_manager.publish_event(
    event_type=EventType.USER_CREATED,
    data={"user_id": "123", "email": "user@example.com"},
    user_id="123",
    priority=EventPriority.MEDIUM
)
```

### 5. Service Interface Usage

```python
from app.services.optimized_user_service import OptimizedUserService
from app.core.repositories.user_repository import UserRepository

# Initialize service with dependency injection
user_repo = UserRepository(db_session, User)
user_service = OptimizedUserService(user_repo)

# Use service methods
user = await user_service.create_user(user_create_data)
user = await user_service.get_user_by_id(user_id)
users = await user_service.get_users_with_pagination(skip=0, limit=10)
```

## Integration with Existing Code

### 1. Updating Existing Services

**Before (Old Pattern)**:
```python
class UserService:
    def __init__(self):
        self.db = get_db_client()  # Direct database access
    
    async def create_user(self, user_data):
        # Direct SQL operations
        pass
```

**After (New Pattern)**:
```python
class OptimizedUserService(IUserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository  # Dependency injection
    
    async def create_user(self, user_data: UserCreate) -> User:
        # Use repository pattern
        return await self.user_repository.create(user_data)
```

### 2. Updating Routers

**Before**:
```python
@router.post("/users")
async def create_user(request: UserCreate):
    service = UserService()  # Direct instantiation
    return await service.create_user(request)
```

**After**:
```python
@router.post("/users")
async def create_user(
    request: UserCreate,
    user_service: OptimizedUserService = Depends(get_user_service)
):
    return await user_service.create_user(request)
```

### 3. Dependency Injection Setup

```python
# dependency_injection.py
from app.core.repositories.user_repository import UserRepository
from app.services.optimized_user_service import OptimizedUserService

def get_user_repository(db_session: AsyncSession = Depends(get_db_session)):
    return UserRepository(db_session, User)

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return OptimizedUserService(user_repo)
```

## Testing Examples

### 1. Repository Testing

```python
import pytest
from unittest.mock import AsyncMock
from app.core.repositories.user_repository import UserRepository

@pytest.fixture
def mock_db_session():
    return AsyncMock()

@pytest.fixture
def user_repository(mock_db_session):
    return UserRepository(mock_db_session, User)

@pytest.mark.asyncio
async def test_create_user(user_repository):
    # Mock database response
    user_repository.db_session.add = AsyncMock()
    user_repository.db_session.flush = AsyncMock()
    user_repository.db_session.refresh = AsyncMock()
    
    # Test user creation
    user_data = UserCreate(email="test@example.com", username="testuser", password="password123")
    result = await user_repository.create(user_data)
    
    assert result is not None
    assert user_repository.db_session.add.called
```

### 2. Service Testing

```python
@pytest.fixture
def mock_user_repository():
    return AsyncMock(spec=UserRepository)

@pytest.fixture
def user_service(mock_user_repository):
    return OptimizedUserService(mock_user_repository)

@pytest.mark.asyncio
async def test_create_user_service(user_service, mock_user_repository):
    # Mock repository response
    mock_user = User(id="123", email="test@example.com")
    mock_user_repository.create.return_value = mock_user
    mock_user_repository.get_by_email.return_value = None
    
    # Test service method
    user_data = UserCreate(email="test@example.com", username="testuser", password="password123")
    result = await user_service.create_user(user_data)
    
    assert result == mock_user
    mock_user_repository.create.assert_called_once_with(user_data)
```

### 3. Strategy Testing

```python
@pytest.mark.asyncio
async def test_openai_strategy():
    strategy = OpenAIStrategy(api_key="test-key")
    
    # Mock OpenAI client
    with patch('openai.AsyncOpenAI') as mock_client:
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock(text="Generated response")]
        mock_client.return_value.completions.create.return_value = mock_response
        
        result = await strategy.generate_completion("Test prompt")
        
        assert result == "Generated response"
```

## Migration Strategy

### Phase 1: Core Infrastructure (Week 1)
1. Implement base repository pattern
2. Create core interfaces
3. Set up dependency injection

### Phase 2: Service Migration (Week 2-3)
1. Migrate user service
2. Migrate authentication service
3. Update related routers

### Phase 3: Advanced Patterns (Week 4)
1. Implement command pattern
2. Implement observer pattern
3. Add event-driven features

### Phase 4: Testing and Optimization (Week 5)
1. Add comprehensive tests
2. Performance optimization
3. Documentation updates

## Best Practices

### 1. Repository Pattern
- Always use Unit of Work for transactions
- Keep repositories focused on data access
- Use specialized repositories for complex queries
- Implement proper error handling

### 2. Strategy Pattern
- Use factory for strategy creation
- Implement fallback mechanisms
- Monitor strategy performance
- Keep strategies stateless when possible

### 3. Command Pattern
- Always implement undo functionality
- Keep commands atomic
- Use command history for audit trails
- Handle command failures gracefully

### 4. Observer Pattern
- Keep observers lightweight
- Use asynchronous processing
- Implement proper error handling in observers
- Monitor observer performance

### 5. Dependency Injection
- Use constructor injection
- Register dependencies in DI container
- Keep dependencies minimal
- Use interfaces for dependencies

## Performance Considerations

### 1. Repository Pattern
- Use connection pooling
- Implement query optimization
- Add caching where appropriate
- Monitor database performance

### 2. Strategy Pattern
- Cache strategy instances
- Implement connection pooling
- Monitor provider performance
- Use circuit breakers for external providers

### 3. Command Pattern
- Limit command history size
- Use async command execution
- Implement command batching
- Monitor command performance

### 4. Observer Pattern
- Use async observers
- Implement observer timeouts
- Batch event processing
- Monitor observer performance

## Monitoring and Debugging

### 1. Logging
- Log all repository operations
- Log strategy selections
- Log command executions
- Log observer notifications

### 2. Metrics
- Repository query performance
- Strategy execution times
- Command success/failure rates
- Observer processing times

### 3. Health Checks
- Repository connectivity
- Strategy availability
- Command queue status
- Observer health status

This integration guide provides everything needed to successfully implement and use the design pattern optimizations in the Cognomega AI system.
