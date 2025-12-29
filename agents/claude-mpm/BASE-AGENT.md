# Claude MPM Framework Awareness

> This BASE-AGENT.md provides awareness of the Claude MPM (Multi-agent Project Manager) framework to all agents in this directory.

## What is Claude MPM?

Claude MPM is a multi-agent orchestration framework for Claude Code that enables:
- **Specialized agents** for different tasks (engineering, QA, ops, research, etc.)
- **Delegation-based workflow** coordinated by a Project Manager (PM) agent
- **Memory management** for context retention across sessions
- **Auto-deployment** based on project type detection
- **Hierarchical organization** of agents by functional relationships

## Claude MPM Architecture

### Three-Tier Agent Hierarchy

1. **System-Level Agents** (`~/.claude-mpm/agents/`)
   - Bundled with Claude MPM installation
   - Available to all projects
   - Updated via Claude MPM releases

2. **User-Level Agents** (`~/.claude-mpm/user-agents/`)
   - Installed by user across all projects
   - Custom or community agents
   - User-specific modifications

3. **Project-Level Agents** (`{project}/.claude-mpm/agents/`)
   - Project-specific agents
   - Overrides for system/user agents
   - Team-shared via version control

### Agent Cache Location

**Primary Cache**: `~/.claude-mpm/agents/`

All available agents are stored here, organized by category:
```
~/.claude-mpm/agents/
├── universal/
│   ├── mpm-agent-manager.md
│   ├── memory-manager.md
│   └── ...
├── engineer/
│   ├── frontend/
│   ├── backend/
│   └── ...
├── qa/
├── ops/
└── ...
```

## Agent Discovery & Deployment

### Auto-Deployment Process

1. **Project Detection**
   - Scan project root for indicator files (package.json, pyproject.toml, etc.)
   - Determine project type(s) (Python, JavaScript, Rust, etc.)
   - Identify frameworks (React, Next.js, Django, etc.)

2. **Agent Selection**
   - Universal agents (always deployed)
   - Language-specific agents (based on detection)
   - Framework-specific agents (based on dependencies)
   - Platform-specific agents (Vercel, GCP, etc.)

3. **Deployment**
   - Load agents from `~/.claude-mpm/agents/`
   - Apply project-level overrides if present
   - Initialize agent contexts
   - Make available to PM for delegation

### Manual Deployment

Users can manually deploy additional agents:
```bash
# Deploy specific agent
claude-mpm agents deploy <agent-name>

# List available agents
claude-mpm agents list

# Show deployed agents
claude-mpm agents status
```

## Agent Cache Scanning

### Agent Discovery

MPM agents should scan the cache to:
1. **List available agents** not currently deployed
2. **Suggest relevant agents** based on project context
3. **Provide agent information** (description, capabilities, use cases)
4. **Enable on-demand deployment** when user requests specific functionality

### Cache Scanning API

```python
# Pseudo-code for agent cache scanning

def scan_agent_cache():
    """Scan ~/.claude-mpm/agents/ for all available agents."""
    cache_dir = Path.home() / ".claude-mpm" / "agents"

    agents = {
        "universal": [],
        "engineer": {"frontend": [], "backend": [], "mobile": [], "data": [], "specialized": []},
        "qa": [],
        "ops": {"core": [], "platform": [], "tooling": []},
        "security": [],
        "documentation": [],
        "claude-mpm": []
    }

    # Scan each category
    for category in agents.keys():
        category_path = cache_dir / category
        if category_path.exists():
            # Find all .md files (excluding BASE-AGENT.md)
            for agent_file in category_path.rglob("*.md"):
                if agent_file.name != "BASE-AGENT.md":
                    agents[category].append(parse_agent_metadata(agent_file))

    return agents

def get_deployed_agents():
    """Get currently deployed agents for this project."""
    # Read from .claude-mpm/deployed-agents.json
    pass

def get_available_agents():
    """Get agents in cache but not deployed."""
    all_agents = scan_agent_cache()
    deployed = get_deployed_agents()
    return difference(all_agents, deployed)

def suggest_agents(user_request, project_context):
    """Suggest agents based on user request and project context."""
    available = get_available_agents()

    # Semantic matching based on:
    # - User request keywords
    # - Project type/framework
    # - Task domain (testing, deployment, refactoring, etc.)

    return ranked_suggestions
```

### Agent Metadata

Each agent file contains metadata in YAML frontmatter:
```yaml
---
name: Agent Name
description: Brief description of agent capabilities
agent_id: unique-identifier
agent_type: engineer|qa|ops|universal|documentation
tags:
  - technology
  - domain
  - use-case
category: engineering|qa|ops|research
---
```

MPM agents should parse this metadata for:
- **Agent discovery**: List available agents
- **Semantic matching**: Match user requests to appropriate agents
- **Capability description**: Explain what each agent can do
- **Deployment recommendations**: Suggest when to deploy each agent

## PM Delegation Model

### How PM Works with Agents

The Project Manager (PM) agent:
1. **Receives user requests**
2. **Determines which agent(s)** should handle the work
3. **Delegates tasks** to appropriate agents
4. **Tracks progress** via TodoWrite
5. **Collects results** and verifies completion
6. **Reports back** to user with evidence

### Agent Interaction Patterns

**Handoff Protocol**:
- Engineer → QA (after implementation)
- Engineer → Security (for auth/crypto changes)
- Research → Engineer (after investigation)
- QA → Engineer (when bugs found)
- Any → Documentation (after code changes)

**Sequential Workflows**:
```
Request → Research → Code Analyzer → Engineer → QA → Ops (deploy) → Ops (verify) → Documentation
```

**Parallel Workflows**:
```
Request → Engineer (backend) + Engineer (frontend) → QA (API) + QA (Web) → Ops
```

## Memory System

### How Memory Works

1. **Capture**: Agents store learnings in `.claude-mpm/memories/{agent-name}.md`
2. **Routing**: Memory system routes info to appropriate agent memories
3. **Retention**: Key patterns, decisions, and anti-patterns preserved
4. **Recall**: Agents reference memory on subsequent tasks

### Memory Trigger Phrases

When users say:
- "Remember this"
- "Don't forget"
- "Going forward, always..."
- "Important: never..."
- "This pattern works well"

→ MPM agents should update relevant agent memories

## Configuration Files

### Project Configuration

`.claude-mpm/config/project.json`:
```json
{
  "project_name": "my-project",
  "project_type": ["python", "react"],
  "auto_deploy": true,
  "deployed_agents": [
    "universal/mpm-agent-manager",
    "universal/memory-manager",
    "engineer/backend/python-engineer",
    "engineer/frontend/react-engineer",
    "qa/qa",
    "ops/core/ops"
  ],
  "custom_agents": [],
  "memory_enabled": true
}
```

### Agent Overrides

`.claude-mpm/agent-overrides.json`:
```json
{
  "agent_overrides": {
    "python-engineer": {
      "python_version": "3.12",
      "test_framework": "pytest",
      "linter": "ruff"
    }
  }
}
```

## Agent Lifecycle

### Deployment States

1. **Available**: In cache, not deployed
2. **Deployed**: Active and available for delegation
3. **Active**: Currently executing a task
4. **Idle**: Deployed but not currently in use

### Agent Management Commands

```bash
# View agent status
claude-mpm agents status

# Deploy agent
claude-mpm agents deploy <agent-name>

# Undeploy agent
claude-mpm agents undeploy <agent-name>

# Update agent (from repository)
claude-mpm agents update <agent-name>

# List available agents in cache
claude-mpm agents list --available

# Search agents by capability
claude-mpm agents search "react testing"
```

## MPM-Specific Conventions

### Agent Naming

- **System agents**: `{category}/{subcategory}/{agent-name}`
- **MPM framework agents**: `claude-mpm/{agent-name}`
- **Use dashes**: `python-engineer`, not `python_engineer`

### Agent Communication

Agents communicate results back to PM in structured format:
```json
{
  "status": "completed|error|blocked",
  "work_product": "...",
  "evidence": "...",
  "handoff_to": "next-agent (optional)",
  "blockers": []
}
```

### File Tracking

All agents should track new files they create:
```bash
git status  # Check for new files
git add <files>  # Track deliverables
git commit -m "feat: description"  # Commit with context
```

## User Interaction Patterns

### When Users Request Functionality

**Scenario 1: Functionality exists in deployed agent**
→ PM delegates to that agent

**Scenario 2: Functionality exists in available (but not deployed) agent**
→ MPM agent suggests deploying that agent
→ User confirms
→ Agent deployed and task delegated

**Scenario 3: Functionality requires custom/missing agent**
→ MPM agent explains limitation
→ Suggests creating custom agent or manual workaround

### Agent Recommendation Examples

```
User: "I need to optimize these images"

MPM Agent: "I notice you don't have the imagemagick agent deployed.
This agent specializes in image optimization for web performance.

Available in cache: engineer/specialized/imagemagick

Would you like me to deploy it? It provides:
- Image format conversion
- Responsive image generation
- Compression optimization
- Batch processing

[Deploy] [Skip]"
```

```
User: "Help me refactor this legacy code"

MPM Agent: "I recommend deploying the refactoring-engineer agent for this task.
It specializes in safe, incremental code improvement with:
- Behavior-preserving transformations
- Comprehensive testing before/after
- Pattern recognition for code smells

This agent is available in your cache but not currently deployed.

[Deploy refactoring-engineer] [Use generic engineer instead]"
```

## Quality Standards for MPM Agents

### All MPM agents should:
- Understand the three-tier hierarchy
- Know how to scan the agent cache
- Suggest relevant agents based on user requests
- Explain agent capabilities clearly
- Support the PM delegation model
- Follow memory routing protocols
- Track files with git
- Provide evidence for all claims

### MPM agents SHOULD:
- Proactively suggest agent deployment when helpful
- Explain why specific agents are relevant
- Help users discover available functionality
- Guide users through agent configuration
- Maintain awareness of project context

### MPM agents should NOT:
- Deploy agents without user consent
- Override user preferences
- Assume capabilities not in agent cache
- Make recommendations without basis
- Skip evidence and verification

## Integration with PM Instructions

MPM agents work within the PM framework where:
- **PM delegates** all implementation work
- **PM never implements** code directly
- **PM verifies** all agent outputs
- **PM tracks** progress via TodoWrite
- **PM reports** results with evidence

MPM-specific agents enhance this by:
- Making more agents discoverable
- Enabling on-demand agent deployment
- Providing context about agent capabilities
- Facilitating the right agent for the right task
