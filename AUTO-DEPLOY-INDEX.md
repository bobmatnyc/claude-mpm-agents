# Auto-Deploy Index

This file defines automatic agent deployment based on project type detection.

## How It Works

Claude MPM scans the project root directory for indicator files and automatically deploys relevant agents. Users can then add additional agents via the configurator or agent-manager.

## Universal Agents (Always Deployed)

These agents are deployed for **ALL** projects regardless of type:

### Claude MPM Framework Agents
- `claude-mpm/mpm-agent-manager` - Agent discovery, recommendations, and deployment orchestration

### Universal Agents
- `universal/memory-manager` - Project-specific memory management
- `universal/research` - Codebase investigation and analysis
- `universal/code-analyzer` - Code review and pattern identification

### Documentation Agents
- `documentation/documentation` - Technical documentation
- `documentation/ticketing` - Ticket management and tracking

## Project Type Detection

### Python Projects

**Indicator Files**: `pyproject.toml`, `requirements.txt`, `setup.py`, `Pipfile`, `poetry.lock`

**Auto-Deploy Agents**:
- `engineer/backend/python-engineer` - Python development
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations
- `security/security` - Security analysis

**Optional Agents** (based on additional files):
- `engineer/backend/data-engineer` - If `dbt_project.yml`, `airflow.cfg`, or `prefect.yaml` detected
- `engineer/frontend/web-ui` - If `templates/` or `static/` directory exists (Flask/Django)
- `ops/platform/gcp-ops` - If `cloudbuild.yaml` or `.gcloudignore` exists
- `ops/platform/vercel-ops` - If `vercel.json` exists

### JavaScript/TypeScript Projects

**Indicator Files**: `package.json`

**Auto-Deploy Agents**:
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations
- `security/security` - Security analysis

**Conditional Agents** (based on package.json dependencies):

#### React Projects
**Dependencies**: `"react"` in dependencies
- `engineer/frontend/react-engineer`
- `qa/web-qa` - Browser testing

#### Next.js Projects
**Dependencies**: `"next"` in dependencies
- `engineer/frontend/nextjs-engineer`
- `qa/web-qa` - Browser testing
- `ops/platform/vercel-ops` - If `vercel.json` exists

#### Svelte Projects
**Dependencies**: `"svelte"` in dependencies
- `engineer/frontend/svelte-engineer`
- `qa/web-qa` - Browser testing

#### Node.js Backend
**Dependencies**: `"express"`, `"fastify"`, or `"koa"` in dependencies
- `engineer/backend/javascript-engineer`
- `qa/api-qa` - API testing

#### TypeScript Projects
**Dependencies**: `"typescript"` in devDependencies
- `engineer/data/typescript-engineer`

### Rust Projects

**Indicator Files**: `Cargo.toml`

**Auto-Deploy Agents**:
- `engineer/backend/rust-engineer` - Rust development
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations
- `security/security` - Security analysis

**Optional Agents**:
- `engineer/mobile/tauri-engineer` - If `src-tauri/` directory exists

### Go Projects

**Indicator Files**: `go.mod`, `go.sum`

**Auto-Deploy Agents**:
- `engineer/backend/golang-engineer` - Go development
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations
- `security/security` - Security analysis

### Java Projects

**Indicator Files**: `pom.xml`, `build.gradle`, `build.gradle.kts`, `gradlew`

**Auto-Deploy Agents**:
- `engineer/backend/java-engineer` - Java/Spring Boot development
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations
- `security/security` - Security analysis

**Optional Agents**:
- `ops/platform/gcp-ops` - If `cloudbuild.yaml` exists

### Ruby Projects

**Indicator Files**: `Gemfile`, `Gemfile.lock`, `config.ru`

**Auto-Deploy Agents**:
- `engineer/backend/ruby-engineer` - Ruby/Rails development
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations
- `security/security` - Security analysis

### PHP Projects

**Indicator Files**: `composer.json`, `composer.lock`

**Auto-Deploy Agents**:
- `engineer/backend/php-engineer` - PHP/Laravel development
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations
- `security/security` - Security analysis

### Dart/Flutter Projects

**Indicator Files**: `pubspec.yaml`, `pubspec.lock`

**Auto-Deploy Agents**:
- `engineer/mobile/dart-engineer` - Flutter development
- `qa/qa` - Testing and quality assurance
- `ops/core/ops` - Deployment and operations

### Multi-Language Projects

When multiple language indicators are detected, deploy agents for ALL detected languages:

**Example**: Python + React project
- `engineer/backend/python-engineer`
- `engineer/frontend/react-engineer`
- `qa/qa`
- `qa/web-qa`
- `ops/core/ops`
- `security/security`

## Platform-Specific Detection

### Vercel
**Indicator Files**: `vercel.json`, `.vercelignore`
- `ops/platform/vercel-ops`

### Google Cloud Platform
**Indicator Files**: `cloudbuild.yaml`, `app.yaml`, `.gcloudignore`
- `ops/platform/gcp-ops`

### Clerk Authentication
**Indicator Files**: `.env` containing `CLERK_` variables, or `clerk.json`
- `ops/platform/clerk-ops`

### Docker/Containers
**Indicator Files**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`
- `ops/platform/local-ops` - Local development with Docker

### PM2 (Node.js)
**Indicator Files**: `ecosystem.config.js`, `pm2.config.js`
- `ops/platform/local-ops` - Local development with PM2

## Specialized Detection

### Data Engineering
**Indicator Files**:
- `dbt_project.yml` (dbt)
- `airflow.cfg` (Apache Airflow)
- `prefect.yaml` (Prefect)
- `dagster.yaml` (Dagster)

**Deploy**:
- `engineer/data/data-engineer`

### Image Processing
**Indicator Files**:
- `package.json` with `"sharp"`, `"jimp"`, or `"imagemagick"` dependencies
- `requirements.txt` with `Pillow` or `imagemagick`

**Deploy**:
- `engineer/specialized/imagemagick`

### Build Optimization
**Indicator Files**: `Makefile`, `webpack.config.js`, `vite.config.ts`, `rollup.config.js`

**Deploy**:
- `engineer/specialized/agentic-coder-optimizer`

## Version Control Detection

**Indicator Files**: `.git/` directory

**Auto-Deploy Agents**:
- `ops/tooling/version-control` - Git operations

## Detection Priority

When multiple indicators match:

1. **Universal agents** - Always deployed first
2. **Language-specific agents** - Based on primary language
3. **Framework-specific agents** - Based on dependencies
4. **Platform-specific agents** - Based on deployment targets
5. **Specialized agents** - Based on specific tools/libraries

## Agent Deployment Order

```
1. Universal agents (agent-manager, memory-manager, research, etc.)
2. Primary language engineer (python, rust, javascript, etc.)
3. Framework engineers (react, nextjs, etc.)
4. QA agents (qa, api-qa, web-qa)
5. Ops agents (ops, platform-specific)
6. Security agent
7. Specialized agents (optional based on detection)
```

## Configuration Override

Users can override auto-detection by creating `.claude-mpm/agent-config.json`:

```json
{
  "auto_deploy": true,
  "override_agents": {
    "include": [
      "engineer/specialized/refactoring-engineer",
      "universal/product-owner"
    ],
    "exclude": [
      "qa/web-qa"
    ]
  },
  "deployment_priority": [
    "universal/*",
    "engineer/*",
    "qa/*",
    "ops/*",
    "security/*"
  ]
}
```

## Default Deployment Sets

### Minimal (Micro Projects)
- Universal agents only
- Primary language engineer
- Generic QA
- Generic Ops

### Standard (Most Projects)
- All detected language/framework agents
- Appropriate QA agents
- Platform-specific ops
- Security

### Full (Enterprise Projects)
- All detected agents
- Specialized agents (refactoring, optimization)
- Product owner
- Full platform coverage

## Detection Implementation

The auto-deploy logic should:

1. **Scan project root** for indicator files
2. **Read configuration files** (package.json, pyproject.toml, etc.)
3. **Build agent list** based on detection rules
4. **Remove duplicates** (same agent from multiple rules)
5. **Order by priority** (universal → language → framework → platform)
6. **Apply user overrides** (if `.claude-mpm/agent-config.json` exists)
7. **Deploy agents** in order

## Example Detection Results

### Example 1: Next.js + TypeScript Project

**Detected Files**:
- `package.json` (with "next", "typescript", "react")
- `vercel.json`
- `.git/`

**Auto-Deploy**:
```
Claude MPM Framework:
  - claude-mpm/mpm-agent-manager

Universal:
  - universal/memory-manager
  - universal/research
  - universal/code-analyzer

Documentation:
  - documentation/documentation
  - documentation/ticketing

Engineering:
  - engineer/frontend/nextjs-engineer
  - engineer/frontend/react-engineer
  - engineer/data/typescript-engineer

QA:
  - qa/qa
  - qa/web-qa

Ops:
  - ops/core/ops
  - ops/platform/vercel-ops
  - ops/tooling/version-control

Security:
  - security/security
```

### Example 2: Python FastAPI + React Project

**Detected Files**:
- `pyproject.toml` (FastAPI dependencies)
- `package.json` (React dependencies)
- `Dockerfile`
- `.git/`

**Auto-Deploy**:
```
Claude MPM Framework:
  - claude-mpm/mpm-agent-manager

Universal:
  - universal/memory-manager
  - universal/research
  - universal/code-analyzer

Documentation:
  - documentation/documentation
  - documentation/ticketing

Engineering:
  - engineer/backend/python-engineer
  - engineer/frontend/react-engineer

QA:
  - qa/qa
  - qa/api-qa
  - qa/web-qa

Ops:
  - ops/core/ops
  - ops/platform/local-ops (Docker detected)
  - ops/tooling/version-control

Security:
  - security/security
```

### Example 3: Rust CLI Tool

**Detected Files**:
- `Cargo.toml`
- `.git/`

**Auto-Deploy**:
```
Claude MPM Framework:
  - claude-mpm/mpm-agent-manager

Universal:
  - universal/memory-manager
  - universal/research
  - universal/code-analyzer

Documentation:
  - documentation/documentation
  - documentation/ticketing

Engineering:
  - engineer/backend/rust-engineer

QA:
  - qa/qa

Ops:
  - ops/core/ops
  - ops/tooling/version-control

Security:
  - security/security
```

## Agent Schema Validation

Agent frontmatter is validated at build time via `build-agent.py`. The `schema_version` field is required in all agent frontmatter and is checked against the current canonical version (`1.3.0`). Agents with a missing or outdated `schema_version` will produce validation warnings.

To validate all agents: `python3 build-agent.py --validate`

## Maintenance

This index should be updated when:
- New agents are added
- New detection patterns are identified
- Platform integrations change
- User feedback indicates missing detection rules
