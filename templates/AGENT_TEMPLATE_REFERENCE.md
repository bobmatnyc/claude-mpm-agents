# Agent Template Reference Guide

## Overview

This is the **single comprehensive reference** for creating Claude Code agents manually. Claude Code does **not support template inheritance** (no `extends:` or `base:` fields), so this document serves as a style guide and pattern reference for authoring agents.

**How to Use This Guide:**
1. Copy the complete template structure below
2. Fill in your agent-specific details
3. Follow the best practices and examples from top-performing agents
4. Reference the "Real Examples" section for patterns from production agents

---

## Complete Template Structure

```yaml
---
# ============================================================================
# REQUIRED METADATA FIELDS
# ============================================================================

name: agent-name                          # REQUIRED: Use kebab-case (lowercase-with-hyphens)
                                          # Examples: python-engineer, research-agent, product-owner

description: |                            # REQUIRED: Clear, concise description (1-2 sentences)
  Single-line description of what this agent does.
  Can span multiple lines for clarity.

version: 1.0.0                            # REQUIRED: Semantic versioning (MAJOR.MINOR.PATCH)
                                          # Increment MAJOR for breaking changes, MINOR for features, PATCH for fixes

schema_version: 1.3.0                     # REQUIRED: Current agent schema version (use 1.3.0)

agent_id: agent-name                      # REQUIRED: Must match 'name' field exactly

agent_type: engineer                      # REQUIRED: One of: engineer, qa, ops, research, product, specialized
                                          # This determines agent behavior and routing patterns

# ============================================================================
# OPTIONAL METADATA FIELDS
# ============================================================================

model: sonnet                             # OPTIONAL: AI model to use (sonnet, opus, haiku)
                                          # Default: sonnet (recommended for most agents)

resource_tier: standard                   # OPTIONAL: Resource allocation (standard, high, low)
                                          # Default: standard
                                          # Use 'high' for memory-intensive research agents

tags:                                     # OPTIONAL: Keywords for discovery and routing
  - tag1                                  # Use lowercase, hyphenated format
  - tag2                                  # Examples: python, typescript, testing, devops
  - tag3                                  # Be specific and relevant to agent capabilities

category: engineering                     # OPTIONAL: High-level category (engineering, testing, operations, research, product)

color: green                              # OPTIONAL: UI color hint (green, blue, purple, orange, red, yellow)

author: Your Name or Team                 # OPTIONAL: Attribution for agent creation

temperature: 0.2                          # OPTIONAL: LLM temperature (0.0-1.0)
                                          # Lower = more deterministic (0.2 for code)
                                          # Higher = more creative (0.3-0.5 for product/research)

max_tokens: 4096                          # OPTIONAL: Maximum response tokens (default: 4096)
                                          # Research agents may use 16384 for longer analysis

timeout: 900                              # OPTIONAL: Task timeout in seconds (default: 900 = 15 min)
                                          # Increase for long-running operations (1800 = 30 min)

# ============================================================================
# CAPABILITIES (Resource Limits)
# ============================================================================

capabilities:
  memory_limit: 2048                      # OPTIONAL: Memory limit in MB (default: 2048)
  cpu_limit: 50                           # OPTIONAL: CPU percentage (default: 50)
  network_access: true                    # OPTIONAL: Whether agent needs network (default: true)

# ============================================================================
# DEPENDENCIES
# ============================================================================

dependencies:
  python:                                 # Python package dependencies
    - package-name>=version               # Examples: pytest>=8.0.0, black>=24.0.0
    - another-package>=version

  system:                                 # System-level dependencies
    - python3.12+                         # Examples: python3.12+, node18+, docker
    - git

  optional: false                         # Whether dependencies are optional (default: false)

# ============================================================================
# SKILLS (Claude Code Skills)
# ============================================================================

skills:                                   # OPTIONAL: Claude Code skills this agent uses
  - test-driven-development               # Examples from obra/superpowers, alirezarezvani/claude-skills
  - systematic-debugging                  # Skills are loaded at Claude Code STARTUP only
  - async-testing

# ============================================================================
# CHANGELOG (Version History)
# ============================================================================

template_version: 1.0.0                   # RECOMMENDED: Template version for tracking

template_changelog:                       # RECOMMENDED: Document all version changes
  - version: 1.0.0
    date: '2025-11-30'                    # YYYY-MM-DD format
    description: 'Initial release with core capabilities'

  - version: 1.1.0
    date: '2025-12-15'
    description: 'Added feature X and enhanced Y for better Z'

# ============================================================================
# KNOWLEDGE (Agent Expertise)
# ============================================================================

knowledge:
  domain_expertise:                       # What this agent knows and specializes in
    - Topic 1: Specific area of expertise
    - Topic 2: Another specialized area
    - Topic 3: Technical patterns and practices

  best_practices:                         # How this agent operates
    - Best practice 1 with clear actionable guidance
    - Best practice 2 with specific examples
    - "Use quotes for multi-line or special characters"

  constraints:                            # Hard requirements and limitations
    - MUST do X when Y condition
    - SHOULD prefer A over B
    - NEVER do Z under any circumstances

  examples:                               # Real-world usage scenarios (optional but recommended)
    - scenario: Creating type-safe service
      approach: Define interface, implement with patterns, add tests
    - scenario: Optimizing slow operation
      approach: Profile first, identify bottleneck, apply targeted optimization

# ============================================================================
# INTERACTIONS (Input/Output Specs)
# ============================================================================

interactions:
  input_format:
    required_fields:                      # Fields user must provide
      - task                              # Example: task description

    optional_fields:                      # Fields user may provide
      - context                           # Example: additional context
      - constraints                       # Example: specific requirements

  output_format:
    structure: markdown                   # Output format (markdown, json, code)
    includes:                             # What's included in output
      - analysis
      - recommendations
      - code_examples

  handoff_agents:                         # Agents this can delegate to
    - engineer
    - qa
    - research

  triggers:                               # Keywords that activate this agent
    - keyword 1
    - keyword 2
    - "multi-word trigger phrase"

# ============================================================================
# MEMORY ROUTING (What This Agent Remembers)
# ============================================================================

memory_routing:
  description: High-level summary of what this agent stores in memory

  categories:                             # Memory organization categories
    - Category 1: Type of information stored
    - Category 2: Another information type
    - Category 3: Specific patterns and decisions

  keywords:                               # Keywords for memory recall
    - keyword1
    - keyword2
    - multi-word-keyword

  paths:                                  # File paths this agent works with
    - src/
    - tests/
    - "*.py"                              # Glob patterns supported

  extensions:                             # File extensions this agent handles
    - .py
    - .ts
    - .md

---

# Agent Name

## Identity
[Brief paragraph describing agent's core purpose and specialization]

## When to Use Me
- Use case 1: Specific scenario and value
- Use case 2: When this agent adds most value
- Use case 3: Key differentiator from other agents

## Core Capabilities

### Capability 1: [Name]
[Description of this capability with details]

**Key Features:**
- Feature A with explanation
- Feature B with benefits
- Feature C with examples

### Capability 2: [Name]
[Another major capability area]

**Important Notes:**
- Critical consideration 1
- Important pattern 2
- Best practice 3

## Knowledge Areas

### Domain Expertise
What this agent knows deeply:
- Expertise area 1 with depth
- Expertise area 2 with breadth
- Expertise area 3 with practical application

### Best Practices
How this agent operates effectively:
1. **Practice 1**: Clear actionable guidance
2. **Practice 2**: Specific implementation details
3. **Practice 3**: Measurable outcomes

### Constraints
Hard limits and requirements:
- ❌ **NEVER**: Things to absolutely avoid
- ✅ **ALWAYS**: Non-negotiable requirements
- ⚠️ **CAUTION**: Areas requiring careful consideration

## Common Patterns

### Pattern 1: [Scenario Name]
```[language]
# Example code showing pattern
# Include comments explaining key concepts
# Show best practices in action
```

**When to Use**: Specific conditions that trigger this pattern

**Benefits**: Clear value proposition

### Pattern 2: [Another Scenario]
```[language]
# Another practical example
# With inline documentation
# Demonstrating correct approach
```

**Anti-Pattern** (what NOT to do):
```[language]
# Wrong approach
# Why this is problematic
# What to do instead
```

## Quality Standards

### Standard 1: [Area]
- Metric 1: Measurable criterion
- Metric 2: Specific threshold
- Metric 3: Success indicator

### Standard 2: [Another Area]
- Requirement A with justification
- Requirement B with examples
- Requirement C with enforcement

## Integration Points

**Works With:**
- **Agent Type 1**: How they collaborate, what's handed off
- **Agent Type 2**: Workflow integration, shared responsibilities
- **Agent Type 3**: Communication patterns, dependencies

## Success Metrics

**Effectiveness Measures:**
- Metric 1: Specific KPI with target
- Metric 2: Quality indicator with threshold
- Metric 3: Performance benchmark with goal

## Memory Categories

**What This Agent Remembers:**
- Category 1: Type of information and why it matters
- Category 2: Patterns and decisions to recall
- Category 3: Context for future operations

---

```

## Best Practices for Agent Authoring

### Metadata Best Practices

**Naming Conventions:**
- Use kebab-case for `name` and `agent_id` (e.g., `python-engineer`, `research-agent`)
- Keep names concise but descriptive (2-3 words maximum)
- Avoid redundant suffixes like `-agent` unless needed for clarity

**Version Management:**
- Follow semantic versioning: MAJOR.MINOR.PATCH
- Increment MAJOR for breaking changes (behavior changes, removed features)
- Increment MINOR for new features (added capabilities, new patterns)
- Increment PATCH for bug fixes (corrections, clarifications)
- Always update `template_changelog` with each version

**Description Writing:**
- Keep to 1-2 sentences, max 150 characters
- Focus on unique value and key differentiators
- Use active voice and specific terminology
- Example: "Python 3.12+ specialist delivering type-safe, async-first code with SOA patterns"

### Knowledge Section Best Practices

**Domain Expertise:**
- List specific technologies, frameworks, versions
- Include both breadth (what areas) and depth (how deep)
- Prioritize most important/frequently used knowledge first
- Example: "Python 3.12-3.13 features (JIT, free-threaded, TypeForm)"

**Best Practices Structure:**
- Start with MANDATORY practices using strong language (MUST, ALWAYS, NEVER)
- Follow with RECOMMENDED practices (SHOULD, PREFER)
- Include context for when practices apply
- Use measurable criteria when possible
- Example: "MUST achieve 100% type coverage (mypy --strict)"

**Constraints Clarity:**
- Separate hard requirements (MUST/NEVER) from soft guidelines (SHOULD)
- Explain WHY for non-obvious constraints
- Provide concrete examples or thresholds
- Link constraints to quality standards
- Example: "HARD LIMIT: Maximum 3-5 files via Read tool PER ENTIRE SESSION - NON-NEGOTIABLE"

### Examples Section Best Practices

**Scenario-Based Examples:**
```yaml
examples:
  - scenario: Clear, specific situation description
    approach: Step-by-step approach with concrete actions
```

**Good Examples:**
- Scenario: "Optimizing slow data processing"
- Approach: "Profile with cProfile, identify bottlenecks, implement caching, use async for I/O, benchmark improvements"

**What Makes Examples Effective:**
- Concrete scenarios users will actually encounter
- Actionable step-by-step guidance
- Tools and techniques mentioned by name
- Measurable outcomes or success criteria

### Changelog Best Practices

**Writing Good Changelog Entries:**
```yaml
template_changelog:
  - version: 1.2.0
    date: '2025-11-30'
    description: 'CATEGORY: Brief summary. Detailed explanation of changes, impact, and reasoning. What problems this solves or features it adds.'
```

**Categories to Use:**
- **MAJOR**: Breaking changes, architecture shifts
- **FEATURE**: New capabilities added
- **ENHANCEMENT**: Improvements to existing features
- **FIX**: Bug fixes and corrections
- **OPTIMIZATION**: Performance improvements
- **INTEGRATION**: New tool or system integrations

**Good Changelog Example** (from research-agent):
```yaml
- version: 2.9.0
  date: '2025-11-25'
  description: 'MCP-SKILLSET INTEGRATION: Added optional mcp-skillset MCP server integration for enhanced research capabilities. Research agent now detects and leverages skill-based tools (web_search, code_analysis) as supplementary research layer when available.'
```

### Content Section Best Practices

**Structure for Clarity:**
1. Start with Identity: Brief 1-2 sentence introduction
2. When to Use Me: Bulleted list of specific use cases
3. Core Capabilities: Major sections with subsections
4. Common Patterns: Code examples with explanations
5. Quality Standards: Measurable criteria
6. Integration Points: How this works with other agents

**Writing Style:**
- Use active voice and imperative mood
- Be specific and concrete, avoid vague language
- Include code examples for technical agents
- Provide decision trees or flowcharts for complex logic
- Use visual hierarchy: headings, bullets, code blocks

**Code Examples:**
```python
# Good Example: Includes context and explanation
def process_data(data: list[dict]) -> list[str]:
    """Process user data with validation.

    This pattern demonstrates:
    1. Type hints for clarity
    2. Pydantic validation at boundaries
    3. Error handling with specific exceptions
    """
    validated = [UserSchema.parse_obj(item) for item in data]
    return [user.email for user in validated if user.active]
```

**Anti-Patterns:**
Always show both ❌ wrong and ✅ correct approaches:
```python
# ❌ WRONG - Bare except catches everything
try:
    risky_operation()
except:
    pass

# ✅ CORRECT - Specific exception with logging
try:
    risky_operation()
except ValueError as e:
    logger.exception("Operation failed: %s", e)
    raise
```

---

## Real Examples from Top-Performing Agents

### Example 1: Python Engineer (Excellent Knowledge Structure)

**What Makes It Good:**
- Clear domain expertise with specific versions (Python 3.12-3.13)
- Measurable best practices (100% type coverage, 90%+ test coverage)
- Strong constraints with enforcement language (MUST, SHOULD)
- Concrete examples with code patterns

**Key Patterns to Adopt:**
```yaml
knowledge:
  domain_expertise:
    - Python 3.12-3.13 features (JIT, free-threaded, TypeForm)
    - Service-oriented architecture with ABC interfaces
    - 'Common algorithm patterns: sliding window, BFS/DFS, binary search'

  best_practices:
    - Search-first for complex problems and latest patterns
    - 100% type coverage with mypy --strict
    - Profile before optimizing (avoid premature optimization)

  constraints:
    - MUST use WebSearch for medium-complex problems
    - MUST achieve 100% type coverage (mypy --strict)
    - SHOULD optimize only after profiling
```

### Example 2: Research Agent (Excellent Changelog)

**What Makes It Good:**
- Detailed version history with clear categorization
- Explains WHY changes were made, not just WHAT changed
- Links versions to specific improvements and outcomes
- Uses version numbers to track major feature additions

**Changelog Pattern:**
```yaml
template_changelog:
  - version: 2.9.0
    date: '2025-11-25'
    description: 'MCP-SKILLSET INTEGRATION: Added optional mcp-skillset MCP server integration for enhanced research capabilities. Includes decision trees, tool selection strategy, graceful degradation when unavailable.'

  - version: 2.8.0
    date: '2025-11-23'
    description: 'TICKET-FIRST WORKFLOW ENFORCEMENT: Made ticket attachment MANDATORY when ticket context exists. Strengthened imperatives, clear decision tree, non-blocking failure handling.'
```

### Example 3: Product Owner (Excellent Examples)

**What Makes It Good:**
- Scenario-based examples with clear context
- Step-by-step approach with specific actions
- Multiple scenarios covering different use cases
- Actionable guidance with framework references

**Examples Pattern:**
```yaml
examples:
  - scenario: Evaluate feature request from stakeholder
    approach: Search for prioritization best practices, apply RICE framework, gather user evidence through interviews, analyze data, calculate RICE score, recommend based on evidence, document decision rationale

  - scenario: Plan quarterly roadmap
    approach: Search for roadmap best practices 2025, review OKRs, gather user insights, create opportunity solution tree, prioritize with RICE, organize in Now-Next-Later format
```

### Example 4: Research Agent (Excellent Content Structure)

**What Makes It Good:**
- Clear Identity section establishing purpose
- Comprehensive "When to Use Me" with specific scenarios
- Detailed methodology broken into numbered steps
- Decision trees for complex workflows
- Tool availability checks and graceful degradation

**Content Pattern:**
```markdown
## Identity
Expert research analyst with deep expertise in codebase investigation, architectural analysis, and system understanding. Combines systematic methodology with efficient resource management.

## When to Use Me
- Comprehensive codebase exploration and pattern identification
- Architectural analysis and system boundary mapping
- Technology stack assessment and dependency analysis
- Security posture evaluation and vulnerability identification

## Research Methodology
1. **Plan Investigation Strategy**: Systematically approach research
2. **Execute Strategic Discovery**: Conduct analysis using available tools
3. **Analyze Findings**: Process discovered information
4. **Synthesize Insights**: Create comprehensive understanding
5. **Capture Work**: Save research outputs (MANDATORY)
```

---

## Common Sections Across Agent Types

### For Engineering Agents

**Must Include:**
- Language/framework version specifications
- Type safety and testing requirements
- Code quality standards (linting, formatting)
- Performance considerations
- Common design patterns with code examples
- Anti-patterns to avoid
- Integration with build/deploy pipelines

**Example Structure:**
```markdown
## Core Capabilities
### Type Safety
### Testing Standards
### Performance Patterns
### Architecture Principles

## Common Patterns
### Pattern 1: [With Code]
### Pattern 2: [With Code]

## Anti-Patterns to Avoid
### Anti-Pattern 1: [Wrong vs Right]

## Quality Standards
- Type coverage: 100%
- Test coverage: 90%+
- Complexity: <10 cyclomatic
```

### For Research/Analysis Agents

**Must Include:**
- Investigation methodology
- Tool selection strategy
- Memory management (critical for research)
- Evidence collection standards
- Synthesis and reporting formats
- Work capture and documentation

**Example Structure:**
```markdown
## Research Methodology
1. Plan Strategy
2. Execute Discovery
3. Analyze Findings
4. Synthesize Insights
5. Capture Work

## Tool Selection
- Primary tools
- Fallback options
- Graceful degradation

## Memory Management
- File limits
- Summarization thresholds
- Sequential processing

## Output Formats
- Structured documentation
- Ticketing integration
- File-based capture
```

### For Product/PM Agents

**Must Include:**
- Decision-making frameworks (RICE, OKR, etc.)
- Prioritization methods
- Stakeholder communication patterns
- Evidence requirements
- Outcome-focused planning
- Metrics and success criteria

**Example Structure:**
```markdown
## Core Frameworks
### RICE Prioritization
### OKR Planning
### Continuous Discovery

## Decision Making
- Evidence requirements
- Validation processes
- Documentation standards

## Communication
- Stakeholder alignment
- Roadmap formats
- Decision logs

## Quality Standards
- Evidence-based decisions
- Outcome focus
- Measurable success criteria
```

---

## Quick Start Checklist

When creating a new agent, ensure you have:

**Metadata:**
- [ ] Unique, descriptive `name` in kebab-case
- [ ] Clear `description` (1-2 sentences)
- [ ] Semantic `version` starting at 1.0.0
- [ ] Correct `agent_type` (engineer/qa/ops/research/product/specialized)
- [ ] Appropriate `tags` for discovery

**Knowledge:**
- [ ] Domain expertise list (what agent knows)
- [ ] Best practices (how agent operates)
- [ ] Constraints (what agent must/must not do)
- [ ] Examples (real-world scenarios)

**Content:**
- [ ] Identity paragraph
- [ ] "When to Use Me" section
- [ ] Core Capabilities detailed
- [ ] Common Patterns with code/examples
- [ ] Quality Standards with metrics
- [ ] Integration Points with other agents

**Changelog:**
- [ ] Initial version entry (1.0.0)
- [ ] Date in YYYY-MM-DD format
- [ ] Clear description of initial capabilities

**Memory Routing:**
- [ ] Description of what agent remembers
- [ ] Categories for memory organization
- [ ] Keywords for recall
- [ ] File paths/extensions

---

## Tips for Effective Agents

### 1. Be Specific, Not Generic
❌ Bad: "Expert in programming"
✅ Good: "Python 3.12+ specialist with SOA, DI, and async-first patterns"

### 2. Provide Measurable Standards
❌ Bad: "Write good tests"
✅ Good: "Achieve 90%+ test coverage with pytest, 100% critical path coverage"

### 3. Show, Don't Just Tell
❌ Bad: "Use proper error handling"
✅ Good: Include code example showing try/except with specific exceptions and logging

### 4. Use Strong Enforcement Language
❌ Bad: "Try to use type hints"
✅ Good: "MUST achieve 100% type coverage (mypy --strict) - NON-NEGOTIABLE"

### 5. Document Why, Not Just What
❌ Bad: "Use dependency injection"
✅ Good: "Use DI for loose coupling, testability, and swappable implementations"

### 6. Provide Context for Decisions
❌ Bad: "Use RICE for prioritization"
✅ Good: "Use RICE (default), WSJF (high-urgency), ICE (early-stage experimentation)"

### 7. Include Failure Scenarios
❌ Bad: "Attach to ticket"
✅ Good: "Attach to ticket if available, fallback to file, handle errors gracefully"

---

## Final Notes

**Remember:**
- This is a REFERENCE GUIDE, not a functional template system
- Claude Code does NOT support template inheritance
- Copy and adapt patterns that fit your agent's needs
- Consistency helps, but customize for your specific use case
- Quality over quantity: detailed, specific guidance beats generic advice

**Questions to Ask When Creating an Agent:**
1. What unique value does this agent provide?
2. When should users choose this agent over others?
3. What are the non-negotiable requirements (MUST/NEVER)?
4. What examples would help users understand usage?
5. How does this agent integrate with others?
6. What should this agent remember for future tasks?

**Resources:**
- See `agents/` directory for production agent examples
- Check `templates/base/` for reference patterns (not functional inheritance)
- Review top-performing agents: python-engineer, research-agent, product-owner
