# tRPC Issue Tracker

## Current Status: BLOCKED
**Date**: October 3, 2025  
**Priority**: High  
**Impact**: Frontend build fails due to TypeScript errors

## Problem Summary
tRPC integration is failing with TypeScript compilation errors related to router type definitions and method naming conflicts.

## Error Messages
```
Type error: Property 'createClient' does not exist on type '"The property 'useContext' in your router collides with a built-in method, rename this router or procedure on your backend."'

Type error: Property 'Provider' does not exist on type '"The property 'useContext' in your router collides with a built-in method, rename this router or procedure on your backend."'
```

## Root Cause Analysis
The error message suggests that there are naming conflicts in the backend router where procedures are named `useContext`, `useUtils`, or `withTRPC` which collide with built-in tRPC methods.

## Files Involved

### Frontend
- `frontend/lib/trpc.ts` - tRPC client configuration
- `frontend/components/providers.tsx` - Provider setup (currently disabled)

### Backend  
- `backend/app/routers/index.py` - Main router file
- `backend/app/routers/auth.py` - Auth router
- `backend/app/routers/payments.py` - Payments router
- `backend/app/routers/voice.py` - Voice router
- Other router files...

## Investigation Needed

### 1. Check Backend Router Definitions
Need to search for procedures named:
- `useContext`
- `useUtils` 
- `withTRPC`
- Any other methods that might conflict with tRPC built-ins

### 2. Verify tRPC Versions
Check version compatibility:
- Frontend: `@trpc/client`, `@trpc/next`, `@trpc/react-query`
- Backend: `trpc` Python package

### 3. AppRouter Type Export
Verify that `AppRouter` is properly exported from backend and imported in frontend.

## Temporary Workaround
Removed tRPC from providers to unblock build:
```typescript
// Simplified providers without tRPC
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <JotaiProvider>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </JotaiProvider>
    </QueryClientProvider>
  )
}
```

## Action Items

### Immediate (High Priority)
1. **Search backend routers for conflicting procedure names**
   ```bash
   grep -r "useContext\|useUtils\|withTRPC" backend/app/routers/
   ```

2. **Check tRPC package versions**
   ```bash
   # Frontend
   npm list @trpc/client @trpc/next @trpc/react-query
   
   # Backend  
   pip list | grep trpc
   ```

3. **Verify AppRouter export in backend**
   ```python
   # Check backend/app/routers/index.py
   # Ensure AppRouter is properly defined and exported
   ```

### Medium Priority
4. **Update router procedure names** (if conflicts found)
5. **Fix type exports and imports**
6. **Re-enable tRPC in providers**
7. **Test tRPC integration**

### Low Priority  
8. **Add tRPC error handling**
9. **Optimize tRPC configuration**

## Related Issues
- Frontend build failing
- API communication between frontend/backend
- Type safety between client/server

## Dependencies
- Backend router refactoring
- Frontend provider setup
- Type definitions alignment

## Notes
- This issue blocks full-stack functionality
- Current workaround allows frontend to build but breaks API integration
- Need to prioritize this fix for production readiness

---
*Update this document as investigation progresses and fixes are implemented.*
