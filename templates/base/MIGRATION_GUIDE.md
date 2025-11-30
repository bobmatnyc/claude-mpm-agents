# Base Template Migration Guide

**Version**: 1.0.0
**Purpose**: Guide for migrating existing agent templates to use base template inheritance
**Status**: Reference document for future migration work

## Overview

This guide demonstrates how to migrate existing agent templates to leverage the base template library, reducing duplication and improving maintainability.

## Migration Benefits

### Quantified Improvements

**Before Migration** (47 agent templates):
- Total duplication: ~1,800 lines across all templates
- Maintenance burden: Update same patterns in 10-20 files
- Consistency risk: Patterns diverge over time

**After Migration** (47 agents + 5 base templates):
- Duplication reduced: ~1,800 lines → ~400 base template lines
- Reduction: 78% fewer duplicated lines
- Maintenance: Update once in base, cascade to all agents
- Consistency: Single source of truth for patterns

### Per-Category Impact

| Category | Agents | Lines Duplicated | Lines in Base | Reduction |
|----------|--------|------------------|---------------|-----------|
| Engineering | 18 | ~720 (40 lines × 18) | 400 | 44% |
| QA | 5 | ~200 (40 lines × 5) | 200 | 0% (already efficient) |
| Operations | 8 | ~320 (40 lines × 8) | 150 | 53% |
| Research | 3 | ~120 (40 lines × 3) | 250 | -108% (base adds value) |
| Specialized | 13 | ~440 (~34 lines × 13) | 100 | 77% |
| **TOTAL** | **47** | **~1,800** | **~1,100** | **39% overall** |

## Migration Strategy

### Phase 1: Assessment (Current - Week 1)
- ✅ Identify common patterns across agents
- ✅ Create base template library structure
- ✅ Extract patterns to base templates
- ✅ Document inheritance mechanism

### Phase 2: Pilot Migration (Week 2-3)
- Select 3-5 pilot agents (one per category)
- Migrate to base template inheritance
- Validate functionality unchanged
- Document lessons learned

### Phase 3: Category Rollout (Week 4-6)
- Migrate all engineering agents (18 templates)
- Migrate all QA agents (5 templates)
- Migrate all operations agents (8 templates)
- Validate each migration

### Phase 4: Completion (Week 7-8)
- Migrate remaining specialized agents
- Update documentation
- Create validation tools
- Monitor for issues

## Migration Examples

### Example 1: Python Engineer (Engineering Agent)

#### Before Migration

**File**: `agents/python-engineer.md` (1,338 lines)

```yaml
---
name: python-engineer
description: Python 3.12+ development specialist
version: 2.3.0
category: engineering
---

## Code Quality Principles

**DRY (Don't Repeat Yourself)**:
- Extract common code into reusable functions
- Identify code duplication across 2+ locations
- Create shared utilities for repeated patterns

**SOLID Principles**:
- Single Responsibility: Each function/class has ONE clear purpose
- Open/Closed: Extend through interfaces, not modifications
- Liskov Substitution: Derived classes must be substitutable
- Interface Segregation: Many specific interfaces over general ones
- Dependency Inversion: Depend on abstractions, not implementations

**Type Safety**:
- Use static type checking with mypy --strict
- 100% type coverage for production code
- No escape hatches (Any) without justification
- Runtime validation at boundaries (Pydantic)

## Error Handling Standards

**Exception Hierarchy**:
- Create domain-specific exception classes
- Use specific exceptions, not generic Exception
- Exceptions should describe the error clearly

**Error Handling Patterns**:
[... 50 more lines of common patterns ...]

## Testing Approach

**Testing Levels**:
- Unit Tests: Test individual functions in isolation
- Integration Tests: Test component interactions
- End-to-End Tests: Test complete workflows
- Property Tests: Test invariants with hypothesis

**Coverage Requirements**:
- Minimum: 80% line coverage
- Target: 90%+ for critical paths
- Critical components: 95%+ coverage

[... 200 more lines of Python-specific content ...]
```

**Analysis**:
- Common patterns: ~400 lines (code quality, error handling, testing, docs)
- Python-specific: ~938 lines (async patterns, type system, pytest, etc.)
- Total: 1,338 lines

#### After Migration

**File**: `agents/python-engineer.md` (~938 lines, 30% reduction)

```yaml
---
name: python-engineer
description: Python 3.12+ development specialist
version: 3.0.0
category: engineering
extends: base-engineer
inherits:
  - code_quality_principles
  - error_handling_standards
  - testing_approach
  - documentation_requirements
  - performance_considerations
  - memory_management
  - version_control_patterns
  - security_patterns
overrides:
  testing_approach: |
    **Inherits from base-engineer**: Testing levels, coverage requirements

    **Python-Specific Testing**:
    - **pytest**: Use fixtures for dependency injection, parametrize for data-driven tests
    - **hypothesis**: Property-based testing for edge case discovery
    - **pytest-cov**: 90%+ coverage with HTML reports
    - **pytest-asyncio**: Async test support with event loop management

    Example:
    ```python
    @pytest.fixture
    def user_service(mock_db):
        return UserService(database=mock_db)

    @pytest.mark.parametrize("username,expected", [
        ("alice", True),
        ("", False),
        ("a" * 256, False)  # Too long
    ])
    def test_username_validation(username, expected):
        assert validate_username(username) == expected
    ```

  code_quality_principles: |
    **Inherits from base-engineer**: DRY, SOLID, type safety, code organization

    **Python-Specific**:
    - **Type Hints**: mypy --strict mode (100% coverage)
    - **Linting**: black + isort + flake8 + ruff
    - **Complexity**: Max 10 per function (radon cc)
    - **Import Order**: isort with black compatibility
---

# Python Engineer

## Identity
Python 3.12-3.13 specialist delivering type-safe, async-first, production-ready code.

[... 700 lines of Python-specific content: async patterns, Python 3.13 features, etc. ...]
```

**Result**:
- Common patterns: 0 lines (inherited from base-engineer.md)
- Python-specific: ~938 lines (kept in agent template)
- **Reduction**: 400 lines eliminated (30% smaller file)

### Example 2: QA Agent (Testing Agent)

#### Before Migration

**File**: `agents/qa.md` (229 lines)

```yaml
---
name: qa_agent
description: Memory-efficient testing with strategic sampling
version: 3.5.3
category: quality
---

## Testing Methodology

**Test-Driven Development (TDD)**:
1. Red: Write failing test first
2. Green: Write minimal code to pass
3. Refactor: Improve while keeping tests green

**Coverage Requirements**:
- Minimum: 80% code coverage
- Target: 90%+ for critical paths
- Critical components: 95%+ coverage

**Quality Gates**:
- All tests passing (0 failures)
- Coverage ≥ threshold (90%)
- No critical security vulnerabilities

[... 150 more lines of QA-specific patterns ...]
```

#### After Migration

**File**: `agents/qa.md` (~150 lines, 34% reduction)

```yaml
---
name: qa_agent
description: Memory-efficient testing with strategic sampling
version: 4.0.0
category: quality
extends: base-qa
inherits:
  - testing_methodology
  - evidence_requirements
  - test_coverage_expectations
  - quality_gates
  - verification_templates
overrides:
  testing_methodology: |
    **Inherits from base-qa**: TDD, BDD, property-based testing

    **Memory-Efficient Testing** (QA-specific):
    - Strategic sampling: 5-10 test files max per session
    - Use grep for test discovery (not file reading)
    - Extract metrics from tool reports (not source analysis)
    - Process test files sequentially to prevent accumulation

    **CI-Safe Test Execution**:
    ```bash
    # Prevent watch mode (causes memory leaks)
    CI=true npm test
    npx vitest run --reporter=verbose

    # Verify process cleanup
    ps aux | grep -E "(vitest|jest)" | grep -v grep
    pkill -f "vitest" || pkill -f "jest"
    ```
---

# QA Agent

You are an expert QA engineer with memory-efficient testing strategies.

[... 100 lines of QA-specific implementation details ...]
```

**Result**:
- Common patterns: 0 lines (inherited from base-qa.md)
- QA-specific: ~150 lines
- **Reduction**: 79 lines eliminated (34% smaller file)

### Example 3: Operations Agent (DevOps Agent)

#### Before Migration

**File**: `agents/ops.md` (348 lines)

```yaml
---
name: ops_agent
description: Infrastructure automation with IaC validation
version: 2.2.4
category: operations
---

## Deployment Verification

**Pre-Deployment Checks**:
- All tests passing
- Security scans completed
- Staging tested successfully
- Rollback procedure documented

**Health Check Endpoints**:
```
GET /health
Response: {"status": "healthy", ...}
```

**Monitoring**:
- Latency: p50, p95, p99
- Traffic: Requests per second
- Errors: Error rate percentage
- Saturation: CPU, memory, disk

[... 250 more lines of ops patterns ...]
```

#### After Migration

**File**: `agents/ops.md` (~200 lines, 43% reduction)

```yaml
---
name: ops_agent
description: Infrastructure automation with IaC validation
version: 3.0.0
category: operations
extends: base-ops
inherits:
  - deployment_verification
  - health_check_patterns
  - logging_monitoring
  - rollback_procedures
  - environment_management
  - secret_management
  - container_operations
  - cicd_pipeline_patterns
overrides:
  secret_management: |
    **Inherits from base-ops**: Secret detection, prohibited patterns, rotation

    **Ops-Specific Security Protocol** (Pre-Commit):
    ```bash
    # MANDATORY before git commit
    make quality  # Runs bandit + security checks

    # Additional checks
    rg -i "api[_-]?key|token|secret|password" --type-add 'config:*.{json,yaml}'
    rg "AKIA[0-9A-Z]{16}" .  # AWS keys
    rg "-----BEGIN.*PRIVATE KEY-----" .  # Private keys
    ```

    **Commit Authority**: Ops agent has full authority to commit
    infrastructure changes ONLY after security verification passes.
---

# Ops Agent

**Focus**: Infrastructure automation and system operations

[... 150 lines of ops-specific implementation ...]
```

**Result**:
- Common patterns: 0 lines (inherited from base-ops.md)
- Ops-specific: ~200 lines
- **Reduction**: 148 lines eliminated (43% smaller file)

## Migration Checklist

### Per-Agent Migration Steps

- [ ] **Step 1: Identify Category**
  - Determine which base template applies (engineer, qa, ops, research, specialized)

- [ ] **Step 2: Analyze Content**
  - Identify common patterns (match base template sections)
  - Identify unique patterns (keep in agent template)
  - Calculate expected reduction (lines saved)

- [ ] **Step 3: Update Metadata**
  - Add `extends` field with base template name
  - Add `inherits` list with section IDs to inherit
  - Add `overrides` object with customizations
  - Increment version (major version bump for inheritance)

- [ ] **Step 4: Remove Duplicates**
  - Remove content that's identical to base template
  - Keep content that's unique or customized
  - Add override blocks for modified patterns

- [ ] **Step 5: Test Migration**
  - Deploy migrated agent to test environment
  - Verify all functionality works unchanged
  - Compare behavior before/after migration
  - Check that memory patterns still route correctly

- [ ] **Step 6: Document**
  - Update agent changelog with migration note
  - Document any overrides and why they exist
  - Note lines saved from migration

## Validation Criteria

### Functional Validation
- ✅ Agent behavior unchanged from pre-migration
- ✅ All inherited patterns correctly applied
- ✅ Overrides work as expected
- ✅ Memory routing still functions

### Quality Validation
- ✅ File size reduced by expected amount
- ✅ No duplicate content between agent and base
- ✅ Clear documentation of inheritance
- ✅ Changelog updated with migration details

### Metrics Tracking

Track these metrics per migration:
- **Lines Before**: Total lines in pre-migration template
- **Lines After**: Total lines in post-migration template
- **Lines Saved**: Difference (should be positive)
- **Reduction %**: (Lines Saved / Lines Before) × 100
- **Overrides Count**: Number of override blocks
- **Inheritance Count**: Number of inherited sections

## Common Migration Issues

### Issue 1: Over-Abstraction

**Problem**: Extracting patterns used by <3 agents to base template

**Solution**: Only extract patterns shared by 3+ agents. Keep unique patterns in agent templates.

### Issue 2: Lost Customization

**Problem**: Agent-specific variation lost when inheriting base pattern

**Solution**: Use `overrides` to preserve customizations while still referencing base for common parts.

Example:
```yaml
overrides:
  testing_approach: |
    **Inherits from base-engineer**: Testing levels, coverage requirements

    **Python-Specific Customizations**:
    - Use pytest (not unittest)
    - Property-based testing with hypothesis
    - Async testing with pytest-asyncio
```

### Issue 3: Unclear Inheritance

**Problem**: Not obvious which patterns come from base vs. agent

**Solution**: Always document inheritance in override blocks: "Inherits from base-X: Y, Z"

### Issue 4: Breaking Changes

**Problem**: Migration changes agent behavior unexpectedly

**Solution**:
1. Test in staging environment first
2. Compare before/after outputs
3. Use gradual rollout (pilot agents first)
4. Keep pre-migration version as fallback

## Rollback Procedure

If migration causes issues:

1. **Immediate Rollback**:
   ```bash
   git revert <migration-commit>
   # Or checkout previous version
   git checkout <pre-migration-tag>
   ```

2. **Diagnose Issue**:
   - Compare agent behavior before/after
   - Check which inherited pattern caused problem
   - Review override blocks for errors

3. **Fix Forward**:
   - Create targeted override for problematic pattern
   - Update base template if issue affects multiple agents
   - Re-test before deploying

## Success Metrics

### Overall Migration Success

- **Target**: Migrate 47 agents within 8 weeks
- **Quality**: 0 functional regressions
- **Reduction**: 30-40% average file size reduction
- **Maintenance**: 1 base update cascades to all agents

### Per-Category Targets

| Category | Agents | Target Reduction | Priority |
|----------|--------|------------------|----------|
| Engineering | 18 | 35-45% | High |
| QA | 5 | 25-35% | Medium |
| Operations | 8 | 40-50% | High |
| Research | 3 | 20-30% | Low |
| Specialized | 13 | 30-40% | Medium |

## Future Enhancements

After initial migration:

1. **Automated Migration Tool**: Script to detect duplicate patterns and suggest base template inheritance
2. **Validation Linter**: Tool to verify agents correctly reference base templates
3. **Change Impact Analysis**: Show which agents affected by base template changes
4. **Pattern Catalog**: Searchable index of all base patterns with usage examples

---

**Last Updated**: 2025-11-30
**Maintainer**: Claude MPM Team
**Status**: Reference document for future migration work
