# Development Workflow Guide

## Overview
This document outlines the complete development workflow, coding standards, and best practices for the Voice-to-App SaaS Platform.

## 🚨 CRITICAL REMINDERS

### "PARALLELLY KEEP UPDATING THE DOCUMENTS"

**MANDATORY**: Every code change, feature addition, bug fix, or system modification MUST be accompanied by parallel documentation updates. This is not optional - it's essential for project success and team productivity.

**See**: `DOCUMENTATION_MAINTENANCE.md` for detailed documentation update protocols.

### "PERFORMANCE OPTIMIZATION PROTOCOL"

**MANDATORY**: Every performance issue identified MUST follow the mandatory performance optimization workflow:

1. **EXAMINE CODEBASE** - Thoroughly analyze for performance issues
2. **PLAN OPTIMIZED SOLUTION** - Design replacement with optimized service/component
3. **IMPLEMENT OPTIMIZATION** - Build and deploy optimized version
4. **TEST NO PRODUCTION IMPACT** - Ensure zero downtime and functionality loss
5. **REMOVE OLD FILES** - Clean up performance-issue files/services/components
6. **FINAL TESTING** - Validate no production impact after cleanup
7. **RESOLVE ISSUES** - Fix any issues found until completely resolved

**See**: `PERFORMANCE_OPTIMIZATION_PROTOCOL.md` for complete details.

## Development Environment Setup

### Prerequisites
- **Node.js**: 18.x or higher
- **Python**: 3.10 or higher
- **Git**: Latest version
- **Docker**: For containerized development
- **VS Code**: Recommended IDE with extensions

### Required VS Code Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode.vscode-github-actions"
  ]
}
```

### Environment Setup
```bash
# Clone repository
git clone https://github.com/Bharath-kolekar/cogone.git
cd cogone

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Database setup (Supabase)
# 1. Create Supabase project
# 2. Apply schema from supabase/schema.sql
# 3. Configure environment variables
```

## Git Workflow

### Branch Strategy
```
main (production)
├── develop (staging)
├── feature/feature-name (feature branches)
├── hotfix/hotfix-name (emergency fixes)
└── release/release-name (release preparation)
```

### Commit Message Convention
```
type(scope): description

Types:
- feat: new feature
- fix: bug fix
- docs: documentation
- style: formatting
- refactor: code refactoring
- test: adding tests
- chore: maintenance

Examples:
feat(auth): add 2FA login support
fix(api): resolve tRPC router conflicts
docs(readme): update installation instructions
```

### Pull Request Process
1. Create feature branch from `develop`
2. Implement changes with tests
3. Update documentation if needed
4. Create pull request to `develop`
5. Code review and approval
6. Merge to `develop`
7. Deploy to staging for testing
8. Create PR from `develop` to `main` for production

## Coding Standards

### Python (Backend)

#### Code Style
```python
# Use type hints
def process_user_data(user_id: str, data: dict) -> User:
    """Process user data with proper validation."""
    # Implementation here
    pass

# Use Pydantic models for data validation
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

# Use async/await for I/O operations
async def get_user(user_id: str) -> User:
    async with get_database() as db:
        return await db.fetch_user(user_id)

# Use dependency injection
from fastapi import Depends

async def get_current_user(token: str = Depends(get_token)) -> User:
    return await verify_token(token)
```

#### File Organization
```
backend/app/
├── main.py              # Application entry point
├── core/                # Core functionality
│   ├── config.py        # Configuration
│   ├── database.py      # Database connection
│   └── security.py      # Security utilities
├── models/              # Data models
│   ├── __init__.py
│   ├── base.py          # Base model classes
│   └── user.py          # User-specific models
├── routers/             # API endpoints
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   └── users.py         # User management routes
├── services/            # Business logic
│   ├── __init__.py
│   ├── auth_service.py  # Authentication logic
│   └── user_service.py  # User management logic
└── utils/               # Utility functions
    ├── __init__.py
    └── helpers.py       # Helper functions
```

#### Error Handling
```python
from fastapi import HTTPException, status

# Use specific HTTP exceptions
async def get_user(user_id: str) -> User:
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# Use custom exceptions for business logic
class UserNotFoundError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass
```

### TypeScript (Frontend)

#### Code Style
```typescript
// Use interfaces for object shapes
interface User {
  id: string;
  email: string;
  fullName: string;
  createdAt: string;
}

// Use type aliases for unions and primitives
type Status = 'loading' | 'success' | 'error';
type UserRole = 'admin' | 'user' | 'moderator';

// Use React.FC for functional components
const UserProfile: React.FC<UserProfileProps> = ({ user, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  
  return (
    <div className="user-profile">
      {/* Component JSX */}
    </div>
  );
};

// Use custom hooks for reusable logic
const useUser = (userId: string) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  
  return { user, loading };
};
```

#### Component Organization
```
frontend/
├── components/
│   ├── ui/              # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Modal.tsx
│   ├── forms/           # Form components
│   │   ├── LoginForm.tsx
│   │   └── UserForm.tsx
│   └── layout/          # Layout components
│       ├── Header.tsx
│       └── Sidebar.tsx
├── hooks/               # Custom React hooks
│   ├── useAuth.ts
│   └── useApi.ts
├── lib/                 # Utility libraries
│   ├── api.ts
│   └── utils.ts
└── types/               # TypeScript type definitions
    ├── user.ts
    └── api.ts
```

#### State Management
```typescript
// Use React Query for server state
import { useQuery, useMutation } from '@tanstack/react-query';

const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

const useCreateUser = () => {
  return useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
};

// Use Jotai for client state
import { atom } from 'jotai';

export const userAtom = atom<User | null>(null);
export const themeAtom = atom<'light' | 'dark'>('light');
```

## Testing Strategy

### Backend Testing
```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrong_password"
    })
    assert response.status_code == 401

# Run tests
pytest tests/ -v --cov=app
```

### Frontend Testing
```typescript
// __tests__/UserProfile.test.tsx
import { render, screen } from '@testing-library/react';
import { UserProfile } from '../components/UserProfile';

describe('UserProfile', () => {
  it('renders user information', () => {
    const user = {
      id: '1',
      email: 'test@example.com',
      fullName: 'Test User',
      createdAt: '2025-10-03T00:00:00Z'
    };
    
    render(<UserProfile user={user} />);
    
    expect(screen.getByText('Test User')).toBeInTheDocument();
    expect(screen.getByText('test@example.com')).toBeInTheDocument();
  });
});

// Run tests
npm test
```

## Database Management

### Migration Strategy
```sql
-- migrations/001_create_users_table.sql
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- migrations/002_add_user_2fa_table.sql
CREATE TABLE user_2fa (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    totp_secret VARCHAR(255) NOT NULL,
    backup_codes TEXT[],
    is_enabled BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Seed Data
```sql
-- seeds/001_admin_user.sql
INSERT INTO users (email, password_hash, full_name) VALUES
('admin@example.com', '$2b$12$hash', 'Admin User');

-- Update admin user role
UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

## API Development

### OpenAPI Documentation
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="Voice-to-App API",
    description="API for voice-to-app generation platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Automatic OpenAPI schema generation
@app.get("/openapi.json")
async def get_openapi():
    return app.openapi()
```

### API Versioning
```python
# backend/app/routers/v1/auth.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/login")
async def login_v1():
    # V1 implementation
    pass

# backend/app/routers/v2/auth.py
router = APIRouter(prefix="/api/v2/auth", tags=["Authentication V2"])

@router.post("/login")
async def login_v2():
    # V2 implementation with improvements
    pass
```

## Performance Optimization

### Backend Optimization
```python
# Use connection pooling
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30
)

# Use Redis caching
import redis.asyncio as redis

redis_client = redis.from_url(REDIS_URL)

@cache(expire=300)  # 5 minutes
async def get_user_profile(user_id: str):
    # Expensive operation
    return await database.fetch_user_profile(user_id)
```

### Frontend Optimization
```typescript
// Use React.memo for expensive components
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* Expensive rendering */}</div>;
});

// Use useMemo for expensive calculations
const ExpensiveCalculation = ({ items }) => {
  const processedItems = useMemo(() => {
    return items.map(item => expensiveProcess(item));
  }, [items]);
  
  return <div>{/* Render processed items */}</div>;
};

// Use dynamic imports for code splitting
const LazyComponent = lazy(() => import('./LazyComponent'));

const App = () => (
  <Suspense fallback={<Loading />}>
    <LazyComponent />
  </Suspense>
);
```

## Security Best Practices

### Backend Security
```python
# Input validation
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request):
    # Login logic
    pass

# SQL injection prevention
from sqlalchemy import text

# ❌ Vulnerable
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ Safe
query = text("SELECT * FROM users WHERE id = :user_id")
result = await db.execute(query, {"user_id": user_id})
```

### Frontend Security
```typescript
// XSS prevention
const sanitizeHtml = (html: string) => {
  return DOMPurify.sanitize(html);
};

// CSRF protection
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
  headers: {
    'X-CSRF-Token': getCsrfToken(),
  },
});

// Input validation
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const validateUserInput = (data: unknown) => {
  return userSchema.parse(data);
};
```

## Monitoring and Debugging

### Backend Monitoring
```python
# Logging configuration
import logging
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Error tracking
import sentry_sdk

sentry_sdk.init(
    dsn="your_sentry_dsn",
    traces_sample_rate=1.0,
)
```

### Frontend Monitoring
```typescript
// Error boundary
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Send to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}

// Performance monitoring
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

## Documentation Standards

### Code Documentation
```python
def process_user_data(user_id: str, data: dict) -> User:
    """
    Process user data with validation and transformation.
    
    Args:
        user_id: Unique identifier for the user
        data: Raw user data dictionary
        
    Returns:
        User: Processed user object
        
    Raises:
        ValidationError: If data validation fails
        UserNotFoundError: If user doesn't exist
        
    Example:
        >>> user = process_user_data("123", {"name": "John"})
        >>> print(user.name)
        John
    """
    # Implementation here
    pass
```

### API Documentation
```python
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Create a new user",
    description="Create a new user account with email and password"
)
async def create_user(
    user_data: UserCreate,
    db: Database = Depends(get_database)
) -> UserResponse:
    """
    Create a new user account.
    
    - **email**: User's email address (must be unique)
    - **password**: User's password (minimum 8 characters)
    - **full_name**: User's full name (optional)
    
    Returns the created user object with generated ID and timestamps.
    """
    # Implementation here
    pass
```

## Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Code review completed
- [ ] **🚨 DOCUMENTATION UPDATED** (MANDATORY - see DOCUMENTATION_MAINTENANCE.md)
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Security scan completed
- [ ] Performance tests passed

### Post-deployment
- [ ] Health checks passing
- [ ] Monitoring alerts configured
- [ ] Error tracking active
- [ ] Performance metrics normal
- [ ] User acceptance testing
- [ ] Rollback plan ready

---
**Last Updated**: October 3, 2025  
**Version**: 1.0
