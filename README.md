# Claude MPM Agent Templates

A curated collection of specialized AI agent templates for [Claude MPM](https://github.com/bobmatnyc/claude-mpm) - the multi-agent orchestration framework for Claude Code.

**Key Features:**
- 🏗️ **BASE-AGENT.md Inheritance System** - Convention-based template inheritance eliminates duplication
- 📦 **Hierarchical Organization** - Agents organized by functional relationships (engineer, qa, ops, etc.)
- 🤖 **Auto-Deployment** - Intelligent agent selection based on project type detection
- 🔍 **Agent Discovery** - Cache scanning with semantic matching for recommendations
- ⚡ **57% Less Duplication** - Shared instructions managed in one place

## Overview

This repository contains production-ready agent templates in Markdown format with YAML frontmatter. Each agent is designed for specific engineering, operations, or quality assurance tasks within the Claude MPM framework.

The repository uses a **hierarchical organization with BASE-AGENT.md inheritance** to eliminate duplication and maintain consistency across related agents. When building an agent, content from BASE-AGENT.md files at each directory level is automatically combined, allowing shared instructions to be defined once and inherited by all agents in that category.

## Repository Structure

```
claude-mpm-agents/
├── agents/                          # Deployable agent templates
│   ├── BASE-AGENT.md               # Universal instructions (ALL agents inherit)
│   │
│   ├── claude-mpm/                 # Claude MPM framework agents
│   │   ├── BASE-AGENT.md          # MPM framework awareness
│   │   └── mpm-agent-manager.md   # Agent discovery & deployment
│   │
│   ├── universal/                  # Cross-cutting concerns
│   │   ├── memory-manager.md
│   │   ├── research.md
│   │   └── ...
│   │
│   ├── engineer/                   # Implementation specialists
│   │   ├── BASE-AGENT.md          # Shared engineering principles
│   │   ├── core/
│   │   │   └── engineer.md
│   │   ├── frontend/
│   │   │   ├── react-engineer.md
│   │   │   ├── nextjs-engineer.md
│   │   │   └── ...
│   │   ├── backend/
│   │   │   ├── python-engineer.md
│   │   │   ├── golang-engineer.md
│   │   │   └── ...
│   │   └── ...
│   │
│   ├── qa/                         # Quality assurance
│   │   ├── BASE-AGENT.md          # Shared QA standards
│   │   ├── qa.md
│   │   ├── api-qa.md
│   │   └── web-qa.md
│   │
│   └── ops/                        # Operations & deployment
│       ├── BASE-AGENT.md          # Shared ops protocols
│       ├── core/
│       │   └── ops.md
│       ├── platform/
│       │   ├── vercel-ops.md
│       │   └── ...
│       └── ...
│
├── templates/                       # Reference materials (NOT agents)
│   ├── circuit-breakers.md        # PM violation patterns
│   ├── pm-examples.md             # PM behavior examples
│   ├── validation-templates.md    # Verification templates
│   └── ...
│
├── build-agent.py                   # Build script for flattening agents
└── AUTO-DEPLOY-INDEX.md            # Project type detection rules
```

## BASE-AGENT.md Inheritance System

This repository uses a **convention-based inheritance system** to reduce duplication and maintain consistency.

### How It Works

When building an agent, content is combined in this order:

1. **Agent-specific content** (`{agent-name}.md`) - Unique instructions for this agent
2. **Directory BASE-AGENT.md** (if exists) - Shared instructions for agents in this directory
3. **Parent BASE-AGENT.md files** (recursive) - Instructions from parent directories
4. **Root BASE-AGENT.md** (always) - Universal instructions for ALL agents

**Example**: For `agents/engineer/backend/python-engineer.md`:
```
python-engineer.md
  + agents/engineer/backend/BASE-AGENT.md (if exists)
  + agents/engineer/BASE-AGENT.md
  + agents/BASE-AGENT.md
```

### BASE-AGENT.md Levels

#### Root Level (`agents/BASE-AGENT.md`)
Universal instructions for ALL agents:
- Git workflow standards
- Memory routing protocols
- Output format standards
- Handoff protocols
- Quality standards

#### Category Level (`agents/engineer/BASE-AGENT.md`, `agents/qa/BASE-AGENT.md`, etc.)
Shared instructions for all agents in a category:
- **Engineer**: SOLID principles, code reduction, type safety, testing requirements
- **QA**: Testing strategies, coverage standards, memory-efficient testing
- **Ops**: Deployment verification, security scanning, monitoring requirements

#### Subcategory Level (e.g., `agents/engineer/frontend/BASE-AGENT.md`)
Specific instructions for subcategories (optional, as needed)

### Building Flattened Agents

Agents in this repository are **modular** (source files) and must be **flattened** before use:

```bash
# Build a single agent
./build-agent.py agents/engineer/backend/python-engineer.md

# Build all agents
./build-agent.py --all

# Build to specific output directory
./build-agent.py --all --output-dir dist/agents

# Validate all agent definitions
./build-agent.py --validate
```

Built agents are placed in `dist/agents/` with the full inheritance chain combined.

### Why This Approach?

**Benefits**:
- ✅ **DRY (Don't Repeat Yourself)**: Common instructions defined once
- ✅ **Consistency**: All agents in a category follow same standards
- ✅ **Maintainability**: Update shared instructions in one place
- ✅ **Modularity**: Agent-specific content stays focused
- ✅ **Flexibility**: Add BASE-AGENT.md at any level as needed

**Example**: All engineering agents inherit:
- Root: Git workflows, output standards (200 lines)
- Engineer: SOLID principles, code reduction (300 lines)
- Agent: Python-specific patterns (150 lines)

**Total**: 650 lines, but only 150 lines are Python-specific!

## Agent Categories

### Claude MPM Framework Agents
Framework-level agents with MPM-specific awareness:
- **mpm-agent-manager** - Agent discovery, cache scanning, intelligent recommendations, and deployment orchestration

### Universal Agents
Cross-cutting concerns that apply to multiple domains:
- **memory-manager** - Project-specific memory management
- **product-owner** - Product strategy and prioritization
- **project-organizer** - Project organization and workflow
- **research** - Codebase investigation and analysis
- **code-analyzer** - Code review and pattern identification
- **content-agent** - Content optimization and SEO

### Engineering Agents

#### Core
- **engineer** - General-purpose software engineering

#### Frontend
- **web-ui** - Generic web UI development
- **react-engineer** - React with hooks and modern patterns
- **nextjs-engineer** - Next.js App Router and Server Components
- **svelte-engineer** - Svelte 5 with Runes and SvelteKit

#### Backend
- **python-engineer** - Python 3.12+ with type safety and async
- **golang-engineer** - Go with concurrency patterns
- **phoenix-engineer** - Elixir/Phoenix with LiveView, Ecto, and OTP foundations
- **java-engineer** - Java/Spring Boot with hexagonal architecture
- **ruby-engineer** - Ruby/Rails with service objects
- **rust-engineer** - Rust with ownership and safety
- **php-engineer** - PHP/Laravel with strict types
- **javascript-engineer** - Node.js/Express backend

#### Mobile
- **dart-engineer** - Dart/Flutter with clean architecture
- **tauri-engineer** - Tauri desktop applications

#### Data
- **data-engineer** - Data pipelines and ETL
- **typescript-engineer** - TypeScript 5.6+ with branded types

#### Specialized
- **refactoring-engineer** - Safe code refactoring
- **agentic-coder-optimizer** - Build system optimization
- **imagemagick** - Image optimization specialist
- **prompt-engineer** - Prompt optimization for Claude 4.5

### Quality Assurance Agents
- **qa** - General quality assurance
- **api-qa** - API testing and validation
- **web-qa** - Web application testing with Playwright

### Operations Agents

#### Core
- **ops** - General DevOps and infrastructure

#### Platform
- **vercel-ops** - Vercel deployment
- **gcp-ops** - Google Cloud Platform
- **clerk-ops** - Clerk authentication
- **local-ops** - Local development with PM2/Docker

#### Tooling
- **version-control** - Git operations and release coordination

### Security
- **security** - Security analysis and vulnerability assessment

### Documentation
- **documentation** - Technical documentation and API docs
- **ticketing** - Ticket management and tracking

## Template Format

Each agent template uses Markdown with YAML frontmatter:

```markdown
---
name: agent-name
description: Agent purpose and capabilities
agent_id: unique-identifier
agent_type: engineer|qa|ops|universal|documentation
model: sonnet|opus|haiku
version: 2.0.0
tags:
  - technology
  - domain
category: engineering|qa|ops|research
---

# Agent Name

Agent-specific instructions...

<!-- BASE-AGENT.md content automatically appended during build -->
```

## Usage

### With Claude MPM

These templates are designed to be used with Claude MPM:

1. **Build agents** (flattened with inheritance):
   ```bash
   ./build-agent.py --all --output-dir ~/.claude-mpm/agents
   ```

2. **Deploy agents** via Claude MPM CLI:
   ```bash
   claude-mpm agents deploy <agent-name>
   ```

3. **Use in Claude Code** via delegation:
   ```
   PM delegates to engineer agent for implementation tasks
   ```

### Customizing Templates

#### For Project-Specific Needs
1. Fork this repository
2. Modify BASE-AGENT.md files for project standards
3. Add custom agents as needed
4. Build and deploy to your Claude MPM instance

#### For Temporary Changes
1. Edit agent files in `agents/` directory
2. Rebuild with `./build-agent.py --all`
3. Deploy updated agents

## Template Schema

All templates follow the Claude MPM Agent Template Schema v1.3.0:

- **Metadata**: Name, version, description, tags, category
- **Configuration**: Model selection, resource limits, timeouts
- **Capabilities**: Memory limits, CPU allocation, network access
- **Dependencies**: Python packages, system requirements
- **Skills**: Reusable skill references
- **Knowledge**: Domain expertise, best practices, constraints
- **Interactions**: Input/output formats, handoff patterns
- **Memory Routing**: Memory categorization and keywords

## Development

### Building Agents

```bash
# Install Python 3.9+ (no additional dependencies required)

# Build single agent
./build-agent.py agents/engineer/backend/python-engineer.md

# Build all agents
./build-agent.py --all

# Validate all agents
./build-agent.py --validate

# Custom output directory
./build-agent.py --all --output-dir ~/my-agents
```

### Adding New Agents

1. **Determine category**: universal, engineer, qa, ops, etc.
2. **Create agent file**: `agents/{category}/{subcategory}/{agent-name}.md`
3. **Add YAML frontmatter**: name, description, agent_id, etc.
4. **Write agent-specific content**: Focus on unique instructions
5. **Build and validate**: `./build-agent.py --validate`

### Modifying BASE-AGENT.md Files

When updating shared instructions:

1. **Edit appropriate BASE-AGENT.md**:
   - Root level: Universal changes
   - Category level: Category-wide changes
   - Subcategory level: Specific subcategory changes

2. **Rebuild all affected agents**:
   ```bash
   ./build-agent.py --all
   ```

3. **Validate changes**:
   ```bash
   ./build-agent.py --validate
   ```

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

Part of the Claude MPM project. See main repository for license details.

## Related

- **Claude MPM**: https://github.com/bobmatnyc/claude-mpm
- **Documentation**: https://docs.claude.com/en/docs/claude-code
- **Community**: Claude MPM GitHub Discussions

---

**Repository Structure**: Agent templates with BASE-AGENT.md inheritance for consistency and maintainability.
