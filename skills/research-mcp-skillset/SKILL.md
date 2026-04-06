---
name: Research MCP-Skillset Integration
description: MCP-skillset detection, workflow patterns, tool selection matrix, and decision tree examples for enhanced research
version: 1.0.0
category: agent-protocol
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Leverage mcp-skillset MCP server for enhanced research capabilities"
    when_to_use: "When semantic search and code analysis tasks require deeper contextual analysis"
    quick_start: "Check for mcp__mcp-skillset__* tools -> use as TIER 2 supplement to standard tools"
context_limit: 700
tags:
  - research
  - mcp-skillset
  - enhanced-research
  - multi-source-validation
  - semantic-search
  - code-analysis
requires_tools: []
---

# MCP-Skillset Integration (Optional Enhancement)

When conducting research, you can leverage additional skill-based research capabilities if mcp-skillset MCP server is installed and available. This is an OPTIONAL enhancement that supplements (not replaces) your standard research tools.

## Detection

Check for mcp-skillset tools by looking for tools with the prefix: `mcp__mcp-skillset__*`

Common mcp-skillset tools that enhance research capabilities:
- **mcp__mcp-skillset__web_search** - Enhanced web search with contextual understanding
- **mcp__mcp-skillset__code_analysis** - Deep code pattern analysis and architectural insights
- **mcp__mcp-skillset__documentation_lookup** - API and library documentation search
- **mcp__mcp-skillset__best_practices** - Industry best practices and standards research
- **mcp__mcp-skillset__technology_research** - Technology evaluation and comparison analysis
- **mcp__mcp-skillset__security_analysis** - Security patterns and vulnerability research

## Research Workflow with MCP-Skillset

When mcp-skillset tools are available, enhance your research process:

1. **Primary Research Layer** (Always executed - standard tools):
   - Use Glob for file pattern discovery
   - Use Grep for code content search
   - Use Read for file analysis (with memory limits)
   - Use WebSearch for general web queries
   - Use WebFetch for fetching and analyzing web pages
   - Use mcp-vector-search for semantic code search (if available)

2. **Enhanced Research Layer** (Optional - if mcp-skillset available):
   - Use mcp-skillset tools for deeper contextual analysis
   - Cross-reference findings between standard and skillset tools
   - Leverage skill-specific expertise for specialized research
   - Combine multiple perspectives for richer insights

3. **Synthesis** (Comprehensive analysis):
   - Integrate findings from all available sources
   - Identify patterns across different tool outputs
   - Provide multi-dimensional analysis with confidence levels
   - Document which tools contributed to each finding

## Example Research Decision Trees

### Example 1: Authentication Best Practices Research

```
User Request: "Research authentication best practices for Node.js"

Standard Approach (Always executed):
|- WebSearch: "Node.js authentication best practices 2025"
|- Grep: Search codebase for existing auth patterns
|- Read: Review authentication middleware files
'- Synthesize: Compile findings into recommendations

Enhanced with mcp-skillset (if available):
|- WebSearch: "Node.js authentication best practices 2025"
|- mcp__mcp-skillset__best_practices: "Node.js authentication security"
|- Grep: Search codebase for existing auth patterns
|- mcp__mcp-skillset__code_analysis: Analyze auth pattern implementations
|- Read: Review authentication middleware files
|- mcp__mcp-skillset__security_analysis: "JWT token security Node.js"
'- Synthesize: Combine findings from 6 sources for comprehensive analysis

Result: Richer analysis with industry standards, security insights, and code patterns
```

### Example 2: Technology Stack Evaluation

```
User Request: "Evaluate database options for high-throughput API"

Standard Approach (Always executed):
|- WebSearch: "database comparison high throughput API"
|- WebFetch: Fetch benchmark articles and comparisons
|- Grep: Check existing database usage in codebase
'- Synthesize: Present options with trade-offs

Enhanced with mcp-skillset (if available):
|- WebSearch: "database comparison high throughput API"
|- mcp__mcp-skillset__technology_research: "PostgreSQL vs MongoDB throughput"
|- WebFetch: Fetch benchmark articles and comparisons
|- mcp__mcp-skillset__best_practices: "database selection criteria"
|- Grep: Check existing database usage in codebase
|- mcp__mcp-skillset__code_analysis: Analyze current data access patterns
'- Synthesize: Multi-source analysis with benchmark data and best practices

Result: Data-driven recommendations with industry context and codebase analysis
```

### Example 3: API Documentation Research

```
User Request: "Find documentation for Stripe payment intents API"

Standard Approach (Always executed):
|- WebSearch: "Stripe payment intents API documentation"
|- WebFetch: https://stripe.com/docs/api/payment_intents
'- Summarize: Key endpoints and usage patterns

Enhanced with mcp-skillset (if available):
|- WebSearch: "Stripe payment intents API documentation"
|- mcp__mcp-skillset__documentation_lookup: "Stripe payment intents"
|- WebFetch: https://stripe.com/docs/api/payment_intents
|- mcp__mcp-skillset__code_analysis: Find Stripe usage in codebase
'- Synthesize: Documentation + existing implementation patterns + examples

Result: Complete picture of API capabilities and current usage in project
```

## Integration Guidelines

**DO:**
- Check if mcp-skillset tools are available before attempting to use them
- Use mcp-skillset as **supplementary research** (not a replacement for standard tools)
- Combine findings from standard tools AND mcp-skillset for richer analysis
- Fall back gracefully to standard tools if mcp-skillset is unavailable
- Document which tools contributed to each finding in your analysis
- Leverage mcp-skillset for specialized domains (security, best practices, etc.)
- Cross-validate findings between different tool sources

**DON'T:**
- Require mcp-skillset tools (they are optional enhancements)
- Block or fail research if mcp-skillset tools are not available
- Replace standard research tools entirely with mcp-skillset
- Assume mcp-skillset is always installed or available
- Provide error messages or warnings if mcp-skillset is unavailable
- Skip standard research steps when mcp-skillset is available
- Use mcp-skillset without first executing standard research approaches

## Tool Selection Strategy

**TIER 1: Standard Tools (Always Use - Foundation)**
- Glob: File pattern matching and discovery
- Grep: Code content search with regex patterns
- Read: Direct file reading (with memory management)
- WebSearch: General web search queries
- WebFetch: Fetch and analyze web content
- mcp-vector-search: Semantic code search (if available)

**TIER 2: Enhanced Tools (Use When Available - Supplementary)**
- mcp__mcp-skillset__web_search: Context-aware web research
- mcp__mcp-skillset__code_analysis: Deep architectural analysis
- mcp__mcp-skillset__documentation_lookup: API/library documentation
- mcp__mcp-skillset__best_practices: Industry standards and patterns
- mcp__mcp-skillset__security_analysis: Security vulnerability research
- mcp__mcp-skillset__technology_research: Technology evaluation and comparison

## Selection Decision Matrix

```
Research Task Type          | Standard Tools              | +mcp-skillset Enhancement
---------------------------|----------------------------|---------------------------
Code Pattern Search        | Grep, mcp-vector-search    | +code_analysis
Architectural Analysis     | Read, Glob, Grep           | +code_analysis
Best Practices Research    | WebSearch, WebFetch        | +best_practices
Security Evaluation        | Grep (vulnerabilities)     | +security_analysis
API Documentation          | WebSearch, WebFetch        | +documentation_lookup
Technology Comparison      | WebSearch, WebFetch        | +technology_research
Industry Standards         | WebSearch                  | +best_practices
Performance Analysis       | Grep, Read                 | +code_analysis
```

## Availability Check Pattern

Before using mcp-skillset tools, verify availability in your tool set:

```python
# Conceptual pattern (not literal code)
available_tools = [list of available tools]
mcp_skillset_available = any(tool.startswith('mcp__mcp-skillset__') for tool in available_tools)

if mcp_skillset_available:
    # Enhanced research workflow with skillset tools
    use_standard_tools()
    use_mcp_skillset_tools()  # Supplementary layer
    synthesize_all_findings()
else:
    # Standard research workflow only
    use_standard_tools()
    synthesize_findings()
    # No error/warning needed - optional enhancement
```

## Research Quality with MCP-Skillset

When mcp-skillset is available, enhance research quality by:
- **Multi-Source Validation**: Cross-reference findings from 4-6 sources instead of 2-3
- **Deeper Context**: Leverage skill-specific expertise for specialized domains
- **Richer Insights**: Combine code analysis with best practices and documentation
- **Higher Confidence**: Validate patterns across multiple analytical perspectives
- **Comprehensive Coverage**: Standard tools provide breadth, skillset adds depth

## Graceful Degradation

If mcp-skillset tools are not available:
- Proceed with standard research tools without any interruption
- Maintain same research methodology and quality standards
- No need to inform user about unavailable optional enhancements
- Continue to deliver comprehensive analysis using available tools
- Research quality remains high with standard tool suite