---
name: Research Google Workspace Integration
description: Google Workspace integration with Calendar, Gmail, and Drive for research tasks
version: 1.0.0
category: agent-protocol
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Leverage Google Workspace tools for calendar, email, and Drive research"
    when_to_use: "When research involves calendar, email, or Drive tasks requiring Google Workspace access"
    quick_start: "Check for mcp__google-workspace-mpm__* tools -> use as supplementary research layer"
context_limit: 700
tags:
  - research
  - google-workspace
  - calendar-research
  - email-research
  - drive-research
  - gmail
requires_tools: []
---

# Google Workspace Integration (Optional Enhancement)

When conducting research that involves the user's calendar, email, or Drive files, you can leverage the google-workspace-mpm MCP server if it is installed and authenticated. This is an OPTIONAL enhancement that supplements your standard research tools.

## Prerequisites

- User must have authenticated via `/oauth setup workspace-mcp`
- The google-workspace-mpm MCP server must be configured in the project

## Detection

Check for Google Workspace tools by looking for tools with the prefix: `mcp__google-workspace-mpm__*`

Available google-workspace-mpm tools:
- **mcp__google-workspace-mpm__list_calendars** - List all accessible Google Calendars
- **mcp__google-workspace-mpm__get_events** - Get calendar events with time range filtering
  - Parameters: `calendar_id` (default: "primary"), `time_min`, `time_max` (RFC3339 format), `max_results`
- **mcp__google-workspace-mpm__search_gmail_messages** - Search Gmail using query strings
  - Parameters: `query` (Gmail search syntax like "from:user@example.com subject:meeting"), `max_results`
- **mcp__google-workspace-mpm__get_gmail_message_content** - Get full email content by message ID
  - Parameters: `message_id`
- **mcp__google-workspace-mpm__search_drive_files** - Search Drive files by query
  - Parameters: `query` (Drive search syntax like "name contains 'requirements'"), `max_results`
- **mcp__google-workspace-mpm__get_drive_file_content** - Get file content (exports Google Docs to text)
  - Parameters: `file_id`

## When to Use Google Workspace Tools

| Research Task | Google Workspace Tool | Example Use Case |
|---------------|----------------------|------------------|
| Finding meeting times | get_events | "When is the next sprint planning meeting?" |
| Checking availability | get_events + list_calendars | "What's my availability next Tuesday?" |
| Email context gathering | search_gmail_messages | "Find emails about the API redesign" |
| Reading specific email | get_gmail_message_content | "Read the full email from Jane about requirements" |
| Finding requirements docs | search_drive_files | "Find specs for the authentication feature" |
| Reading project documents | get_drive_file_content | "Read the architecture document from Drive" |

## Research Workflow with Google Workspace

When Google Workspace tools are available, enhance your research process:

1. **Standard Research Layer** (Always executed):
   - Use Glob/Grep for codebase search
   - Use mcp-vector-search for semantic code discovery (if available)
   - Use WebSearch/WebFetch for external resources
   - Use mcp-skillset for enhanced analysis (if available)

2. **Google Workspace Layer** (Optional - if authenticated):
   - Search user's emails for project context and correspondence
   - Check calendar for meeting notes, scheduling context
   - Search Drive for requirements documents, specs, and project materials
   - Cross-reference findings with codebase analysis

3. **Synthesis** (Comprehensive analysis):
   - Integrate findings from all available sources
   - Connect code patterns to business requirements from Drive docs
   - Link implementation decisions to email discussions
   - Correlate timeline with calendar events

## Example Research Decision Trees

### Example 1: Requirements Research with Drive Integration

```
User Request: "Research the requirements for the payment feature"

Standard Approach (Always executed):
|- WebSearch: "payment feature requirements best practices"
|- Grep: Search codebase for payment-related code
|- Read: Review existing payment implementation
'- Synthesize: Compile findings

Enhanced with Google Workspace (if available):
|- search_drive_files: query="payment requirements" OR "payment spec"
|- get_drive_file_content: Read requirements doc from results
|- search_gmail_messages: query="subject:payment feature"
|- get_gmail_message_content: Read relevant email threads
|- Grep: Search codebase for payment-related code
|- Read: Review existing payment implementation
'- Synthesize: Requirements from Drive + email context + code analysis

Result: Complete picture of requirements, stakeholder discussions, and current implementation
```

### Example 2: Meeting Context Research

```
User Request: "What was discussed in the architecture review meeting?"

Standard Approach (Always executed):
|- search_drive_files: "architecture review notes"
|- Read: Check for meeting notes in project docs/
'- Synthesize: Available documentation

Enhanced with Google Workspace (if available):
|- get_events: calendar_id="primary", time_min=<last_week>, time_max=<now>
|   -> Find "architecture review" event
|- search_drive_files: "architecture review" + meeting date
|- get_drive_file_content: Read meeting notes document
|- search_gmail_messages: "subject:architecture review" + attendees
|- get_gmail_message_content: Read follow-up emails
'- Synthesize: Calendar event + meeting notes + follow-up discussions

Result: Full context including when it happened, what was discussed, and follow-ups
```

### Example 3: Project Context with Email History

```
User Request: "Research the decision history for choosing PostgreSQL"

Standard Approach (Always executed):
|- Grep: Search for PostgreSQL references in codebase
|- Read: Review database configuration and migration files
|- WebSearch: "PostgreSQL vs alternatives"
'- Synthesize: Technical analysis

Enhanced with Google Workspace (if available):
|- search_gmail_messages: "subject:database" OR "subject:postgresql"
|- get_gmail_message_content: Read decision-related emails
|- search_drive_files: "database decision" OR "tech stack"
|- get_drive_file_content: Read ADR or decision documents
|- Grep: Search for PostgreSQL references in codebase
|- Read: Review database configuration
'- Synthesize: Decision emails + docs + current implementation

Result: Complete decision history with stakeholder input and rationale
```

## Integration Guidelines

**DO:**
- Check if google-workspace-mpm tools are available before attempting to use them
- Use Google Workspace as **supplementary research** (not a replacement for standard tools)
- Respect user privacy - only access workspace data relevant to research task
- Use appropriate time ranges for calendar queries (RFC3339 format)
- Use Gmail query syntax for precise email searches
- Combine workspace data with codebase analysis for richer context
- Fall back gracefully if workspace tools are unavailable or fail

**DON'T:**
- Require Google Workspace tools (they are optional enhancements)
- Block or fail research if workspace tools are not authenticated
- Access workspace data unrelated to the research task
- Provide error messages if workspace tools are unavailable
- Skip standard research steps when workspace is available
- Assume authentication is always valid (tokens can expire)

## Gmail Query Syntax Examples

- `from:john@example.com` - Emails from specific sender
- `to:team@example.com` - Emails to specific recipient
- `subject:requirements` - Emails with specific subject
- `has:attachment` - Emails with attachments
- `after:2024/01/01 before:2024/06/01` - Date range
- `label:important` - Emails with specific label
- Combine with AND/OR: `from:john@example.com subject:api has:attachment`

## Drive Query Syntax Examples

- `name contains 'requirements'` - Files with name containing text
- `mimeType = 'application/vnd.google-apps.document'` - Google Docs only
- `modifiedTime > '2024-01-01T00:00:00'` - Recently modified files
- `'folder_id' in parents` - Files in specific folder

## Availability Check Pattern

Before using Google Workspace tools, verify availability in your tool set:

```python
# Conceptual pattern (not literal code)
available_tools = [list of available tools]
google_workspace_available = any(tool.startswith('mcp__google-workspace-mpm__') for tool in available_tools)

if google_workspace_available:
    # Enhanced research workflow with workspace tools
    use_standard_tools()
    use_google_workspace_tools()  # Supplementary layer
    synthesize_all_findings()
else:
    # Standard research workflow only
    use_standard_tools()
    synthesize_findings()
    # No error/warning needed - optional enhancement
```

## Graceful Degradation

If Google Workspace tools are not available or not authenticated:
- Proceed with standard research tools without any interruption
- Maintain same research methodology and quality standards
- No need to inform user about unavailable optional enhancements
- If user explicitly requests workspace data, inform them: "Google Workspace integration not available. Please authenticate via `/oauth setup workspace-mcp` to enable calendar, email, and Drive access."
- Continue to deliver comprehensive analysis using available tools