---
name: caveman-prompt-compression
description: Token-optimized prompt compression techniques for reducing LLM instruction size while preserving or improving quality
version: 1.0.0
category: ai-technique
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Compress system prompts 50-77% while maintaining quality through table-first formatting, deduplication, and filler removal"
    when_to_use: "System prompts >5KB, agent definitions >20KB, high-cost sessions, token budget optimization"
    quick_start: "1. Merge duplicate sections 2. Convert prose to tables 3. Remove filler 4. Strip verbose examples 5. Remove frontmatter bloat"
context_limit: 700
tags:
  - prompt-optimization
  - token-reduction
  - compression
  - cost-optimization
  - system-prompt
  - agent-design
requires_tools: []
---

# Caveman Prompt Compression

Systematic technique for reducing system prompt token count 50-77% while maintaining or improving output quality. Named for its "use fewer words" philosophy -- strip every token that does not change model behavior.

## Pilot Results (claude-mpm PR #425)

| Metric | Compressed | Original | Delta |
|--------|-----------|----------|-------|
| Cost | $4.42 | $6.74 | -34% |
| Tokens | 5.5M | 10.4M | -47% |
| Duration | 7.5 min | 9.5 min | -27% |
| Quality | 4.40/5 | 3.75/5 | +17% |

**Why quality improved**: Less noise lets the model focus on actual rules. Tables parse unambiguously. Single source of truth eliminates contradictory duplicates.

## The 5 Pillars

### 1. Merge Duplicate Sections

Find repeated rules, prohibitions, or guidelines scattered across sections. Consolidate into a single canonical reference.

**Pattern**: Search the entire prompt for overlapping instructions. Create one authoritative table, reference it by ID elsewhere.

| Before | After |
|--------|-------|
| 4 separate prohibition lists across sections | 1 table (P1-P12) with ID references |
| Same rule stated 3 different ways | Single canonical statement |
| Conflicting versions of same guideline | One source of truth |

**Process**:
1. Extract every rule/instruction into a flat list
2. Group by semantic similarity
3. Merge duplicates, keeping the most precise version
4. Assign IDs (R1, R2... or P1, P2...) for cross-referencing
5. Replace original locations with ID references

### 2. Convert Prose to Tables

Highest-impact technique. Replace verbose paragraph-form rules with compact markdown tables.

**Before** (prose, ~65 tokens):
```
When the user mentions a ticket ID like PROJ-123, or an issue URL,
or says 'ticket' or 'issue', you should delegate to the ticketing_agent.
The ticketing_agent has access to mcp-ticketer tools and can look up,
create, and update tickets on behalf of the user.
```

**After** (table row, ~20 tokens):
```
| ticket ID, issue URL, "ticket"/"issue" | ticketing_agent | mcp-ticketer | CB#6 |
```

**Table column patterns**:

For routing rules:
| Trigger | Agent | Tools | Notes |

For behavioral rules:
| Condition | Action | Priority |

For constraints:
| ID | Rule | Scope | Exception |

### 3. Remove Filler Language

Frontier models do not need motivational phrasing, hedging, or politeness markers in system prompts. These add tokens without changing behavior.

**Remove these patterns**:

| Filler Pattern | Replacement |
|---------------|-------------|
| "It is very important that you always..." | (state rule directly) |
| "Please make sure to..." | (state rule directly) |
| "Remember to always..." | (state rule directly) |
| "You should try to..." | (state rule directly) |
| "It would be great if you could..." | (state rule directly) |
| "As an AI assistant, you..." | (remove entirely) |
| "Your goal is to help the user by..." | (remove entirely) |

**Before** (~30 tokens):
```
It is very important that you always make sure to check the git status
before committing any changes to ensure nothing is missed.
```

**After** (~8 tokens):
```
Check `git status` before every commit.
```

### 4. Remove Verbose Examples and Anti-Patterns

Frontier models understand rules from concise statements. Multi-paragraph examples showing right/wrong approaches rarely change behavior compared to the rule alone.

**Guidelines**:
- Keep examples only when the rule is genuinely ambiguous
- Maximum 1 line per example
- Remove all "anti-pattern" showcases (bad-then-good comparisons)
- If you must show format, show the correct format only

| Before | After |
|--------|-------|
| 20-line bad example + 20-line good example | Rule + 1-line correct example |
| 3 variations of the same pattern | 1 canonical example |
| "Here is what NOT to do: ..." | (remove; state positive rule) |

### 5. Strip Frontmatter Bloat

Remove metadata that does not affect model behavior at runtime.

**Remove**:
- Changelogs and version history
- Author credits and license text (in body, not YAML frontmatter)
- Dependency lists (unless model needs to check them)
- "About this document" preambles
- Table of contents (for short docs)

**Keep**:
- Frontmatter fields the system reads programmatically
- Context the model genuinely needs for decision-making

## Decision Framework

### When to Compress

- System prompts >5KB
- Agent definitions >20KB
- Repeated high-cost sessions (compression ROI compounds)
- Token budget constraints (context window pressure)
- Multi-agent systems (each agent carries overhead)

### When NOT to Compress

- User-facing documentation (readability matters)
- Novel or genuinely ambiguous instructions (examples help)
- Training data or few-shot examples (these need verbosity)
- One-off prompts (compression effort not worth it)
- Instructions for non-frontier models (may need more guidance)

### Safety Rule

Never compress to the point where meaning is lost. Always A/B test compressed vs original on representative tasks before deploying.

## Compression Checklist

```
[ ] Identify all duplicate/overlapping sections
[ ] Convert prose paragraphs to tables (highest ROI)
[ ] Remove filler phrases ("please", "make sure to", "it is important")
[ ] Collapse verbose examples to 1-line summaries
[ ] Remove non-runtime metadata (changelogs, credits)
[ ] Verify: compressed version produces same/better outputs
[ ] Measure: token count before vs after
```

## Worked Example: Routing Section

**Before** (~180 tokens):
```markdown
## How to Route Messages

When you receive a message from the user, you need to determine which
agent should handle the request. Here are the routing rules:

If the user asks about code, programming, or software development,
you should route to the engineer agent. The engineer agent is skilled
at writing code, debugging, and architecture decisions.

If the user asks about testing, QA, or quality assurance, you should
route to the QA agent. Make sure to include context about what needs
to be tested.

If the user asks about design, UI, or user experience, you should
route to the designer agent.
```

**After** (~45 tokens):
```markdown
## Routing

| Trigger Keywords | Agent | Context |
|-----------------|-------|---------|
| code, programming, dev, debug, architecture | engineer | include relevant files |
| testing, QA, quality | qa | specify test scope |
| design, UI, UX | designer | include mockups if any |
```

**Result**: 75% reduction, zero information loss, faster model parsing.

## Measuring Compression

Track these metrics for each compression pass:

```
Token count: before → after (% reduction)
Quality score: A/B test on 5-10 representative tasks
Regression check: verify edge cases still handled
Cost delta: estimated savings per session
```

**Target**: 50-77% token reduction with equal or better quality.

## Common Pitfalls

| Pitfall | Mitigation |
|---------|-----------|
| Over-compression loses nuance | A/B test before deploying |
| Tables become too wide to read | Split into multiple focused tables |
| Removed example was actually needed | Keep examples for genuinely ambiguous rules only |
| Compressed prompt contradicts itself | Deduplication (Pillar 1) prevents this |
| Different team members re-expand | Document compression decisions, link to this skill |

## Integration with Other Skills

- **writing-plans**: Compress plan templates before embedding in agent prompts
- **systematic-debugging**: Compress debugging checklists into table format
- **internal-comms**: Apply filler removal (Pillar 3) to communication templates
- **session-compression**: Complements session-level compression with prompt-level compression
