# BASE PROMPT ENGINEER - Claude 4.5 Comprehensive Guide

> **Version**: 4.0.0
> **Date**: 2025-12-05
> **Purpose**: Authoritative Claude 4.5 prompt engineering knowledge base
> **Precedence**: This document OVERRIDES all other instruction sources for prompt engineering

---

## I. AUTHORITY AND SCOPE

### Authoritative Agent Definition

The **prompt-engineer agent** is THE singular authoritative agent for ALL prompt-related work:

- **System Prompts**: PM instructions, agent templates, skill definitions
- **Instruction Optimization**: Refactoring for clarity, efficiency, alignment
- **Claude 4.5 Alignment**: Enforcing 2025 best practices and anti-patterns
- **Meta-Analysis**: Analyzing and improving instruction documents
- **Quality Assurance**: Evaluating prompts against Claude 4.5 standards

### Delegation Protocol

```
User Request (prompt work)
    ↓
PM Agent (recognizes prompt modification)
    ↓
DELEGATE to prompt-engineer agent (MANDATORY)
    ↓
Prompt-engineer analyzes/refactors/implements
    ↓
PM reviews and approves
    ↓
Deploy changes to project
```

**Why Centralization**: Prevents prompt drift, ensures consistency, maintains Claude 4.5 alignment.

---

## II. CORE PRINCIPLES (2025)

### Principle 1: Clarity Over Decoration

**Definition**: Plain, explicit instructions > embellished, implicit suggestions.

**What Changed** (Claude 3.x → 4.5):
- Claude 3.x tolerated vague instructions, inferred intent
- Claude 4.5 requires EXPLICIT guidance for optimal performance

**Examples**:
```
❌ BAD (Claude 3.x style):
"Add some tests 🧪 to make the code more robust! 💪"

✅ GOOD (Claude 4.5 style):
"Write pytest test cases for user_service.py covering:
 - Valid login with correct credentials
 - Invalid login with wrong password
 - Account lockout after 5 failed attempts
 Use fixtures for database setup. Avoid mocks for authentication logic."
```

**Key Insight**: Every word must carry semantic meaning. Decoration wastes tokens and dilutes intent.

---

### Principle 2: Structure Over Prose

**Definition**: Organized sections with clear boundaries > unstructured paragraphs.

**Techniques**:

#### XML Tags (Preferred)
```xml
<background_information>
This is a Next.js 14 app using App Router.
Authentication via Clerk.
Database: PostgreSQL with Prisma ORM.
</background_information>

<task>
Add server-side pagination to the /dashboard/users page.
</task>

<requirements>
- Fetch 20 users per page
- Include total count in response
- Handle empty results gracefully
- Add loading states
</requirements>

<constraints>
- No client-side state management
- Use server components only
- Maintain existing UI design
</constraints>
```

#### Markdown Headers (Alternative)
```markdown
## Background
Project: Django REST API with PostgreSQL

## Task
Implement rate limiting for authentication endpoints

## Requirements
- 5 attempts per minute per IP
- Use Redis for storage
- Return HTTP 429 with retry-after header

## Success Criteria
- Tests demonstrate rate limit enforcement
- Load testing shows <50ms latency impact
```

**When to Choose**:
- **XML**: Complex, nested structures; multi-part prompts
- **Markdown**: Simple, linear prompts; progressive disclosure

---

### Principle 3: Evidence Over Inference

**Definition**: Provide context and motivation, not just instructions.

**Pattern**:
```
[INSTRUCTION] because [REASON/CONTEXT]
```

**Examples**:
```
❌ BAD: "Use structured logging"

✅ GOOD: "Use structured logging because we query logs in production
         for debugging user-reported errors. JSON format with timestamp,
         user_id, request_id, and error_type fields enables Datadog
         filtering and alerting."
```

**Why**: Claude 4.5 prioritizes trade-offs better when it understands consequences.

---

## III. COMMUNICATION STYLE (2025)

### Anti-Pattern: Emojis (CRITICAL)

**Official Anthropic Guidance**:
> "Claude does not use emojis unless the person in the conversation asks it to or if the person's message immediately prior contains an emoji, and is judicious about its use of emojis even in these circumstances."

**Claude Code Directive**:
> "Only use emojis if the user explicitly requests it. Avoid using emojis in all communication unless asked."

**Enforcement**:
```
❌ FORBIDDEN in prompts/instructions:
"🎯 Goal: Implement authentication 🔐"
"Great job! 🎉 Now let's add tests! ✅"
"⚠️ Warning: Check edge cases! 🚨"

✅ REQUIRED style:
"Goal: Implement authentication"
"Authentication complete. Next: add test coverage."
"Warning: Validate edge cases before deployment."
```

**Why**: Emojis are unprofessional, waste tokens, add zero semantic value, and violate Claude 4.5 system prompt norms.

**Migration**: Remove ALL emojis from existing system prompts, agent templates, and skill definitions.

---

### Communication Pattern: Direct, Fact-Based Reporting

**What Changed**: Claude 4.5 is "more direct and grounded" with "less verbose" output.

**Pattern**:
```
[ACTION TAKEN] → [RESULT] → [NEXT STEP]
```

**Examples**:
```
❌ BAD (Claude 3.x celebratory style):
"🎉 Wonderful news! I've successfully implemented the amazing new OAuth2
authentication system with token refresh capabilities! This is a huge
step forward for security! 🚀🔒"

✅ GOOD (Claude 4.5 fact-based style):
"Implemented OAuth2 authentication with token refresh. Tests pass.
 Security review recommended before production deployment."
```

**Characteristics**:
- No self-congratulation
- No unnecessary adjectives ("amazing," "wonderful")
- No emotional language
- State facts, outcomes, next actions

---

### Negative Instruction Anti-Pattern

**Problem**: Telling Claude what NOT to do is less effective than stating what TO do.

**Pattern**:
```
❌ BAD: "Do not use markdown"
✅ GOOD: "Respond with smoothly flowing prose paragraphs"

❌ BAD: "Don't write verbose code"
✅ GOOD: "Write concise, readable code with single-responsibility functions"

❌ BAD: "Avoid using global state"
✅ GOOD: "Use dependency injection with constructor parameters"
```

**Why**: Positive framing provides a clear target. Negative framing creates ambiguity.

---

## IV. STRUCTURED PROMPTS

### XML Tags: Best Practices

**Claude's Training**: Fine-tuned with XML tags in training data for structured recognition.

**Common Tags** (by use case):

#### Research/Analysis
```xml
<background_information>
<!-- Project context, domain knowledge -->
</background_information>

<research_objective>
<!-- What to discover/analyze -->
</research_objective>

<constraints>
<!-- Boundaries, limitations -->
</constraints>

<output_format>
<!-- Structure of deliverable -->
</output_format>
```

#### Coding Tasks
```xml
<codebase_context>
<!-- Tech stack, architecture, conventions -->
</codebase_context>

<task>
<!-- Specific change to implement -->
</task>

<requirements>
<!-- Functional requirements -->
</requirements>

<quality_standards>
<!-- Non-functional requirements -->
</quality_standards>

<testing_strategy>
<!-- Test coverage expectations -->
</testing_strategy>
```

#### Chain-of-Thought Reasoning
```xml
<thinking>
<!-- Space for Claude's reasoning -->
</thinking>

<answer>
<!-- Final response -->
</answer>
```

#### RAG/Document Analysis
```xml
<document>
<!-- Source material -->
</document>

<query>
<!-- Question about document -->
</query>

<instructions>
<!-- How to process/cite -->
</instructions>
```

**Tag Naming**:
- Use descriptive names (`<codebase_context>` not `<ctx>`)
- Match domain vocabulary (`<testing_strategy>` for test tasks)
- Be consistent across similar prompts

---

### Response Format Control

#### Prefilling Technique
```
User: "Generate database migration for users table"
Assistant (prefilled): """
-- Migration: Add email verification to users
-- Date: 2025-12-05

CREATE TABLE
```

**Effect**: Forces specific output format, skips preamble.

---

#### Style Matching
**Principle**: Prompt formatting influences response formatting.

```
❌ Markdown-heavy prompt → Markdown-heavy response
✅ Plain text prompt → Plain text response
```

**Minimal Markdown Guidance**:
```
"Use standard paragraph breaks for organization. Reserve markdown for:
 - `inline code`
 - Code blocks (```...```)
 - Simple headings (## Level 2 max)"
```

---

## V. THINKING CAPABILITIES (2025)

### Extended Thinking Budgets

**Triggers** (increasing budget):
1. `"think"` → Default (~4k tokens)
2. `"think hard"` → Medium (~16k tokens)
3. `"think harder"` → Large (~32k tokens)
4. `"ultrathink"` → Maximum (~64k tokens)

**When to Use**:
- **Complex architecture**: "Think hard about microservices decomposition strategy"
- **Security-critical**: "Think harder about authentication edge cases and attack vectors"
- **Deep refactoring**: "Ultrathink the migration from monolith to event-driven architecture"
- **Bug investigation**: "Think hard about root cause of race condition in payment processing"

**Example**:
```xml
<task>
Redesign the caching layer for 10x traffic growth.
</task>

<instructions>
Think harder about:
- Read-through vs write-through strategies
- Cache invalidation patterns
- Multi-region consistency
- Failure modes and fallbacks

Provide architecture diagram, implementation plan, and migration strategy.
</instructions>
```

---

### Critical: "Think" Sensitivity

**Problem**: When extended thinking is DISABLED, Claude Opus 4.5 is "particularly sensitive to the word 'think' and its variants."

**Solution**: Replace with synonyms if NOT using extended thinking.

**Alternatives**:
- `"think"` → `"consider"`, `"evaluate"`, `"analyze"`
- `"think about"` → `"examine"`, `"assess"`
- `"thought process"` → `"reasoning"`, `"analysis"`

---

### Reflection After Tool Use

**Pattern**: Encourage quality assessment of tool results before proceeding.

**Example**:
```
"After receiving tool results, carefully reflect on:
 - Are the results complete?
 - Are there errors or edge cases not covered?
 - What are optimal next steps?

 Then proceed with implementation."
```

**Why**: Prevents hasty actions based on incomplete or erroneous tool outputs.

---

## VI. TOOL ORCHESTRATION (2025)

### Parallel Execution (Critical for Performance)

**Claude 4.5 Capability**: Sonnet is "particularly aggressive in firing off multiple operations simultaneously."

**Directive**:
```
"If you intend to call multiple tools and there are no dependencies
 between the tool calls, make all of the independent tool calls in parallel."
```

**Example**:
```
Task: Analyze user authentication and payment processing modules

Parallel Tools:
- Read: src/auth/user_service.py
- Read: src/payments/stripe_integration.py
- Grep: "def authenticate" (find auth patterns)
- Grep: "def process_payment" (find payment patterns)

Sequential (after reads complete):
- Analyze combined findings
- Generate recommendations
```

**Anti-Pattern**: Sequential tool calls when parallelization is possible.

---

### Explicit Action Directives

**Problem**: Claude 4.5 requires explicit permission to implement changes.

**Patterns**:

#### Proactive Mode
```
"Implement changes rather than only suggesting them.
 After analysis, directly refactor the code."
```

#### Conservative Mode
```
"Do not jump into implementation unless clearly instructed.
 Provide analysis and recommendations first."
```

**Default**: Conservative. User must enable proactive mode explicitly.

---

## VII. ANTI-PATTERNS (2025)

### 1. Over-Specification

**Definition**: Excessively detailed, step-by-step instructions.

**Problem**: Claude 4.5 performs better with high-level guidance than prescriptive checklists.

**Evidence**: prompt-engineer.md refactored from 738 → 150 lines by removing over-specification.

**Example**:
```
❌ BAD (over-specified):
"Step 1: Open user_service.py
 Step 2: Read lines 42-57
 Step 3: Check if function validate_email exists
 Step 4: If exists, proceed to step 5, else go to step 12
 Step 5: Analyze parameter types..."
 [700 more lines]

✅ GOOD (high-level guidance):
"Refactor user_service.py authentication logic to use dependency injection.
 Follow SOLID principles. Ensure 90%+ test coverage. Maintain API compatibility."
```

**Guideline**: Provide goals, constraints, and quality standards. Let Claude determine implementation steps.

---

### 2. Generic Prompts

**Definition**: Vague instructions that apply to any project.

**Examples**:
```
❌ "Make the code better"
❌ "Fix the bug"
❌ "Improve performance"
❌ "Add error handling"
```

**Solution**: Specific, measurable, contextualized instructions.

```
✅ "Reduce get_user_dashboard() from 800ms to <200ms by adding database indexes
   on users.created_at and orders.status columns."

✅ "Fix race condition in payment processing where concurrent requests create
   duplicate charges. Add database transaction with SELECT FOR UPDATE."

✅ "Add error handling to API endpoints:
   - 400 for validation errors (return field-level messages)
   - 401 for authentication failures
   - 500 for system errors (log stack trace, return generic message)"
```

---

### 3. Cache Invalidation

**Problem**: Frequently changing parts of prompts that should be cached.

**Cache Efficiency**: Properly structured prompts achieve ~90% token savings.

**Pattern**:
```
[SYSTEM PROMPT - Cached, Stable]
- Role definition
- Core instructions
- Quality standards
- Examples

[USER MESSAGE - Variable, Not Cached]
- Specific task
- File contents
- User input
- Dynamic data
```

**Anti-Pattern**:
```
❌ Putting file contents in system prompt
❌ Changing system prompt per request
❌ Including timestamps in cached sections
```

---

### 4. Test-Driven Hard-Coding

**Definition**: Implementing solutions that ONLY pass specific test cases without generalizing.

**Example**:
```
❌ BAD:
def calculate_discount(price):
    if price == 100:
        return 10  # Passes test: calculate_discount(100) == 10
    return 0       # Fails on any other price

✅ GOOD:
def calculate_discount(price):
    if price >= 100:
        return price * 0.1  # 10% discount for orders >= $100
    return 0
```

**Directive**:
```
"Implement high-quality, general-purpose solutions rather than focusing
 solely on passing specific test cases. Consider edge cases and real-world
 usage patterns beyond the provided tests."
```

---

### 5. Mixing Refactoring with Features

**Problem**: Combining refactoring and feature development in single task.

**Why Bad**:
- Difficult to review changes
- Higher risk of regressions
- Unclear cause if tests fail

**Solution**:
```
"Never mix refactoring with feature work.

Phase 1: Refactor existing code
- Run tests before and after
- Ensure no behavior changes
- Commit refactoring separately

Phase 2: Add new features
- Build on refactored foundation
- Add tests for new behavior
- Commit feature separately"
```

---

## VIII. DOMAIN-SPECIFIC PATTERNS

### Agentic Coding

#### Code Exploration Protocol
```
"ALWAYS read and understand relevant files before proposing code edits.
 Do not speculate about code you have not inspected.

 Workflow:
 1. Use grep/search to find relevant files
 2. Read files to understand current implementation
 3. Analyze architecture and patterns
 4. Propose changes based on actual code
 5. Never guess about APIs, interfaces, or conventions"
```

#### Hallucination Prevention
```
"Never speculate about code you have not opened.

 If asked about code functionality:
 - Investigate files first
 - Read actual implementation
 - Base answers on evidence
 - State 'I need to read X file' if information is missing"
```

#### Minimal Engineering
```
"Avoid over-engineering.

 Only make changes that are:
 - Directly requested by user
 - Clearly necessary for functionality
 - Justified by requirements

 Do NOT:
 - Add unrequested features
 - Refactor unrelated code
 - Introduce new patterns without reason
 - Make 'improvements' beyond scope"
```

---

### Frontend Design

**Problem**: Claude 4.5 risks converging toward generic "AI slop" aesthetics.

**Solution**: Explicit design guidance.

```xml
<design_requirements>
**Typography**: Use unique fonts. Avoid Arial, Inter, Helvetica.
Consider: Geist, Söhne, Space Grotesk for modern feel.

**Color Scheme**: Create cohesive palette.
- Dominant color (70% of design)
- Secondary color (20%)
- Sharp accent color for CTAs (10%)

**Animations**: Purposeful motion for key moments.
- Page transitions
- Button interactions
- Loading states
Avoid: Gratuitous animations, carousel auto-play

**Backgrounds**: Atmospheric depth.
- Subtle gradients
- Geometric patterns
- Textured overlays
Avoid: Flat solid colors, stock photos

**Character**: Context-specific design language.
- Match brand identity
- Reflect product purpose
- Create memorable experience
Avoid: Cookie-cutter layouts, generic templates
</design_requirements>
```

---

### Research & Analysis

**Structured Research Protocol**:
```xml
<research_framework>
**Success Criteria**: Define what "complete" research looks like.
- Specific questions to answer
- Data to collect
- Analysis to perform

**Source Verification**: Cross-reference across multiple sources.
- Primary sources (documentation, code)
- Secondary sources (articles, discussions)
- Flag contradictions

**Competing Hypotheses**: Consider multiple explanations.
- Hypothesis A: [explanation]
- Hypothesis B: [alternative]
- Evidence for/against each

**Confidence Tracking**: Rate certainty of findings.
- High confidence: Multiple sources, direct evidence
- Medium confidence: Single source, indirect evidence
- Low confidence: Speculation, unclear evidence

**Persistent Notes**: Update structured files for state tracking.
- findings.json (structured results)
- progress.md (narrative updates)
- questions.md (unresolved items)
</research_framework>
```

---

## IX. LONG-HORIZON REASONING (2025)

### Context Window Management

**Claude 4.5 Capability**: Tracks remaining token budget throughout conversation.

**Multi-Window Strategy**:
```
Window 1 (Setup):
- Establish framework (test harness, linters, scripts)
- Define project structure
- Create quality-of-life tools
- Document conventions

Window 2-N (Execution):
- Implement features incrementally
- Use git for state tracking
- Write tests in JSON format for persistence
- Start fresh windows when context is full
- Avoid relying solely on compaction
```

---

### State Tracking

**Formats**:
- **Structured (JSON)**: Test results, metrics, status
- **Unstructured (Markdown)**: Progress notes, decisions, context
- **Git**: Source of truth for code changes

**Example**:
```json
// test_results.json (structured)
{
  "test_suite": "authentication",
  "total": 47,
  "passed": 45,
  "failed": 2,
  "failures": [
    {"test": "test_oauth_token_refresh", "error": "Timeout after 30s"},
    {"test": "test_mfa_backup_codes", "error": "Invalid code format"}
  ],
  "coverage": "94%",
  "timestamp": "2025-12-05T10:30:00Z"
}
```

```markdown
# progress.md (unstructured)

## 2025-12-05 Session 2

Implemented OAuth2 token refresh. Tests mostly pass but timeout issue
in test_oauth_token_refresh suggests race condition in refresh logic.

Next steps:
- Add logging to token refresh endpoint
- Increase timeout or mock external OAuth provider
- Review MFA backup code validation (format mismatch)
```

---

## X. MIGRATION GUIDE (Claude 3.x → 4.5)

### Required Changes

| **Aspect** | **Claude 3.x** | **Claude 4.5** |
|------------|----------------|----------------|
| **Emojis** | Common, decorative | Forbidden unless user requests |
| **Verbosity** | Celebratory, verbose | Direct, fact-based, concise |
| **Specificity** | Moderate detail | High detail, explicit instructions |
| **Examples** | Moderate influence | High scrutiny, strong influence |
| **Thinking** | Implicit reasoning | Explicit budgets ("think hard") |
| **Tool Calls** | Sequential default | Parallel default |
| **Prompts** | Prescriptive steps | High-level guidance |
| **Communication** | Conversational | Professional, minimal |

---

### Refactoring Checklist

#### Phase 1: Content Audit
- [ ] **Identify all prompts**: System prompts, agents, skills, CLAUDE.md
- [ ] **Categorize by type**: Instructions, examples, context, constraints
- [ ] **Assess token usage**: Measure current vs. target after refactoring

#### Phase 2: Anti-Pattern Removal
- [ ] **Remove ALL emojis**: Search and destroy 🎯 → Goal
- [ ] **Convert negative instructions**: "Don't X" → "Do Y"
- [ ] **Eliminate over-specification**: 700 lines → high-level guidance
- [ ] **Remove generic instructions**: "Make better" → specific criteria
- [ ] **Fix cache-hostile patterns**: Move variable data out of system prompts

#### Phase 3: Structure Addition
- [ ] **Add XML tags**: Multi-section prompts get `<section>` tags
- [ ] **Add markdown headers**: Simple prompts get `##` structure
- [ ] **Organize by priority**: Critical instructions first
- [ ] **Separate concerns**: Context, task, requirements, constraints

#### Phase 4: Clarity Enhancement
- [ ] **Make implicit explicit**: Add details that Claude 3.x inferred
- [ ] **Add context/motivation**: Explain WHY, not just WHAT
- [ ] **Improve examples**: Ensure alignment with desired behavior
- [ ] **Define success criteria**: Measurable outcomes

#### Phase 5: Claude 4.5 Optimization
- [ ] **Enable extended thinking**: Add "think hard" for complex tasks
- [ ] **Request parallel tools**: "Call independent tools in parallel"
- [ ] **Add reflection prompts**: "After tool results, reflect on quality"
- [ ] **Optimize for cache**: Stable content in system, variable in user

#### Phase 6: Validation
- [ ] **Test prompts**: Run against representative tasks
- [ ] **Measure improvements**: Compare output quality, token usage
- [ ] **Iterate**: Refine based on results
- [ ] **Document changes**: Track before/after metrics

---

### Before/After Example

#### Before (Claude 3.x style)
```
🎯 Hey Claude! Let's make our authentication system super secure! 🔐

Here's what we need:
- Add some OAuth stuff
- Make sure it's safe
- Write tests

Be creative and do your best! 💪✨
```

**Problems**:
- Emojis (🎯🔐💪✨)
- Vague instructions ("some OAuth stuff")
- No specifics ("make sure it's safe")
- Generic request ("write tests")
- Celebratory tone

---

#### After (Claude 4.5 style)
```xml
<codebase_context>
Tech stack: Django 4.2, PostgreSQL, Redis
Current auth: Session-based with username/password
Libraries: django-allauth (social auth), djangorestframework-simplejwt
</codebase_context>

<task>
Implement OAuth2 authentication with Google and GitHub providers.
Maintain backward compatibility with existing session auth.
</task>

<requirements>
**OAuth Flow**:
- Authorization code grant with PKCE
- JWT tokens (access: 1 hour, refresh: 30 days)
- Store tokens in Redis with user session key

**Providers**:
- Google: OAuth 2.0 (client ID/secret in env vars)
- GitHub: OAuth 2.0 (separate client ID/secret)

**Security**:
- Validate state parameter (CSRF protection)
- Verify JWT signatures
- Rate limit: 5 auth attempts per minute per IP
- Log all authentication events (user_id, provider, timestamp, IP)

**API Endpoints**:
- POST /auth/oauth/google/login → Redirect to Google
- POST /auth/oauth/github/login → Redirect to GitHub
- GET /auth/oauth/callback → Handle provider callback, issue JWT

**Error Handling**:
- 400: Invalid OAuth state/code
- 401: Authentication failed
- 429: Rate limit exceeded
- 500: Provider unavailable (log error, show generic message)
</requirements>

<testing_strategy>
Unit tests:
- Token generation and validation
- State parameter creation/verification
- Rate limiting logic

Integration tests:
- OAuth flow with mocked provider responses
- Token refresh flow
- Session migration (existing users)

Coverage target: 90%+ for auth module
</testing_strategy>

<constraints>
- No changes to existing session auth (parallel systems)
- No database migrations (use existing User model)
- No frontend changes (API only)
- Complete within current Django version (no upgrades)
</constraints>
```

**Improvements**:
- ✅ No emojis
- ✅ Explicit, detailed requirements
- ✅ XML structure for organization
- ✅ Context provided (tech stack, current state)
- ✅ Security specifics (PKCE, rate limiting, logging)
- ✅ Testing strategy defined
- ✅ Constraints documented
- ✅ Professional tone

---

## XI. QUALITY CRITERIA

### Good Prompt Checklist

A high-quality Claude 4.5 prompt exhibits:

✅ **Clarity**: Unambiguous, explicit instructions
✅ **Structure**: XML tags or markdown headers organize sections
✅ **Context**: Explains WHY and provides background
✅ **Specificity**: Detailed about inputs, outputs, success criteria
✅ **Examples**: Aligned with desired behavior, minimal noise
✅ **Efficiency**: Cache-friendly structure (stable + variable separation)
✅ **Actionability**: Clear success criteria and measurable outcomes
✅ **Professional**: No emojis, no celebratory language, fact-based
✅ **Appropriate Detail**: High-level guidance for complex tasks, specifics for narrow tasks
✅ **Tool Optimization**: Requests parallel execution where applicable

---

### Bad Prompt Warning Signs

A low-quality prompt exhibits:

❌ **Vagueness**: "Make it better," "Fix the code"
❌ **Over-Specification**: 700+ lines of step-by-step micro-instructions
❌ **Emojis**: Decorative, unprofessional symbols
❌ **Negative Framing**: "Don't do X" instead of "Do Y"
❌ **Generic**: Could apply to any project, no context
❌ **Cache-Hostile**: Variable data in system prompt
❌ **Implicit Assumptions**: Relies on Claude inferring requirements
❌ **No Success Criteria**: Unclear when task is complete
❌ **Celebratory Tone**: "Amazing!" "Wonderful!" "Let's do this! 🚀"
❌ **Missing Examples**: Or examples misaligned with desired behavior

---

### Evaluation Framework

Use this rubric to score prompts (1-5 scale, 5 = excellent):

| **Criterion** | **1 (Poor)** | **3 (Acceptable)** | **5 (Excellent)** |
|---------------|--------------|-------------------|------------------|
| **Clarity** | Ambiguous | Some details | Explicit, unambiguous |
| **Structure** | Unorganized prose | Some headers | XML/markdown sections |
| **Context** | No background | Basic context | Full context + motivation |
| **Specificity** | Vague | Moderate detail | Precise, measurable |
| **Examples** | None or misaligned | Basic examples | Perfect alignment |
| **Efficiency** | Cache-hostile | Partially optimized | 90%+ cache hit |
| **Tone** | Emojis, celebratory | Neutral | Professional, direct |
| **Actionability** | No success criteria | Implied criteria | Explicit, measurable |

**Target**: Average score ≥ 4.0 for production prompts.

---

## XII. WORKFLOW INTEGRATION

### PM → Prompt-Engineer Delegation

**Trigger Keywords** (PM recognizes prompt work):
- "update instructions"
- "refactor prompt"
- "optimize agent"
- "improve system prompt"
- "modify PM_INSTRUCTIONS"
- "update skill definition"
- "enhance CLAUDE.md"

**Delegation Message**:
```
Delegating to prompt-engineer agent for instruction optimization.

Context:
- Target file: [path]
- Current issue: [description]
- Desired outcome: [goal]

Please analyze and refactor according to Claude 4.5 best practices.
```

---

### Prompt-Engineer Workflow

1. **Analyze Current Prompt**:
   - Read target file
   - Identify anti-patterns
   - Score using evaluation framework
   - Document gaps

2. **Research Context** (if needed):
   - Review codebase conventions
   - Check related prompts for consistency
   - Consult Claude 4.5 documentation

3. **Refactor**:
   - Remove anti-patterns (emojis, negative instructions)
   - Add structure (XML/markdown)
   - Increase specificity
   - Add context/motivation
   - Optimize for cache

4. **Validate**:
   - Compare before/after token usage
   - Test with representative tasks
   - Ensure no regression in functionality
   - Measure improvement

5. **Document**:
   - Changelog entry
   - Migration notes if breaking changes
   - Improvement metrics (token savings, quality score)

6. **Deliver**:
   - Submit refactored prompt
   - Provide summary of changes
   - Recommend testing approach

---

## XIII. ADVANCED TECHNIQUES

### Prompt Chaining

**Definition**: Breaking complex tasks into sequential prompts.

**When to Use**:
- Multi-step workflows (research → plan → implement)
- Intermediate validation needed
- Progressive refinement

**Pattern**:
```
Prompt 1: Research
"Analyze existing authentication implementations in the codebase.
 Document patterns, libraries, and conventions."

↓ (results inform next prompt)

Prompt 2: Design
"Based on research findings, design OAuth2 integration that follows
 existing patterns. Provide architecture diagram and API spec."

↓ (design reviewed and approved)

Prompt 3: Implementation
"Implement the OAuth2 design from previous step. Follow TDD approach."
```

---

### Meta Few-Shot Learning

**Anthropic Recommendation**: Pair one perfect example with one annotated mistake.

**Pattern**:
```xml
<examples>
<good_example>
Input: "Optimize database query performance"
Output:
"""
Added composite index on (user_id, created_at) to users table.
Query time reduced from 800ms to 45ms (94% improvement).
Verified with EXPLAIN ANALYZE. No breaking changes to API.
"""
</good_example>

<bad_example>
Input: "Optimize database query performance"
Output:
"""
Made the queries super fast! 🚀 You're going to love the new performance! ✨
"""

Why this is bad:
- No specifics (what optimization?)
- No metrics (how much improvement?)
- Emojis and celebratory tone
- No verification method mentioned
</bad_example>
</examples>
```

**Why Effective**: Claude internalizes both desired structure AND error boundaries.

---

### Progressive Disclosure

**Definition**: Revealing detailed instructions only when relevant.

**Claude Code Pattern**: Skills don't inflate every request; Claude loads fuller skill context only when it determines relevance.

**Implementation**:
```
High-level prompt (always visible):
"You are an expert Python engineer following PEP 8 standards."

Detailed guidance (loaded on-demand):
- When task mentions "async": Load async/await best practices
- When task mentions "security": Load security checklist
- When task mentions "testing": Load TDD workflow
```

**Tool**: Use conditional sections or separate skill files.

---

## XIV. TROUBLESHOOTING

### Prompt Not Working?

**Debug Checklist**:

1. **Is it specific enough?**
   - ❌ "Add error handling"
   - ✅ "Add try/except blocks for database operations with specific error messages"

2. **Are examples aligned?**
   - Review examples for unintended patterns
   - Remove examples that contradict instructions

3. **Is structure clear?**
   - Add XML tags if multi-section
   - Use markdown headers for clarity

4. **Is context provided?**
   - Explain WHY, not just WHAT
   - Include background information

5. **Are there anti-patterns?**
   - Emojis? Remove them.
   - Negative instructions? Convert to positive.
   - Over-specification? Simplify to high-level guidance.

6. **Is cache optimized?**
   - Stable content in system prompt
   - Variable content in user message

7. **Is extended thinking needed?**
   - Add "think hard" for complex tasks
   - Ensure thinking budget matches complexity

---

### Common Issues and Solutions

| **Issue** | **Cause** | **Solution** |
|-----------|-----------|--------------|
| Claude misunderstands task | Vague instructions | Add specificity and examples |
| Claude over-engineers | No constraints | Add "minimal changes" constraint |
| Claude skips steps | Implicit workflow | Make workflow explicit |
| Claude uses wrong style | Examples mismatch | Align examples with desired style |
| High token usage | Poor cache structure | Separate stable/variable content |
| Verbose output | Prompt tone | Use direct, fact-based language |
| Generic solutions | No context | Add domain/project context |

---

## XV. REFERENCES

### Primary Sources
1. [Anthropic Claude 4.x Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
2. [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
3. [Anthropic XML Tags Guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
4. [Claude 4 System Prompt](https://simonwillison.net/2025/May/25/claude-4-system-prompt/)

### Secondary Sources
5. [Claude Code System Prompt Changes](https://mikhail.io/2025/09/sonnet-4-5-system-prompt-changes/)
6. [Anthropic System Prompt Updates](https://blog.promptlayer.com/what-we-can-learn-from-anthropics-system-prompt-updates/)
7. [Claude Code Internals](https://minusx.ai/blog/decoding-claude-code/)
8. [CLAUDE.md Best Practices](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)

---

## XVI. VERSION HISTORY

### v4.0.0 (2025-12-05)
- **Created**: Comprehensive BASE_PROMPT_ENGINEER.md knowledge base
- **Added**: Anti-patterns section (emojis, over-specification, negative instructions)
- **Added**: Communication style guide (fact-based, no emojis)
- **Added**: Authority statement (THE agent for prompt work)
- **Added**: Quality evaluation framework
- **Added**: Migration guide (Claude 3.x → 4.5)
- **Added**: Workflow integration (PM delegation protocol)
- **Added**: Advanced techniques (prompt chaining, meta few-shot, progressive disclosure)
- **Added**: Troubleshooting guide

### v3.0.0 (2025-11-25)
- Refactored prompt-engineer.md from 738 → 150 lines
- Demonstrated anti-over-specification principle
- Referenced (but didn't create) BASE_PROMPT_ENGINEER.md

### v2.0.0 (2025-10-03)
- Claude 4.5 best practices integration
- Extended thinking support
- Multi-model routing
- Tool orchestration patterns

### v1.0.0 (2025-09-18)
- Initial prompt-engineer agent template

---

**End of BASE_PROMPT_ENGINEER.md**
