# Code Style Guide

## Python (Backend)

### General Guidelines
- **Python Version**: 3.10+
- **Formatting**: Black (line length: 100)
- **Import Sorting**: isort
- **Linting**: flake8, mypy
- **Type Hints**: Required for all public functions

### Code Formatting
```python
# Good
def process_data(data: Dict[str, Any]) -> List[str]:
    """Process data and return results.
    
    Args:
        data: Input data dictionary
        
    Returns:
        List of processed strings
    """
    return [str(item) for item in data.values()]

# Bad
def process_data(data):
    return [str(item) for item in data.values()]
```

### Testing
- Use `pytest` for all tests
- Aim for 95%+ code coverage
- Name test files as `test_*.py`

## TypeScript/JavaScript (Frontend)

### General Guidelines
- **TypeScript**: Strict mode enabled
- **Formatting**: Prettier
- **Linting**: ESLint
- **Style**: Airbnb style guide (modified)

### Naming Conventions
- Components: PascalCase (`UserProfile.tsx`)
- Functions: camelCase (`getUserData`)
- Constants: UPPER_SNAKE_CASE (`API_BASE_URL`)
- Files: kebab-case for utilities, PascalCase for components

## Git Commit Messages

Format: `<type>: <description>`

**Types:**
- `fix`: Bug fix
- `feat`: New feature
- `refactor`: Code refactoring
- `docs`: Documentation changes
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Example:**
```
fix: resolve syntax error in compliance_engine.py
feat: add documentation archiving script
refactor: consolidate 118 routers into 15
```

## Documentation

- Use Markdown for all documentation
- Keep documentation in sync with code changes
- Update CHANGELOG.md for all user-facing changes

---

*Last Updated: October 10, 2025*

