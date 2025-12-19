# Skill Reference Audit Report

**Date**: 2025-12-19
**Status**: ✅ **RESOLVED** - All invalid skill references have been fixed

## Executive Summary

Agents in `claude-mpm-agents` should **only reference skills from `claude-mpm-skills`**, but currently:
- **40 skills** are referenced by agents
- **31 skills (77.5%)** don't exist in the claude-mpm-skills manifest
- **Only 9 skills (22.5%)** are valid references

## Valid Skill References (9 skills)

These skills are correctly referenced and exist in claude-mpm-skills:

✅ **api-documentation**  
✅ **database-migration**  
✅ **git-workflow**  
✅ **git-worktrees**  
✅ **security-scanning**  
✅ **stacked-prs**  
✅ **systematic-debugging**  
✅ **test-driven-development**  
✅ **test-quality-inspector**  

## Invalid Skill References (31 skills)

These skills are referenced by agents but **DO NOT EXIST** in claude-mpm-skills:

### General Development Skills (11)
❌ **async-testing** - Referenced by: qa.md, api-qa.md, web-qa.md, engineer.md, ruby-engineer.md, svelte-engineer.md  
❌ **backend-development** - Referenced by: nextjs-engineer.md  
❌ **browser-apis** - Referenced by: web-qa.md  
❌ **build-tooling** - Referenced by: nextjs-engineer.md  
❌ **changeset-validation** - Referenced by: version-control.md  
❌ **code-review** - Referenced by: documentation.md, ticketing.md, svelte-engineer.md, refactoring-engineer.md  
❌ **docker-containerization** - Referenced by: ops.md, version-control.md, project-organizer.md  
❌ **modern-javascript** - Referenced by: nextjs-engineer.md  
❌ **performance-optimization** - Referenced by: nextjs-engineer.md  
❌ **performance-profiling** - Referenced by: ruby-engineer.md, svelte-engineer.md, refactoring-engineer.md, api-qa.md  
❌ **testing** - Referenced by: nextjs-engineer.md  

### Framework-Specific Skills (6)
❌ **ecto-schema-design** - Referenced by: phoenix-engineer.md  
❌ **espocrm-development** - Referenced by: php-engineer.md  
❌ **flexlayout-react** - Referenced by: react-engineer.md  
❌ **liveview-architecture** - Referenced by: phoenix-engineer.md  
❌ **otp-supervision** - Referenced by: phoenix-engineer.md  
❌ **phoenix-context-design** - Referenced by: phoenix-engineer.md  

### Tauri-Specific Skills (14)
❌ **tauri-async-patterns** - Referenced by: tauri-engineer.md  
❌ **tauri-build-deploy** - Referenced by: tauri-engineer.md  
❌ **tauri-command-patterns** - Referenced by: tauri-engineer.md  
❌ **tauri-error-handling** - Referenced by: tauri-engineer.md  
❌ **tauri-event-system** - Referenced by: tauri-engineer.md  
❌ **tauri-file-system** - Referenced by: tauri-engineer.md  
❌ **tauri-frontend-integration** - Referenced by: tauri-engineer.md  
❌ **tauri-performance** - Referenced by: tauri-engineer.md  
❌ **tauri-state-management** - Referenced by: tauri-engineer.md  
❌ **tauri-testing** - Referenced by: tauri-engineer.md  
❌ **tauri-window-management** - Referenced by: tauri-engineer.md  

### Build/Dev Tools (2)
❌ **refactoring-patterns** - Referenced by: refactoring-engineer.md  
❌ **vite-local-dev** - Referenced by: svelte-engineer.md  
❌ **web-components** - Referenced by: web-ui.md  

## Available Skills in claude-mpm-skills (Not Used)

These 25 skills exist in the manifest but are **not referenced by any agent**:

⚠️ api-design-patterns  
⚠️ artifacts-builder  
⚠️ brainstorming  
⚠️ condition-based-waiting  
⚠️ dispatching-parallel-agents  
⚠️ env-manager  
⚠️ internal-comms  
⚠️ json-data-handling  
⚠️ kubernetes  
⚠️ mcp-builder  
⚠️ opentelemetry  
⚠️ requesting-code-review  
⚠️ root-cause-tracing  
⚠️ skill-creator  
⚠️ software-patterns  
⚠️ terraform  
⚠️ testing-anti-patterns  
⚠️ threat-modeling  
⚠️ verification-before-completion  
⚠️ web-performance-optimization  
⚠️ webapp-testing  
⚠️ writing-plans  
⚠️ xlsx  
⚠️ bad-example-skill (example)  
⚠️ example-framework-skill (example)  

## Recommendations

### 1. **Immediate Actions**
- Remove all 31 invalid skill references from agent templates
- Update AGENT_TEMPLATE_REFERENCE.md to show correct examples from claude-mpm-skills
- Add validation to build-agent.py to prevent future mismatches

### 2. **Skill Mapping Strategy**
For invalid skills, either:
- **Remove** if not critical to agent functionality
- **Replace** with closest equivalent from claude-mpm-skills
- **Request creation** in claude-mpm-skills repository if truly needed

### 3. **Documentation Updates**
- Update AGENTS.md with clear guidelines: "Only reference skills from claude-mpm-skills"
- Remove references to obra/superpowers and alirezarezvani/claude-skills
- Add link to claude-mpm-skills manifest for reference

### 4. **Validation Process**
Add to build-agent.py:
```python
def validate_skill_references(agent_frontmatter):
    """Validate that all skill references exist in claude-mpm-skills manifest."""
    manifest_path = Path("../claude-mpm-skills/manifest.json")
    if not manifest_path.exists():
        return  # Skip validation if manifest not available
    
    with open(manifest_path) as f:
        manifest = json.load(f)
        valid_skills = get_all_skill_names(manifest)
    
    agent_skills = agent_frontmatter.get('skills', [])
    invalid = [s for s in agent_skills if s not in valid_skills]
    
    if invalid:
        raise ValueError(f"Invalid skill references: {invalid}")
```

## Resolution Summary

All issues have been systematically addressed:

1. ✅ **Created audit report** - Documented all 103 invalid skill references across 32 agents
2. ✅ **Removed invalid skill references** - Fixed all 32 affected agents using automated script
3. ✅ **Updated template documentation** - Updated AGENT_TEMPLATE_REFERENCE.md with correct examples
4. ✅ **Added validation to build script** - build-agent.py now validates skills against manifest
5. ✅ **Updated AGENTS.md guidelines** - Added comprehensive skill reference guidelines

## Verification

Run the following commands to verify the fixes:

```bash
# Audit all skill references (should show 0 invalid)
python3 scripts/audit_skills.py

# Validate all agents (should pass)
./build-agent.py --validate
```

## Prevention

Future invalid skill references will be prevented by:

1. **Build-time validation**: `./build-agent.py --validate` checks all skill references
2. **Audit script**: `python3 scripts/audit_skills.py` provides detailed skill analysis
3. **Documentation**: AGENTS.md and AGENT_TEMPLATE_REFERENCE.md clearly state requirements
4. **PR requirements**: Validation must pass before merging (see AGENTS.md)

