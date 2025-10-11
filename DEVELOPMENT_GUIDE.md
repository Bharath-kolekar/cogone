# Development Guide

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend when restored)
- PostgreSQL (via Supabase)
- Git

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/cognomega.git
   cd cognomega
   ```

2. **Backend setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration (see CONFIGURATION.md)
   ```

4. **Verify syntax**:
   ```bash
   python check_all_backend_syntax.py
   # Should show: "ALL FILES OK!"
   ```

5. **Run backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

6. **Test backend**:
   ```bash
   curl http://localhost:8000/api/v1/health
   # Should return: {"status": "ok"}
   ```

## Development Workflow

### Daily Workflow
1. Pull latest changes: `git pull origin main`
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes
4. Run syntax check: `python check_all_backend_syntax.py`
5. Run tests: `cd backend && pytest`
6. Commit changes: `git commit -m "feat: your feature"`
7. Push: `git push origin feature/your-feature`
8. Create pull request

### Running Tests
```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_specific.py

# Verbose output
pytest -v
```

### Code Quality Checks
```bash
# Syntax check
python check_all_backend_syntax.py

# Format code
cd backend
black app/
isort app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## Project Structure

```
cognomega/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main entry point
│   │   ├── routers/        # 118 files (→ 15 target)
│   │   ├── services/       # 296 files (→ 40 target)
│   │   ├── models/         # Pydantic models
│   │   └── tests/          # Test files
│   └── requirements.txt    # Python dependencies
├── quarantine/             # Quarantined frontend
├── archive/                # Archived documentation
└── [documentation files]   # Essential docs only
```

## Frontend (When Restored)

Frontend is currently quarantined. See `ARCHITECTURE_IMPROVEMENT_PLAN.md` for recovery plan.

## Troubleshooting

See `TROUBLESHOOTING.md` for common issues and solutions.

## Resources

- **Architecture Plan**: `ARCHITECTURE_IMPROVEMENT_PLAN.md`
- **CTO Review**: `CTO_REVIEW_REPORT.md`
- **API Docs**: `API_DOCUMENTATION.md`
- **Code Style**: `CODE_STYLE.md`

---

*Last Updated: October 10, 2025*

