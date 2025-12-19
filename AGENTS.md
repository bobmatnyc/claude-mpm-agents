# Repository Guidelines

## Project Structure & Module Organization
- `agents/`: Source agent templates with YAML frontmatter. Each category (engineer, qa, ops, universal, claude-mpm, documentation, security) may include a `BASE-AGENT.md` for inherited standards plus agent-specific files such as `agents/engineer/backend/python-engineer.md`.
- `templates/`: Reference material and examples (`AGENT_TEMPLATE_REFERENCE.md`, `circuit-breakers.md`, validation patterns); not deployed.
- `docs/`: Research notes and analyses that inform template authoring.
- `build-agent.py`: Python 3.9+ build tool that flattens inheritance and validates agents. Default output is `build/` (use `--output-dir` to change).

## Build, Test, and Development Commands
- `./build-agent.py --all`: Build every agent into `build/` using the inheritance chain.
- `./build-agent.py --validate`: Run structure/frontmatter checks (required before PRs).
- `./build-agent.py --preview agents/engineer/backend/python-engineer.md`: Show the compiled output for one agent.
- `./build-agent.py --show-inheritance agents/engineer/backend/python-engineer.md`: Inspect which `BASE-AGENT.md` files are applied.
- `./build-agent.py --create engineer/backend/kotlin-engineer`: Scaffold a new agent path with starter frontmatter.

## Coding Style & Naming Conventions
- File names: lowercase kebab-case (`kotlin-engineer.md`), stored in the directory that matches the `category` frontmatter.
- Required frontmatter fields: `agent_id`, `category`, `model` (`sonnet|opus|haiku`), `version` (semver). Keep YAML indented with two spaces.
- Content rules: Put shared instructions in the nearest `BASE-AGENT.md`; keep agent files focused on technology- or workflow-specific guidance. Avoid duplicating universal standards.
- Formatting: Markdown with concise headings; prefer bullet lists and short, actionable sentences.

## Skill References
- **IMPORTANT**: Only reference skills from the `claude-mpm-skills` repository (110 production-ready skills).
- Skills are Claude Code skills loaded at startup that provide specialized knowledge and patterns.
- Available skills are organized into `universal/` (32 skills) and `toolchains/` (76 skills).
- See `../claude-mpm-skills/manifest.json` for the complete list of valid skill names.
- See `../claude-mpm-skills/README.md` for skill descriptions and categories.
- Common universal skills: `test-driven-development`, `systematic-debugging`, `security-scanning`, `git-workflow`, `git-worktrees`, `stacked-prs`, `database-migration`, `api-documentation`, `test-quality-inspector`.
- **Validation**: Run `python3 scripts/audit_skills.py` to verify all skill references are valid.
- **Never** reference skills from external repositories (e.g., obra/superpowers, alirezarezvani/claude-skills).

## Testing Guidelines
- Primary check is validation: run `./build-agent.py --validate` and fix any frontmatter or path mismatches.
- For inheritance sanity, run `--preview` and skim for duplicated or missing sections before publishing.
- If adding auto-deploy routing, confirm patterns in `AUTO-DEPLOY-INDEX.md` and keep keyword/path lists minimal.

## Commit & Pull Request Guidelines
- Use Conventional Commits (`feat: add kotlin engineer agent`, `docs: update base agent inheritance guide`). Include `!` for breaking reorganizations.
- PRs should state the agent(s) touched, why changes live in agent vs. `BASE-AGENT.md`, and note `./build-agent.py --validate` output. Link related issues and update `README.md` or `AUTO-DEPLOY-INDEX.md` when categories or routing change.
- Avoid committing generated artifacts; keep `build/` out of PRs unless explicitly requested.

## Security & Configuration Tips
- Do not embed secrets or proprietary data in agent instructions or frontmatter.
- Keep routing rules narrowly scoped to avoid over-deploying agents; prefer specific file patterns (`pyproject.toml`, `package.json`) and domain keywords.
- When adding new categories, include a `BASE-AGENT.md` describing shared security, quality, and handoff expectations.
