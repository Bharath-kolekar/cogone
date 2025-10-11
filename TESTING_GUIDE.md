# Testing Guide

## Testing Philosophy

- **Test Pyramid**: 70% unit, 20% integration, 10% E2E
- **Coverage Goal**: 95%+ code coverage
- **Test-Driven**: Write tests before or with code
- **Fast Feedback**: Tests should run quickly

---

## Current Testing Status

🔴 **NEEDS IMPROVEMENT**

**Current:**
- Some unit tests exist
- Test coverage unknown
- No comprehensive integration tests
- No E2E test suite

**Target (Weeks 5-6):**
- 95%+ code coverage
- Comprehensive test suite
- Automated testing in CI/CD
- Performance benchmarks

---

## Running Tests

### Backend Tests (pytest)

```bash
# All tests
cd backend
pytest

# Specific file
pytest tests/test_auth.py

# Specific test
pytest tests/test_auth.py::test_login

# With coverage
pytest --cov=app --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run only failed tests
pytest --lf
```

### Frontend Tests (When Restored)

```bash
cd frontend

# Unit tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# E2E tests
npm run test:e2e
```

---

## Test Structure

### Backend Tests

```
backend/app/tests/
├── unit/                    # Unit tests (70%)
│   ├── test_auth_service.py
│   ├── test_voice_service.py
│   └── ...
├── integration/             # Integration tests (20%)
│   ├── test_voice_to_app_flow.py
│   ├── test_payment_flow.py
│   └── ...
└── e2e/                    # End-to-end tests (10%)
    ├── test_user_journey.py
    └── ...
```

---

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_auth_service.py
import pytest
from app.services.auth_service import AuthService

def test_login_success():
    """Test successful login"""
    service = AuthService()
    result = service.login("user@example.com", "password123")
    assert result["success"] is True
    assert "token" in result

def test_login_invalid_password():
    """Test login with invalid password"""
    service = AuthService()
    with pytest.raises(ValueError):
        service.login("user@example.com", "wrong_password")
```

### Integration Test Example

```python
# tests/integration/test_voice_to_app_flow.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_voice_to_app_flow():
    """Test complete voice-to-app generation flow"""
    # 1. Upload voice file
    response = client.post(
        "/api/v1/voice/upload",
        files={"file": ("audio.wav", audio_data, "audio/wav")}
    )
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    
    # 2. Process voice
    response = client.post(f"/api/v1/voice/process/{session_id}")
    assert response.status_code == 200
    
    # 3. Generate app
    response = client.post(
        "/api/v1/apps/generate",
        json={"session_id": session_id}
    )
    assert response.status_code == 200
    assert "app_id" in response.json()
```

---

## Test Fixtures

```python
# conftest.py
import pytest
from app.core.database import get_db

@pytest.fixture
def db_session():
    """Provide a database session for tests"""
    db = get_db()
    yield db
    db.rollback()  # Clean up after test

@pytest.fixture
def auth_token():
    """Provide an authentication token"""
    # Generate test token
    return "test_token_123"

@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    yield user
    db_session.delete(user)
    db_session.commit()
```

---

## Mocking

```python
from unittest.mock import Mock, patch

def test_external_api_call():
    """Test function that calls external API"""
    with patch('app.services.external_api.call') as mock_call:
        mock_call.return_value = {"success": True}
        
        result = my_function()
        
        assert result["success"] is True
        mock_call.assert_called_once()
```

---

## Performance Testing

### Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def voice_to_app(self):
        self.client.post(
            "/api/v1/voice/process",
            json={"audio": "base64_audio_data"}
        )
    
    @task(2)
    def list_apps(self):
        self.client.get("/api/v1/apps")
```

Run load tests:
```bash
locust -f locustfile.py --host=http://localhost:8000
```

---

## Continuous Integration

### GitHub Actions (Planned)

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run tests
        run: cd backend && pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Testing Checklist

### Before Committing
- [ ] All new code has tests
- [ ] All tests pass locally
- [ ] Code coverage ≥ 95%
- [ ] No linter errors

### Before Merging PR
- [ ] CI/CD tests pass
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Integration tests pass

### Before Deploying
- [ ] All tests pass on staging
- [ ] Load tests completed
- [ ] Security tests passed
- [ ] Rollback plan documented

---

## Test Data

### Managing Test Data

```python
# Use factories for test data
from factory import Factory, Faker

class UserFactory(Factory):
    class Meta:
        model = User
    
    email = Faker('email')
    name = Faker('name')
    created_at = Faker('date_time')

# Usage
user = UserFactory.create()
```

---

## Debugging Tests

```bash
# Run with debugger
pytest --pdb

# Print output
pytest -s

# Very verbose
pytest -vv

# Show local variables on failure
pytest -l
```

---

## Next Steps

1. **Week 5**: Create comprehensive test suite
2. **Week 6**: Achieve 95%+ coverage
3. **Week 7**: Add performance tests
4. **Week 8**: Add E2E tests

See `ARCHITECTURE_IMPROVEMENT_PLAN.md` for complete timeline.

---

*Last Updated: October 10, 2025*



