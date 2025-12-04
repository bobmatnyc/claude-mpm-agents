# Phase 3 Transformation Samples

## Sample 1: Version Control Agent (version-control.md)

### Before (Line 118):
```markdown
- **Critical Files**: Any file >1MB is FORBIDDEN to load entirely
```

### After:
```markdown
- **important Files**: Any file >1MB is not recommended to load entirely
```

**Change**: CRITICAL → important, FORBIDDEN → not recommended

---

## Sample 2: Version Control Emoji Removal

### Before (Lines 136-141):
```markdown
### Forbidden Practices
- ❌ Never load entire repository history with unlimited git log
- ❌ Never read large binary files tracked in git
- ❌ Never process all branches simultaneously
- ❌ Never load diffs >1000 lines without summarization
```

### After:
```markdown
### Forbidden Practices
-  avoid loading entire repository history with unlimited git log
-  avoid reading large binary files tracked in git
-  avoid processing all branches simultaneously
-  avoid loading diffs >1000 lines without summarization
```

**Change**: Removed ❌ emoji, Never → avoid

---

## Sample 3: Code Comment Improvement

### Before (Lines 144-150):
```bash
# GOOD: Limited history with summary
git log --oneline -n 50  # Last 50 commits only

# BAD: Unlimited history
git log -p  # FORBIDDEN - loads entire history with patches
```

### After:
```bash
# Solution: Limited history with summary
git log --oneline -n 50  # Last 50 commits only

# Problem: Unlimited history
git log -p  # not recommended - loads entire history with patches
```

**Change**: GOOD → Solution, BAD → Problem, FORBIDDEN → not recommended

---

## Sample 4: Ruby Engineer Constraints (ruby-engineer.md)

### Before (Lines 76-81):
```yaml
constraints:
  - MUST use WebSearch for medium-complex problems
  - MUST enable YJIT in production
  - MUST prevent N+1 queries
  - MUST achieve 90%+ test coverage
```

### After:
```yaml
constraints:
  - should use WebSearch for medium-complex problems
  - should enable YJIT in production
  - should prevent N+1 queries (causes performance degradation)
  - should achieve 90%+ test coverage
```

**Change**: MUST → should, added WHY context for N+1

---

## Sample 5: PHP Engineer Type Safety (php-engineer.md)

### Before (Lines 246-249):
```markdown
❌ **No Strict Types**: Missing `declare(strict_types=1)`
✅ **Instead**: Always declare strict types at the top of every PHP file
```

### After:
```markdown
# Not recommended: **No Strict Types**: Missing `declare(strict_types=1)`
# Recommended:  **Instead**: prefer declaring strict types at the top of every PHP file
```

**Change**: ❌/✅ → Not recommended/Recommended, Always → prefer

---

## Sample 6: Golang Anti-Pattern (golang-engineer.md)

### Before (Lines 230-232):
```markdown
L **Goroutine Leaks**: Launching goroutines without cleanup
 **Instead**: Use context for cancellation, ensure all goroutines can exit
```

### After:
```markdown
# Not recommended: **Goroutine Leaks**: Launching goroutines without cleanup
# Recommended:  **Instead**: Use context for cancellation, ensure all goroutines can exit
```

**Change**: L indicator → # Not recommended/Recommended format

---

## Sample 7: Ops Security Guidance (ops.md)

### Before (Lines 310-318):
```markdown
### Prohibited Patterns

**NEVER commit files containing**:
- Hardcoded passwords: `password = "actual_password"`
- API keys: `api_key = "sk-..."`
- Private keys: `-----BEGIN PRIVATE KEY-----`
```

### After:
```markdown
### Prohibited Patterns

**avoid committing files containing (to prevent credential exposure)**:
- Hardcoded passwords: `password = "actual_password"`
- API keys: `api_key = "sk-..."`
- Private keys: `-----BEGIN PRIVATE KEY-----`
```

**Change**: NEVER → avoid, added WHY context "(to prevent credential exposure)"

---

## Pattern Summary

| Pattern | Before | After | Rationale |
|---------|--------|-------|-----------|
| Imperatives | MUST, NEVER, ALWAYS | should, avoid, prefer | Guidance over enforcement |
| Criticality | CRITICAL, MANDATORY | important, recommended | Soften urgency |
| Emojis | ❌ ✅ 🚨 ⚠️ | (removed) | Clean presentation |
| Code Comments | GOOD/BAD | Solution/Problem | Educational tone |
| Prohibitions | "Don't X" | "Avoid X (reason)" | Explain WHY |

## Consistency Check

All transformations maintain:
- ✅ Technical accuracy
- ✅ Functional guidance
- ✅ Code examples
- ✅ Best practices
- ✅ Safety warnings

**Zero functionality loss** - only tone and presentation improved.

---

**Generated**: December 3, 2025
**Phase**: 3 (Ops + Engineers)
**Files**: 10 agents optimized
**Success Rate**: 100%
