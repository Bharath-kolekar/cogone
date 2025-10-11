# Troubleshooting Guide

## Common Issues & Solutions

---

## Backend Issues

### Issue: Syntax Errors

**Symptoms:**
```
SyntaxError: unmatched ')'
SyntaxError: f-string: empty expression not allowed
```

**Solution:**
✅ **FIXED** (October 10, 2025)

All 6 syntax errors have been resolved. Verify with:
```bash
python check_all_backend_syntax.py
# Should show: "ALL FILES OK!"
```

---

### Issue: Backend Won't Start

**Symptoms:**
```
ModuleNotFoundError: No module named 'app'
ImportError: cannot import name 'X' from 'Y'
```

**Solutions:**

1. **Check Python version:**
   ```bash
   python --version
   # Should be 3.10 or higher
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Check working directory:**
   ```bash
   # Should be in backend/ when running uvicorn
   cd backend
   uvicorn app.main:app --reload
   ```

---

### Issue: Database Connection Errors

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
Connection refused
```

**Solutions:**

1. **Check Supabase credentials:**
   ```bash
   # Verify .env file
   cat .env | grep SUPABASE
   ```

2. **Test connection:**
   ```bash
   # Try connecting via psql
   psql $DATABASE_URL
   ```

3. **Check Supabase dashboard:**
   - Visit: https://app.supabase.com
   - Verify project is active
   - Check connection pooler settings

---

### Issue: Redis Connection Errors

**Symptoms:**
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Solutions:**

1. **Check Redis URL:**
   ```bash
   echo $REDIS_URL
   # Should be valid redis:// URL
   ```

2. **Test Redis connection:**
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

3. **Check Upstash dashboard:**
   - Visit: https://console.upstash.com
   - Verify Redis database is active

---

## Configuration Issues

### Issue: Missing Environment Variables

**Symptoms:**
```
KeyError: 'SECRET_KEY'
ValidationError: field required
```

**Solution:**

1. **Copy environment template:**
   ```bash
   cp env.example .env
   ```

2. **Fill in required variables:**
   ```bash
   # Minimum required:
   SECRET_KEY=your-secret-key-min-32-chars
   JWT_SECRET=your-jwt-secret-min-32-chars
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_SERVICE_KEY=your-service-key
   ```

3. **Validate configuration:**
   ```bash
   cd backend
   python -c "from app.core.config import settings; print('Config valid!')"
   ```

---

## Frontend Issues (When Restored)

### Issue: Frontend Not Found

**Status:** Frontend is currently quarantined

**Location:** `quarantine/frontend_corrupted_20251009_081509/`

**Solution:** See `ARCHITECTURE_IMPROVEMENT_PLAN.md` Week 4 for frontend recovery plan.

---

## Documentation Issues

### Issue: Can't Find Documentation

**Problem:** 371 documentation files → 5 essential files

**Solution:**

**Current essential docs (root directory):**
1. README.md
2. CTO_REVIEW_REPORT.md
3. ARCHITECTURE_IMPROVEMENT_PLAN.md
4. EXECUTIVE_SUMMARY.md
5. API_DOCUMENTATION.md
6-18. Other essential guides (ARCHITECTURE.md, etc.)

**Archived docs:** `archive/documentation_archive_2025_10_10/`

---

## API Issues

### Issue: 404 Not Found on API Endpoint

**Symptoms:**
```
404 {"detail": "Not Found"}
```

**Solutions:**

1. **Check API is running:**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **Check endpoint exists:**
   ```bash
   # View all endpoints
   curl http://localhost:8000/openapi.json
   ```

3. **Check correct base path:**
   - Backend runs on: http://localhost:8000
   - API prefix: /api/v1/
   - Example: http://localhost:8000/api/v1/auth/login

---

### Issue: 500 Internal Server Error

**Symptoms:**
```
500 {"detail": "Internal Server Error"}
```

**Solutions:**

1. **Check backend logs:**
   ```bash
   # Logs show in terminal where uvicorn is running
   # Look for stack traces
   ```

2. **Enable debug mode:**
   ```bash
   # In .env
   DEBUG=True
   ```

3. **Check database:**
   - Verify tables exist
   - Check migrations applied

---

## Performance Issues

### Issue: Slow API Response Times

**Symptoms:**
- API responses > 1 second
- Timeout errors

**Solutions:**

1. **Check database indexes:**
   ```sql
   -- Missing indexes?
   SELECT * FROM pg_stat_user_tables;
   ```

2. **Enable caching:**
   - Verify Redis is connected
   - Check cache hit rate

3. **Profile slow endpoints:**
   ```python
   # Add timing logs
   import time
   start = time.time()
   # ... code ...
   print(f"Took {time.time() - start}s")
   ```

---

## Testing Issues

### Issue: Tests Failing

**Symptoms:**
```
FAILED tests/test_something.py::test_something
```

**Solutions:**

1. **Run tests verbosely:**
   ```bash
   pytest -vv
   ```

2. **Run single test:**
   ```bash
   pytest tests/test_something.py::test_something -s
   ```

3. **Check test database:**
   ```bash
   # Tests might need clean database
   # Clear test data between runs
   ```

---

## Git Issues

### Issue: Merge Conflicts

**Solution:**
```bash
# View conflicts
git status

# Edit conflicted files
# Remove conflict markers (<<<<, ====, >>>>)

# Mark as resolved
git add <file>
git commit
```

---

## Still Stuck?

1. **Check architecture docs:**
   - `CTO_REVIEW_REPORT.md` - Current state
   - `ARCHITECTURE_IMPROVEMENT_PLAN.md` - Roadmap
   - `EXECUTIVE_SUMMARY.md` - Quick overview

2. **Check archived docs:**
   ```bash
   # Search archived docs
   grep -r "your search term" archive/documentation_archive_2025_10_10/
   ```

3. **Run diagnostics:**
   ```bash
   # Syntax check
   python check_all_backend_syntax.py
   
   # Test backend startup
   cd backend && uvicorn app.main:app --reload
   ```

4. **Create an issue:**
   - Include error messages
   - Include steps to reproduce
   - Include environment details

---

*Last Updated: October 10, 2025*



