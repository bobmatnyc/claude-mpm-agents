# Base Template Library - REFERENCE PATTERNS ONLY

**Version**: 1.1.0
**Purpose**: Reference patterns and best practices for manual agent authoring
**Status**: ⚠️ REFERENCE ONLY - Claude Code does NOT support template inheritance

## Important Notice

**Claude Code does NOT support template inheritance** (no `extends:`, `inherits:`, or `base:` fields).

These base templates serve as **REFERENCE DOCUMENTATION** showing common patterns extracted from top-performing agents. When creating a new agent, **manually copy relevant patterns** from these files into your agent template.

For a comprehensive single-file reference guide, see: **[`templates/AGENT_TEMPLATE_REFERENCE.md`](../AGENT_TEMPLATE_REFERENCE.md)**

## Overview

The base template library documents reusable patterns extracted from 47+ production agents. Use these as a style guide and pattern reference when manually authoring new agents.

## Benefits

- **Pattern Reference**: See proven patterns from 47+ production agents
- **Maintain Consistency**: Follow established best practices and conventions
- **Learn by Example**: Understand how top-performing agents structure knowledge
- **Copy and Adapt**: Manually copy relevant patterns for your specific use case
- **Reduce Learning Curve**: See what works in production before creating new agents

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

## How to Use These Reference Patterns

⚠️ **No Automatic Inheritance**: Claude Code does NOT process `extends:`, `inherits:`, or `overrides:` fields.

### Manual Pattern Adoption Process

1. **Browse Base Templates**: Review `base-engineer.md`, `base-qa.md`, etc. for relevant patterns
2. **Identify Patterns**: Find sections that apply to your agent type
3. **Copy Manually**: Copy relevant markdown sections into your agent template
4. **Customize**: Adapt the pattern to your specific technology/domain
5. **Document**: Note where patterns came from for future reference

### Example: Adopting Error Handling Pattern

**Step 1**: Find pattern in `base-engineer.md`:
```markdown
## Error Handling Standards

- Use specific exceptions, not generic Exception
- Log errors with context before raising
- Propagate errors with raise from original exception
```

**Step 2**: Copy to your `my-new-agent.md` and customize:
```markdown
## Error Handling Standards

**Python-Specific**:
- Use specific exceptions: ValueError, TypeError, CustomError
- Log with logger.exception() for automatic stack traces
- Propagate with `raise CustomError() from e`
- Add type hints for exception types in function signatures
```

## Practical Usage Examples

### Example 1: Creating a New Engineer Agent

**Scenario**: You're creating a Go engineer agent.

**Process**:
1. Start with [`templates/AGENT_TEMPLATE_REFERENCE.md`](../AGENT_TEMPLATE_REFERENCE.md) for structure
2. Review `base-engineer.md` for engineering best practices
3. Copy relevant sections (code quality, testing, error handling)
4. Adapt to Go-specific patterns (gofmt, go test, error wrapping)
5. Add Go-specific knowledge (goroutines, channels, defer)

### Example 2: Creating a QA Agent

**Scenario**: You're creating a mobile app QA agent.

**Process**:
1. Use template reference for basic structure
2. Review `base-qa.md` for testing methodology
3. Copy evidence requirements and quality gates
4. Customize for mobile: UI testing, device matrix, performance
5. Add mobile-specific tools: Appium, XCTest, Espresso

### Example 3: Creating a Specialized Agent

**Scenario**: You're creating a database migration agent.

**Process**:
1. Start with template reference
2. Review `base-specialized.md` for domain expertise patterns
3. Copy integration guidelines
4. Add database-specific knowledge: migration tools, rollback strategies
5. Include safety checks: backup verification, dry-run testing

## Pattern Extraction Examples

### Pattern Reuse Across Agent Types

**Common Pattern** (from `base-engineer.md`):
```markdown
## Code Quality Principles

- **DRY (Don't Repeat Yourself)**: Extract common code into reusable functions
- **SOLID Principles**: Single responsibility, open/closed, Liskov substitution
- **Type Safety**: Use static analysis tools for type checking
- **Test Coverage**: 90%+ for critical paths
```

**Adapted for Python** (manually copied and customized):
```markdown
## Code Quality Principles

Follows engineering best practices with Python-specific tooling:

- **DRY**: Extract to functions, modules, use decorators for cross-cutting concerns
- **SOLID**: Apply with ABC interfaces, dependency injection patterns
- **Type Safety**: mypy --strict mode, 100% type coverage required
- **Test Coverage**: 90%+ with pytest-cov, property-based tests with hypothesis
- **Formatting**: black + isort + flake8 for consistent style
```

**Adapted for TypeScript** (manually copied and customized):
```markdown
## Code Quality Principles

Follows engineering best practices with TypeScript-specific tooling:

- **DRY**: Extract to functions, custom hooks (React), composition patterns
- **SOLID**: Apply with interfaces, dependency injection containers
- **Type Safety**: strict mode in tsconfig.json, no `any` types in production
- **Test Coverage**: 90%+ with Jest/Vitest, integration tests with Testing Library
- **Formatting**: ESLint + Prettier for consistent style
```

**Benefit**: Consistency across agents while allowing technology-specific customization.

## Maintenance Guidelines

### Updating Base Templates

**When to Update**:
- Pattern appears in 3+ production agents (document in base)
- Best practices evolve (update base reference)
- New common requirement emerges (add to base template)

**Update Process**:
1. Identify pattern commonality across agents
2. Document pattern in appropriate base template
3. Add example showing how to adapt pattern
4. Update base template changelog
5. Note in base template: "Used by: python-engineer, typescript-engineer, etc."

**Note**: Updates to base templates do NOT automatically update agents. Agents must manually adopt new patterns.

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
- Pattern appears in 5+ production agents
- Clear category boundary (engineering, QA, ops, etc.)
- Significant shared content (100+ lines of similar guidance)

**Process**:
1. Create new base template in `templates/base/`
2. Document in this README.md
3. Extract patterns from existing agents
4. Provide adaptation examples for different technologies
5. Note which agents already use similar patterns

## Best Practices

### ✅ DO

- **Use as Reference**: Treat base templates as documentation, not functional code
- **Copy and Adapt**: Manually copy relevant patterns into your agent
- **Document Source**: Note which base template inspired your pattern
- **Keep Generic**: Base templates show general patterns adaptable to many technologies
- **Provide Examples**: Show how to adapt patterns for different use cases
- **Version Changes**: Track base template updates with changelog

### ❌ DON'T

- **Expect Inheritance**: Claude Code does NOT support `extends:` or `inherits:` fields
- **Copy Blindly**: Always adapt patterns to your specific technology/domain
- **Over-Abstract**: Don't document patterns used by <3 agents
- **Deploy Base Templates**: Base templates are reference docs, not deployable agents
- **Assume Auto-Update**: Changes to base templates don't affect existing agents

## Reference Template Status

### Available Reference Templates

| Base Template | Status | Pattern Examples From | Lines |
|--------------|--------|----------------------|-------|
| base-engineer.md | ✅ Available | python-engineer, typescript-engineer, rust-engineer | ~400 |
| base-qa.md | ✅ Available | qa-agent, web-qa, api-qa | ~200 |
| base-ops.md | ✅ Available | ops-agent, vercel-ops, local-ops | ~150 |
| base-research.md | ✅ Available | research-agent, code-analyzer | ~250 |
| base-specialized.md | ✅ Available | imagemagick, circuit-breakers, git-tracking | ~100 |

### Documentation Status

- **Reference Templates**: Created and documented ✅
- **Single Template Guide**: [`AGENT_TEMPLATE_REFERENCE.md`](../AGENT_TEMPLATE_REFERENCE.md) ✅
- **Usage Examples**: Provided in this README ✅
- **Best Practices**: Documented for manual adoption ✅

## Potential Future Enhancements

### Tooling Ideas

1. **Pattern Search Tool**: CLI to search base templates for specific patterns
2. **Duplication Detector**: Identify opportunities for new base patterns
3. **Pattern Catalog**: Web-based searchable index of all patterns
4. **Agent Generator**: Interactive tool to create agents from base patterns

### Additional Base Templates

- **Language-Specific**: `base-python.md`, `base-typescript.md` for language idioms
- **Domain-Specific**: `base-backend.md`, `base-frontend.md` for architecture patterns
- **Tool-Specific**: `base-pytest.md`, `base-docker.md` for tool-specific workflows

**Note**: These are reference ideas only. Current base templates serve as comprehensive pattern documentation.

## References

### Exemplar Templates

These templates were analyzed to extract base patterns:
- **Engineering**: `agents/python-engineer.md` (1,338 lines, v2.3.0)
- **Research**: `agents/research.md` (959 lines, v4.9.0)
- **QA**: `agents/qa.md` (229 lines, v3.5.3)
- **Operations**: `agents/ops.md` (348 lines, v2.2.4)

### Related Documentation

- **Single Template Reference**: [`templates/AGENT_TEMPLATE_REFERENCE.md`](../AGENT_TEMPLATE_REFERENCE.md) - Comprehensive guide
- **Production Agents**: `agents/` directory - Real-world examples
- **Base Templates**: Current directory - Pattern reference library

---

**Last Updated**: 2025-11-30
**Maintainer**: Claude MPM Team
**Version**: 1.1.0 (Updated for manual reference only)
