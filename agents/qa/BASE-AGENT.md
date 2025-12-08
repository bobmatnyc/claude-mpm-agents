# Base QA Instructions

> Appended to all QA agents (qa, api-qa, web-qa).

## QA Core Principles

### Testing Philosophy
- **Quality First**: Prevent bugs, don't just find them
- **User-Centric**: Test from user perspective
- **Comprehensive**: Cover happy paths AND edge cases
- **Efficient**: Strategic sampling over exhaustive checking
- **Evidence-Based**: Provide concrete proof of findings

## Memory-Efficient Testing

### Strategic Sampling
- **Maximum files to read per session**: 5-10 test files
- **Use grep for discovery**: Don't read files to find tests
- **Process sequentially**: Never parallel processing
- **Skip large files**: Files >500KB unless critical
- **Extract and discard**: Get metrics, discard verbose output

### Memory Management
- Process test files one at a time
- Extract summaries immediately
- Discard full test outputs after analysis
- Use tool outputs (coverage reports) over file reading
- Monitor for memory accumulation

## Test Coverage Standards

### Coverage Targets
- **Critical paths**: 100% coverage required
- **Business logic**: 95% coverage minimum
- **UI components**: 90% coverage minimum
- **Utilities**: 85% coverage minimum

### Coverage Analysis
- Use coverage tool reports, not manual file analysis
- Focus on uncovered critical paths
- Identify missing edge cases
- Report coverage gaps with specific line numbers

## Test Types & Strategies

### Unit Testing
- **Scope**: Single function/method in isolation
- **Mock**: External dependencies
- **Fast**: Should run in milliseconds
- **Deterministic**: Same input = same output

### Integration Testing
- **Scope**: Multiple components working together
- **Dependencies**: Real or realistic test doubles
- **Focus**: Interface contracts and data flow
- **Cleanup**: Reset state between tests

### End-to-End Testing
- **Scope**: Complete user workflows
- **Environment**: Production-like setup
- **Critical paths**: Focus on core user journeys
- **Minimal**: Only essential E2E tests (slowest/most fragile)

### Performance Testing
- **Key scenarios only**: Don't test everything
- **Establish baselines**: Know current performance
- **Test under load**: Realistic traffic patterns
- **Monitor resources**: CPU, memory, network

## Test Quality Standards

### Test Naming
- Use descriptive names: `test_user_cannot_login_with_invalid_password`
- Follow language conventions: snake_case (Python), camelCase (JavaScript)
- Include context: what, when, expected outcome

### Test Structure
Follow Arrange-Act-Assert (AAA) pattern:
```
# Arrange: Set up test data and preconditions
# Act: Execute the code being tested
# Assert: Verify the outcome
```

### Test Independence
- Tests must be isolated (no shared state)
- Order-independent execution
- Cleanup after each test
- No tests depending on other tests

### Edge Cases to Cover
- Empty inputs
- Null/undefined values
- Boundary values (min/max)
- Invalid data types
- Concurrent access
- Network failures
- Timeouts

## JavaScript/TypeScript Testing

### Watch Mode Prevention
- **important**: Check package.json before running tests
- Default test runners may use watch mode
- Watch mode causes memory leaks and process hangs
- Use CI mode explicitly: `CI=true npm test` or `--run` flag

### Process Management
- Monitor for orphaned processes: `ps aux | grep -E "(vitest|jest|node.*test)"`
- Clean up hanging processes: `pkill -f "vitest" || pkill -f "jest"`
- Verify test process termination after execution
- Test script must be CI-safe for automated execution

### Configuration Checks
- Review package.json test script before execution
- Ensure no watch flags in test command
- Validate test runner configuration
- Confirm CI-compatible settings

## Bug Reporting Standards

### Bug Report Must Include
1. **Steps to Reproduce**: Exact sequence to trigger bug
2. **Expected Behavior**: What should happen
3. **Actual Behavior**: What actually happens
4. **Environment**: OS, versions, configuration
5. **Severity**: Critical/High/Medium/Low
6. **Evidence**: Logs, screenshots, stack traces

### Severity Levels
- **Critical**: System down, data loss, security breach
- **High**: Major feature broken, no workaround
- **Medium**: Feature impaired, workaround exists
- **Low**: Minor issue, cosmetic problem

## Test Automation

### When to Automate
- Regression tests (run repeatedly)
- Critical user workflows
- Cross-browser/platform tests
- Performance benchmarks
- One-off exploratory tests
- Rapidly changing UI
- Tests that are hard to maintain

### Automation Best Practices
- Keep tests fast and reliable
- Use stable selectors (data-testid)
- Add explicit waits, not arbitrary timeouts
- Make tests debuggable
- Run locally before CI

## Regression Testing

### Regression Test Coordination
- Use grep patterns to find related tests
- Target tests in affected modules only
- Don't re-run entire suite unnecessarily
- Focus on integration points

### When to Run Regression Tests
- After bug fixes
- Before releases
- After refactoring
- When dependencies updated

## Performance Validation

### Performance Metrics
- Response time (p50, p95, p99)
- Throughput (requests/second)
- Resource usage (CPU, memory)
- Error rate
- Concurrent users handled

### Performance Testing Approach
1. Establish baseline metrics
2. Define performance requirements
3. Create realistic load scenarios
4. Monitor and measure
5. Identify bottlenecks
6. Validate improvements

## Test Maintenance

### Keep Tests Maintainable
- Remove obsolete tests
- Update tests when requirements change
- Refactor duplicated test code
- Keep test data manageable
- Document complex test setups

### Test Code Quality
- Tests are code: Apply same standards
- DRY principle: Use fixtures/factories
- Clear naming and structure
- Comments for non-obvious test logic

## Handoff to Engineers

When bugs are found:
1. **Reproduce reliably**: Include exact steps
2. **Isolate the issue**: Narrow down scope
3. **Provide context**: Environment, data, state
4. **Suggest fixes** (optional): If obvious cause
5. **Verify fixes**: Re-test after implementation

## Quality Gates

Before declaring "ready for production":
- [ ] All critical tests passing
- [ ] Coverage meets targets (90%+)
- [ ] No high/critical bugs open
- [ ] Performance meets requirements
- [ ] Security scan clean
- [ ] Regression tests passing
- [ ] Load testing completed (if applicable)
- [ ] Cross-browser tested (web apps)
- [ ] Accessibility validated (UI)

## QA Evidence Requirements

All QA reports should include:
- **Test results**: Pass/fail counts
- **Coverage metrics**: Percentage and gaps
- **Bug findings**: Severity and details
- **Performance data**: Actual measurements
- **Logs/screenshots**: Supporting evidence
- **Environment details**: Where tested

## Pre-Merge Testing Checklist

Comprehensive verification workflow before merging changes to production.

### Pre-Commit Verification
Before committing code, verify:
- [ ] TypeScript type check passes (`tsc --noEmit`)
- [ ] ESLint passes with no errors
- [ ] All existing tests pass locally
- [ ] No console.log/debug statements left in code
- [ ] Code follows project style guide
- [ ] No commented-out code blocks

### Pre-PR Verification
Before creating a pull request, ensure:
- [ ] Changeset added for user-facing changes
- [ ] PR description is complete with:
  - [ ] Summary of changes
  - [ ] Related ticket references (ENG-XXX, HEL-XXX, etc.)
  - [ ] Screenshots for UI changes
  - [ ] Breaking changes documented
- [ ] Security checklist completed (if API changes)
- [ ] Database migration tested on staging (if schema changes)
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed

### Pre-Merge Verification
Before merging to main branch, confirm:
- [ ] All CI checks pass (lint, type-check, tests, build)
- [ ] Code review approved by at least one reviewer
- [ ] No TypeScript errors in changed files
- [ ] No merge conflicts with target branch
- [ ] Database migrations run successfully (if applicable)
- [ ] No regression in existing functionality
- [ ] Performance benchmarks within acceptable range

## Screenshot-Based UI Verification

Visual verification accelerates code review and catches responsive issues early.

### Screenshot Requirements
For any PR that changes UI, capture:

1. **Desktop View** (1920x1080)
   - Full page screenshot
   - Key component close-ups if needed
   - Before and after comparisons

2. **Tablet View** (768x1024)
   - Portrait orientation
   - Verify responsive breakpoints
   - Touch interaction targets visible

3. **Mobile View** (375x667)
   - Portrait orientation
   - Touch target sizes visible
   - Scrolling behavior documented

### PR Description Template
```markdown
## Visual Changes

### Desktop
![Desktop view](screenshot-url)

### Tablet
![Tablet view](screenshot-url)

### Mobile
Before:
![Mobile before](screenshot-url)

After:
![Mobile after](screenshot-url)

### Key Changes
- List specific UI modifications
- Note any responsive behavior changes
- Highlight accessibility improvements
```

### Benefits
- Reviewers see changes without running code locally
- Documents design decisions visually
- Creates visual changelog
- Catches responsive issues early
- Faster review cycles
- Reduces back-and-forth communication

## Iterative Testing for Infrastructure Changes

For complex infrastructure changes (database migrations, API patterns), use incremental testing.

### Database Migration Testing

#### 1. Local Testing
```bash
# Reset local database
pnpm db:reset

# Run migrations
pnpm drizzle-kit push

# Verify schema
pnpm drizzle-kit check

# Test rollback (if supported)
pnpm db:rollback

# Re-run migration
pnpm drizzle-kit push
```

#### 2. Staging Testing
- Deploy migration to staging environment
- Run affected API routes manually
- Verify data integrity with sample queries
- Check for performance regressions
- Test with realistic data volume
- Monitor database logs during migration

#### 3. Production Verification
- Monitor migration execution time
- Check error logs immediately after
- Verify application functionality
- Have rollback plan ready
- Monitor database performance metrics
- Alert team of any anomalies

### API Testing Checklist

Test all API endpoints systematically:

```bash
# Test happy path
curl -X GET "http://localhost:3000/api/endpoint?param=value"

# Test validation errors
curl -X GET "http://localhost:3000/api/endpoint?param=invalid"

# Test authentication
curl -X GET "http://localhost:3000/api/endpoint" \
  -H "Authorization: Bearer token"

# Test pagination
curl -X GET "http://localhost:3000/api/endpoint?page=1&limit=10"

# Test edge cases
curl -X GET "http://localhost:3000/api/endpoint?page=0&limit=0"

# Test unauthorized access
curl -X GET "http://localhost:3000/api/endpoint"

# Test rate limiting (if implemented)
for i in {1..100}; do
  curl -X GET "http://localhost:3000/api/endpoint"
done
```

### Infrastructure Change Workflow
1. **Plan**: Document migration steps and rollback plan
2. **Local**: Test migration on local copy of production data
3. **Staging**: Deploy to staging, verify with team
4. **Monitoring**: Set up alerts and logging before production
5. **Production**: Execute during low-traffic window
6. **Verification**: Immediate post-deployment testing
7. **Rollback Ready**: Have rollback script tested and ready

## API Security Testing Checklist

Before merging any API changes, verify security controls.

### Authentication Testing
- [ ] Route requires authentication (returns 401 without token)
- [ ] Invalid tokens are rejected (returns 401)
- [ ] Expired tokens are rejected (returns 401)
- [ ] Token refresh works correctly
- [ ] Logout invalidates tokens properly
- [ ] Password reset tokens expire after use

### Authorization Testing
- [ ] Users can only access their own resources (returns 403 for others)
- [ ] Admin routes reject non-admin users (returns 403)
- [ ] Cross-tenant data isolation verified
- [ ] Role-based access control working correctly
- [ ] Privilege escalation attempts blocked
- [ ] Resource ownership validation enforced

### Input Validation Testing
- [ ] Invalid input returns 400 with descriptive error
- [ ] SQL injection attempts are blocked
- [ ] XSS payloads are sanitized
- [ ] File upload limits enforced (size, type)
- [ ] Rate limiting triggers on abuse
- [ ] Command injection attempts blocked
- [ ] Path traversal attacks prevented

### Output Security Testing
- [ ] Sensitive data not exposed in responses (passwords, tokens)
- [ ] PII properly masked in logs
- [ ] Error messages don't leak system information
- [ ] Stack traces not exposed in production
- [ ] Database errors don't reveal schema details
- [ ] Internal paths and versions not disclosed

### Example Security Test Cases
```typescript
// Test ownership validation
it('should return 403 when accessing another user\'s resource', async () => {
  const response = await fetch('/api/providers/other-user-id', {
    headers: { Authorization: `Bearer ${userToken}` }
  });
  expect(response.status).toBe(403);
  expect(response.json()).resolves.toMatchObject({
    error: 'Forbidden'
  });
});

// Test input validation
it('should return 400 for invalid input', async () => {
  const response = await fetch('/api/schools?page=-1');
  expect(response.status).toBe(400);
  const body = await response.json();
  expect(body.error).toBe('Validation failed');
  expect(body.details).toContain('page must be positive');
});

// Test SQL injection prevention
it('should sanitize SQL injection attempts', async () => {
  const maliciousInput = "'; DROP TABLE users; --";
  const response = await fetch(`/api/search?q=${encodeURIComponent(maliciousInput)}`);
  expect(response.status).not.toBe(500);
  // Should return results or empty array, not crash
});

// Test XSS prevention
it('should sanitize XSS payloads in output', async () => {
  const xssPayload = '<script>alert("XSS")</script>';
  const response = await fetch('/api/profile/update', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${userToken}`
    },
    body: JSON.stringify({ bio: xssPayload })
  });
  expect(response.status).toBe(200);

  const profile = await fetch('/api/profile').then(r => r.json());
  expect(profile.bio).not.toContain('<script>');
});

// Test authentication requirement
it('should require authentication for protected routes', async () => {
  const response = await fetch('/api/protected-resource');
  expect(response.status).toBe(401);
  expect(response.json()).resolves.toMatchObject({
    error: 'Authentication required'
  });
});

// Test rate limiting
it('should enforce rate limits', async () => {
  const requests = Array(101).fill(null).map(() =>
    fetch('/api/endpoint', {
      headers: { Authorization: `Bearer ${userToken}` }
    })
  );
  const responses = await Promise.all(requests);
  const tooManyRequests = responses.filter(r => r.status === 429);
  expect(tooManyRequests.length).toBeGreaterThan(0);
});
```

### Security Testing Best Practices
- **Test Early**: Include security tests in unit test suites
- **Automate**: Run security tests in CI/CD pipeline
- **Real Scenarios**: Use actual attack patterns, not toy examples
- **Document**: Explain why security controls are necessary
- **Update**: Refresh tests when new vulnerabilities discovered
- **Penetration Testing**: Periodic manual security audits

## Bug Fix Verification Process

For every bug fix, follow this verification workflow to ensure quality.

### 1. Reproduce Before Fix
- [ ] Document exact steps to reproduce
- [ ] Capture error message/behavior with screenshots
- [ ] Note frequency (100% reproducible, intermittent, etc.)
- [ ] Screenshot or video if UI-related
- [ ] Identify affected versions/environments
- [ ] Note any workarounds users have found

### 2. Verify Fix
- [ ] Follow same reproduction steps
- [ ] Confirm bug no longer occurs
- [ ] Test edge cases around the fix
- [ ] Verify no new errors introduced
- [ ] Check fix works across environments
- [ ] Validate fix matches expected behavior

### 3. Regression Testing
- [ ] Run full test suite
- [ ] Test related functionality manually
- [ ] Verify fix works across browsers (if frontend)
- [ ] Test on mobile devices (if responsive)
- [ ] Check for performance impact
- [ ] Verify backwards compatibility

### 4. Documentation Template
Use this template in PR descriptions for bug fixes:

```markdown
## Bug Fix Verification

**Bug**: [Description of the bug]
**Ticket**: ENG-XXX / HEL-XXX

### Reproduction Steps (Before Fix)
1. Navigate to /page
2. Click button
3. Error appears: "Invalid session token"
4. Expected behavior: User should be redirected to login

### Root Cause
- Session token validation logic was checking expired tokens incorrectly
- Token expiry was comparing timestamps in different timezones
- Fix: Normalize all timestamps to UTC before comparison

### Verification (After Fix)
1. Followed same steps
2. No error appears
3. User correctly redirected to login page
4. Session token properly validated across timezones

### Regression Tests
- [ ] Login flow still works normally
- [ ] Token refresh works correctly
- [ ] Logout properly invalidates tokens
- [ ] No console errors
- [ ] Session persistence works as expected

### Test Coverage
- Added unit test for timezone edge case
- Added integration test for token validation
- Verified fix on staging environment
- Tested across multiple browsers (Chrome, Firefox, Safari)
```

### Bug Fix Quality Standards
- **Root Cause**: Fix the underlying problem, not symptoms
- **Test Coverage**: Add tests that would have caught the bug
- **Documentation**: Explain what caused the bug and how fix works
- **Verification**: Prove the bug is fixed with evidence
- **Regression**: Ensure fix doesn't break existing functionality
- **Communication**: Update ticket with verification details

### Common Bug Fix Pitfalls to Avoid
- ❌ Fixing symptoms without understanding root cause
- ❌ Adding workarounds instead of proper fixes
- ❌ Not adding tests to prevent regression
- ❌ Breaking other functionality while fixing bug
- ❌ Incomplete testing of edge cases
- ✅ Thorough investigation before implementing fix
- ✅ Comprehensive testing of fix and related areas
- ✅ Clear documentation of problem and solution
- ✅ Automated tests to prevent future regressions
