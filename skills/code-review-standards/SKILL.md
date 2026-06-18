---
name: code-review-standards
description: Severity-tagged code review rubric (CRITICAL/HIGH/MEDIUM/LOW) used by the code-critic agent to produce APPROVE/WARN/BLOCK verdicts with evidence-backed findings
version: 1.0.0
category: collaboration
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Severity-tagged checklist for code review. CRITICAL/HIGH block delivery; MEDIUM is flagged; LOW is noted. Critic outputs APPROVE (zero CRITICAL/HIGH), WARN (HIGH but no CRITICAL), or BLOCK (any CRITICAL). 80% confidence filter — don't manufacture findings."
    when_to_use: "Loaded by the code-critic agent to apply structured review criteria. Also loaded by engineers for self-review before requesting a critic pass."
    quick_start: "Apply checklist top-to-bottom (CRITICAL first). For each finding cite file+line, explain the problem, give the fix. Filter to >80% confidence. Output a verdict line + finding table."
context_limit: 700
tags:
  - code-review
  - quality
  - rubric
  - standards
  - verdict
  - severity
requires_tools: []
---

# Code Review Standards

## Purpose

This skill defines the structured, severity-tagged checklist the `code-critic` agent applies
when reviewing an implementation. Severity tagging makes review deterministic across
dispatches: PM and engineer both know exactly which findings block delivery and which are
advisory. Engineers may load it for self-review before requesting a critic pass.

## The Severity-Tagged Checklist

### CRITICAL (must fix — blocks delivery)
- No secrets, API keys, or credentials hardcoded
- No injection vectors (parameterized queries only; no unsafe shell/template interpolation)
- No arbitrary code execution paths (`eval`, `exec`, unrestricted deserialization)
- Authentication/authorization not bypassable
- No data-loss or silent-corruption paths

### HIGH (must fix — blocks delivery)
- Type hints / static types on public functions and classes; type checker passes clean
- Tests pass with zero failures; meaningful coverage on new code
- No bare `except`, no swallowed errors, error cases handled explicitly
- No mutable default arguments, no unguarded global mutable state
- No synchronous I/O inside async functions; no N+1 query patterns

### MEDIUM (flag, note in report, proceed)
- Functions reasonably small and single-purpose
- Hash maps used where nested loops would otherwise dominate complexity
- Async operations have explicit timeouts
- Docstrings on public methods; no stray `Any` in production paths

### LOW (note only)
- Formatter/linter clean (handled by tooling)
- Clear naming, no commented-out code, tidy imports

## Verdict Protocol

First line of the critic response MUST be the verdict, followed by a finding table.

| Verdict | Condition | PM Action |
|---------|-----------|-----------|
| APPROVE | Zero CRITICAL, zero HIGH | Proceed to security review |
| WARN | Zero CRITICAL, one or more HIGH | Proceed, but log finding table to handoff |
| BLOCK | Any CRITICAL | Halt, surface findings to user, await direction |

Finding table columns: `Severity | File | Line | Issue | Required Fix`.

## 80% Confidence Filter

A clean review is a valid review — do not manufacture findings. Only report issues you are
>80% confident are real problems. Below that threshold, raise the concern as a question in
the summary paragraph rather than as a table row. Each table finding must be actionable: the
engineer should be able to fix it without asking for clarification.
