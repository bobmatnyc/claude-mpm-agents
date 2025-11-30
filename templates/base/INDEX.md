# Base Template Index

Quick reference guide for the base template library.

## Files

| File | Lines | Purpose |
|------|-------|---------|
| **README.md** | 423 | Complete documentation and usage guide |
| **base-engineer.md** | 399 | Engineering patterns (SOLID, testing, docs) |
| **base-qa.md** | 427 | QA patterns (testing, coverage, quality gates) |
| **base-ops.md** | 494 | Operations patterns (deployment, monitoring) |
| **base-research.md** | 420 | Research patterns (analysis, evidence) |
| **base-specialized.md** | 519 | Specialized patterns (domain expertise) |
| **MIGRATION_GUIDE.md** | 524 | Migration examples and strategy |
| **IMPLEMENTATION_SUMMARY.md** | 510 | Project completion summary |
| **INDEX.md** | This file | Quick reference index |

**Total**: 3,716 lines of documentation and reusable patterns

## Quick Links

### Getting Started
- [Overview](README.md#overview) - What is the base template library?
- [Benefits](README.md#benefits) - Why use base templates?
- [Inheritance Mechanism](README.md#inheritance-mechanism) - How to use base templates

### Base Templates
- [base-engineer.md](base-engineer.md) - For engineering agents (18 agents)
- [base-qa.md](base-qa.md) - For QA agents (5 agents)
- [base-ops.md](base-ops.md) - For operations agents (8 agents)
- [base-research.md](base-research.md) - For research agents (3 agents)
- [base-specialized.md](base-specialized.md) - For specialized agents (13 agents)

### Migration
- [Migration Guide](MIGRATION_GUIDE.md) - How to migrate existing agents
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Project completion report

## Pattern Catalog

### Engineering Patterns (base-engineer.md)

| Section ID | Description | Lines |
|------------|-------------|-------|
| `code_quality_principles` | DRY, SOLID, type safety | 30 |
| `error_handling_standards` | Exception hierarchy, logging | 35 |
| `testing_approach` | Test levels, coverage, organization | 45 |
| `documentation_requirements` | Docstrings, API docs, examples | 40 |
| `performance_considerations` | Profiling, complexity analysis | 30 |
| `memory_management` | Resource cleanup, streaming | 25 |
| `version_control_patterns` | Commit messages, git workflow | 20 |
| `security_patterns` | Input validation, auth, secrets | 35 |
| `code_review_standards` | Review checklist, focus areas | 25 |
| `anti_patterns` | Common mistakes to avoid | 40 |

### QA Patterns (base-qa.md)

| Section ID | Description | Lines |
|------------|-------------|-------|
| `testing_methodology` | TDD, BDD, property-based testing | 40 |
| `evidence_requirements` | Test logs, coverage, performance | 35 |
| `test_coverage_expectations` | Coverage thresholds, analysis | 30 |
| `quality_gates` | Pre-merge, continuous, release gates | 30 |
| `verification_templates` | Functional, performance, security | 40 |
| `test_strategies` | Unit, integration, e2e, performance | 35 |
| `test_organization` | File structure, naming conventions | 25 |
| `bug_reporting` | Bug report template, severity levels | 30 |
| `test_automation` | CI/CD integration, test selection | 30 |
| `test_data_management` | Fixtures, factories, mocks | 30 |
| `memory_efficient_testing` | Strategic sampling, process cleanup | 25 |

### Operations Patterns (base-ops.md)

| Section ID | Description | Lines |
|------------|-------------|-------|
| `deployment_verification` | Pre/post deployment checks | 40 |
| `health_check_patterns` | Liveness, readiness, startup | 45 |
| `logging_monitoring` | Log levels, structured logging, metrics | 50 |
| `rollback_procedures` | Automated/manual rollback, testing | 35 |
| `environment_management` | Env separation, configuration | 35 |
| `secret_management` | Secret detection, storage, rotation | 40 |
| `container_operations` | Docker best practices, security | 35 |
| `cicd_pipeline_patterns` | Pipeline stages, best practices | 35 |
| `monitoring_alerting` | Observability, alerts, on-call | 35 |

### Research Patterns (base-research.md)

| Section ID | Description | Lines |
|------------|-------------|-------|
| `analysis_framework` | Systematic investigation process | 40 |
| `evidence_collection` | Quantitative, qualitative, source evidence | 45 |
| `knowledge_synthesis` | Synthesis process, structure | 50 |
| `documentation_standards` | Research document structure | 45 |
| `confidence_levels` | Confidence rating, uncertainty handling | 30 |
| `memory_efficient_research` | Strategic sampling, tool selection | 35 |
| `work_capture` | Automatic documentation, ticketing | 25 |

### Specialized Patterns (base-specialized.md)

| Section ID | Description | Lines |
|------------|-------------|-------|
| `domain_expertise_patterns` | Specialized knowledge areas | 45 |
| `integration_guidelines` | API integration, tool chaining | 55 |
| `tool_specific_workflows` | Workflow template, error handling | 50 |
| `configuration_management` | Layered configuration, validation | 45 |
| `specialized_testing` | Domain-specific test patterns | 35 |
| `performance_optimization` | Batch processing, caching | 40 |

## Usage Examples

### Example 1: Inherit All Engineering Patterns

```yaml
---
name: typescript-engineer
extends: base-engineer
inherits:
  - code_quality_principles
  - error_handling_standards
  - testing_approach
  - documentation_requirements
---
```

### Example 2: Inherit with Overrides

```yaml
---
name: python-engineer
extends: base-engineer
inherits:
  - code_quality_principles
  - testing_approach
overrides:
  testing_approach: |
    **Inherits from base-engineer**: Testing levels, coverage

    **Python-Specific**:
    - pytest with fixtures and parametrize
    - hypothesis for property-based testing
    - 90%+ coverage with pytest-cov
---
```

### Example 3: Partial Inheritance

```yaml
---
name: qa-agent
extends: base-qa
inherits:
  - testing_methodology
  - evidence_requirements
  - quality_gates
# Does not inherit: test_automation, bug_reporting
---
```

## Search Tips

### Find Pattern by Topic
- **Code quality**: See `base-engineer.md#code_quality_principles`
- **Testing**: See `base-qa.md#testing_methodology` or `base-engineer.md#testing_approach`
- **Deployment**: See `base-ops.md#deployment_verification`
- **Security**: See `base-engineer.md#security_patterns` or `base-ops.md#secret_management`
- **Documentation**: See `base-engineer.md#documentation_requirements`

### Find Pattern by Agent Category
- **Engineering agents** (18 total): Use `base-engineer.md`
- **QA agents** (5 total): Use `base-qa.md`
- **Operations agents** (8 total): Use `base-ops.md`
- **Research agents** (3 total): Use `base-research.md`
- **Specialized agents** (13 total): Use `base-specialized.md`

## Maintenance

### Update a Pattern
1. Edit appropriate base template (e.g., `base-engineer.md`)
2. Update version in metadata section
3. Add changelog entry
4. Pattern automatically cascades to all inheriting agents

### Add New Pattern
1. Identify which base template applies
2. Add pattern with section ID: `## Pattern Name {#pattern_id}`
3. Document in pattern catalog (this file)
4. Update version and changelog

### Deprecate a Pattern
1. Mark as deprecated in base template
2. Suggest alternative pattern
3. Update agents to use new pattern
4. Remove after migration complete

---

**Last Updated**: 2025-11-30
**Maintainer**: Claude MPM Team
**Version**: 1.0.0
