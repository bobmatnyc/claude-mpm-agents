---
name: mutation-testing
description: Audit whether a test suite actually detects regressions (not just whether it runs) by introducing small code mutations and measuring how many your tests catch. Advisory and on-demand — not a blocking CI gate.
version: 1.0.0
category: testing
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "A second-order test-quality signal: instead of 'do my tests run?', it asks 'do my tests detect regressions?'. Mutate the source, re-run tests, measure the kill rate. Most valuable on logic-dense code, applied on-demand."
    when_to_use: "When auditing test-suite effectiveness on a critical module, evaluating whether green tests actually protect behavior after a near-miss bug, or deciding whether to invest more in coverage."
    quick_start: "Pick a logic-dense module. Run a mutation tool (mutmut / cosmic-ray for Python). Inspect SURVIVED mutants — each is a behavior no test pins down. Add assertions to kill them. Track kill rate, not 100%."
context_limit: 700
tags:
  - testing
  - quality-assurance
  - mutation-testing
  - test-effectiveness
  - advisory
requires_tools: []
---

# Mutation Testing

A second-order test-quality signal. Line coverage tells you a line *executed*; mutation
testing tells you whether any assertion would *fail* if that line were wrong. Use it to audit
the strength of an existing suite — most valuable on logic-dense code, applied on-demand,
never as a default blocking CI gate.

## What it does

A mutation tool makes small automatic edits ("mutants") to your source, e.g.:

- `<` -> `<=` (boundary / off-by-one)
- `and` -> `or` (predicate logic)
- `==` -> `!=` (negated condition)
- `return x` -> `return None`, `+` -> `-`, deleting a statement
- removing a list/dict entry (allowlist/denylist coverage)

For each mutant it re-runs the test suite:

- **Killed** — at least one test fails. Good: your tests detect that change.
- **Survived** — all tests still pass. Bad: the mutant models a real bug your suite would
  not catch.

**Kill rate** = killed / total mutants. It measures test *effectiveness*, not code execution.
You can have 100% line coverage with a 40% kill rate: every line runs, but half the logic
changes go undetected because the tests assert too little.

## When to use it (and when not to)

**Use it to:** audit a critical module before relying on it (payment math, auth predicates,
allowlists gating filesystem/network access); harden tests after a near-miss bug; turn "we
have 90% coverage" into "here are the specific behaviors no test pins down".

**Do NOT use it as:** a default blocking CI gate (runtime is `N mutants x full suite`); a
metric to chase to 100% (some mutants are *equivalent* — semantically identical — and can
never be killed).

## Workflow

1. Choose one logic-dense module with existing green tests.
2. Run a mutation tool scoped to that module (Python: `mutmut` or `cosmic-ray`; JS/TS:
   `stryker`).
3. List SURVIVED mutants. Each names a behavior no test verifies.
4. For each survivor that represents a real bug, add or strengthen an assertion to kill it.
5. Re-run; confirm the kill rate rose. Stop when survivors are only equivalent mutants.

A rising kill rate on a critical module is the goal — not a perfect score.
