# Contributing to Cognomega

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Read the documentation**:
   - `README.md` - Project overview
   - `ARCHITECTURE_IMPROVEMENT_PLAN.md` - Current roadmap
   - `CTO_REVIEW_REPORT.md` - Current state analysis

2. **Set up your development environment**:
   - See `DEVELOPMENT_GUIDE.md` for setup instructions
   - Ensure all syntax checks pass: `python check_all_backend_syntax.py`

## How to Contribute

### Reporting Issues
- Check existing issues first
- Provide clear description and reproduction steps
- Include relevant logs and error messages

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**:
   - Follow the code style guidelines (see `CODE_STYLE.md`)
   - Add tests for new functionality
   - Update documentation as needed
4. **Run tests**: Ensure all tests pass
5. **Commit your changes**: Follow commit message guidelines
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Submit a pull request**

### Pull Request Guidelines
- Provide clear description of changes
- Reference related issues
- Ensure CI/CD checks pass
- Request review from maintainers

## Current Priorities (October 2025)

Based on the **Architecture Improvement Plan**, the current priorities are:

### Week 1 (Current)
- ✅ Fix syntax errors (COMPLETE)
- ✅ Documentation cleanup (COMPLETE)
- 🔜 Frontend assessment
- 🔜 CI/CD pipeline setup

### Weeks 2-3
- Router consolidation (118 → 15)
- Service consolidation (296 → 40)
- Remove DNA systems (14 → 0)

See `ARCHITECTURE_IMPROVEMENT_PLAN.md` for complete timeline.

## Code Review Process

1. All changes require code review
2. At least one approval required
3. All CI/CD checks must pass
4. Documentation must be updated

## Questions?

- Open an issue for questions
- Check archived documentation for historical context

---

*Last Updated: October 10, 2025*

