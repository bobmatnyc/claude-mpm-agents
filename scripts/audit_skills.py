#!/usr/bin/env python3
"""
Audit skill references in agents against claude-mpm-skills manifest.
"""
import json
import re
from pathlib import Path
from collections import defaultdict


def extract_skills_from_manifest(manifest_path):
    """Extract all skill names from the manifest."""
    with open(manifest_path) as f:
        manifest = json.load(f)

    skills = set()

    # Handle universal skills (list of dicts)
    if 'universal' in manifest['skills']:
        for skill in manifest['skills']['universal']:
            if isinstance(skill, dict) and 'name' in skill:
                skills.add(skill['name'])

    # Handle toolchains (nested dict of lists of dicts)
    if 'toolchains' in manifest['skills']:
        for toolchain, toolchain_skills in manifest['skills']['toolchains'].items():
            if isinstance(toolchain_skills, list):
                for skill in toolchain_skills:
                    if isinstance(skill, dict) and 'name' in skill:
                        skills.add(skill['name'])

    # Handle examples (if present)
    if 'examples' in manifest['skills']:
        for skill in manifest['skills']['examples']:
            if isinstance(skill, dict) and 'name' in skill:
                skills.add(skill['name'])

    return skills


def extract_skills_from_agent(agent_path):
    """Extract skills from agent frontmatter using regex."""
    content = agent_path.read_text()

    # Find the skills section in YAML frontmatter
    # Match from "skills:" to the next top-level key (no indentation) or end of frontmatter
    pattern = r'skills:\s*\n((?:- .+\n)+)'
    match = re.search(pattern, content)

    if not match:
        return []

    skills_text = match.group(1)
    skills = []
    for line in skills_text.split('\n'):
        line = line.strip()
        if line.startswith('- '):
            skill = line[2:].strip()
            skills.append(skill)

    return skills


def main():
    # Load valid skills from manifest
    manifest_path = Path("../claude-mpm-skills/manifest.json")
    if not manifest_path.exists():
        print(f"❌ Manifest not found at {manifest_path}")
        return
    
    valid_skills = extract_skills_from_manifest(manifest_path)
    print(f"✅ Found {len(valid_skills)} valid skills in manifest\n")
    
    # Scan all agents
    agents_dir = Path("agents").resolve()
    agents_with_invalid = []

    for agent_file in agents_dir.rglob("*.md"):
        if agent_file.name == "BASE-AGENT.md":
            continue

        agent_skills = extract_skills_from_agent(agent_file)
        if not agent_skills:
            continue

        valid = [s for s in agent_skills if s in valid_skills]
        invalid = [s for s in agent_skills if s not in valid_skills]

        if invalid:
            # Get relative path from current directory
            try:
                rel_path = str(agent_file.relative_to(Path.cwd().resolve()))
            except ValueError:
                rel_path = str(agent_file)

            agents_with_invalid.append({
                'path': rel_path,
                'valid': valid,
                'invalid': invalid,
                'all_skills': agent_skills
            })
    
    # Print results
    print("=== AGENTS WITH INVALID SKILL REFERENCES ===\n")
    for agent in sorted(agents_with_invalid, key=lambda x: x['path']):
        print(f"📄 {agent['path']}")
        if agent['valid']:
            print(f"   ✅ Keep: {', '.join(agent['valid'])}")
        print(f"   ❌ Remove: {', '.join(agent['invalid'])}")
        print()
    
    print(f"Summary:")
    print(f"  Agents affected: {len(agents_with_invalid)}")
    print(f"  Invalid references: {sum(len(a['invalid']) for a in agents_with_invalid)}")
    
    # Return data for programmatic use
    return agents_with_invalid, valid_skills


if __name__ == "__main__":
    main()

