# Base QA Template

---
template_type: base
category: qa
version: 1.0.0
description: Base template for QA agents with common testing patterns, quality gates, and validation approaches
usage: Reference patterns from specific QA agent templates using extends/inherits/overrides
---

## Purpose

This base template provides common QA and testing patterns shared across all QA agent templates (qa-agent, web-qa, api-qa, test-quality-inspector, etc.). Agent templates inherit these patterns and customize them for specific testing domains.

## Pattern Categories

### Testing Methodology {#testing_methodology}

**Test-Driven Development (TDD)**:
1. **Red**: Write failing test first
2. **Green**: Write minimal code to pass test
3. **Refactor**: Improve code while keeping tests green

**Behavior-Driven Development (BDD)**:
- Given-When-Then structure
- Focus on business requirements
- Executable specifications

**Property-Based Testing**:
- Define invariants (properties) that should always hold
- Generate random test inputs
- Discover edge cases automatically

**Regression Testing**:
- Maintain comprehensive regression suite
- Run on every code change
- Automate in CI/CD pipeline

### Evidence Requirements {#evidence_requirements}

**Test Execution Evidence**:
- Test run logs with timestamps
- Pass/fail status for each test
- Error messages and stack traces for failures
- Test execution duration

**Coverage Evidence**:
- Line coverage percentage
- Branch coverage percentage
- Function/method coverage
- Untested code locations

**Performance Evidence**:
- Response time metrics (p50, p95, p99)
- Throughput measurements (requests/second)
- Resource usage (CPU, memory)
- Load test results

**Visual Evidence** (for UI testing):
- Screenshots of application state
- Screen recordings of test execution
- Visual regression diffs

**Log Evidence**:
- Application logs during test execution
- Error logs with stack traces
- Warning logs for potential issues

### Test Coverage Expectations {#test_coverage_expectations}

**Coverage Thresholds**:
- **Minimum**: 80% line coverage for new code
- **Target**: 90%+ coverage for critical paths
- **Critical Components**: 95%+ coverage (auth, payments, data processing)

**Coverage Analysis**:
- Analyze coverage metrics from tool reports (not manual file reads)
- Identify untested branches and edge cases
- Prioritize testing based on risk and complexity

**Coverage Reporting**:
```bash
# Example: pytest coverage report
pytest --cov=src --cov-report=html --cov-fail-under=90

# Example: JavaScript coverage with Istanbul
npx jest --coverage --coverageThreshold='{"global":{"lines":90}}'
```

**What Coverage Doesn't Measure**:
- Test quality (coverage ≠ good tests)
- Edge case handling
- Business logic correctness
- User experience quality

### Quality Gates {#quality_gates}

**Pre-Merge Quality Gates**:
- [ ] All tests passing (0 failures)
- [ ] Code coverage ≥ threshold (e.g., 90%)
- [ ] No critical security vulnerabilities
- [ ] No high-severity linting errors
- [ ] Performance benchmarks within acceptable range

**Continuous Quality Gates**:
- [ ] Automated tests run on every commit
- [ ] Static analysis passes (no type errors)
- [ ] Security scanning passes (no critical issues)
- [ ] Code review approved by human reviewer

**Release Quality Gates**:
- [ ] All regression tests passing
- [ ] Performance tests within SLA
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Rollback procedure tested

### Verification Templates {#verification_templates}

**Functional Verification**:
```
Test: User Authentication
Given: Valid user credentials
When: User submits login form
Then: User is authenticated and redirected to dashboard

Evidence:
- Test log showing successful authentication
- Screenshot of dashboard after login
- Session token created in database
```

**Performance Verification**:
```
Test: API Endpoint Performance
Given: API endpoint /api/users
When: 1000 concurrent requests sent
Then: p95 response time < 200ms

Evidence:
- Load test results showing p95 = 180ms
- CPU usage graph during test
- No errors in application logs
```

**Security Verification**:
```
Test: SQL Injection Protection
Given: Login form with SQL injection attempt
When: User submits "admin' OR '1'='1" as username
Then: Login fails with validation error

Evidence:
- Test log showing validation error
- Database logs showing no malicious queries
- No authentication granted
```

### Test Strategies {#test_strategies}

**Unit Testing Strategy**:
- Test individual functions/methods in isolation
- Mock external dependencies
- Fast execution (< 1 second per test)
- No I/O operations (no network, no database)

**Integration Testing Strategy**:
- Test component interactions
- Use test databases/services
- Verify data flows correctly
- Test error propagation

**End-to-End Testing Strategy**:
- Test complete user workflows
- Use real or realistic environment
- Cover critical user journeys
- Minimize flakiness with proper waits

**Performance Testing Strategy**:
- Baseline performance metrics
- Load testing under expected traffic
- Stress testing under peak traffic
- Identify breaking points

### Test Organization {#test_organization}

**Test Structure**:
```
tests/
├── unit/              # Fast, isolated unit tests
├── integration/       # Component interaction tests
├── e2e/              # End-to-end user workflow tests
├── performance/      # Load and performance tests
├── fixtures/         # Test data and mock objects
└── conftest.py       # Shared test configuration
```

**Test Naming Conventions**:
- Descriptive names: `test_user_login_with_valid_credentials()`
- Avoid generic names: `test_login()`, `test_1()`
- Use naming pattern: `test_<function>_<scenario>_<expected_result>`

**Test File Organization**:
- Mirror source code structure
- One test file per source file
- Group related tests in classes/describe blocks

### Bug Reporting {#bug_reporting}

**Bug Report Template**:
```markdown
## Bug Description
[Clear, concise description of the issue]

## Steps to Reproduce
1. Navigate to /users page
2. Click "Add User" button
3. Submit form with empty name field

## Expected Behavior
Form validation error should appear

## Actual Behavior
Application crashes with 500 error

## Evidence
- Screenshot: [attach]
- Error logs: [paste]
- Browser console: [paste]

## Environment
- OS: macOS 14.1
- Browser: Chrome 120.0.0
- App Version: 2.3.1

## Severity
Critical (application crash)

## Priority
High (blocking user workflow)
```

**Bug Severity Levels**:
- **Critical**: Application crash, data loss, security vulnerability
- **High**: Major functionality broken, no workaround
- **Medium**: Functionality impaired, workaround exists
- **Low**: Minor issue, cosmetic problem

### Test Automation {#test_automation}

**Automation Principles**:
- Automate repetitive tests
- Prioritize high-value, stable tests
- Maintain test code like production code
- Keep tests deterministic (no flakiness)

**Test Selection for Automation**:
- ✅ Regression tests (run frequently)
- ✅ Smoke tests (critical paths)
- ✅ Integration tests (component boundaries)
- ❌ Exploratory testing (manual)
- ❌ Usability testing (manual)

**CI/CD Integration**:
```yaml
# Example: GitHub Actions test workflow
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Test Data Management {#test_data_management}

**Test Data Strategies**:
- **Fixtures**: Predefined test data loaded before tests
- **Factories**: Generate test data programmatically
- **Seeders**: Populate test databases with sample data
- **Mocks**: Fake external API responses

**Test Data Best Practices**:
- Keep test data minimal (only what's needed)
- Use realistic data (representative of production)
- Isolate test data (no shared state between tests)
- Clean up test data after tests

**Example**:
```python
# Factory pattern for test data
class UserFactory:
    @staticmethod
    def create(username="testuser", email="test@example.com"):
        return User(
            username=username,
            email=email,
            password_hash=hash_password("test_password")
        )

# Usage in tests
def test_user_creation():
    user = UserFactory.create(username="alice")
    assert user.username == "alice"
```

### Memory-Efficient Testing {#memory_efficient_testing}

**Strategic Sampling**:
- Sample 5-10 representative test files (not all)
- Use grep for test discovery instead of reading files
- Process test files sequentially (not parallel)
- Skip large test files (>500KB) unless critical

**Metric Extraction**:
- Extract metrics from tool outputs (coverage reports)
- Don't read source files to calculate coverage manually
- Use test framework reporting features

**Test Process Management**:
- Check test configuration before running (avoid watch mode)
- Use CI-safe flags: `CI=true npm test` or `pytest --no-watch`
- Verify test process termination after execution
- Clean up orphaned processes: `pkill -f "vitest" || pkill -f "jest"`

## Anti-Patterns {#anti_patterns}

### Flaky Tests

```python
# ❌ WRONG - Time-dependent test
def test_cache_expiry():
    cache.set("key", "value", ttl=1)
    time.sleep(1)  # Flaky! May fail if sleep isn't exact
    assert cache.get("key") is None

# ✅ CORRECT - Mock time
def test_cache_expiry(mock_time):
    cache.set("key", "value", ttl=1)
    mock_time.advance(seconds=1)
    assert cache.get("key") is None
```

### Shared State Between Tests

```python
# ❌ WRONG - Shared state
class TestUserService:
    user = None  # Shared across tests

    def test_create_user(self):
        self.user = create_user("alice")

    def test_delete_user(self):
        delete_user(self.user)  # Depends on previous test!

# ✅ CORRECT - Isolated tests
class TestUserService:
    def test_create_user(self):
        user = create_user("alice")
        assert user.username == "alice"

    def test_delete_user(self):
        user = create_user("bob")  # Own test data
        delete_user(user)
        assert get_user(user.id) is None
```

### Testing Implementation Details

```python
# ❌ WRONG - Testing internal implementation
def test_user_service():
    service = UserService()
    assert service._internal_cache == {}  # Testing private details

# ✅ CORRECT - Testing public behavior
def test_user_service():
    service = UserService()
    user = service.get_user(123)
    assert user.username == "expected_name"
```

## Memory Routing {#memory_routing}

**Memory Categories**:
- **Testing Strategies**: Test approaches and coverage requirements
- **Quality Standards**: Acceptance criteria and quality gates
- **Bug Patterns**: Common defects and regression risks
- **Test Infrastructure**: Testing tools and framework configurations

**Keywords**:
- test, testing, quality, bug, defect, validation, verification
- coverage, automation, regression, acceptance, criteria, metrics
- pytest, jest, junit, selenium, playwright, cypress
- unit test, integration test, e2e, performance test

**File Paths**:
- Test directories: `tests/`, `spec/`, `__tests__/`, `test/`
- Test configuration: `pytest.ini`, `jest.config.js`, `vitest.config.ts`
- Coverage reports: `.coverage`, `coverage/`, `htmlcov/`

## Extension Points

QA agent templates can extend this base with:
- **Domain-Specific Testing**: Web UI testing, API testing, mobile testing
- **Framework-Specific Patterns**: Pytest fixtures, Jest mocks, Playwright locators
- **Tool Integration**: Selenium, Playwright, Cypress, Appium
- **Specialized Testing**: Accessibility testing, security testing, performance testing

## Versioning

**Current Version**: 1.0.0

**Changelog**:
- **1.0.0** (2025-11-30): Initial base QA template with core patterns extracted from qa-agent and web-qa templates

---

**Maintainer**: Claude MPM Team
**Last Updated**: 2025-11-30
**Status**: ✅ Active
