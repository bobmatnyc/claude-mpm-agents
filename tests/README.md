# DeepEval Testing Framework for Agent Instruction Compliance

This testing framework validates that Claude MPM agents follow their BASE-AGENT.md instructions using [DeepEval](https://docs.confident-ai.com/), a testing framework specifically designed for LLM applications.

## Overview

The framework tests three main areas:

1. **Instruction Compliance**: Validates agents follow BASE-AGENT.md rules
2. **Role Boundaries**: Ensures agents stay within their defined roles
3. **Agent Registry**: Validates agent metadata and frontmatter

## Installation

```bash
# Install test dependencies
pip install -e ".[test]"

# Install dev dependencies (includes ruff)
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tests --cov-report=html

# Run specific test categories
pytest -m instruction_compliance
pytest -m role_boundary
pytest -m registry

# Run specific test file
pytest tests/test_instruction_compliance.py -v

# Run with verbose output
pytest -v -s
```

## Test Categories

### Instruction Compliance Tests

Tests that agent responses follow BASE-AGENT.md instructions:

- **Git Workflow**: Conventional commits, proper commit messages
- **Output Format**: Markdown headers, code blocks, structure
- **Category-Specific Rules**: Engineer (type safety), QA (bug reports), Ops (deployment verification)

```python
# Example: Test conventional commit format
def test_git_workflow_conventional_commits(mock_generator):
    response = mock_generator.generate_compliant_response(
        agent_type="engineer",
        task_type="implement_feature"
    )

    test_case = LLMTestCase(
        input="Add new feature",
        actual_output=response.content,
    )

    metric = GitWorkflowComplianceMetric(threshold=0.9)
    assert_test(test_case, [metric])
```

### Role Boundary Tests

Tests that agents stay within their role boundaries:

- **Engineer**: Should code/implement, should NOT deploy to production
- **QA**: Should test/verify, should NOT implement features
- **Ops**: Should deploy/monitor, should NOT write business logic

```python
# Example: Test engineer doesn't cross into ops territory
def test_engineer_does_not_deploy():
    response_content = """
    I've deployed the changes to production using kubectl apply.
    """

    test_case = LLMTestCase(
        input="Deploy the feature",
        actual_output=response_content,
    )

    metric = RoleBoundaryMetric(agent_type="engineer", threshold=0.9)
    # This should fail - engineers shouldn't deploy
    with pytest.raises(AssertionError):
        assert_test(test_case, [metric])
```

### Agent Registry Tests

Tests that validate agent metadata and structure:

- **Required Fields**: name, description, agent_id, agent_type
- **Unique Constraints**: agent_ids must be unique
- **Valid Types**: agent_type from approved list
- **Handoff Validation**: Referenced agents exist
- **Content Quality**: Non-empty body, references BASE-AGENT concepts

```python
# Example: Test required fields present
@pytest.mark.parametrize("field_name", ["name", "description", "agent_id"])
def test_required_fields_present(all_agents, field_name):
    missing = [
        agent for agent in all_agents
        if not getattr(agent, field_name)
    ]
    assert not missing, f"Agents missing {field_name}: {missing}"
```

## Custom Metrics

### InstructionComplianceMetric

Validates responses against extracted BASE-AGENT.md rules using regex patterns.

```python
metric = InstructionComplianceMetric(
    rules=root_base_rules,
    threshold=0.8,  # 80% of rules must pass
    strict_mode=False  # If True, ALL rules must pass
)
```

### GitWorkflowComplianceMetric

Specifically validates git workflow compliance:
- Conventional commit format (feat:, fix:, etc.)
- Explanation of WHY (not just WHAT)
- No bad commit messages (update code, fix bug, etc.)

```python
metric = GitWorkflowComplianceMetric(threshold=0.9)
```

### OutputFormatComplianceMetric

Validates markdown output format:
- Markdown headers (##)
- Code blocks with language tags
- Clear structure (multiple sections)
- Sufficient length (not too terse)
- Lists and bullet points

```python
metric = OutputFormatComplianceMetric(threshold=0.7)
```

### RoleBoundaryMetric

Validates agent stays within role boundaries:
- Has allowed patterns for role
- No forbidden patterns from other roles

```python
metric = RoleBoundaryMetric(
    agent_type="engineer",
    threshold=0.9
)
```

### HandoffComplianceMetric

Validates proper handoff format:
- States what was accomplished
- Lists remaining tasks
- Provides context
- Identifies next agent

```python
metric = HandoffComplianceMetric(threshold=0.8)
```

## Fixtures

### Agent Loading

- `project_root`: Path to project root
- `agents_dir`: Path to agents directory
- `agent_loader`: AgentLoader instance
- `all_agents`: List of all agent definitions
- `engineer_agents`, `qa_agents`, `ops_agents`: Filtered by type

### Instruction Extraction

- `instruction_extractor`: InstructionExtractor instance
- `root_base_rules`: Rules from root BASE-AGENT.md
- `category_rules`: Function to get category-specific rules

### Mock Responses

- `mock_generator`: MockResponseGenerator instance

```python
# Generate compliant response
response = mock_generator.generate_compliant_response(
    agent_type="engineer",
    task_type="implement_feature"
)

# Generate non-compliant response
response = mock_generator.generate_non_compliant_response(
    agent_type="engineer",
    task_type="poor_commit",
    violations=["git_conventional_commits"]
)
```

## CI/CD Integration

Tests run automatically on GitHub Actions:

- **Trigger**: Push/PR to main with changes to agents/, tests/, or pyproject.toml
- **Jobs**:
  - `test`: Run pytest with coverage, validate agents with build-agent.py
  - `lint`: Run ruff on tests/

See `.github/workflows/agent-tests.yml` for configuration.

## Project Structure

```
tests/
├── __init__.py
├── README.md
├── conftest.py                          # Pytest fixtures
├── fixtures/
│   ├── __init__.py
│   ├── agent_loader.py                  # Load agent markdown files
│   ├── instruction_extractor.py         # Extract testable rules
│   └── mock_responses.py                # Generate mock responses
├── metrics/
│   ├── __init__.py
│   ├── instruction_compliance.py        # Instruction compliance metrics
│   └── role_boundary.py                 # Role boundary metrics
├── test_instruction_compliance.py       # Instruction compliance tests
├── test_role_boundaries.py              # Role boundary tests
└── test_agent_registry.py               # Agent registry validation
```

## Extending the Framework

### Add New Testable Rules

Edit `tests/fixtures/instruction_extractor.py`:

```python
def extract_category_rules(self, category: str) -> list[TestableRule]:
    if category == "my_category":
        rules.append(
            TestableRule(
                rule_id="my_custom_rule",
                category="my_category",
                description="My custom validation rule",
                positive_patterns=[r"required_pattern"],
                negative_patterns=[r"forbidden_pattern"],
                source_file=str(category_base),
                severity="error",
            )
        )
    return rules
```

### Add New Mock Responses

Edit `tests/fixtures/mock_responses.py`:

```python
COMPLIANT_TEMPLATES = {
    "my_agent_type": {
        "my_task_type": """
## My Compliant Response

Proper structure and content here.
"""
    }
}
```

### Add New Metrics

Create a new metric by extending `BaseMetric`:

```python
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class MyCustomMetric(BaseMetric):
    @property
    def __name__(self) -> str:
        return "My Custom Metric"

    def measure(self, test_case: LLMTestCase) -> float:
        # Implement validation logic
        self.score = 1.0  # 0.0 to 1.0
        self.success = self.score >= self.threshold
        self.reason = "Explanation of result"
        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return self.success
```

## Best Practices

1. **Use Descriptive Test Names**: Test names should explain what they validate
2. **Parametrize When Possible**: Use `@pytest.mark.parametrize` for similar tests
3. **Skip Gracefully**: Use `pytest.skip()` when data not available
4. **Test Both Positive and Negative**: Test compliant AND non-compliant cases
5. **Keep Fixtures Pure**: Fixtures should not have side effects
6. **Document Metrics**: Explain what each metric validates and why

## Troubleshooting

### Tests Fail with "No agents found"

Ensure agents are in `/Users/masa/Projects/claude-mpm-agents/agents/` and have valid YAML frontmatter.

### DeepEval AssertionError

Check the metric's `reason` attribute for details on why the test failed:

```python
try:
    assert_test(test_case, [metric])
except AssertionError as e:
    print(f"Failure reason: {metric.reason}")
    print(f"Violations: {metric.violations}")
```

### Import Errors

Ensure you've installed test dependencies:

```bash
pip install -e ".[test]"
```

## Agent Validation Tests (Static Analysis)

In addition to DeepEval behavior tests, we have comprehensive static validation tests that check agent structure and metadata.

### New Validation Categories

1. **Domain Pattern Tests** (`test_agent_patterns.py`) - 32 tests
   - Verifies agents contain terminology specific to their domain
   - Example: `python-engineer` should mention `pytest`, `mypy`, `async`
   - Validates testing tool mentions, deployment platforms, quality metrics

2. **Skills Validation Tests** (`test_agent_skills.py`) - 10 tests
   - Ensures all skill references exist in skills registry
   - Validates agents have appropriate skills for their category
   - Checks skill naming conventions and counts

3. **Knowledge & Interactions Tests** (`test_agent_knowledge.py`) - 14 tests
   - Validates knowledge structure (domain_expertise, best_practices)
   - Checks interaction patterns (handoff_agents, collaboration)
   - Ensures knowledge is actionable and specific

### Running Validation Tests

```bash
# Run all validation tests
pytest tests/test_agent_patterns.py tests/test_agent_skills.py tests/test_agent_knowledge.py -v

# Run by category
pytest -m patterns -v      # Domain patterns
pytest -m skills -v        # Skills validation
pytest -m knowledge -v     # Knowledge validation

# Run specific test
pytest tests/test_agent_patterns.py::test_engineer_agents_mention_testing_tools -v
```

### Current Validation Status

**Overall:** 50/56 tests passing (89.3%)

| Category | Tests | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| Domain Patterns | 32 | 30 | 2 | 93.8% |
| Skills | 10 | 9 | 1 | 90.0% |
| Knowledge | 14 | 11 | 3 | 78.6% |

See [VALIDATION_REPORT.md](./VALIDATION_REPORT.md) for detailed failure analysis.

### Test Markers

New markers added to `pyproject.toml`:

- `@pytest.mark.patterns` - Domain pattern tests
- `@pytest.mark.skills` - Skills validation tests
- `@pytest.mark.knowledge` - Knowledge and expertise tests

### Example Validation Test

```python
@pytest.mark.patterns
@pytest.mark.parametrize("agent_id,patterns", AGENT_PATTERNS.items())
def test_agent_has_domain_patterns(compiled_agents, agent_id, patterns):
    """Test each agent contains its expected domain-specific patterns."""
    agent = compiled_agents[agent_id]
    content = agent.compiled_content

    missing = []
    for pattern in patterns:
        if not re.search(pattern, content, re.IGNORECASE):
            missing.append(pattern)

    assert not missing, f"{agent_id} missing patterns: {missing}"
```

## Resources

- [DeepEval Documentation](https://docs.confident-ai.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Project BASE-AGENT.md](../agents/BASE-AGENT.md)
- [Validation Report](./VALIDATION_REPORT.md) - Detailed validation test results
