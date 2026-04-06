---
name: Research Ticketing Protocol
description: Ticket attachment decision trees, enforcement protocols, communication templates, and worked examples for research outputs
version: 1.0.0
category: agent-protocol
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Enforce ticket attachment when ticket context exists in research tasks"
    when_to_use: "When ticket IDs or issue URLs are detected in research requests"
    quick_start: "Check ticket context -> classify work type -> attach to ticket or save to docs/research/"
context_limit: 700
tags:
  - research
  - ticketing
  - work-capture
  - traceability
  - structured-output
requires_tools: []
---

# Ticket Attachment Imperatives (Required)

**Important: Research outputs should be attached to tickets when ticket context exists.**

## When Ticket Attachment is Required

**Generally REQUIRED (100% enforcement)**:
1. **User provides ticket ID/URL explicitly**
   - User says: "Research X for TICKET-123"
   - User includes ticket URL in request
   - PM delegation includes ticket context
   -> Research should attach findings to TICKET-123

2. **PM passes ticket context in delegation**
   - PM includes "TICKET CONTEXT" section
   - Delegation mentions: "for ticket {TICKET_ID}"
   - Task includes: "related to {TICKET_ID}"
   -> Research should attach findings to TICKET_ID

3. **mcp-ticketer tools available + ticket context exists**
   - Check: mcp__mcp-ticketer__* tools in tool set
   - AND: Ticket ID/context present in task
   -> Research should attempt ticket attachment (with fallback)

## When Ticket Attachment is OPTIONAL

**File-based capture ONLY**:
1. **No ticket context provided**
   - User asks: "Research authentication patterns" (no ticket mentioned)
   - PM delegates without ticket context
   - Ad-hoc research request
   -> Research saves to docs/research/ only (no ticketing)

2. **mcp-ticketer tools unavailable**
   - No mcp__mcp-ticketer__* tools detected
   - AND: No ticketing-agent available
   -> Research saves to docs/research/ + informs user about ticketing unavailability

## Attachment Decision Tree

```
Start Research Task
    |
    v
Check: Ticket context provided?
    |
    +-- NO --> Save to docs/research/ only (inform user)
    |
    +-- YES --> Check: mcp-ticketer tools available?
                |
                +-- NO --> Save to docs/research/ + inform user
                |           "Ticketing integration unavailable, saved locally"
                |
                +-- YES --> required TICKET ATTACHMENT
                            |
                            v
                         Classify Work Type
                            |
                            +-- Actionable --> Create subtask under ticket
                            |                  Link findings
                            |                  Save to docs/research/
                            |
                            +-- Informational --> Attach file to ticket
                                                  Add comment with summary
                                                  Save to docs/research/
                            |
                            v
                         Verify Attachment Success
                            |
                            +-- SUCCESS --> Report to user
                            |               "Attached to {TICKET_ID}"
                            |
                            +-- FAILURE --> Fallback to file-only
                                            Log error details
                                            Report to user with error
```

## Enforcement Language

**YOU should attach research findings to {TICKET_ID}**
Ticket attachment is required when ticket context exists.
DO NOT complete research without attaching to {TICKET_ID}.

## Failure Handling

**Important: Attachment failures should NOT block research delivery.**

**Fallback Chain**:
1. Attempt ticket attachment (MCP tools)
2. If fails: Log error details + save to docs/research/
3. Report to user with specific error message
4. Deliver research results regardless

## User Communication Templates

**Success Message**:
```
Research Complete and Attached

Research: OAuth2 Implementation Analysis
Saved to: docs/research/oauth2-patterns-2025-11-23.md

Ticket Integration:
- Attached findings to TICKET-123
- Created subtask TICKET-124: Implement token refresh
- Added comment summarizing key recommendations

Next steps available in TICKET-124.
```

**Partial Failure Message**:
```
Research Complete (Partial Ticket Integration)

Research: OAuth2 Implementation Analysis  
Saved to: docs/research/oauth2-patterns-2025-11-23.md

Ticket Integration:
- Attached research file to TICKET-123
- Failed to create subtasks (API error: "Rate limit exceeded")

Manual Action Required:
Please create these subtasks manually in your ticket system:
1. Implement token refresh mechanism (under TICKET-123)
2. Add OAuth2 error handling (under TICKET-123)  
3. Write OAuth2 integration tests (under TICKET-123)

Full research with implementation details available in local file.
```

**Complete Failure Message**:
```
Research Complete (Ticket Integration Unavailable)

Research: OAuth2 Implementation Analysis
Saved to: docs/research/oauth2-patterns-2025-11-23.md

Ticket Integration Failed:
Error: "Ticketing service unavailable"

Your research is safe in the local file. To attach to TICKET-123:
1. Check mcp-ticketer service status
2. Manually upload docs/research/oauth2-patterns-2025-11-23.md to ticket
3. Or retry: [provide retry command]

Research findings delivered successfully regardless of ticketing status.
```

## Priority Matrix

**OPTION 1: Create Subtask (HIGHEST PRIORITY)**
- Criteria: Ticket context + tools available + ACTIONABLE work
- Action: `mcp__mcp-ticketer__issue_create(parent_id="{TICKET_ID}")`

**OPTION 2: Attach File + Comment (MEDIUM PRIORITY)**
- Criteria: Ticket context + tools available + INFORMATIONAL work
- Action: `mcp__mcp-ticketer__ticket_attach` + `ticket_comment`

**OPTION 3: Comment Only (LOW PRIORITY)**
- Criteria: File attachment failed (too large, API limit)
- Action: `mcp__mcp-ticketer__ticket_comment` with file reference

**OPTION 4: File Only (FALLBACK)**
- Criteria: No ticket context OR no tools available
- Action: Save to docs/research/ + inform user

## Work Classification Decision Tree

```
Start Research
    |
    v
Conduct Analysis
    |
    v
Classify Work Type:
    |
    +-- Actionable Work?
    |   - Contains TODO items
    |   - Requires implementation
    |   - Identifies bugs/issues
    |   - Proposes changes
    |
    +-- Informational Only?
        - Background research
        - Reference material
        - No immediate actions
        - Comparative analysis
        |
        v
Save to docs/research/{filename}.md (generally)
        |
        v
Check Ticketing Tools Available?
    |
    +-- NO --> Inform user (file-based only)
    |
    +-- YES --> Check Context:
                 |
                 +-- Issue ID?
                 |   |
                 |   +-- Actionable --> Create subtask
                 |   +-- Informational --> Attach + comment
                 |
                 +-- Project/Epic?
                 |   |
                 |   +-- Actionable --> Create issue in project
                 |   +-- Informational --> Attach to project
                 |
                 +-- No Context --> File-based only
        |
        v
Inform User:
    - File path: docs/research/{filename}.md
    - Ticket ID: {ISSUE_ID or SUBTASK_ID} (if created/attached)
    - Action: What was done with research
        |
        v
Done (Non-blocking)
```

## Worked Examples

### Example 1: Issue-Based Actionable Research

```
User: "Research OAuth2 implementation patterns for ISSUE-123"

Research Agent Actions:
1. Conducts OAuth2 research using vector search and grep
2. Identifies actionable work: Need to implement OAuth2 flow
3. Saves to: docs/research/oauth2-implementation-patterns-2025-11-22.md
4. Checks: mcp-ticketer tools available? YES
5. Detects: ISSUE-123 context
6. Classifies: Actionable work (implementation required)
7. Creates subtask:
   - Title: "Research: OAuth2 Implementation Patterns"
   - Parent: ISSUE-123
   - Description: Link to docs/research file + summary
   - Tags: ["research", "authentication"]
8. Links subtask to ISSUE-123
9. Attaches research document
10. Informs user:
    "Research completed and saved to docs/research/oauth2-implementation-patterns-2025-11-22.md
    
    Created subtask ISSUE-124 under ISSUE-123 with action items:
    - Implement OAuth2 authorization flow
    - Add token refresh mechanism
    - Update authentication middleware
    
    Full research findings attached to ISSUE-123."
```

### Example 2: Project-Level Informational Research

```
User: "Analyze database scaling options for Project-AUTH"

Research Agent Actions:
1. Conducts database scaling research
2. Finds: Comparative analysis, no immediate action required
3. Saves to: docs/research/database-scaling-analysis-2025-11-22.md
4. Checks: mcp-ticketer tools available? YES
5. Detects: No ISSUE ID, but Project-AUTH exists
6. Classifies: Informational (no immediate action)
7. Attaches to Project-AUTH:
   - file_path: docs/research/database-scaling-analysis-2025-11-22.md
   - description: "Database scaling options analysis"
8. Adds comment to Project-AUTH:
   - "Completed database scaling analysis. Key findings:
     - PostgreSQL can scale to 10K QPS with read replicas
     - Aurora Serverless recommended for variable workloads
     - Redis caching reduces DB load by 40%
     
     Full analysis: docs/research/database-scaling-analysis-2025-11-22.md"
9. Informs user:
    "Research completed and saved to docs/research/database-scaling-analysis-2025-11-22.md
    
    Attached findings to Project-AUTH with summary of scaling options.
    
    Recommendation: Review analysis before making infrastructure decisions."
```

### Example 3: Ad-Hoc Research (No Ticketing Context)

```
User: "Research latest trends in AI agents"

Research Agent Actions:
1. Conducts AI agents research using WebSearch and analysis
2. Compiles findings on current trends
3. Saves to: docs/research/ai-agents-trends-2025-11-22.md
4. Checks: mcp-ticketer tools available? YES
5. Detects: No ISSUE ID, no Project context
6. Classifies: Informational, no ticketing context
7. Logs: "No ticketing context available for AI agents research"
8. Informs user:
    "Research completed and saved to docs/research/ai-agents-trends-2025-11-22.md
    
    Key trends identified:
    - Multi-agent systems gaining traction
    - Tool use and function calling becoming standard
    - Focus on reliability and error recovery
    
    No ticketing context available. To track this research:
    - Create issue: 'Review AI agent trends'
    - Or attach to existing project/epic"
```

### Example 4: File Write Error with Fallback

```
User: "Research performance bottlenecks in API layer"

Research Agent Actions:
1. Conducts performance research
2. Identifies bottlenecks: N+1 queries, missing indexes
3. Attempts: Write to docs/research/api-performance-bottlenecks-2025-11-22.md
4. Error: Permission denied (docs/research/ doesn't exist or no write permission)
5. Fallback: mkdir -p docs/research/ && retry
6. If still fails: Try ./research/api-performance-bottlenecks-2025-11-22.md
7. If still fails: Try ./api-performance-bottlenecks-2025-11-22.md
8. Success: Saved to ./api-performance-bottlenecks-2025-11-22.md
9. Informs user:
    "Research completed but encountered permission error with docs/research/
    
    Saved to: ./api-performance-bottlenecks-2025-11-22.md
    
    To fix permissions:
    mkdir -p docs/research && chmod u+w docs/research
    mv ./api-performance-bottlenecks-2025-11-22.md docs/research/
    
    Key findings:
    - N+1 query problem in user endpoint (fix: add eager loading)
    - Missing index on orders.created_at (add migration)
    - API response time: 800ms avg, target <200ms"
```