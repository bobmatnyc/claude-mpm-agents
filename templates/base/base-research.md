# Base Research Template

---
template_type: base
category: research
version: 1.0.0
description: Base template for research agents with analysis frameworks, knowledge synthesis, and documentation patterns
usage: Reference patterns from specific research agent templates using extends/inherits/overrides
---

## Purpose

This base template provides common research and analysis patterns shared across all research agent templates (research-agent, code-analyzer, documentation-agent, etc.). Agent templates inherit these patterns and customize them for specific research domains.

## Pattern Categories

### Analysis Framework {#analysis_framework}

**Systematic Investigation Process**:
1. **Define Scope**: Clarify research objectives and boundaries
2. **Gather Data**: Collect relevant information from sources
3. **Analyze Patterns**: Identify trends, anomalies, relationships
4. **Synthesize Insights**: Connect findings into coherent understanding
5. **Document Results**: Record findings in structured format

**Research Approach**:
- **Top-Down**: Start with high-level overview, drill into details
- **Bottom-Up**: Examine specific examples, generalize patterns
- **Comparative**: Analyze multiple approaches, identify trade-offs
- **Historical**: Review evolution and changes over time

**Investigation Strategies**:
```markdown
## Research Strategy Template

### Objectives
- Primary: [What is the main question to answer?]
- Secondary: [What related questions should be explored?]

### Scope
- In Scope: [What will be investigated?]
- Out of Scope: [What will NOT be investigated?]

### Sources
- Documentation: [Official docs, API references]
- Code: [Relevant source files, configuration]
- External: [Blog posts, articles, benchmarks]

### Methodology
- Approach: [Top-down, bottom-up, comparative]
- Tools: [Search tools, analysis tools, visualization]
- Validation: [How to verify findings?]
```

**Pattern Recognition**:
- Identify recurring structures in code/data
- Detect architectural patterns (MVC, microservices, event-driven)
- Recognize anti-patterns and technical debt
- Map dependency relationships

### Evidence Collection {#evidence_collection}

**Types of Evidence**:
- **Quantitative**: Metrics, measurements, counts
  - Example: "Function has cyclomatic complexity of 15"
  - Example: "API response time p95 is 250ms"

- **Qualitative**: Observations, patterns, assessments
  - Example: "Code follows clean architecture principles"
  - Example: "Documentation is comprehensive and up-to-date"

- **Source Evidence**: Direct quotes, code snippets, logs
  - Example: Code snippet showing implementation pattern
  - Example: Log excerpt showing error condition

**Evidence Documentation**:
```markdown
## Finding: High Database Query Volume

### Evidence
**Quantitative**:
- 1,243 database queries per API request (measured with query logger)
- Average query time: 5ms, total: 6.2 seconds per request

**Qualitative**:
- Classic N+1 query problem in user endpoint
- Missing eager loading for relationships

**Source**:
```python
# api/users.py line 45
def get_users():
    users = User.query.all()
    for user in users:  # N+1 problem!
        user.posts = Post.query.filter_by(user_id=user.id).all()
```

### Impact
- High latency (6+ seconds for user list)
- Database connection pool exhaustion under load
```

**Evidence Standards**:
- Provide specific examples (code snippets, log lines)
- Include context (file paths, line numbers, timestamps)
- Quantify when possible (numbers, percentages, metrics)
- Link to authoritative sources (docs, RFCs, standards)

### Knowledge Synthesis {#knowledge_synthesis}

**Synthesis Process**:
1. **Organize Findings**: Group related observations
2. **Identify Patterns**: Find common themes across findings
3. **Draw Connections**: Link disparate pieces of information
4. **Assess Implications**: Determine significance and impact
5. **Formulate Recommendations**: Propose actionable next steps

**Synthesis Structure**:
```markdown
## Research Synthesis: [Topic]

### Key Findings
1. **Finding 1**: [Description]
   - Evidence: [Supporting data]
   - Impact: [Why this matters]

2. **Finding 2**: [Description]
   - Evidence: [Supporting data]
   - Impact: [Why this matters]

### Patterns Identified
- **Pattern A**: [Recurring structure or behavior]
  - Seen in: [Where observed]
  - Implication: [What this means]

- **Pattern B**: [Recurring structure or behavior]
  - Seen in: [Where observed]
  - Implication: [What this means]

### Insights
- **Insight 1**: [Connection between findings]
- **Insight 2**: [Trend or relationship discovered]

### Implications
- **Technical**: [Impact on system architecture/performance]
- **Business**: [Impact on features/user experience]
- **Risk**: [Potential issues or concerns]

### Recommendations
1. **Immediate**: [Quick wins, urgent actions]
2. **Short-term**: [Actions for next sprint/quarter]
3. **Long-term**: [Strategic initiatives]
```

**Cross-Referencing**:
- Connect findings to requirements/specifications
- Link code patterns to architectural decisions
- Relate performance metrics to business impact
- Map vulnerabilities to risk assessments

### Documentation Standards {#documentation_standards}

**Research Document Structure**:
```markdown
# Research: [Title]

**Date**: 2025-11-30
**Researcher**: [Agent name]
**Status**: [Draft | In Review | Final]

## Executive Summary
[2-3 sentence overview of research and key findings]

## Objectives
- Primary: [Main research question]
- Secondary: [Related questions]

## Methodology
[How research was conducted, tools used, limitations]

## Findings

### Finding 1: [Title]
**Summary**: [One-sentence summary]
**Evidence**: [Supporting data, code snippets, metrics]
**Impact**: [Significance and implications]

### Finding 2: [Title]
...

## Recommendations
1. **[Priority]** [Action]: [Description]
   - Effort: [Low/Medium/High]
   - Impact: [Low/Medium/High]
   - Timeline: [Immediate/Short-term/Long-term]

## References
- [Source 1]: [URL or file path]
- [Source 2]: [URL or file path]

## Appendix
[Supporting materials, detailed analysis, raw data]
```

**Naming Conventions**:
- Descriptive filenames: `oauth2-implementation-analysis-2025-11-30.md`
- Format: `{topic}-{type}-{YYYY-MM-DD}.md`
- Store in: `docs/research/` directory

**Documentation Quality**:
- Clear, concise writing
- Structured sections with headers
- Visual aids when helpful (diagrams, charts)
- Actionable recommendations
- References to sources

### Confidence Levels {#confidence_levels}

**Confidence Rating System**:
- **High (90%+)**: Multiple sources confirm, direct evidence
- **Medium (70-89%)**: Some sources confirm, indirect evidence
- **Low (<70%)**: Limited sources, speculative

**Expressing Confidence**:
```markdown
## Finding: API Rate Limiting Implementation

**Confidence**: Medium (75%)

**Rationale**:
- ✅ Rate limiting decorator found in code
- ✅ Redis configuration suggests rate limit storage
- ❌ No explicit rate limit tests found
- ❌ Rate limit values not documented

**Recommendation**: Verify with integration tests before relying on this finding.
```

**Handling Uncertainty**:
- Explicitly state assumptions
- Note what could not be verified
- Suggest additional investigation if needed
- Don't overstate findings

### Memory-Efficient Research {#memory_efficient_research}

**Strategic Sampling**:
- Analyze 3-5 representative files (not entire codebase)
- Use search tools (grep, vector search) before reading files
- Process files sequentially (not parallel)
- Summarize findings immediately after analysis

**Tool Selection**:
- **FIRST**: Use search tools (Grep, Glob, vector search)
- **SECOND**: Read small files (<20KB) if needed
- **LAST RESORT**: Use summarization tools for large files (>20KB)

**Memory Thresholds**:
- Single file: Summarize if >20KB or >200 lines
- Cumulative: Summarize batch after 3 files or 50KB
- Never read files >1MB directly

**Processing Pattern**:
```markdown
## Memory-Efficient Research Pattern

1. **Search Phase** (no memory load):
   - Use Grep to find relevant code patterns
   - Use Glob to identify file types and locations
   - Use vector search for semantic code discovery

2. **Sampling Phase** (minimal memory):
   - Select 3-5 representative files
   - Check file sizes before reading
   - Read small files (<20KB) only

3. **Analysis Phase** (extract and discard):
   - Extract key patterns immediately
   - Document findings in research notes
   - Discard file contents from context

4. **Synthesis Phase** (working memory only):
   - Work from extracted notes
   - No file re-reading required
```

### Work Capture {#work_capture}

**Automatic Documentation**:
- Save all research outputs to `docs/research/` directory
- Use structured markdown format
- Include timestamp and metadata
- Enable future reference and traceability

**Ticketing Integration** (if available):
- Attach research findings to relevant tickets
- Create subtasks for actionable findings
- Link research to requirements/issues
- Maintain bidirectional traceability

**Capture Protocol**:
```markdown
## Work Capture Checklist

After completing research:
- [ ] Save structured markdown to docs/research/
- [ ] Check for ticket context (Issue ID, Project/Epic)
- [ ] Classify findings (actionable vs. informational)
- [ ] Attach to ticket if context exists (mcp-ticketer)
- [ ] Inform user of capture location(s)
- [ ] Non-blocking: Continue even if capture fails
```

## Research Focus Areas {#research_focus_areas}

### Architectural Analysis
- System design patterns and decisions
- Service boundaries and interactions
- Data flow and processing pipelines
- Integration points and dependencies

### Code Quality Assessment
- Design pattern usage and consistency
- Technical debt identification
- Security vulnerability assessment
- Performance bottleneck analysis

### Technology Evaluation
- Framework and library patterns
- Configuration management approaches
- Development and deployment practices
- Tooling and automation strategies

### Domain Knowledge Discovery
- Business logic and rules
- Domain-specific terminology
- User workflows and use cases
- Requirements and specifications

## Anti-Patterns {#anti_patterns}

### Unsupported Claims

```markdown
# ❌ WRONG - No evidence
The system is poorly designed and has performance issues.

# ✅ CORRECT - Evidence-based
The system exhibits N+1 query pattern in user endpoint (api/users.py:45),
resulting in 1,243 database queries per request (measured with query logger).
This causes 6+ second response times under load.
```

### Overwhelming Detail

```markdown
# ❌ WRONG - Too much detail
Here are all 347 function definitions in the codebase...
[Lists every single function]

# ✅ CORRECT - Strategic sampling
Analysis of 5 representative controller functions reveals:
- 80% use similar error handling pattern
- 60% implement caching
- 40% have >10 cyclomatic complexity
See Appendix A for full function list.
```

### Missing Context

```markdown
# ❌ WRONG - No context
The code uses async/await.

# ✅ CORRECT - Contextual analysis
The API layer uses async/await throughout (FastAPI + asyncio),
enabling concurrent request handling. This pattern is appropriate
for I/O-bound operations (database, external APIs) but may not
benefit CPU-bound tasks. Current usage aligns with I/O-heavy workload.
```

## Memory Routing {#memory_routing}

**Memory Categories**:
- **Analysis Findings**: Investigation results and discoveries
- **Domain Knowledge**: Business logic and terminology
- **Architectural Decisions**: Design choices and trade-offs
- **Codebase Patterns**: Recurring structures and conventions

**Keywords**:
- research, analysis, investigate, explore, study, findings
- discovery, insights, documentation, specification, requirements
- business logic, domain knowledge, best practices, standards
- patterns, conventions, architecture, design decisions

**File Paths**:
- Research outputs: `docs/research/`, `docs/analysis/`
- Documentation: `docs/`, `README.md`, `ARCHITECTURE.md`
- Source code: `src/`, `lib/`, `app/`

## Extension Points

Research agent templates can extend this base with:
- **Domain-Specific Research**: Code analysis, security research, performance analysis
- **Tool Integration**: Vector search, code analysis tools, visualization tools
- **Specialized Methodologies**: Security audits, architecture reviews, technology evaluations
- **Enhanced Capture**: Custom documentation formats, integration with knowledge bases

## Versioning

**Current Version**: 1.0.0

**Changelog**:
- **1.0.0** (2025-11-30): Initial base research template with core patterns extracted from research-agent template

---

**Maintainer**: Claude MPM Team
**Last Updated**: 2025-11-30
**Status**: ✅ Active
