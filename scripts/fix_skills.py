#!/usr/bin/env python3
"""
Fix invalid skill references in agents by removing them.
"""
import re
from pathlib import Path
from audit_skills import extract_skills_from_manifest, extract_skills_from_agent


def fix_agent_skills(agent_path, valid_skills):
    """Remove invalid skills from an agent file."""
    content = agent_path.read_text()
    
    # Extract current skills
    current_skills = extract_skills_from_agent(agent_path)
    if not current_skills:
        return False, "No skills found"
    
    # Filter to only valid skills
    valid_agent_skills = [s for s in current_skills if s in valid_skills]
    invalid_skills = [s for s in current_skills if s not in valid_skills]
    
    if not invalid_skills:
        return False, "No invalid skills"
    
    # Find and replace the skills section
    pattern = r'(skills:\s*\n)((?:- .+\n)+)'
    match = re.search(pattern, content)
    
    if not match:
        return False, "Could not find skills section"
    
    # Build new skills section
    if valid_agent_skills:
        new_skills_section = match.group(1)  # Keep "skills:\n"
        for skill in valid_agent_skills:
            new_skills_section += f"- {skill}\n"
    else:
        # If no valid skills remain, remove the entire skills section
        new_skills_section = ""
    
    # Replace in content
    new_content = content[:match.start()] + new_skills_section + content[match.end():]
    
    # Write back
    agent_path.write_text(new_content)
    
    return True, f"Removed {len(invalid_skills)} invalid skills: {', '.join(invalid_skills)}"


def main():
    # Change to repo root if we're in scripts/
    if Path.cwd().name == "scripts":
        import os
        os.chdir("..")

    # Load valid skills
    manifest_path = Path("../claude-mpm-skills/manifest.json")
    if not manifest_path.exists():
        print(f"❌ Manifest not found at {manifest_path}")
        return

    valid_skills = extract_skills_from_manifest(manifest_path)
    print(f"✅ Found {len(valid_skills)} valid skills in manifest\n")

    # Scan and fix all agents
    agents_dir = Path("agents").resolve()
    fixed_count = 0
    error_count = 0
    
    for agent_file in sorted(agents_dir.rglob("*.md")):
        if agent_file.name == "BASE-AGENT.md":
            continue
        
        agent_skills = extract_skills_from_agent(agent_file)
        if not agent_skills:
            continue
        
        invalid = [s for s in agent_skills if s not in valid_skills]
        if not invalid:
            continue
        
        # Fix the agent
        try:
            rel_path = str(agent_file.relative_to(Path.cwd().resolve()))
        except ValueError:
            rel_path = str(agent_file)
        
        success, message = fix_agent_skills(agent_file, valid_skills)
        
        if success:
            print(f"✅ {rel_path}")
            print(f"   {message}")
            fixed_count += 1
        else:
            print(f"❌ {rel_path}")
            print(f"   Error: {message}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Fixed: {fixed_count} agents")
    print(f"  Errors: {error_count} agents")


if __name__ == "__main__":
    import sys
    
    if "--dry-run" in sys.argv:
        print("DRY RUN MODE - No changes will be made\n")
        from audit_skills import main as audit_main
        audit_main()
    else:
        main()

