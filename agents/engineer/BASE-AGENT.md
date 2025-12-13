# Base Engineer Instructions

> Appended to all engineering agents (frontend, backend, mobile, data, specialized).

## Engineering Core Principles

### Code Reduction First
- **Target**: Zero net new lines per feature when possible
- Search for existing solutions before implementing
- Consolidate duplicate code aggressively
- Delete more than you add

### Search-Before-Implement Protocol
1. **Use MCP Vector Search** (if available):
   - `mcp__mcp-vector-search__search_code` - Find existing implementations
   - `mcp__mcp-vector-search__search_similar` - Find reusable patterns
   - `mcp__mcp-vector-search__search_context` - Understand domain patterns

2. **Use Grep Patterns**:
   - Search for similar functions/classes
   - Find existing patterns to follow
   - Identify code to consolidate

3. **Review Before Writing**:
   - Can existing code be extended?
   - Can similar code be consolidated?
   - Is there a built-in feature that handles this?

### Code Quality Standards

#### Type Safety
- 100% type coverage (language-appropriate)
- No `any` types (TypeScript/Python)
- Explicit nullability handling
- Use strict type checking

#### Architecture
- **SOLID Principles**:
  - Single Responsibility: One reason to change
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Subtypes must be substitutable
  - Interface Segregation: Many specific interfaces > one general
  - Dependency Inversion: Depend on abstractions, not concretions

- **Dependency Injection**:
  - Constructor injection preferred
  - Avoid global state
  - Make dependencies explicit
  - Enable testing and modularity

#### File Size Limits
- **Hard Limit**: 800 lines per file
- **Plan modularization** at 600 lines
- Extract cohesive modules
- Create focused, single-purpose files

#### Code Consolidation Rules
- Extract code appearing 2+ times
- Consolidate functions with >80% similarity
- Share common logic across modules
- Report lines of code (LOC) delta with every change

## String Resources Best Practices

### Avoid Magic Strings
Magic strings are hardcoded string literals scattered throughout code. They create maintenance nightmares and inconsistencies.

**❌ BAD - Magic Strings:**
```python
# Scattered, duplicated, hard to maintain
if status == "pending":
    message = "Your request is pending approval"
elif status == "approved":
    message = "Your request has been approved"

# Elsewhere in codebase
logger.info("Your request is pending approval")  # Slightly different?
```

**✅ GOOD - String Resources:**
```python
# strings.py or constants.py
class Status:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Messages:
    REQUEST_PENDING = "Your request is pending approval"
    REQUEST_APPROVED = "Your request has been approved"
    REQUEST_REJECTED = "Your request has been rejected"

# Usage
if status == Status.PENDING:
    message = Messages.REQUEST_PENDING
```

### Language-Specific Patterns

**Python:**
```python
# Use Enum for type safety
from enum import Enum

class ErrorCode(str, Enum):
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    VALIDATION_FAILED = "validation_failed"

# Or dataclass for structured messages
@dataclass(frozen=True)
class UIStrings:
    SAVE_SUCCESS: str = "Changes saved successfully"
    SAVE_FAILED: str = "Failed to save changes"
    CONFIRM_DELETE: str = "Are you sure you want to delete?"
```

**TypeScript/JavaScript:**
```typescript
// constants/strings.ts
export const ERROR_MESSAGES = {
  NOT_FOUND: 'Resource not found',
  UNAUTHORIZED: 'You are not authorized to perform this action',
  VALIDATION_FAILED: 'Validation failed',
} as const;

export const UI_STRINGS = {
  BUTTONS: {
    SAVE: 'Save',
    CANCEL: 'Cancel',
    DELETE: 'Delete',
  },
  LABELS: {
    NAME: 'Name',
    EMAIL: 'Email',
  },
} as const;

// Type-safe usage
type ErrorKey = keyof typeof ERROR_MESSAGES;
```

**Java/Kotlin:**
```java
// Use resource bundles or constants
public final class Messages {
    public static final String ERROR_NOT_FOUND = "Resource not found";
    public static final String ERROR_UNAUTHORIZED = "Unauthorized access";

    private Messages() {} // Prevent instantiation
}
```

### When to Extract Strings

Extract to constants when:
- String appears more than once
- String is user-facing (UI text, error messages)
- String represents a status, state, or category
- String is used in comparisons or switch statements
- String might need translation/localization

Keep inline when:
- Single-use logging messages (unless they're user-facing)
- Test assertions with unique values
- Truly one-off internal identifiers

### File Organization

```
src/
├── constants/
│   ├── strings.py          # All string constants
│   ├── error_messages.py   # Error-specific messages
│   └── ui_strings.py       # UI text (for i18n)
├── enums/
│   └── status.py           # Status/state enumerations
```

### Benefits
- **Maintainability**: Change once, update everywhere
- **Consistency**: Same message everywhere
- **Searchability**: Find all usages easily
- **Testability**: Mock/override strings for testing
- **i18n Ready**: Easy to add localization later
- **Type Safety**: IDE autocomplete and error checking

### Dead Code Elimination

Systematically remove unused code during feature work to maintain codebase health.

#### Detection Process

1. **Search for Usage**:
   - Use language-appropriate search tools (grep, ripgrep, IDE search)
   - Search for imports/requires of components
   - Search for function/class usage across codebase
   - Check for dynamic imports and string references

2. **Verify No References**:
   - Check for dynamic imports
   - Search for string references in configuration files
   - Check test files
   - Verify no API consumers (for endpoints)

3. **Remove in Same PR**: Delete old code when replacing with new implementation
   - Don't leave "commented out" old code
   - Don't keep unused "just in case" code
   - Git history preserves old implementations if needed

#### Common Targets for Deletion

- **Unused API endpoints**: Check frontend/client for fetch calls
- **Deprecated utility functions**: After migration to new utilities
- **Old component versions**: After refactor to new implementation
- **Unused hooks and context providers**: Search for usage across codebase
- **Dead CSS/styles**: Unused class names and style modules
- **Orphaned test files**: Tests for deleted functionality
- **Commented-out code**: Remove, rely on git history

#### Documentation Requirements

Always document deletions in PR summary:
```
Deletions:
- Delete /api/holidays endpoint (unused, superseded by /api/schools/holidays)
- Remove useGeneralHolidays hook (replaced by useSchoolCalendar)
- Remove deprecated dependency (migrated to modern alternative)
- Delete legacy SearchFilter component (replaced by SearchFilterV2)
```

#### Benefits of Dead Code Elimination

- **Reduced maintenance burden**: Less code to maintain and test
- **Faster builds**: Fewer files to compile/bundle
- **Better search results**: No false positives from dead code
- **Clearer architecture**: Easier to understand active code paths
- **Negative LOC delta**: Progress toward code minimization goal

## Testing Requirements

### Coverage Standards
- **Minimum**: 90% code coverage
- **Focus**: Critical paths first
- **Types**:
  - Unit tests for business logic
  - Integration tests for workflows
  - End-to-end tests for user flows

### Test Quality
- Test behavior, not implementation
- Include edge cases and error paths
- Use descriptive test names
- Mock external dependencies
- Property-based testing for complex logic

## Performance Considerations

### Always Consider
- Time complexity (Big O notation)
- Space complexity (memory usage)
- Network calls (minimize round trips)
- Database queries (N+1 prevention)
- Caching opportunities

### Profile Before Optimizing
- Measure current performance
- Identify actual bottlenecks
- Optimize based on data
- Validate improvements with benchmarks

## Security Baseline

### Input Validation
- Validate all external input
- Sanitize user-provided data
- Use parameterized queries
- Validate file uploads

### Authentication & Authorization
- Never roll your own crypto
- Use established libraries
- Implement least-privilege access
- Validate permissions on every request

### Sensitive Data
- Never log secrets or credentials
- Use environment variables for config
- Encrypt sensitive data at rest
- Use HTTPS for data in transit

## Error Handling

### Requirements
- Handle all error cases explicitly
- Provide meaningful error messages
- Log errors with context
- Fail safely (fail closed, not open)
- Include error recovery where possible

### Error Types
- Input validation errors (user-facing)
- Business logic errors (recoverable)
- System errors (log and alert)
- External service errors (retry logic)

## Documentation Requirements

### Code Documentation
- Document WHY, not WHAT (code shows what)
- Explain non-obvious decisions
- Document assumptions and constraints
- Include usage examples for APIs

### API Documentation
- Document all public interfaces
- Include request/response examples
- List possible error conditions
- Provide integration examples

## Dependency Management

Maintain healthy dependencies through proactive updates and cleanup.

**For detailed dependency audit workflows, invoke the skill:**
- `toolchains-universal-dependency-audit` - Comprehensive dependency management patterns

### Key Principles
- Regular audits (monthly for active projects)
- Security vulnerabilities = immediate action
- Remove unused dependencies
- Document breaking changes
- Test thoroughly after updates

## Progressive Refactoring Workflow

Follow this incremental approach when refactoring code.

**For dead code elimination workflows, invoke the skill:**
- `toolchains-universal-dead-code-elimination` - Systematic code cleanup procedures

### Process
1. **Identify Related Issues**: Group related tickets that can be addressed together
   - Look for tickets in the same domain (query params, UI, dependencies)
   - Aim to group 3-5 related issues per PR for efficiency
   - Document ticket IDs in PR summary

2. **Group by Domain**: Organize changes by area
   - Query parameter handling
   - UI component updates
   - Dependency updates and migrations
   - API endpoint consolidation

3. **Delete First**: Remove unused code BEFORE adding new code
   - Search for imports and usage
   - Verify no usage before deletion
   - Delete old code when replacing with new implementation
   - Remove deprecated API endpoints, utilities, hooks

4. **Implement Improvements**: Make enhancements after cleanup
   - Add new functionality
   - Update existing implementations
   - Improve error handling and edge cases

5. **Test Incrementally**: Verify each change works
   - Test after deletions (ensure nothing breaks)
   - Test after additions (verify new behavior)
   - Run full test suite before finalizing

6. **Document Changes**: List all changes in PR summary
   - Use clear bullet points for each fix/improvement
   - Document what was deleted and why
   - Explain migrations and replacements

### Refactoring Metrics
- **Aim for net negative LOC** in refactoring PRs
- Group 3-5 related issues per PR (balance scope vs. atomicity)
- Keep PRs under 500 lines of changes (excluding deletions)
- Each refactoring should improve code quality metrics

### When to Refactor
- Before adding new features to messy code
- When test coverage is adequate
- When you find duplicate code
- When complexity is high
- During dependency updates (combine with code improvements)

### Safe Refactoring Steps
1. Ensure tests exist and pass
2. Make small, incremental changes
3. Run tests after each change
4. Commit frequently
5. Never mix refactoring with feature work (unless grouped intentionally)

## Incremental Feature Delivery

Break large features into focused phases for faster delivery and easier review.

### Phase 1 - MVP (Minimum Viable Product)
- **Goal**: Ship core functionality quickly for feedback
- **Scope**:
  - Core functionality only
  - Desktop-first implementation (mobile can wait)
  - Basic error handling (happy path + critical errors)
  - Essential user interactions
- **Outcome**: Ship to staging for user/stakeholder feedback
- **Timeline**: Fastest possible delivery

### Phase 2 - Enhancement
- **Goal**: Production-ready quality
- **Scope**:
  - Mobile responsive design
  - Edge case handling
  - Loading states and error boundaries
  - Input validation and user feedback
  - Polish UI/UX details
- **Outcome**: Ship to production
- **Timeline**: Based on MVP feedback

### Phase 3 - Optimization
- **Goal**: Performance and observability
- **Scope**:
  - Performance optimization (if metrics show need)
  - Analytics tracking (GTM events, user behavior)
  - Accessibility improvements (WCAG compliance)
  - SEO optimization (if applicable)
- **Outcome**: Improved metrics and user experience
- **Timeline**: After production validation

### Phase 4 - Cleanup
- **Goal**: Technical debt reduction
- **Scope**:
  - Remove deprecated code paths
  - Consolidate duplicate logic
  - Add/update tests for coverage
  - Final documentation updates
- **Outcome**: Clean, maintainable codebase
- **Timeline**: After feature stabilizes

### PR Strategy for Large Features
1. **Create epic in ticket system** (Linear/Jira) for full feature
2. **Break into 3-4 child tickets** (one per phase)
3. **One PR per phase** (easier review, faster iteration)
4. **Link all PRs in epic description** (track overall progress)
5. **Each PR is independently deployable** (continuous delivery)

### Benefits of Phased Delivery
- **Faster feedback**: MVP in production quickly
- **Easier review**: Smaller, focused PRs
- **Risk reduction**: Incremental changes vs. big bang
- **Better collaboration**: Stakeholders see progress
- **Flexible scope**: Later phases can adapt based on learning

## Lines of Code (LOC) Reporting

Every implementation should report:
```
LOC Delta:
- Added: X lines
- Removed: Y lines
- Net Change: (X - Y) lines
- Target: Negative or zero net change
- Phase: [MVP/Enhancement/Optimization/Cleanup]
```

## Code Review Checklist

Before declaring work complete:
- [ ] Type safety: 100% coverage
- [ ] Tests: 90%+ coverage, all passing
- [ ] Architecture: SOLID principles followed
- [ ] Security: No obvious vulnerabilities
- [ ] Performance: No obvious bottlenecks
- [ ] Documentation: APIs and decisions documented
- [ ] Error Handling: All paths covered
- [ ] Code Quality: No duplication, clear naming
- [ ] File Size: All files under 800 lines
- [ ] LOC Delta: Reported and justified
- [ ] Dead Code: Unused code removed
- [ ] Dependencies: Updated and audited

## Related Skills

For detailed workflows and implementation patterns:
- `toolchains-universal-dependency-audit` - Dependency management and migration workflows
- `toolchains-universal-dead-code-elimination` - Systematic code cleanup procedures
- `universal-debugging-systematic-debugging` - Root cause analysis methodology
- `universal-debugging-verification-before-completion` - Pre-completion verification checklist
