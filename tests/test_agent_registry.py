"""Tests for agent registry validation."""

import pytest

from tests.fixtures.agent_loader import AgentDefinition


@pytest.mark.registry
class TestAgentFrontmatter:
    """Test agent frontmatter validation."""

    @pytest.mark.parametrize(
        "field_name",
        ["name", "description", "agent_id", "agent_type"],
    )
    def test_required_fields_present(self, all_agents: list[AgentDefinition], field_name: str):
        """Test that all agents have required frontmatter fields.

        Args:
            all_agents: List of all agent definitions
            field_name: Name of required field to check
        """
        if not all_agents:
            pytest.skip("No agents found in repository")

        missing = []
        for agent in all_agents:
            value = getattr(agent, field_name, None)
            if not value or (isinstance(value, str) and not value.strip()):
                missing.append(agent.path)

        assert not missing, (
            f"Agents missing required field '{field_name}': {[str(p) for p in missing]}"
        )

    def test_agent_ids_unique(self, all_agents: list[AgentDefinition]):
        """Test that all agent IDs are unique."""
        if not all_agents:
            pytest.skip("No agents found in repository")

        agent_ids = [agent.agent_id for agent in all_agents if agent.agent_id]
        duplicates = [aid for aid in agent_ids if agent_ids.count(aid) > 1]

        assert not duplicates, f"Duplicate agent IDs found: {set(duplicates)}"

    def test_agent_types_valid(self, all_agents: list[AgentDefinition]):
        """Test that all agent types are from valid set."""
        if not all_agents:
            pytest.skip("No agents found in repository")

        valid_types = {
            "engineer",
            "qa",
            "ops",
            "security",
            "research",
            "documentation",
            "devops",
            "data",
            "frontend",
            "backend",
            "mobile",
            "infra",
            "platform",
            "sre",
            "pm",
            "universal",
            "agent_manager",
            "skills_manager",
            "memory_manager",
            "content",
            "imagemagick",
            "product",
            "system",
            "claude-mpm",
            "analysis",
            "refactoring",
            "specialized",
        }

        invalid = [
            (agent.path, agent.agent_type)
            for agent in all_agents
            if agent.agent_type and agent.agent_type not in valid_types
        ]

        assert not invalid, f"Agents with invalid types: {[(str(p), t) for p, t in invalid]}"

    def test_handoff_agents_exist(self, all_agents: list[AgentDefinition]):
        """Test that handoff references point to existing agents."""
        if not all_agents:
            pytest.skip("No agents found in repository")

        agent_ids = {agent.agent_id for agent in all_agents if agent.agent_id}

        missing_refs = []
        for agent in all_agents:
            interactions = agent.interactions
            if not isinstance(interactions, dict):
                continue

            handoff_to = interactions.get("handoff_to", [])
            if isinstance(handoff_to, str):
                handoff_to = [handoff_to]

            for target_id in handoff_to:
                if target_id and target_id not in agent_ids:
                    missing_refs.append((agent.path, target_id))

        assert not missing_refs, (
            f"Agents reference non-existent handoff targets: "
            f"{[(str(p), t) for p, t in missing_refs]}"
        )


@pytest.mark.registry
class TestAgentCategories:
    """Test agent category consistency."""

    def test_engineer_agents_have_engineer_type(self, engineer_agents: list[AgentDefinition]):
        """Test that engineer agents have agent_type='engineer'."""
        if not engineer_agents:
            pytest.skip("No engineer agents found")

        wrong_type = [agent for agent in engineer_agents if agent.agent_type != "engineer"]

        assert not wrong_type, (
            f"Engineer agents with wrong type: {[(a.path, a.agent_type) for a in wrong_type]}"
        )

    def test_qa_agents_have_qa_type(self, qa_agents: list[AgentDefinition]):
        """Test that QA agents have agent_type='qa'."""
        if not qa_agents:
            pytest.skip("No QA agents found")

        wrong_type = [agent for agent in qa_agents if agent.agent_type != "qa"]

        assert not wrong_type, (
            f"QA agents with wrong type: {[(a.path, a.agent_type) for a in wrong_type]}"
        )

    def test_all_agents_have_skills(self, all_agents: list[AgentDefinition]):
        """Test that all agents define skills."""
        if not all_agents:
            pytest.skip("No agents found")

        # Allow some agents to have no skills (they may be generic)
        without_skills = [
            agent for agent in all_agents if not agent.skills or len(agent.skills) == 0
        ]

        # Just warn if more than 20% have no skills
        if len(without_skills) > len(all_agents) * 0.2:
            pytest.fail(
                f"Too many agents ({len(without_skills)}/{len(all_agents)}) "
                f"without skills: {[str(a.path) for a in without_skills[:5]]}"
            )

    def test_ops_agents_in_ops_directory(self, all_agents: list[AgentDefinition]):
        """Test that agents with type 'ops' are in the ops/ directory.

        This ensures proper BASE-AGENT.md inheritance for ops-specific instructions.
        """
        if not all_agents:
            pytest.skip("No agents found")

        misplaced = []
        for agent in all_agents:
            if agent.agent_type == "ops":
                # Check if agent is in ops directory
                parts = agent.path.parts
                if "ops" not in parts:
                    misplaced.append((agent.path, agent.agent_type))

        assert not misplaced, (
            f"Ops agents not in ops/ directory (missing ops/BASE-AGENT.md inheritance): "
            f"{[(str(p), t) for p, t in misplaced]}"
        )

    def test_engineer_agents_in_engineer_directory(self, all_agents: list[AgentDefinition]):
        """Test that agents with type 'engineer' are in the engineer/ directory.

        This ensures proper BASE-AGENT.md inheritance for engineer-specific instructions.
        """
        if not all_agents:
            pytest.skip("No agents found")

        misplaced = []
        for agent in all_agents:
            if agent.agent_type == "engineer":
                parts = agent.path.parts
                if "engineer" not in parts:
                    misplaced.append((agent.path, agent.agent_type))

        assert not misplaced, (
            f"Engineer agents not in engineer/ directory (missing engineer/BASE-AGENT.md inheritance): "
            f"{[(str(p), t) for p, t in misplaced]}"
        )

    def test_qa_agents_in_qa_directory(self, all_agents: list[AgentDefinition]):
        """Test that agents with type 'qa' are in the qa/ directory.

        This ensures proper BASE-AGENT.md inheritance for qa-specific instructions.
        """
        if not all_agents:
            pytest.skip("No agents found")

        misplaced = []
        for agent in all_agents:
            if agent.agent_type == "qa":
                parts = agent.path.parts
                if "qa" not in parts:
                    misplaced.append((agent.path, agent.agent_type))

        assert not misplaced, (
            f"QA agents not in qa/ directory (missing qa/BASE-AGENT.md inheritance): "
            f"{[(str(p), t) for p, t in misplaced]}"
        )


@pytest.mark.registry
class TestAgentContent:
    """Test agent content validation."""

    def test_agents_have_body_content(self, all_agents: list[AgentDefinition]):
        """Test that all agents have non-empty body content."""
        if not all_agents:
            pytest.skip("No agents found")

        empty_content = [
            agent
            for agent in all_agents
            if not agent.body_content or len(agent.body_content.strip()) < 50
        ]

        assert not empty_content, (
            f"Agents with insufficient content: {[str(a.path) for a in empty_content]}"
        )

    def test_agents_reference_base_agent(self, all_agents: list[AgentDefinition]):
        """Test that agents reference or inherit from BASE-AGENT concepts."""
        if not all_agents:
            pytest.skip("No agents found")

        # Check that most agents mention key BASE-AGENT concepts
        base_concepts = [
            "git",
            "commit",
            "test",
            "code",
            "quality",
            "markdown",
        ]

        no_references = []
        for agent in all_agents:
            content = agent.body_content.lower()
            has_concept = any(concept in content for concept in base_concepts)
            if not has_concept:
                no_references.append(agent.path)

        # Allow some agents to not reference (might be specialized)
        if len(no_references) > len(all_agents) * 0.3:
            pytest.fail(
                f"Too many agents ({len(no_references)}/{len(all_agents)}) "
                f"don't reference BASE-AGENT concepts: "
                f"{[str(p) for p in no_references[:5]]}"
            )
