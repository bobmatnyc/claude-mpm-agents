#!/usr/bin/env python3
"""
Agent Builder - Flatten agent definitions with BASE-AGENT.md inheritance

This script builds complete agent definitions by combining:
1. Agent-specific content ({agent-name}.md)
2. Directory BASE-AGENT.md (if exists)
3. Parent directory BASE-AGENT.md files (recursive)
4. Root BASE-AGENT.md (always appended)

Usage:
    ./build-agent.py <agent-path>              # Build single agent
    ./build-agent.py --all                     # Build all agents
    ./build-agent.py --output-dir <path>       # Specify output directory
    ./build-agent.py --validate                # Validate all agents

Examples:
    ./build-agent.py agents/engineer/frontend/react-engineer.md
    ./build-agent.py --all --output-dir dist/agents
    ./build-agent.py --validate
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Set
import re
import json


class AgentBuilder:
    """Builds flattened agent definitions from modular sources with BASE-AGENT.md inheritance."""

    def __init__(self, root_dir: Path, output_dir: Optional[Path] = None):
        self.root_dir = root_dir
        self.output_dir = output_dir or root_dir / "dist" / "agents"
        self._valid_skills: Optional[Set[str]] = None
        self.agents_dir = root_dir / "agents"

    def find_base_agents(self, agent_path: Path) -> List[Path]:
        """
        Find all BASE-AGENT.md files from agent's directory up to root.

        Returns list ordered from root to agent directory (append order).
        """
        base_files = []
        current = agent_path.parent

        # Walk up from agent directory to root
        while current >= self.agents_dir:
            base_file = current / "BASE-AGENT.md"
            if base_file.exists():
                base_files.insert(0, base_file)  # Insert at beginning for correct order
            current = current.parent

        return base_files

    def extract_frontmatter(self, content: str) -> tuple[str, str]:
        """
        Extract YAML frontmatter from content.

        Returns: (frontmatter, body)
        """
        pattern = r'^---\n(.*?)\n---\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)

        if match:
            return match.group(1), match.group(2)
        return "", content

    def build_agent(self, agent_path: Path) -> str:
        """
        Build complete agent definition by combining:
        1. Agent-specific content (with frontmatter)
        2. BASE-AGENT.md from same directory
        3. Parent BASE-AGENT.md files (bottom-up)
        4. Root BASE-AGENT.md

        Returns: Complete agent content
        """
        if not agent_path.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Read agent-specific content
        agent_content = agent_path.read_text(encoding='utf-8')
        frontmatter, body = self.extract_frontmatter(agent_content)

        # Find all BASE-AGENT.md files in hierarchy
        base_files = self.find_base_agents(agent_path)

        # Build combined content
        parts = []

        # 1. Agent frontmatter (if exists)
        if frontmatter:
            parts.append(f"---\n{frontmatter}\n---")

        # 2. Agent-specific body
        parts.append(body.strip())

        # 3. Append BASE-AGENT.md files (root to local)
        for base_file in base_files:
            base_content = base_file.read_text(encoding='utf-8')
            # Remove frontmatter from base files
            _, base_body = self.extract_frontmatter(base_content)
            if base_body.strip():
                parts.append(f"\n<!-- Inherited from {base_file.relative_to(self.agents_dir)} -->\n")
                parts.append(base_body.strip())

        return "\n\n".join(parts)

    def build_all_agents(self) -> dict[Path, str]:
        """
        Build all agent definitions in the repository.

        Returns: Dict mapping agent paths to built content
        """
        results = {}

        # Find all .md files that are NOT BASE-AGENT.md
        for agent_file in self.agents_dir.rglob("*.md"):
            if agent_file.name == "BASE-AGENT.md":
                continue

            try:
                built_content = self.build_agent(agent_file)
                results[agent_file] = built_content
            except Exception as e:
                print(f"Error building {agent_file}: {e}", file=sys.stderr)

        return results

    def write_agent(self, agent_path: Path, content: str) -> Path:
        """
        Write built agent to output directory, preserving structure.

        Returns: Path to output file
        """
        # Preserve directory structure relative to agents/
        relative_path = agent_path.relative_to(self.agents_dir)
        output_path = self.output_dir / relative_path

        # Create output directory
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        output_path.write_text(content, encoding='utf-8')

        return output_path

    def load_valid_skills(self) -> Set[str]:
        """
        Load valid skill names from claude-mpm-skills manifest.

        Returns: Set of valid skill names, or empty set if manifest not found
        """
        if self._valid_skills is not None:
            return self._valid_skills

        manifest_path = self.root_dir.parent / "claude-mpm-skills" / "manifest.json"

        if not manifest_path.exists():
            # Manifest not found - return empty set (validation will be skipped)
            self._valid_skills = set()
            return self._valid_skills

        try:
            with open(manifest_path) as f:
                manifest = json.load(f)

            skills = set()

            # Handle universal skills (list of dicts)
            if 'universal' in manifest.get('skills', {}):
                for skill in manifest['skills']['universal']:
                    if isinstance(skill, dict) and 'name' in skill:
                        skills.add(skill['name'])

            # Handle toolchains (nested dict of lists of dicts)
            if 'toolchains' in manifest.get('skills', {}):
                for toolchain, toolchain_skills in manifest['skills']['toolchains'].items():
                    if isinstance(toolchain_skills, list):
                        for skill in toolchain_skills:
                            if isinstance(skill, dict) and 'name' in skill:
                                skills.add(skill['name'])

            # Handle examples (if present)
            if 'examples' in manifest.get('skills', {}):
                for skill in manifest['skills']['examples']:
                    if isinstance(skill, dict) and 'name' in skill:
                        skills.add(skill['name'])

            self._valid_skills = skills
            return skills

        except Exception:
            # Error loading manifest - return empty set
            self._valid_skills = set()
            return self._valid_skills

    def validate_agent(self, agent_path: Path) -> List[str]:
        """
        Validate agent definition.

        Returns: List of validation errors (empty if valid)
        """
        errors = []

        try:
            content = agent_path.read_text(encoding='utf-8')
            frontmatter, body = self.extract_frontmatter(content)

            # Check for required frontmatter fields
            if not frontmatter:
                errors.append("Missing YAML frontmatter")
            else:
                required_fields = ['name', 'description', 'agent_id', 'agent_type']
                for field in required_fields:
                    if f"{field}:" not in frontmatter:
                        errors.append(f"Missing required field: {field}")

                # Validate skill references
                valid_skills = self.load_valid_skills()
                if valid_skills:  # Only validate if manifest was loaded
                    # Extract skills from frontmatter
                    skills_match = re.search(r'skills:\s*\n((?:- .+\n)+)', content)
                    if skills_match:
                        skills_text = skills_match.group(1)
                        agent_skills = []
                        for line in skills_text.split('\n'):
                            line = line.strip()
                            if line.startswith('- '):
                                skill = line[2:].strip()
                                agent_skills.append(skill)

                        # Check for invalid skills
                        invalid_skills = [s for s in agent_skills if s not in valid_skills]
                        if invalid_skills:
                            errors.append(f"Invalid skill references (not in claude-mpm-skills): {', '.join(invalid_skills)}")

            # Check for content
            if not body.strip():
                errors.append("Missing agent body content")

        except Exception as e:
            errors.append(f"Error reading file: {e}")

        return errors

    def validate_all_agents(self) -> dict[Path, List[str]]:
        """
        Validate all agent definitions.

        Returns: Dict mapping agent paths to validation errors
        """
        results = {}

        for agent_file in self.agents_dir.rglob("*.md"):
            if agent_file.name == "BASE-AGENT.md":
                continue

            errors = self.validate_agent(agent_file)
            if errors:
                results[agent_file] = errors

        return results


def main():
    parser = argparse.ArgumentParser(
        description="Build flattened agent definitions with BASE-AGENT.md inheritance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'agent_path',
        nargs='?',
        type=Path,
        help='Path to agent file to build'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Build all agents in repository'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for built agents (default: dist/agents)'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate all agent definitions'
    )

    parser.add_argument(
        '--root',
        type=Path,
        default=Path.cwd(),
        help='Root directory of repository (default: current directory)'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Print built agent content to stdout after build'
    )

    args = parser.parse_args()

    # Initialize builder
    builder = AgentBuilder(args.root, args.output_dir)

    # Validate mode
    if args.validate:
        print("Validating all agents...")
        validation_results = builder.validate_all_agents()

        if not validation_results:
            print("✅ All agents valid!")
            return 0
        else:
            print(f"❌ Found errors in {len(validation_results)} agents:\n")
            for agent_path, errors in validation_results.items():
                rel_path = agent_path.relative_to(builder.agents_dir)
                print(f"{rel_path}:")
                for error in errors:
                    print(f"  - {error}")
                print()
            return 1

    # Build all mode
    if args.all:
        print("Building all agents...")
        results = builder.build_all_agents()

        for agent_path, content in results.items():
            output_path = builder.write_agent(agent_path, content)
            rel_input = agent_path.relative_to(builder.agents_dir)
            rel_output = output_path.relative_to(builder.root_dir)
            print(f"✅ {rel_input} -> {rel_output}")

        print(f"\n✅ Built {len(results)} agents to {builder.output_dir}")
        return 0

    # Single agent mode
    if args.agent_path:
        agent_path = args.agent_path
        if not agent_path.is_absolute():
            agent_path = builder.root_dir / agent_path

        print(f"Building {agent_path.name}...")

        try:
            content = builder.build_agent(agent_path)
            output_path = builder.write_agent(agent_path, content)

            print(f"✅ Built: {output_path}")
            print(f"\nContent length: {len(content)} characters")
            print(f"Base files inherited: {len(builder.find_base_agents(agent_path))}")

            if args.preview:
                print("\n--- Preview (built content) ---\n")
                print(content)

            return 0

        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            return 1

    # No mode specified
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
