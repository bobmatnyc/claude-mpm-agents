# Base Engineering Template

---
template_type: base
category: engineer
version: 1.0.0
description: Base template for engineering agents with common patterns for code quality, testing, and architecture
usage: Reference patterns from specific agent templates using extends/inherits/overrides
---

## Purpose

This base template provides common engineering patterns shared across all engineering agent templates (Python, TypeScript, Rust, Go, Java, etc.). Agent templates inherit these patterns and customize them for language-specific implementations.

## Pattern Categories

### Code Quality Principles {#code_quality_principles}

**DRY (Don't Repeat Yourself)**:
- Extract common code into reusable functions/classes
- Identify code duplication across 2+ locations
- Create shared utilities for repeated patterns
- Use inheritance or composition for similar implementations

**SOLID Principles**:
- **Single Responsibility**: Each function/class has ONE clear purpose
- **Open/Closed**: Extend through interfaces, not modifications
- **Liskov Substitution**: Derived classes must be substitutable for base classes
- **Interface Segregation**: Many specific interfaces over general ones
- **Dependency Inversion**: Depend on abstractions, not implementations

**Type Safety**:
- Use static type checking (mypy, TypeScript strict, Rust compiler)
- 100% type coverage for production code
- No escape hatches (`Any`, `unknown`) without justification
- Runtime validation at system boundaries (Pydantic, Zod, serde)

**Code Organization**:
- **File Size Limits**:
  - 600+ lines: Create refactoring plan
  - 800+ lines: MUST split into modules
  - Maximum single file: 800 lines
- **Function Complexity**: Max cyclomatic complexity of 10
- **Module Cohesion**: Related functions grouped together
- **Clear Naming**: Descriptive names, avoid abbreviations

### Error Handling Standards {#error_handling_standards}

**Exception Hierarchy**:
- Create domain-specific exception classes
- Use specific exceptions, not generic `Exception`
- Exceptions should describe the error clearly

**Error Handling Patterns**:
```
# ❌ WRONG - Bare except
try:
    risky_operation()
except:
    pass

# ✅ CORRECT - Specific exceptions
try:
    risky_operation()
except (ValueError, KeyError) as e:
    logger.exception("Operation failed: %s", e)
    raise OperationError("Failed to process") from e
```

**Logging Requirements**:
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Include context in error messages
- Propagate exceptions when appropriate
- Never silently swallow errors

**Failure Modes**:
- Document all error conditions in docstrings
- Explain recovery strategies
- Define data consistency guarantees during failures

### Testing Approach {#testing_approach}

**Testing Levels**:
- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Property-Based Tests**: Test invariants across input space

**Coverage Requirements**:
- **Minimum**: 80% code coverage for new code
- **Target**: 90%+ coverage for critical paths
- **Critical Components**: 95%+ coverage

**Test Organization**:
- Mirror source code structure in test directory
- One test file per source file
- Group related tests in classes/modules
- Use descriptive test names

**Test Patterns**:
```
# Good test structure
def test_user_authentication_with_valid_credentials():
    # Arrange
    user = create_test_user()
    credentials = {"username": user.username, "password": "correct"}

    # Act
    result = authenticate(credentials)

    # Assert
    assert result.success
    assert result.user_id == user.id
```

**Mock Testing**:
- Mock external dependencies (APIs, databases)
- Use dependency injection to enable mocking
- Verify mock behavior with assertions
- Reset mocks between tests

### Documentation Requirements {#documentation_requirements}

**Code Documentation**:
- **Public APIs**: MUST have docstrings (Google/NumPy/JSDoc style)
- **Functions**: Document parameters, return values, exceptions
- **Classes**: Document purpose, attributes, methods
- **Modules**: Document module purpose and contents

**Design Documentation**:
- Document architectural decisions (ADRs)
- Explain WHY decisions were made, not just WHAT
- List alternatives considered and why rejected
- Document trade-offs (performance vs. maintainability)

**API Documentation**:
- OpenAPI/Swagger for REST APIs
- Type definitions for all endpoints
- Example requests and responses
- Error codes and meanings

**Example Documentation**:
```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price.

    Design Decision: Use percentage (0-100) rather than decimal (0-1)
    to match business team terminology and reduce conversion errors.

    Args:
        price: Original price in USD (must be positive)
        discount_percent: Discount percentage (0-100, inclusive)

    Returns:
        Final price after discount applied

    Raises:
        ValueError: If price is negative or discount not in 0-100 range

    Examples:
        >>> calculate_discount(100.0, 10.0)
        90.0
        >>> calculate_discount(50.0, 25.0)
        37.5
    """
```

### Performance Considerations {#performance_considerations}

**Profiling Before Optimization**:
- **NEVER** optimize without profiling data
- Use language-specific profilers (cProfile, perf, Instruments)
- Identify actual bottlenecks, not assumed ones
- Benchmark improvements to verify gains

**Complexity Analysis**:
- **Time Complexity**: Document Big-O for algorithms
- **Space Complexity**: Document memory usage
- **Trade-offs**: Explain speed vs. memory decisions

**Optimization Priorities**:
1. **Correctness**: Code must work correctly first
2. **Profiling**: Measure to identify bottlenecks
3. **Algorithm**: Choose optimal algorithm complexity
4. **Data Structures**: Use appropriate structures (hash maps, trees)
5. **Micro-optimizations**: Only after profiling proves necessity

**Common Optimizations**:
- Use hash maps for O(1) lookups (avoid O(n) scans)
- Use appropriate data structures (deque for queues, heaps for priority)
- Cache expensive computations
- Lazy evaluation for large datasets
- Async/parallel processing for I/O operations

### Memory Management {#memory_management}

**Resource Cleanup**:
- Use context managers (RAII, `with`, `using`, `defer`)
- Close files, connections, and resources explicitly
- Implement cleanup in `finally` blocks or destructors

**Memory Patterns**:
- Process large files in chunks (streaming)
- Use generators for lazy evaluation
- Clear temporary variables after use
- Avoid holding references to large objects

**Example**:
```python
# ✅ CORRECT - Stream processing
def process_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:  # Processes one line at a time
            process_line(line)

# ❌ WRONG - Loads entire file into memory
def process_large_file_bad(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()  # All lines in memory
        for line in lines:
            process_line(line)
```

### Version Control Patterns {#version_control_patterns}

**Commit Best Practices**:
- Review file history before modifications: `git log --oneline -5 <file_path>`
- Write succinct commit messages explaining WHAT changed and WHY
- Follow conventional commits format: `feat/fix/docs/refactor/perf/test/chore`
- Keep commits atomic (one logical change per commit)

**Commit Message Structure**:
```
type(scope): short description

- Detailed change 1
- Detailed change 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Conventional Commit Types**:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation only
- `refactor:` Code restructuring (no behavior change)
- `perf:` Performance improvements
- `test:` Adding or updating tests
- `chore:` Maintenance (dependencies, tooling)

### Code Review Standards {#code_review_standards}

**Review Checklist**:
- [ ] Code follows project style guide
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No hardcoded secrets or credentials
- [ ] Error handling comprehensive
- [ ] Performance acceptable (profiled if critical)
- [ ] No unnecessary dependencies added

**Review Focus Areas**:
- **Logic Correctness**: Does code do what it claims?
- **Edge Cases**: Are boundary conditions handled?
- **Error Paths**: Are failures handled gracefully?
- **Testing**: Are tests thorough and meaningful?
- **Readability**: Is code self-documenting?
- **Maintainability**: Can future developers understand this?

### Security Patterns {#security_patterns}

**Input Validation**:
- Validate all user inputs
- Sanitize data before storage/display
- Use parameterized queries (prevent SQL injection)
- Escape output based on context (HTML, JavaScript, SQL)

**Authentication & Authorization**:
- Never store plaintext passwords
- Use established crypto libraries (don't roll your own)
- Implement principle of least privilege
- Validate permissions on every request

**Secret Management**:
- **NEVER** commit secrets to version control
- Use environment variables or secret management services
- Rotate credentials regularly
- Audit secret access

**Common Vulnerabilities**:
- SQL Injection: Use parameterized queries
- XSS: Escape output based on context
- CSRF: Use CSRF tokens
- Path Traversal: Validate and sanitize file paths
- Command Injection: Avoid shell=True, validate inputs

## Anti-Patterns {#anti_patterns}

### Global State

```python
# ❌ WRONG - Global mutable state
CONNECTION = None

def get_data():
    global CONNECTION
    if not CONNECTION:
        CONNECTION = create_connection()
    return CONNECTION.query()

# ✅ CORRECT - Dependency injection
class DatabaseService:
    def __init__(self, connection_pool):
        self._pool = connection_pool

    async def get_data(self):
        async with self._pool.acquire() as conn:
            return await conn.query()
```

### Mutable Default Arguments

```python
# ❌ WRONG - Mutable default
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ CORRECT - None with explicit initialization
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Premature Optimization

```python
# ❌ WRONG - Optimized before profiling
def process_data(data):
    # Complex, hard-to-read optimizations
    return [x for x in data if x > 0]  # List comprehension "for speed"

# ✅ CORRECT - Clear, then optimize if needed
def process_data(data):
    # Clear implementation first
    positive_values = []
    for value in data:
        if value > 0:
            positive_values.append(value)
    return positive_values
    # Optimize ONLY after profiling shows this is slow
```

## Memory Routing {#memory_routing}

**Memory Categories**:
- **Implementation Patterns**: Reusable code structures and designs
- **Architecture Decisions**: System design choices and trade-offs
- **Performance Solutions**: Optimization techniques and bottleneck fixes
- **Testing Strategies**: Test patterns and coverage approaches
- **Technology Choices**: Library/framework selections and rationale

**Keywords**:
- implementation, code, programming, function, method, class, module
- refactor, optimize, performance, algorithm, design pattern, architecture
- testing, test coverage, unit test, integration test
- dependency injection, SOLID, clean architecture, DRY
- git, commit, version control, code review

**File Paths**:
- Source code directories: `src/`, `lib/`, `app/`
- Test directories: `tests/`, `spec/`, `__tests__/`
- Configuration files: `.eslintrc`, `tsconfig.json`, `pyproject.toml`

## Extension Points

Agent templates can extend this base with:
- **Language-Specific Patterns**: Python async, TypeScript generics, Rust lifetimes
- **Framework Patterns**: React hooks, FastAPI dependencies, Spring DI
- **Tooling**: Language-specific linters, formatters, test runners
- **Build Systems**: npm, cargo, go modules, Maven
- **Deployment**: Docker, serverless, platform-specific optimizations

## Versioning

**Current Version**: 1.0.0

**Changelog**:
- **1.0.0** (2025-11-30): Initial base engineering template with core patterns extracted from python-engineer, typescript-engineer, and engineer agents

---

**Maintainer**: Claude MPM Team
**Last Updated**: 2025-11-30
**Status**: ✅ Active
