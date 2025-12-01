---
name: Agent template submission
about: Submit a new agent template for review
title: '[NEW AGENT] '
labels: new-agent, community
assignees: ''
---

## Agent Information

### Metadata
- **Agent name**: (e.g., kotlin-engineer)
- **Category**: (e.g., engineer/backend)
- **Subcategory**: (e.g., backend, frontend, mobile)
- **Model**: (sonnet, opus, haiku)
- **Version**: (e.g., 1.0.0)

### Description
Brief description of what this agent does and when to use it.

### Technology Stack
- Primary language/framework: (e.g., Kotlin 1.9+)
- Key libraries: (e.g., Ktor, Exposed, Kotlinx.coroutines)
- Target platform: (e.g., JVM, Android, multiplatform)

### Capabilities
What can this agent do? List key capabilities:
- [ ] Capability 1
- [ ] Capability 2
- [ ] Capability 3

### Agent File
Please attach or link to your agent template file:
- File name: `{agent-name}.md`
- Location in hierarchy: `agents/{category}/{subcategory}/{agent-name}.md`

### BASE-AGENT.md Inheritance
Which BASE-AGENT.md files should this agent inherit from?
- [ ] `agents/BASE-AGENT.md` (always inherited)
- [ ] `agents/{category}/BASE-AGENT.md` (e.g., engineer, qa, ops)
- [ ] Additional subcategory BASE-AGENT.md (if applicable)

### Testing
Have you tested this agent?
- [ ] Built with `./build-agent.py`
- [ ] Validated with `./build-agent.py --validate`
- [ ] Deployed and tested in Claude MPM
- [ ] Verified inheritance works correctly

### Unique Instructions
What unique instructions are in this agent that aren't in BASE-AGENT.md?
(List the agent-specific content that makes this agent different from others)

### Tags
Suggested tags for this agent:
- Technology tags: (e.g., kotlin, jvm, coroutines)
- Domain tags: (e.g., backend, mobile, web)
- Use case tags: (e.g., api, microservices, android)

### AUTO-DEPLOY-INDEX.md
Should this agent be auto-deployed for certain project types?
- [ ] Yes
- [ ] No

If yes, what detection patterns should trigger auto-deployment?
- Indicator files: (e.g., `build.gradle.kts`, `settings.gradle.kts`)
- Dependencies: (e.g., `kotlin` in package.json)

### Additional Context
Any other context about this agent submission.

## Checklist
- [ ] Agent file follows template format (YAML frontmatter + markdown)
- [ ] Agent-specific instructions are focused and non-duplicative
- [ ] Agent has been tested with build-agent.py
- [ ] Agent uses dash-based naming convention
- [ ] Agent is placed in correct category/subcategory
- [ ] I have read CONTRIBUTING.md guidelines (if available)
