# Claude MPM Agent Templates

A curated collection of specialized AI agent templates for [Claude MPM](https://github.com/bobmatnyc/claude-mpm) - the multi-agent orchestration framework for Claude Code.

## Overview

This repository contains 48 production-ready agent templates in Markdown format with YAML frontmatter. Each agent is designed for specific engineering, operations, or quality assurance tasks within the Claude MPM framework.

## Agent Categories

### Engineering Agents
- **engineer** - General-purpose software engineering
- **python_engineer** - Python development with type safety and testing
- **typescript_engineer** - TypeScript 5.6+ with branded types and strict mode
- **react_engineer** - React development with hooks and modern patterns
- **nextjs_engineer** - Next.js App Router and Server Components
- **golang_engineer** - Go development with concurrency patterns
- **rust_engineer** - Rust development with ownership and safety
- **java_engineer** - Java/Spring Boot with hexagonal architecture
- **ruby_engineer** - Ruby/Rails with service objects and RSpec
- **php_engineer** - PHP/Laravel with strict types and testing
- **dart_engineer** - Dart/Flutter with clean architecture
- **svelte_engineer** - Svelte 5 with Runes and SvelteKit
- **tauri_engineer** - Tauri desktop app development
- **javascript_engineer_agent** - Vanilla JavaScript and Node.js backend
- **data_engineer** - Data pipeline and ETL development

### Quality Assurance Agents
- **qa** - General quality assurance and testing
- **web_qa** - Web application testing with Playwright
- **api_qa** - API testing and validation

### Operations Agents
- **ops** - General DevOps and infrastructure
- **local_ops_agent** - Local development with PM2 and Docker
- **vercel_ops_agent** - Vercel deployment and operations
- **gcp_ops_agent** - Google Cloud Platform operations
- **clerk_ops** - Clerk authentication operations

### Research & Analysis Agents
- **research** - Codebase investigation and analysis
- **code_analyzer** - Code review and pattern identification
- **security** - Security analysis and vulnerability assessment

### Documentation & Support Agents
- **documentation** - Technical documentation and API docs
- **ticketing** - Ticket management and tracking
- **product_owner** - Product strategy and prioritization

### Framework Management Agents
- **agent-manager** - Agent lifecycle and deployment
- **memory_manager** - Project-specific memory management
- **version_control** - Git operations and release coordination
- **project_organizer** - Project organization and workflow

### Specialized Agents
- **refactoring_engineer** - Safe code refactoring
- **prompt_engineer** - Prompt optimization for Claude 4.5
- **content_agent** - Content optimization and SEO
- **imagemagick** - Image optimization specialist
- **agentic_coder_optimizer** - Build system optimization

### Template Documentation
- **circuit_breakers** - PM violation detection rules
- **git_file_tracking** - Git file tracking protocols
- **pm_examples** - PM delegation examples
- **pm_red_flags** - PM violation phrase indicators
- **research_gate_examples** - Research gate protocol examples
- **response_format** - PM response format templates
- **ticket_completeness_examples** - Ticket completeness examples
- **validation_templates** - Validation and verification templates

## Template Format

Each agent template uses Markdown with YAML frontmatter:

```markdown
---
name: agent_name
description: Agent purpose and capabilities
agent_id: unique-identifier
agent_type: engineer|qa|ops|research|documentation
model: sonnet|opus|haiku
version: 2.0.0
tags:
  - technology
  - domain
category: engineering|qa|ops|research
---

# Agent Name

Agent instructions and guidelines...
```

## Usage

These templates are designed to be used with Claude MPM:

1. **Deploy agents** via Claude MPM CLI:
   ```bash
   claude-mpm agents deploy <agent-name>
   ```

2. **Use in Claude Code** via delegation:
   ```
   PM delegates to engineer agent for implementation tasks
   ```

3. **Customize templates** for your specific needs

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

**Generated from Claude MPM v2.8.0** - Agent templates converted from JSON to Markdown format.
