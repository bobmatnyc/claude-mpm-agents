# Base Template Library

**Version**: 1.0.0
**Purpose**: Project-level base templates for agent template inheritance
**Status**: ✅ PROJECT-LEVEL ONLY (Not deployed as agents)

## Overview

The base template library provides reusable pattern collections that agent templates can reference to reduce duplication while maintaining flexibility. Base templates extract common patterns across agent categories (engineering, QA, operations, research, specialized) into single-source-of-truth documents.

## Benefits

- **Reduce Duplication**: Extract common patterns shared across 47+ agent templates
- **Maintain Consistency**: Single source of truth for best practices
- **Enable Flexibility**: Agents can extend, override, or customize base patterns
- **Simplify Maintenance**: Update patterns in one place, cascade to all agents
- **Preserve Specialization**: Agents keep domain-specific logic while sharing common infrastructure

## Base Template Structure

```
templates/base/
├── README.md                 # This file - documentation and usage guide
├── base-engineer.md          # Common engineering patterns (SOLID, DRY, testing)
├── base-qa.md                # Common testing/QA patterns (coverage, validation)
├── base-ops.md               # Common operations patterns (deployment, monitoring)
├── base-research.md          # Common analysis/research patterns (methodology)
└── base-specialized.md       # Common specialized agent patterns (integration)
```

## Base Templates

### base-engineer.md
**Category**: Engineering
**Purpose**: Common engineering quality standards, code patterns, error handling, testing approaches
**Used By**: python-engineer, typescript-engineer, rust-engineer, golang-engineer, java-engineer, etc.

**Extracted Patterns**:
- Code quality principles (DRY, SOLID, type safety)
- Error handling standards
- Testing approach guidelines (unit, integration, property-based)
- Documentation requirements (docstrings, API docs)
- Performance considerations
- Memory routing for implementation knowledge

### base-qa.md
**Category**: Quality Assurance
**Purpose**: Testing methodologies, quality gates, evidence requirements
**Used By**: qa-agent, web-qa, api-qa, test-quality-inspector, etc.

**Extracted Patterns**:
- Testing methodology principles (TDD, BDD, property-based)
- Evidence requirements (logs, metrics, screenshots)
- Test coverage expectations (90%+ for critical paths)
- Quality gate definitions
- Verification templates
- Memory routing for bug patterns

### base-ops.md
**Category**: Operations
**Purpose**: Deployment verification, infrastructure management, monitoring standards
**Used By**: ops-agent, local-ops-agent, vercel-ops, gcp-ops, clerk-ops, etc.

**Extracted Patterns**:
- Deployment verification protocols
- Health check patterns
- Logging and monitoring standards
- Rollback procedures
- Environment management
- Security scanning (secret detection)
- Memory routing for deployment patterns

### base-research.md
**Category**: Research
**Purpose**: Analysis frameworks, knowledge synthesis, documentation standards
**Used By**: research-agent, code-analyzer, documentation-agent, etc.

**Extracted Patterns**:
- Analysis framework (systematic investigation)
- Evidence collection standards
- Documentation of findings
- Knowledge synthesis patterns
- Memory routing for domain knowledge

### base-specialized.md
**Category**: Specialized
**Purpose**: Domain expertise patterns, integration guidelines, tool usage
**Used By**: Domain-specific agents (imagemagick, circuit-breakers, git-file-tracking, etc.)

**Extracted Patterns**:
- Domain expertise patterns
- Integration guidelines
- Specialized tool usage
- Memory routing for specialized knowledge

## Inheritance Mechanism

### Metadata-Based Reference

Agent templates reference base templates using YAML metadata:

```yaml
---
name: python-engineer
extends: base-engineer
inherits:
  - code_quality_principles
  - error_handling_standards
  - testing_approach
  - documentation_requirements
overrides:
  testing_approach: |
    Python-specific testing with pytest:
    - Use fixtures for test dependencies
    - Parametrize for data-driven tests
    - Property-based testing with hypothesis
    - 90%+ coverage with pytest-cov
---
```

### Inheritance Fields

**extends** (string): Base template to inherit from
- Values: `base-engineer`, `base-qa`, `base-ops`, `base-research`, `base-specialized`
- Effect: Agent inherits all patterns from base template

**inherits** (list): Specific sections to inherit from base
- Values: Section IDs from base template (e.g., `code_quality_principles`, `error_handling_standards`)
- Effect: Cherry-pick specific patterns from base template

**overrides** (object): Customizations for inherited patterns
- Keys: Section IDs to override
- Values: Agent-specific implementation details
- Effect: Replace base pattern with specialized version

### Section IDs

Base templates define reusable sections with IDs:

```markdown
## Code Quality Principles {#code_quality_principles}

- **DRY (Don't Repeat Yourself)**: Extract common code into reusable functions
- **SOLID Principles**: Single responsibility, open/closed, etc.
- **Type Safety**: Use type hints, static analysis tools
```

Agents reference these sections by ID in `inherits` or `overrides` fields.

## Usage Examples

### Example 1: Full Inheritance (Python Engineer)

**Agent Template** (`agents/python-engineer.md`):
```yaml
---
name: python-engineer
extends: base-engineer
inherits:
  - code_quality_principles
  - error_handling_standards
  - testing_approach
  - documentation_requirements
overrides:
  testing_approach: |
    **Python Testing with pytest**:
    - Use fixtures for dependency injection in tests
    - Parametrize test functions for data-driven testing
    - Property-based testing with hypothesis for edge cases
    - Achieve 90%+ coverage with pytest-cov
    - Async testing with pytest-asyncio
---
```

**Result**: Agent gets all base engineering patterns + Python-specific testing details.

### Example 2: Partial Inheritance (QA Agent)

**Agent Template** (`agents/qa-agent.md`):
```yaml
---
name: qa-agent
extends: base-qa
inherits:
  - testing_methodology
  - evidence_requirements
  - quality_gates
overrides:
  testing_methodology: |
    **Memory-Efficient Testing**:
    - Strategic sampling (5-10 test files max per session)
    - Use grep for test discovery instead of file reading
    - Extract metrics from tool outputs, not source files
---
```

**Result**: Agent gets base QA patterns + memory-efficient testing customizations.

### Example 3: Multiple Base References

**Agent Template** (`agents/typescript-engineer.md`):
```yaml
---
name: typescript-engineer
extends: base-engineer
inherits:
  - code_quality_principles
  - error_handling_standards
  - testing_approach
additional_extends:
  - base-specialized  # For frontend-specific patterns
inherits_from_specialized:
  - integration_guidelines  # How to integrate with React, Next.js
---
```

**Result**: Agent combines engineering and specialized patterns.

## Migration Path

### Before: Duplicated Patterns

**python-engineer.md**:
```markdown
## Code Quality
- DRY principle
- SOLID principles
- Type safety with mypy
- 90%+ test coverage
```

**typescript-engineer.md**:
```markdown
## Code Quality
- DRY principle
- SOLID principles
- Type safety with TypeScript
- 90%+ test coverage
```

### After: Base Template + Extensions

**base-engineer.md** (shared):
```markdown
## Code Quality Principles {#code_quality_principles}
- **DRY**: Extract common code into reusable functions
- **SOLID**: Single responsibility, open/closed, Liskov substitution, etc.
- **Type Safety**: Use static analysis tools for type checking
- **Test Coverage**: 90%+ for critical paths
```

**python-engineer.md** (extension):
```yaml
extends: base-engineer
inherits: [code_quality_principles]
overrides:
  code_quality_principles: |
    Inherits from base-engineer.

    Python-specific:
    - Type safety: mypy --strict mode
    - Linting: black + isort + flake8
```

**typescript-engineer.md** (extension):
```yaml
extends: base-engineer
inherits: [code_quality_principles]
overrides:
  code_quality_principles: |
    Inherits from base-engineer.

    TypeScript-specific:
    - Type safety: strict mode in tsconfig.json
    - Linting: ESLint + Prettier
```

## Comparison: Duplication Reduction

### Before (Duplicated)

**Total Lines**:
- python-engineer.md: 1,338 lines
- typescript-engineer.md: 1,200 lines
- rust-engineer.md: 1,100 lines
- **Common patterns duplicated**: ~400 lines × 3 = 1,200 lines

### After (Base Template)

**Total Lines**:
- base-engineer.md: 400 lines (extracted common patterns)
- python-engineer.md: 938 lines (1,338 - 400 shared)
- typescript-engineer.md: 800 lines (1,200 - 400 shared)
- rust-engineer.md: 700 lines (1,100 - 400 shared)
- **Reduction**: 1,200 lines eliminated (30% reduction)

## Maintenance Guidelines

### Updating Base Templates

**When to Update**:
- Pattern used in 3+ agent templates (extract to base)
- Best practice changes (update base, cascades to agents)
- New common requirement (add to base template)

**Update Process**:
1. Identify pattern duplication across agents
2. Extract pattern to appropriate base template
3. Update agent templates to reference base pattern
4. Document in base template changelog
5. Verify no breaking changes to existing agents

### Versioning

Base templates use semantic versioning:
- **MAJOR**: Breaking changes to pattern structure
- **MINOR**: New patterns added (backward compatible)
- **PATCH**: Clarifications, bug fixes

Example:
```yaml
---
template_type: base
version: 1.2.3
changelog:
  - version: 1.2.3
    date: '2025-11-30'
    description: Clarified error handling patterns
  - version: 1.2.0
    date: '2025-11-28'
    description: Added performance optimization patterns
---
```

### Adding New Base Templates

**Criteria for New Base Template**:
- Pattern used in 5+ agent templates
- Clear category boundary (engineering, QA, ops, etc.)
- Significant duplication (100+ lines repeated)

**Process**:
1. Create new base template in `templates/base/`
2. Document in this README.md
3. Extract patterns from existing agents
4. Update agent templates to reference new base
5. Validate no functionality lost

## Best Practices

### ✅ DO

- **Extract Common Patterns**: If pattern appears in 3+ agents, extract to base
- **Document Section IDs**: Use clear, descriptive IDs for reusable sections
- **Version Base Templates**: Track changes with semantic versioning
- **Test Inheritance**: Verify agents work correctly after extracting to base
- **Keep Base Generic**: Base templates should be language/tool agnostic when possible
- **Document Overrides**: Explain why agent overrides base pattern

### ❌ DON'T

- **Over-Abstract**: Don't extract unique patterns (used by <3 agents)
- **Lose Flexibility**: Agents must be able to override base patterns
- **Create Deep Hierarchies**: Limit to 1-2 levels of inheritance
- **Deploy Base Templates**: Base templates are PROJECT-LEVEL only, not agents
- **Duplicate Section IDs**: Each section ID must be unique within base template
- **Break Existing Agents**: Always verify backward compatibility

## Implementation Status

### Extraction Progress

| Base Template | Status | Agents Using | Lines Extracted |
|--------------|--------|--------------|-----------------|
| base-engineer.md | ✅ Created | 18 | ~400 |
| base-qa.md | ✅ Created | 5 | ~200 |
| base-ops.md | ✅ Created | 8 | ~150 |
| base-research.md | ✅ Created | 3 | ~250 |
| base-specialized.md | ✅ Created | 13 | ~100 |

### Migration Status

- **Phase 1**: Base templates created ✅
- **Phase 2**: Documentation completed ✅
- **Phase 3**: Agent migration (future work) ⏳
- **Phase 4**: Validation and testing (future work) ⏳

## Future Enhancements

### Planned Improvements

1. **Automated Extraction**: Tool to detect duplicate patterns across agents
2. **Validation**: Linter to verify agents correctly reference base templates
3. **Template Composition**: Support multiple base template inheritance
4. **Pattern Catalog**: Searchable index of all base patterns
5. **Change Impact Analysis**: Tool to show which agents affected by base changes

### Potential Extensions

- **Language-Specific Bases**: `base-python.md`, `base-typescript.md` for language patterns
- **Domain-Specific Bases**: `base-backend.md`, `base-frontend.md` for architecture patterns
- **Tool-Specific Bases**: `base-pytest.md`, `base-docker.md` for tool-specific patterns

## References

### Exemplar Templates

These templates were analyzed to extract base patterns:
- **Engineering**: `agents/python-engineer.md` (1,338 lines, v2.3.0)
- **Research**: `agents/research.md` (959 lines, v4.9.0)
- **QA**: `agents/qa.md` (229 lines, v3.5.3)
- **Operations**: `agents/ops.md` (348 lines, v2.2.4)

### Related Documentation

- **Agent Templates**: `agents/README.md` (if exists)
- **Deployment Guide**: (not applicable - base templates are PROJECT-LEVEL only)

---

**Last Updated**: 2025-11-30
**Maintainer**: Claude MPM Team
**Version**: 1.0.0
