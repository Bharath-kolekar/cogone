# Phase 1.5: Routing & Authentication Fixes

**Date:** October 9, 2025  
**Status:** 🚀 IN PROGRESS  
**Estimated Time:** 2.5 hours  
**Goal:** Unlock the 29 health endpoints already added to code

---

## Objective

Fix routing configuration issues preventing the 29 newly added health endpoints from being accessible. This will increase the endpoint pass rate from ~70% to ~80%.

---

## Tasks

### Task 1: Audit Router Registration (1 hour) 🔄 IN PROGRESS
**Problem:** Not all routers with health endpoints are registered in main.py

**Actions:**
1. List all routers with new health endpoints
2. Check which ones are imported in main.py
3. Check which ones are included in app with app.include_router()
4. Identify missing registrations
5. Verify path prefixes match expected paths

**Expected Output:** List of routers to register/fix

---

### Task 2: Remove Auth from Health Endpoints (30 min) ⏳ PENDING
**Problem:** Some health endpoints require authentication (403/401 errors)

**Actions:**
1. Find health endpoints with auth dependencies
2. Remove Depends(AuthDependencies.get_current_user)
3. Health checks should always be public
4. Test accessibility after removal

**Expected Impact:** +5-10 endpoints accessible

---

### Task 3: Fix Duplicate/Conflicting Routes (30 min) ⏳ PENDING
**Problem:** Some endpoints return 405 (Method Not Allowed)

**Actions:**
1. Find duplicate route definitions
2. Check for conflicting HTTP methods
3. Fix agent-mode/health 405 error
4. Verify no @router.post and @router.get for same path

**Expected Impact:** +2-5 endpoints accessible

---

### Task 4: Improve Error Handling (30 min) ⏳ PENDING
**Problem:** Status endpoints return 500 instead of 503

**Actions:**
1. Add try-catch to all status endpoints
2. Return 503 (Service Unavailable) on initialization errors
3. Add clear error messages
4. Test error scenarios

**Expected Impact:** Better error reporting, +2-4 endpoints working

---

### Task 5: Verify Improvements (30 min) ⏳ PENDING
**Actions:**
1. Restart backend
2. Run verification test
3. Compare before/after results
4. Document actual improvements
5. Commit all changes

**Expected Impact:** Verification of +20-30 endpoints accessible

---

## Expected Results

### Before Phase 1.5
```
Health Endpoints Working: 6/21 (28.6%)
Status Endpoints Working: 1/4 (25.0%)
Total Pass Rate: 338-355/494 (68-72%)
```

### After Phase 1.5
```
Health Endpoints Working: 26-29/29 (90-100%)
Status Endpoints Working: 3-4/4 (75-100%)
Total Pass Rate: 358-385/494 (72-78%)
```

### Target Recovery
**+20-30 endpoints** accessible (additional 4-6% improvement)

---

## Success Criteria

- ✅ All 29 health endpoints registered and accessible
- ✅ No 403/401 errors on health checks
- ✅ No 405 errors on health checks
- ✅ Status endpoints return proper error codes
- ✅ +20-30 more endpoints passing tests
- ✅ All changes production-grade
- ✅ All changes committed to Git

---

**Started:** October 9, 2025  
**Current Task:** Task 1 - Router Registration Audit

