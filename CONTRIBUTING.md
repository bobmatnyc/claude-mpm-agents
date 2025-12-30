# Contributing to Claude MPM Agent Templates

Thank you for your interest in contributing to the Claude MPM Agent Templates repository! This document provides guidelines for contributing agent templates, enhancements, and improvements.

## Overview

This repository contains **agent templates** for Claude MPM, not the main framework. Agent templates are markdown files with YAML frontmatter that define specialized AI agents for different tasks (engineering, QA, operations, etc.).

**Key Concepts:**
- **BASE-AGENT.md Inheritance**: Shared instructions that eliminate duplication across agents
- **Hierarchical Organization**: Agents organized by functional category (engineer, qa, ops, etc.)
- **Build Process**: Templates are compiled into deployable agent definitions
- **Auto-Deployment**: Agents can be automatically deployed based on project detection

## Quick Start for Contributors

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR-USERNAME/claude-mpm-agents.git
cd claude-mpm-agents
```

### 2. Understand the Structure

```
agents/
├── BASE-AGENT.md                    # Root-level shared instructions
├── engineer/
│   ├── BASE-AGENT.md               # Engineer-specific shared instructions
│   ├── backend/
│   │   ├── python-engineer.md      # Agent-specific content only
│   │   ├── golang-engineer.md
│   │   └── ...
│   └── frontend/
│       ├── react-engineer.md
│       └── ...
├── qa/
│   ├── BASE-AGENT.md
│   ├── qa.md
│   └── api-qa.md
└── ...

templates/                           # Reference materials (not deployed)
├── circuit-breakers.md
├── pm-examples.md
└── ...
```

### 3. Create a New Agent

**Option A: Using the build tool (recommended)**
```bash
./build-agent.py --create engineer/backend/kotlin-engineer
```

**Option B: Manual creation**
1. Create file in appropriate category: `agents/engineer/backend/kotlin-engineer.md`
2. Add YAML frontmatter
3. Write agent-specific instructions
4. Build and validate

### 4. Build and Test

```bash
# Build all agents (creates dist/agents/ directory)
./build-agent.py

# Validate structure and frontmatter
./build-agent.py --validate

# Build specific agent
./build-agent.py engineer/backend/kotlin-engineer

# Test in Claude MPM
claude-mpm agents deploy --file dist/agents/engineer/backend/kotlin-engineer.md
```

### 5. Submit Pull Request

```bash
git checkout -b feat/add-kotlin-engineer
git add agents/engineer/backend/kotlin-engineer.md
git commit -m "feat: add Kotlin engineer agent for JVM backend development"
git push origin feat/add-kotlin-engineer
```

Then create a PR on GitHub using the pull request template.

## BASE-AGENT.md Inheritance System

### How Inheritance Works

When you build an agent, the build process automatically **appends** BASE-AGENT.md content from the inheritance chain:

```
agents/engineer/backend/python-engineer.md
    ↓ (inherits from)
agents/engineer/backend/BASE-AGENT.md
    ↓ (inherits from)
agents/engineer/BASE-AGENT.md
    ↓ (inherits from)
agents/BASE-AGENT.md
```

**Final compiled agent** = python-engineer.md content + all BASE-AGENT.md files in chain

### What to Put Where

**❌ DON'T duplicate in agent-specific files:**
- General PM delegation rules
- Common quality standards
- Standard error handling patterns
- Universal testing requirements

**✅ DO include in agent-specific files:**
- Language/framework-specific patterns
- Technology stack capabilities
- Unique tool configurations
- Specialized workflows

**Example: python-engineer.md should contain:**
```markdown
---
agent_id: python-engineer
category: engineer/backend
model: sonnet
version: 1.0.0
---

# Python Engineer Agent

## Technology Stack
- Python 3.11+
- FastAPI, Django, Flask
- SQLAlchemy, Alembic
- pytest, mypy, ruff

## Capabilities
- Type-safe API development with FastAPI
- Database migrations with Alembic
- Async programming with asyncio
- Testing with pytest and fixtures

## Implementation Patterns

### FastAPI Service Pattern
[Agent-specific pattern details...]

### Database Session Management
[Agent-specific pattern details...]
```

**BASE-AGENT.md should contain:**
```markdown
# Common Engineering Standards

## Code Quality Requirements
- All code must pass linting
- Type hints required
- Comprehensive error handling
- Performance considerations

## Testing Requirements
- Unit tests for all functions
- Integration tests for APIs
- 80%+ code coverage

[... shared content for all engineers ...]
```

### Benefits of Inheritance

- **57% less duplication**: Shared instructions in one place
- **Consistency**: All agents follow same base standards
- **Maintainability**: Update once, applies to all agents
- **Focus**: Agent files only contain unique content

## Agent File Guidelines

### File Naming Convention

**✅ Correct:**
- `python-engineer.md`
- `api-qa.md`
- `vercel-ops.md`
- `mpm-agent-manager.md`

**❌ Incorrect:**
- `python_engineer.md` (underscores)
- `PythonEngineer.md` (PascalCase)
- `pythonEngineer.md` (camelCase)

**Rule**: Use lowercase with dashes (kebab-case)

### File Location

Place agents in the category that matches their primary function:

- **engineer/backend**: Backend language engineers (Python, Go, Java, etc.)
- **engineer/frontend**: Frontend framework engineers (React, Vue, Svelte, etc.)
- **engineer/mobile**: Mobile platform engineers (Flutter, React Native, etc.)
- **engineer/fullstack**: Full-stack framework engineers (Next.js, SvelteKit, etc.)
- **qa**: Quality assurance and testing agents
- **ops/platform**: Platform-specific operations (Vercel, GCP, Railway, etc.)
- **ops/infra**: Infrastructure and deployment agents
- **universal**: Cross-cutting agents (research, documentation, etc.)
- **claude-mpm**: MPM-specific agents (agent-manager, ticketing, etc.)

### YAML Frontmatter

**Required fields:**
```yaml
---
agent_id: kotlin-engineer        # Must match filename (without .md)
category: engineer/backend       # Must match directory path
model: sonnet                    # sonnet, opus, or haiku
version: 1.0.0                   # Semantic versioning
---
```

**Optional fields:**
```yaml
tags:                            # Technology and domain tags
  - kotlin
  - jvm
  - spring-boot
  - coroutines

routing:                         # Auto-deployment rules
  keywords:
    - kotlin
    - spring
  paths:
    - "*.kt"
    - "build.gradle.kts"
  priority: 100
```

### Agent Content Structure

**Recommended sections:**

```markdown
---
[frontmatter]
---

# [Agent Name] Agent

## Technology Stack
List primary languages, frameworks, and tools

## Capabilities
What can this agent do?

## When to Use This Agent
Specific use cases and scenarios

## Implementation Patterns
Agent-specific patterns and best practices

## Common Workflows
Step-by-step workflows for typical tasks

## Examples
Code examples and usage demonstrations
```

## Avoiding Duplication with BASE-AGENT.md

### Before Creating a New Agent

**Ask yourself:**
1. Does this content apply to ALL agents? → Put in `agents/BASE-AGENT.md`
2. Does this apply to all engineers? → Put in `agents/engineer/BASE-AGENT.md`
3. Does this apply to all backend engineers? → Put in `agents/engineer/backend/BASE-AGENT.md`
4. Is this Python-specific? → Put in `agents/engineer/backend/python-engineer.md`

### Common Duplication Mistakes

**❌ Mistake 1: Duplicating quality standards**
```markdown
# In python-engineer.md (WRONG)
All code must pass linting and have type hints.
Tests are required with 80%+ coverage.

# Should be in agents/engineer/BASE-AGENT.md or agents/BASE-AGENT.md
```

**❌ Mistake 2: Duplicating PM delegation rules**
```markdown
# In react-engineer.md (WRONG)
Never implement directly. Always delegate to appropriate agent.

# Should be in agents/BASE-AGENT.md
```

**✅ Correct: Agent-specific content only**
```markdown
# In python-engineer.md (CORRECT)
## FastAPI-Specific Patterns

Use dependency injection for database sessions:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
```

## Auto-Deployment Configuration

Agents can be automatically deployed when Claude MPM detects certain project types.

### Adding Auto-Deploy Rules

1. **Add routing to agent frontmatter:**
```yaml
routing:
  keywords:                    # Keywords in dependencies or code
    - fastapi
    - uvicorn
  paths:                       # File patterns to detect
    - "requirements.txt"
    - "pyproject.toml"
  priority: 100                # Higher = preferred when multiple match
```

2. **Update AUTO-DEPLOY-INDEX.md** (if creating new patterns):
   - Document the detection logic
   - Explain why this agent is chosen
   - Note any conflicts with other agents

### Testing Auto-Deployment

```bash
# In a FastAPI project
claude-mpm agents auto-configure --preview

# Should show python-engineer in recommendations
```

## Commit and PR Guidelines

### Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) for versioning:

- `feat: add Kotlin engineer agent` → Minor version bump
- `fix: correct Python engineer FastAPI pattern` → Patch version bump
- `feat!: restructure agent categories` → Major version bump (breaking)
- `docs: update BASE-AGENT.md inheritance guide` → No version bump
- `refactor: rename python_engineer to python-engineer` → No version bump

### PR Process

1. **Create issue first** (for new agents or major changes)
2. **Fork and create branch**: `feat/add-kotlin-engineer`
3. **Make changes** following guidelines above
4. **Build and validate**: `./build-agent.py --validate`
5. **Test locally**: Deploy and test in Claude MPM
6. **Commit with conventional format**
7. **Push and create PR** using the PR template
8. **Address review feedback**

### PR Checklist

Before submitting:
- [ ] Agent uses dash-based naming (`kotlin-engineer.md`, not `kotlin_engineer.md`)
- [ ] Agent is in correct category directory
- [ ] YAML frontmatter is complete and valid
- [ ] Agent-specific content only (no duplication of BASE-AGENT.md)
- [ ] Built successfully with `./build-agent.py`
- [ ] Validated with `./build-agent.py --validate`
- [ ] Tested deployment in Claude MPM
- [ ] AUTO-DEPLOY-INDEX.md updated (if adding auto-deploy rules)
- [ ] README.md updated (if adding new category)

## Building Agents

### Build Process

The build process:
1. Reads agent-specific content from `agents/[category]/[agent].md`
2. Walks up directory tree collecting all `BASE-AGENT.md` files
3. Appends BASE-AGENT.md content in order (root → category → subcategory)
4. Writes compiled agent to `dist/agents/[category]/[agent].md`

### Build Commands

```bash
# Build all agents
./build-agent.py

# Build specific category
./build-agent.py engineer/backend

# Build specific agent
./build-agent.py engineer/backend/python-engineer

# Validate all agents
./build-agent.py --validate

# Show inheritance chain
./build-agent.py --show-inheritance engineer/backend/python-engineer

# Preview final output
./build-agent.py --preview engineer/backend/python-engineer
```

### Validation Rules

The validator checks:
- ✅ Valid YAML frontmatter
- ✅ Required fields present (`agent_id`, `category`, `model`, `version`)
- ✅ File location matches category
- ✅ Filename matches agent_id
- ✅ Dash-based naming convention
- ✅ Model is valid (sonnet, opus, haiku)
- ✅ Version follows semantic versioning

## Common Development Tasks

### Adding a New Language Engineer

1. **Choose category**: `agents/engineer/backend/` or `agents/engineer/frontend/`
2. **Create file**: `agents/engineer/backend/kotlin-engineer.md`
3. **Add frontmatter**:
```yaml
---
agent_id: kotlin-engineer
category: engineer/backend
model: sonnet
version: 1.0.0
tags:
  - kotlin
  - jvm
  - spring-boot
routing:
  keywords:
    - kotlin
    - spring
  paths:
    - "*.kt"
    - "build.gradle.kts"
  priority: 100
---
```
4. **Write content**: Focus on Kotlin-specific patterns only
5. **Build and test**: `./build-agent.py engineer/backend/kotlin-engineer`
6. **Submit PR**

### Enhancing an Existing Agent

1. **Identify what to change**: Agent-specific or shared content?
2. **If shared**: Edit appropriate BASE-AGENT.md file
3. **If agent-specific**: Edit the agent file directly
4. **Rebuild**: `./build-agent.py [agent-path]`
5. **Test**: Deploy updated agent and verify changes
6. **Submit PR** with clear description of enhancement

### Creating a New Category

1. **Create directory**: `agents/new-category/`
2. **Create BASE-AGENT.md**: `agents/new-category/BASE-AGENT.md`
3. **Add shared content** for all agents in this category
4. **Create first agent**: `agents/new-category/first-agent.md`
5. **Update README.md**: Document new category
6. **Submit PR** explaining rationale for new category

## Troubleshooting

### Common Issues

**Issue 1: Build fails with "File not found"**
- **Cause**: Incorrect file path or category mismatch
- **Fix**: Ensure file location matches `category` in frontmatter

**Issue 2: Validation fails with "Invalid frontmatter"**
- **Cause**: YAML syntax error or missing required field
- **Fix**: Check YAML syntax, ensure all required fields present

**Issue 3: Agent content is duplicated**
- **Cause**: Content in agent file that should be in BASE-AGENT.md
- **Fix**: Move shared content to appropriate BASE-AGENT.md file

**Issue 4: Auto-deployment not working**
- **Cause**: Missing or incorrect routing rules
- **Fix**: Add `routing` section to frontmatter with correct patterns

### Getting Help

- **Issue Templates**: Use GitHub issue templates for bug reports or feature requests
- **Discussions**: GitHub Discussions for questions and community support
- **Documentation**: README.md for repository overview and structure
- **Examples**: Study existing agents for patterns and structure

## Questions?

- 📚 **Repository Overview**: [README.md](README.md)
- 🏗️ **Agent Structure**: See "Repository Structure" in README
- 🔧 **Build System**: `./build-agent.py --help`
- 🤖 **Example Agents**: Browse `agents/` directory for reference

Thank you for contributing to Claude MPM Agent Templates! 🚀
