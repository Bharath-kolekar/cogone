# Migration Guide

## Current Migration Status

The system is undergoing major architectural improvements. This guide tracks migration steps.

## Phase 1: Documentation Cleanup ✅

**Status**: COMPLETE (October 10, 2025)

**Changes:**
- Archived 369 non-essential documentation files
- Created 18 essential documentation files
- Archive location: `archive/documentation_archive_2025_10_10/`

**Impact:**
- No code changes
- Documentation now easy to find
- Historical docs preserved in archive

**Migration Required:** None

---

## Phase 2: Router Consolidation 🔜

**Status**: PLANNED (Weeks 2-3)

**Changes:**
- Consolidate 118 routers → 15 focused routers
- Update main.py imports
- Add deprecation warnings to old endpoints

**Impact:**
- API endpoints will have new paths
- Old endpoints will be deprecated (90-day notice)
- Backward compatibility maintained via `archive_router.py`

**Migration Required:**
- Update API client calls to new endpoint paths
- Monitor deprecation warnings
- Plan migration within 90 days

---

## Phase 3: Service Consolidation 🔜

**Status**: PLANNED (Weeks 2-3)

**Changes:**
- Consolidate 296 services → 40 services
- Remove 14 "DNA systems"
- Simplify 13 orchestrators → 1

**Impact:**
- Internal service architecture changes
- No external API changes
- Improved performance

**Migration Required:** None (internal only)

---

## Phase 4: Frontend Recovery 🔜

**Status**: PLANNED (Week 4)

**Changes:**
- Restore or rebuild frontend
- Update API integration
- New component structure

**Impact:**
- New frontend URL structure
- Updated UI components
- Modern user experience

**Migration Required:**
- Users may need to log in again
- Bookmarks may need updating
- Clear browser cache recommended

---

## Database Migrations

### Current Schema Version: 1.0
Location: `supabase/migrations/`

### Applying Migrations

```bash
# Local development
cd supabase
supabase db push

# Production (via Supabase dashboard)
# Migrations applied automatically
```

### Migration History
- **2024-01**: Initial schema (users, apps, payments)
- **2024-02**: Added 2FA tables
- **2024-03**: Added goal integrity tables

---

## Breaking Changes

### October 2025
- ✅ Documentation structure changed (no code impact)
- 🔜 API endpoint consolidation (90-day deprecation period)

### Future Changes
See `ARCHITECTURE_IMPROVEMENT_PLAN.md` for complete roadmap.

---

## Rollback Procedures

### Documentation Rollback
```bash
# Restore archived docs (if needed)
cp archive/documentation_archive_2025_10_10/*.md .
```

### Database Rollback
Use Supabase point-in-time recovery via dashboard.

---

## Support

Questions about migrations? Check:
- `ARCHITECTURE_IMPROVEMENT_PLAN.md` - Complete roadmap
- `TROUBLESHOOTING.md` - Common issues
- `CHANGELOG.md` - Recent changes

---

*Last Updated: October 10, 2025*

