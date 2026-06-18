---
name: code-production-process
description: Production-readiness process checklist covering the code-production pipeline — research, architecture, implementation, tests, critic review, and security gates
version: 1.0.0
category: collaboration
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "6-stage gate pipeline (Research -> Architect -> Implement -> Tests -> Critic -> Security). Hotfix path may skip 1-2; stages 3-6 are mandatory. WARN proceeds with findings logged; BLOCK halts and returns to the user — PM must NOT auto-retry without user direction."
    when_to_use: "When dispatching an engineer for non-trivial implementation (>50 lines OR >1 source file). Excludes docs edits, config-only changes, and version bumps."
    quick_start: "1. Research first. 2. Architect produces an interface spec, no implementation. 3. Engineer implements + tests. 3.5 Tests must pass green. 4. Dispatch code-critic in isolated context. 5. Act on verdict. 6. Security pass."
context_limit: 700
tags:
  - process
  - production-readiness
  - checklist
  - quality-gate
  - release
requires_tools: []
---

# Code Production Process

## Overview

A six-stage quality-gate pipeline that every non-trivial implementation passes through before
being declared complete. Each stage produces a concrete artifact and must clear a defined gate
before the next begins. The pipeline exists because quality must be enforced by automated gates
inside the agent pipeline, not by human review after the fact. The critic operates in isolated
context to prevent anchoring bias from the implementer's framing.

## Trigger Conditions

Triggers when the task will produce >50 lines of source, touch >1 source file, or contains
implementation verbs ("implement", "build", "refactor", "fix bug in ..."). Also triggers
post-dispatch if `git diff --stat` shows source changes. Does NOT trigger for documentation,
commit messages, config-only changes, or dependency bumps. When in doubt, trigger — a false
positive costs one critic dispatch; a false negative ships broken code.

## The Six Stages

| Stage | Agent | Artifact | Gate |
|-------|-------|----------|------|
| 1. Research | research | Spec citing existing code | Spec exists, references prior code, NO implementation |
| 2. Architect | engineer (design mode) | Interface spec (signatures, types, error model) | Interface exists, ZERO implementation logic |
| 3. Implement | engineer | Source + tests | Type checker and tests output provided, zero errors |
| 3.5 Tests gate | PM | (evaluation) | Tests pass green — failing tests return to Stage 3, skip critic |
| 4. Critic | code-critic | Verdict + finding table | Verdict returned (see `code-review-standards`) |
| 5. Security | security | Finding list | Zero CRITICAL/HIGH security findings |

## Critic Isolation Rule

The critic dispatch MUST contain only the spec, the interface, the implementation, and the
test output. It MUST NOT contain the engineer's commit message, stated rationale, or any PM
summary of what the engineer did. An engineer who pre-argues ("I chose this because the
alternative is slower") subtly disarms the critic. The critic must encounter the code cold.

## Verdict Protocol

- **APPROVE** (no CRITICAL/HIGH): proceed to security; pass MEDIUM/LOW notes to docs handoff.
- **WARN** (HIGH, no CRITICAL): proceed to security, but append finding table to handoff and
  log it — never silently drop HIGH findings.
- **BLOCK** (any CRITICAL): halt, surface findings verbatim to the user, await direction. Do
  NOT auto-re-dispatch the engineer without user input.

## Skip Rules

- **Standard path:** all 6 stages (required for features, refactors, auth, data models).
- **Hotfix path:** stages 1-2 skippable only when the bug is confirmed in production, the fix
  is <=20 lines across <=2 files, and it does not touch auth/crypto/serialization. Stages 3-5
  remain mandatory.
- **Docs/config-only path:** all stages skipped when `git diff --stat` shows no source changes.
