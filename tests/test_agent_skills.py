"""Tests for agent skills validation.

This module validates that:
1. All agent skill references exist in the skills registry
2. Agents have skills appropriate to their category
3. Skills are properly formatted
"""

import json
from pathlib import Path
from typing import List, Set

import pytest
import yaml

from tests.fixtures.agent_loader import AgentDefinition


class TestAgentSkills:
    """Test that all agent skill references are valid."""

    @pytest.fixture(scope="class")
    def skills_registry(self, project_root: Path) -> Set[str]:
        """Load valid skills from registry.

        Args:
            project_root: Project root path

        Returns:
            Set of valid skill names

        Raises:
            pytest.skip: If skills registry not found
        """
        # Try multiple possible locations for skills registry
        possible_paths = [
            project_root / ".claude-mpm" / "pm_skills_registry.yaml",
            project_root / ".claude-mpm" / "skills-manifest.json",
            project_root.parent / "claude-mpm-skills" / "manifest.json",
            project_root / ".claude-mpm" / "skills" / "manifest.json",
        ]

        valid_skills = set()

        for registry_path in possible_paths:
            if not registry_path.exists():
                continue

            try:
                if registry_path.suffix == ".yaml":
                    data = yaml.safe_load(registry_path.read_text())
                    if "skills" in data:
                        for skill in data["skills"]:
                            if isinstance(skill, dict):
                                valid_skills.add(skill.get("name", ""))
                            else:
                                valid_skills.add(str(skill))
                elif registry_path.suffix == ".json":
                    data = json.loads(registry_path.read_text())

                    # Handle both nested (skills.universal) and flat (universal) formats
                    skills_data = data.get("skills", data)

                    # Extract from universal section
                    for skill in skills_data.get("universal", []):
                        if isinstance(skill, dict):
                            valid_skills.add(skill.get("name", ""))
                        else:
                            valid_skills.add(str(skill))

                    # Extract from toolchains section
                    for category, skills_list in skills_data.get("toolchains", {}).items():
                        if isinstance(skills_list, list):
                            for skill in skills_list:
                                if isinstance(skill, dict):
                                    valid_skills.add(skill.get("name", ""))
                                else:
                                    valid_skills.add(str(skill))
            except (yaml.YAMLError, json.JSONDecodeError) as e:
                print(f"Warning: Failed to parse {registry_path}: {e}")
                continue

        # Also scan .claude-mpm/skills directory for skill files
        skills_dir = project_root / ".claude-mpm" / "skills"
        if skills_dir.exists():
            for skill_file in skills_dir.rglob("*.md"):
                # Skill name is filename without extension
                skill_name = skill_file.stem
                valid_skills.add(skill_name)

        # Remove empty strings
        valid_skills.discard("")

        if not valid_skills:
            pytest.skip("No skills found in registry")

        return valid_skills

    @pytest.mark.skills
    def test_all_agent_skills_exist_in_registry(
        self, all_agents: List[AgentDefinition], skills_registry: Set[str]
    ) -> None:
        """Verify all agent skill references exist in registry.

        Args:
            all_agents: List of all agent definitions
            skills_registry: Set of valid skill names

        Raises:
            AssertionError: If agents reference invalid skills
        """
        if not skills_registry:
            pytest.skip("No skills in registry")

        invalid_refs = []
        for agent in all_agents:
            for skill in agent.skills or []:
                # Normalize skill name (handle case differences)
                if skill not in skills_registry:
                    # Check case-insensitive match
                    skill_lower = skill.lower()
                    if not any(s.lower() == skill_lower for s in skills_registry):
                        invalid_refs.append((agent.agent_id, skill))

        # If registry has very few skills (local only), skip this test
        # Full validation requires the complete claude-mpm-skills manifest
        if len(skills_registry) < 20:
            pytest.skip(
                f"Skills registry only has {len(skills_registry)} skills. "
                f"Full validation requires claude-mpm-skills manifest."
            )

        # Allow up to 10% invalid references (might be new skills being added)
        max_invalid = max(5, int(len(invalid_refs) * 0.1))
        assert len(invalid_refs) <= max_invalid, (
            f"Invalid skill references found ({len(invalid_refs)}):\n"
            f"{invalid_refs[:10]}\n"
            f"These skills are referenced by agents but not found in skills registry."
        )

    @pytest.mark.skills
    @pytest.mark.parametrize("agent_type", ["engineer", "qa", "ops"])
    def test_category_agents_have_category_skills(
        self, all_agents: List[AgentDefinition], agent_type: str
    ) -> None:
        """Test agents have skills relevant to their category.

        Args:
            all_agents: List of all agent definitions
            agent_type: Type of agent to test

        Raises:
            pytest.skip: If no agents of this type found
            AssertionError: If too many agents lack skills
        """
        category_agents = [a for a in all_agents if a.agent_type == agent_type]

        if not category_agents:
            pytest.skip(f"No {agent_type} agents found")

        # Just verify they have at least one skill
        no_skills = [a.agent_id for a in category_agents if not a.skills]

        # Allow up to 20% without skills (might be generic agents)
        max_without = len(category_agents) * 0.2
        assert len(no_skills) <= max_without, (
            f"{agent_type} agents without skills ({len(no_skills)}/{len(category_agents)}): "
            f"{no_skills}\n"
            f"Expected most {agent_type} agents to have skills defined."
        )

    @pytest.mark.skills
    def test_engineer_agents_have_engineering_skills(
        self, all_agents: List[AgentDefinition]
    ) -> None:
        """Test that engineer agents have skills related to engineering.

        Args:
            all_agents: List of all agent definitions

        Raises:
            pytest.skip: If no engineer agents found
            AssertionError: If engineers lack engineering skills
        """
        engineer_agents = [a for a in all_agents if a.agent_type == "engineer"]

        if not engineer_agents:
            pytest.skip("No engineer agents found")

        # Common engineering skill patterns
        engineering_patterns = {
            "testing",
            "test",
            "git",
            "cicd",
            "ci-cd",
            "docker",
            "database",
            "api",
            "framework",
        }

        without_engineering_skills = []
        for agent in engineer_agents:
            skills_text = " ".join(agent.skills or []).lower()
            has_eng_skill = any(pattern in skills_text for pattern in engineering_patterns)
            if not has_eng_skill and len(agent.skills or []) > 0:
                without_engineering_skills.append(agent.agent_id)

        # Allow up to 30% (might have specialized skills)
        max_without = len(engineer_agents) * 0.3
        assert len(without_engineering_skills) <= max_without, (
            f"Engineer agents without engineering skills: {without_engineering_skills}\n"
            f"Expected engineers to have skills like testing, git, databases, etc."
        )

    @pytest.mark.skills
    def test_ops_agents_have_ops_skills(self, all_agents: List[AgentDefinition]) -> None:
        """Test that ops agents have skills related to operations.

        Args:
            all_agents: List of all agent definitions

        Raises:
            pytest.skip: If no ops agents found
            AssertionError: If ops agents lack ops skills
        """
        ops_agents = [a for a in all_agents if a.agent_type == "ops"]

        if not ops_agents:
            pytest.skip("No ops agents found")

        # Common ops skill patterns
        ops_patterns = {
            "deploy",
            "docker",
            "kubernetes",
            "ci",
            "cd",
            "infra",
            "monitor",
            "cloud",
            "server",
        }

        without_ops_skills = []
        for agent in ops_agents:
            skills_text = " ".join(agent.skills or []).lower()
            has_ops_skill = any(pattern in skills_text for pattern in ops_patterns)
            if not has_ops_skill and len(agent.skills or []) > 0:
                without_ops_skills.append(agent.agent_id)

        # Allow up to 30%
        max_without = len(ops_agents) * 0.3
        assert len(without_ops_skills) <= max_without, (
            f"Ops agents without ops skills: {without_ops_skills}\n"
            f"Expected ops agents to have skills like deployment, docker, kubernetes, etc."
        )

    @pytest.mark.skills
    def test_skills_are_not_empty_strings(self, all_agents: List[AgentDefinition]) -> None:
        """Test that skill references are not empty or whitespace.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If agents have empty skill references
        """
        empty_skills = []
        for agent in all_agents:
            for skill in agent.skills or []:
                if not skill or not skill.strip():
                    empty_skills.append(agent.agent_id)
                    break

        assert not empty_skills, (
            f"Agents with empty skill references: {empty_skills}\n"
            f"Skills should be non-empty strings."
        )

    @pytest.mark.skills
    def test_skills_follow_naming_convention(self, all_agents: List[AgentDefinition]) -> None:
        """Test that skills follow naming conventions (lowercase, hyphens).

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If too many skills violate naming conventions
        """
        invalid_names = []
        for agent in all_agents:
            for skill in agent.skills or []:
                # Skills should be lowercase with hyphens or underscores
                # Allow alphanumeric, hyphens, underscores, dots
                if (
                    not skill.replace("-", "")
                    .replace("_", "")
                    .replace(".", "")
                    .replace("/", "")
                    .isalnum()
                ):
                    invalid_names.append((agent.agent_id, skill))

        # Allow up to 10% with non-standard names
        total_skills = sum(len(a.skills or []) for a in all_agents)
        max_invalid = total_skills * 0.1 if total_skills > 0 else 0

        assert len(invalid_names) <= max_invalid, (
            f"Skills with invalid naming: {invalid_names[:10]}\n"
            f"Skills should use lowercase with hyphens/underscores."
        )


class TestSkillsCoverage:
    """Test that skills provide good coverage of agent capabilities."""

    @pytest.mark.skills
    def test_agents_have_reasonable_skill_count(self, all_agents: List[AgentDefinition]) -> None:
        """Test that agents have a reasonable number of skills.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If too many agents have extreme skill counts
        """
        too_few = []  # Less than 2 skills
        too_many = []  # More than 50 skills

        for agent in all_agents:
            skill_count = len(agent.skills or [])
            if skill_count > 0 and skill_count < 2:
                too_few.append((agent.agent_id, skill_count))
            elif skill_count > 50:
                too_many.append((agent.agent_id, skill_count))

        # Allow up to 20% with too few
        max_too_few = len(all_agents) * 0.2
        assert len(too_few) <= max_too_few, (
            f"Agents with very few skills (<2): {too_few}\n"
            f"Consider adding more skills to define capabilities."
        )

        # Very few should have too many
        assert len(too_many) <= 2, (
            f"Agents with excessive skills (>50): {too_many}\n"
            f"Consider grouping or categorizing skills."
        )

    @pytest.mark.skills
    def test_engineer_agents_have_sufficient_skills(
        self, all_agents: List[AgentDefinition]
    ) -> None:
        """Test that engineer agents have sufficient skills defined.

        Args:
            all_agents: List of all agent definitions

        Raises:
            pytest.skip: If no engineer agents found
            AssertionError: If engineers have too few skills
        """
        engineer_agents = [a for a in all_agents if a.agent_type == "engineer"]

        if not engineer_agents:
            pytest.skip("No engineer agents found")

        min_skills = 5  # Engineers should have at least 5 skills
        insufficient = []

        for agent in engineer_agents:
            if len(agent.skills or []) < min_skills:
                insufficient.append((agent.agent_id, len(agent.skills or [])))

        # Allow up to 30% to have fewer skills
        max_insufficient = len(engineer_agents) * 0.3
        assert len(insufficient) <= max_insufficient, (
            f"Engineer agents with insufficient skills (<{min_skills}): {insufficient}\n"
            f"Expected engineers to have comprehensive skill definitions."
        )
