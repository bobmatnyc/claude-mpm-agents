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

### Dead Code Elimination

Systematically remove unused code during feature work to maintain codebase health.

#### Detection Process

1. **Search for Usage**:
   \`\`\`bash
   # Search for imports of a component/function
   rg "import.*{ComponentName}" --type ts --type tsx
   rg "from.*{ModuleName}" --type python

   # Search for function/class usage
   rg "{FunctionName}" --type ts --type tsx
   rg "class {ClassName}" --type python
   \`\`\`

2. **Verify No References**:
   - Check for dynamic imports: \`rg "import\\(.*ComponentName"\`
   - Search for string references: \`rg "\\"ComponentName\\"" --type json\`
   - Check test files: \`rg "ComponentName" tests/\`
   - Verify no API consumers (for endpoints)

3. **Remove in Same PR**: Delete old code when replacing with new implementation
   - Don't leave "commented out" old code
   - Don't keep unused "just in case" code
   - Git history preserves old implementations if needed

#### Common Targets for Deletion

- **Unused API endpoints**: Check frontend for fetch calls
  \`\`\`bash
  rg "fetch.*\\/api\\/endpoint-name" --type ts
  \`\`\`
- **Deprecated utility functions**: After migration to new utilities
- **Old component versions**: After refactor to new implementation
- **Unused hooks and context providers**: Search for usage across codebase
- **Dead CSS/styles**: Unused class names and style modules
- **Orphaned test files**: Tests for deleted functionality
- **Commented-out code**: Remove, rely on git history

#### Documentation Requirements

Always document deletions in PR summary:
\`\`\`
Deletions:
- Delete /api/holidays endpoint (unused, superseded by /api/schools/holidays)
- Remove useGeneralHolidays hook (replaced by useSchoolCalendar)
- Remove moment.js dependency (migrated to date-fns)
- Delete legacy SearchFilter component (replaced by SearchFilterV2)
\`\`\`

#### Example: Removing Unused Endpoint

\`\`\`bash
# 1. Search for usage in frontend
rg "fetch.*\\/api\\/holidays" --type ts --type tsx
# No results = safe to delete

# 2. Check for string references
rg "holidays" app/api/ --type ts
# Find the endpoint definition

# 3. Delete the endpoint file
rm app/api/holidays/route.ts

# 4. Search for related tests
rg "holidays" tests/ --type ts
# Delete associated tests

# 5. Update documentation
# Remove from API docs if documented

# 6. Document in PR
# List what was deleted and why
\`\`\`

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

### Regular Audit Process

Run these commands regularly (monthly for active projects):

\`\`\`bash
# Check for outdated packages (language-specific)
npm outdated          # Node.js
pnpm outdated        # pnpm
pip list --outdated  # Python
cargo outdated       # Rust

# Check for security vulnerabilities
npm audit            # Node.js
pnpm audit          # pnpm
pip-audit           # Python (pip install pip-audit)
cargo audit         # Rust (cargo install cargo-audit)

# Find unused dependencies
npx depcheck        # Node.js (finds unused packages)
pip-autoremove      # Python (finds unused packages)
\`\`\`

### Migration Priorities

Prioritize dependency updates based on risk and value:

| Priority | Type | Example | Action Timeline |
|----------|------|---------|-----------------|
| P0 | Critical security vulnerabilities | CVE with active exploits | Immediate (same day) |
| P1 | Major version updates | Next.js 13 → 14, React 17 → 18 | Within 1-2 sprints |
| P2 | Deprecated packages with active usage | moment.js → date-fns | Within quarter |
| P3 | Minor updates and patches | Regular maintenance updates | Monthly batch update |
| P4 | Unused dependencies | Remove entirely | During next refactoring |

### Common Package Replacements

Replace heavy or deprecated packages with modern alternatives:

#### JavaScript/TypeScript
- \`moment.js\` → \`date-fns\` + native \`Intl\` (90% smaller, more tree-shakeable)
- \`lodash\` → Native JS methods + specific utilities (ES2015+ has most features)
- \`request\` → \`fetch\` API or \`axios\` (request is deprecated)
- \`jquery\` → Native DOM APIs or modern framework
- Heavy UI libraries → Lighter alternatives or native

#### Python
- \`requests\` (sync) → \`httpx\` or \`aiohttp\` (async support)
- Custom date parsing → \`python-dateutil\` or native \`datetime\`
- \`os.path\` → \`pathlib\` (modern, object-oriented)

### Dependency Update Strategy

Follow this process for safe updates:

1. **Group Related Updates**: Update related packages together
   - Example: Update React, ReactDOM, and React-related packages together
   - Example: Update all ESLint plugins in one PR

2. **Test Thoroughly**: Run full test suite after each update
   - Unit tests
   - Integration tests
   - End-to-end tests if available
   - Manual testing for critical paths

3. **Document Breaking Changes**: Use changesets or commit messages
   \`\`\`
   chore(deps): update react 17 → 18

   Breaking changes:
   - ReactDOM.render replaced with createRoot
   - Automatic batching changes setState behavior
   - New strict mode behaviors in development

   Migration guide: [link to React 18 upgrade guide]
   \`\`\`

4. **One Major Update at a Time**: Don't update multiple major versions simultaneously
   - ❌ WRONG: Update React 16→18 + Next 14→15 in same PR
   - ✅ CORRECT: Update React 16→18, test, then Next 14→15

5. **Keep Changelog**: Document all dependency changes
   - Why updated (security, features, deprecation)
   - What changed (breaking changes, new features)
   - Migration notes for team

### Example: Migrating from moment.js to date-fns

\`\`\`bash
# 1. Audit current usage
rg "import.*moment" --type ts
rg "require.*moment" --type js

# 2. Install replacement
npm install date-fns
npm uninstall moment

# 3. Update imports (one module at a time)
# Before:
import moment from 'moment';
const date = moment().format('YYYY-MM-DD');

# After:
import { format } from 'date-fns';
const date = format(new Date(), 'yyyy-MM-dd');

# 4. Update tests
# Ensure all date-related tests pass

# 5. Document in PR
chore(deps): migrate from moment.js to date-fns

- Reduces bundle size by ~67KB (moment.js 72KB → date-fns 5KB)
- Better tree-shaking (only import needed functions)
- More modern, functional API

Migration:
- Replaced all moment() calls with date-fns equivalents
- Updated date formatting to use date-fns format()
- All existing tests passing

LOC Delta:
- Added: 45 lines (date-fns imports and usage)
- Removed: 67 lines (moment.js imports and usage)
- Net: -22 lines
\`\`\`

### Dependency Health Metrics

Track these metrics to maintain dependency health:

- **Outdated Packages**: Aim for <5 outdated minor versions
- **Security Vulnerabilities**: Zero high/critical vulnerabilities
- **Unused Dependencies**: Zero unused packages in package.json
- **Bundle Size**: Monitor and reduce over time
- **Update Frequency**: Update dependencies monthly (at minimum)

### Automation Opportunities

Consider automating dependency management:

- **Dependabot/Renovate**: Auto-create PRs for updates
- **CI/CD Integration**: Run security audits in pipeline
- **Bundle Size Tracking**: Monitor bundle size in CI
- **Automated Testing**: Ensure tests run on dependency PRs

## Progressive Refactoring Workflow

Follow this incremental approach when refactoring code:

### Process
1. **Identify Related Issues**: Group related tickets that can be addressed together
   - Look for tickets in the same domain (query params, UI, dependencies)
   - Aim to group 3-5 related issues per PR for efficiency
   - Document ticket IDs in PR summary (e.g., ENG-XXX)

2. **Group by Domain**: Organize changes by area
   - Query parameter handling
   - UI component updates
   - Dependency updates and migrations
   - API endpoint consolidation

3. **Delete First**: Remove unused code BEFORE adding new code
   - Search for imports: \`rg "import.*{ComponentName}"\`
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

### PR Summary Template for Refactoring
\`\`\`
Summary:
 - ENG-XXX: Fix query parameter handling in search
 - ENG-YYY: Update mobile responsive design for filters
 - Retire moment.js - migrate to date-fns
 - Delete /api/holidays endpoint (unused, superseded by /api/schools/holidays)
 - Fix TypeScript strict mode violations

LOC Delta:
- Added: 150 lines
- Removed: 380 lines
- Net Change: -230 lines
\`\`\`

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

### Example: Adding Search Filters Feature

**Phase 1 - MVP**:
- Basic filter UI (desktop only)
- Core filter logic (category, price range)
- Search results update on filter change
- PR: ~200 lines, ships in 2-3 days

**Phase 2 - Enhancement**:
- Mobile responsive filters
- URL query params sync
- Filter persistence in session
- Loading states during search
- PR: ~150 lines, ships 2-3 days after MVP feedback

**Phase 3 - Optimization**:
- Add GTM events for filter usage
- Debounce filter changes
- Accessibility keyboard navigation
- PR: ~100 lines, ships after production monitoring

**Phase 4 - Cleanup**:
- Remove old filter implementation
- Consolidate filter utility functions
- Add integration tests
- Update documentation
- PR: ~50 additions, ~200 deletions

## Lines of Code (LOC) Reporting

Every implementation should report:
\`\`\`
LOC Delta:
- Added: X lines
- Removed: Y lines
- Net Change: (X - Y) lines
- Target: Negative or zero net change
- Phase: [MVP/Enhancement/Optimization/Cleanup]
\`\`\`

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
