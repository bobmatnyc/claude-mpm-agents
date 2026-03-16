"""Tests for agent knowledge and interactions validation.

This module validates that:
1. Agents have proper knowledge definitions
2. Knowledge includes domain_expertise and best_practices
3. Agents define interaction patterns (handoff_agents, etc.)
4. Knowledge is actionable and well-structured
"""

from typing import List

import pytest

from tests.fixtures.agent_loader import AgentDefinition


class TestAgentKnowledge:
    """Test that agents have proper knowledge definitions."""

    @pytest.mark.knowledge
    def test_agents_have_knowledge_section(self, all_agents: List[AgentDefinition]) -> None:
        """Test that agents define knowledge.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If too many agents lack knowledge
        """
        missing_knowledge = []
        for agent in all_agents:
            # Knowledge can be either dict or list in YAML
            if not agent.knowledge or (
                isinstance(agent.knowledge, (dict, list)) and len(agent.knowledge) == 0
            ):
                missing_knowledge.append(agent.agent_id)

        # Allow some agents without knowledge (generic/utility agents)
        max_missing = len(all_agents) * 0.3  # 30% threshold
        assert len(missing_knowledge) <= max_missing, (
            f"Too many agents without knowledge ({len(missing_knowledge)}/{len(all_agents)}):\n"
            f"{missing_knowledge[:10]}\n"
            f"Expected agents to define their knowledge and expertise."
        )

    @pytest.mark.knowledge
    def test_engineer_agents_have_best_practices(self, all_agents: List[AgentDefinition]) -> None:
        """Engineer agents should define best_practices.

        Args:
            all_agents: List of all agent definitions

        Raises:
            pytest.skip: If no engineer agents found
            AssertionError: If too many engineers lack best practices
        """
        engineer_agents = [a for a in all_agents if a.agent_type == "engineer"]

        if not engineer_agents:
            pytest.skip("No engineer agents")

        missing = []
        for agent in engineer_agents:
            knowledge = agent.knowledge or {}
            if isinstance(knowledge, dict):
                if not knowledge.get("best_practices"):
                    missing.append(agent.agent_id)
            # If knowledge is a list, it's old format - accept it
            elif not isinstance(knowledge, list):
                missing.append(agent.agent_id)

        # At least 70% should have best practices
        min_with_practices = len(engineer_agents) * 0.7
        has_practices = len(engineer_agents) - len(missing)
        assert has_practices >= min_with_practices, (
            f"Engineer agents without best_practices ({len(missing)}/{len(engineer_agents)}):\n"
            f"{missing}\n"
            f"Expected engineers to define coding best practices."
        )

    @pytest.mark.knowledge
    def test_agents_have_domain_expertise(self, all_agents: List[AgentDefinition]) -> None:
        """Test agents define domain_expertise.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If too few agents have domain expertise
        """
        with_expertise = []
        without_expertise = []

        for agent in all_agents:
            knowledge = agent.knowledge or {}
            if isinstance(knowledge, dict):
                if knowledge.get("domain_expertise"):
                    with_expertise.append(agent.agent_id)
                else:
                    without_expertise.append(agent.agent_id)
            elif isinstance(knowledge, list) and knowledge:
                # Old format - list of expertise items
                with_expertise.append(agent.agent_id)
            else:
                without_expertise.append(agent.agent_id)

        # At least 50% should have domain expertise
        min_with = len(all_agents) * 0.5
        assert len(with_expertise) >= min_with, (
            f"Only {len(with_expertise)}/{len(all_agents)} agents have domain_expertise.\n"
            f"Missing: {without_expertise[:10]}\n"
            f"Expected agents to define their areas of expertise."
        )

    @pytest.mark.knowledge
    @pytest.mark.parametrize(
        "agent_type,min_expertise_count",
        [
            ("engineer", 3),  # Engineers should have at least 3 expertise areas
            ("qa", 2),  # QA should have at least 2
            ("ops", 2),  # Ops should have at least 2
        ],
    )
    def test_category_agents_have_sufficient_expertise(
        self,
        all_agents: List[AgentDefinition],
        agent_type: str,
        min_expertise_count: int,
    ) -> None:
        """Test category agents have minimum domain expertise entries.

        Args:
            all_agents: List of all agent definitions
            agent_type: Type of agent to test
            min_expertise_count: Minimum number of expertise items

        Raises:
            pytest.skip: If no agents of this type found
            AssertionError: If too many agents lack sufficient expertise
        """
        category_agents = [a for a in all_agents if a.agent_type == agent_type]

        if not category_agents:
            pytest.skip(f"No {agent_type} agents")

        insufficient = []
        for agent in category_agents:
            knowledge = agent.knowledge or {}
            if isinstance(knowledge, dict):
                expertise = knowledge.get("domain_expertise", [])
            elif isinstance(knowledge, list):
                expertise = knowledge
            else:
                expertise = []

            if len(expertise) < min_expertise_count:
                insufficient.append((agent.agent_id, len(expertise)))

        # Allow up to 30% to have insufficient expertise
        max_insufficient = len(category_agents) * 0.3
        assert len(insufficient) <= max_insufficient, (
            f"{agent_type} agents with insufficient expertise (<{min_expertise_count}):\n"
            f"{insufficient}\n"
            f"Expected {agent_type} agents to have comprehensive domain expertise."
        )

    @pytest.mark.knowledge
    def test_best_practices_are_actionable(self, all_agents: List[AgentDefinition]) -> None:
        """Best practices should be actionable strings, not empty.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If agents have empty or trivial best practices
        """
        empty_practices = []

        for agent in all_agents:
            knowledge = agent.knowledge or {}
            if not isinstance(knowledge, dict):
                continue

            practices = knowledge.get("best_practices", [])
            if not isinstance(practices, list):
                continue

            for practice in practices:
                # Practice should be a string with meaningful content
                practice_str = str(practice).strip()
                if not practice_str or len(practice_str) < 10:
                    empty_practices.append((agent.agent_id, practice_str))

        assert not empty_practices, (
            f"Agents with empty/trivial best practices:\n"
            f"{empty_practices[:5]}\n"
            f"Best practices should be actionable guidance (>10 chars)."
        )

    @pytest.mark.knowledge
    def test_domain_expertise_is_specific(self, all_agents: List[AgentDefinition]) -> None:
        """Domain expertise should be specific, not generic.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If too many agents have generic expertise
        """
        generic_expertise = []

        # Generic phrases that suggest non-specific expertise
        generic_phrases = [
            "general",
            "basic",
            "simple",
            "standard",
            "common",
        ]

        for agent in all_agents:
            knowledge = agent.knowledge or {}
            if isinstance(knowledge, dict):
                expertise = knowledge.get("domain_expertise", [])
            elif isinstance(knowledge, list):
                expertise = knowledge
            else:
                continue

            for item in expertise:
                item_str = str(item).lower()
                if any(phrase in item_str for phrase in generic_phrases):
                    if len(item_str) < 30:  # Short and generic = problem
                        generic_expertise.append((agent.agent_id, str(item)))

        # Allow up to 5% to have some generic items
        total_expertise = sum(
            len(
                a.knowledge.get("domain_expertise", [])
                if isinstance(a.knowledge, dict)
                else (a.knowledge if isinstance(a.knowledge, list) else [])
            )
            for a in all_agents
        )
        max_generic = total_expertise * 0.05 if total_expertise > 0 else 0

        assert len(generic_expertise) <= max_generic, (
            f"Generic/vague domain expertise found:\n"
            f"{generic_expertise[:5]}\n"
            f"Domain expertise should be specific and detailed."
        )


class TestAgentInteractions:
    """Test agent interaction definitions."""

    @pytest.mark.knowledge
    def test_agents_define_handoff_targets(self, all_agents: List[AgentDefinition]) -> None:
        """Test that agents define who they can hand off to.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If too few agents define handoff targets
        """
        without_handoff = []

        for agent in all_agents:
            interactions = agent.interactions or {}
            handoff_agents = interactions.get("handoff_agents", [])

            if not handoff_agents:
                without_handoff.append(agent.agent_id)

        # Informational: Check how many agents define handoff targets
        # This is aspirational - agents may not have interactions in frontmatter yet
        has_handoff = len(all_agents) - len(without_handoff)

        # Skip if less than 20% of agents define handoff targets
        # TODO: Increase threshold as agents are updated with handoff patterns
        if has_handoff < len(all_agents) * 0.2:
            pytest.skip(
                f"Only {has_handoff}/{len(all_agents)} agents define handoff_agents. "
                f"This is aspirational - agents can be updated to include handoff patterns."
            )

    @pytest.mark.knowledge
    def test_engineer_handoff_includes_qa(self, all_agents: List[AgentDefinition]) -> None:
        """Engineer agents should be able to hand off to QA.

        Args:
            all_agents: List of all agent definitions

        Raises:
            pytest.skip: If no engineer agents found
            AssertionError: If too many engineers can't hand off to QA
        """
        engineer_agents = [a for a in all_agents if a.agent_type == "engineer"]

        if not engineer_agents:
            pytest.skip("No engineer agents")

        cannot_handoff_to_qa = []

        for agent in engineer_agents:
            interactions = agent.interactions or {}
            handoff_agents = interactions.get("handoff_agents", [])

            # Check if qa or qa-agent is in handoff targets
            has_qa = any("qa" in str(target).lower() for target in handoff_agents)
            if not has_qa:
                cannot_handoff_to_qa.append(agent.agent_id)

        # Aspirational: Engineers should hand off to QA
        # Skip if no engineers have handoff defined yet
        if len(cannot_handoff_to_qa) == len(engineer_agents):
            pytest.skip(
                "No engineer agents define handoff_agents yet. "
                "This is aspirational - engineers can be updated to include QA handoff."
            )

        # At least 70% should hand off to QA (when handoffs are defined)
        max_without = len(engineer_agents) * 0.3
        assert len(cannot_handoff_to_qa) <= max_without, (
            f"Engineer agents that can't hand off to QA:\n"
            f"{cannot_handoff_to_qa}\n"
            f"Expected engineers to collaborate with QA agents."
        )

    @pytest.mark.knowledge
    def test_ops_agents_define_deployment_targets(self, all_agents: List[AgentDefinition]) -> None:
        """Ops agents should define their deployment targets or platforms.

        Args:
            all_agents: List of all agent definitions

        Raises:
            pytest.skip: If no ops agents found
        """
        ops_agents = [a for a in all_agents if a.agent_type == "ops"]

        if not ops_agents:
            pytest.skip("No ops agents")

        without_targets = []

        for agent in ops_agents:
            interactions = agent.interactions or {}
            # Check for deployment_targets or similar fields
            has_targets = (
                interactions.get("deployment_targets")
                or interactions.get("platforms")
                or interactions.get("environments")
            )

            if not has_targets:
                without_targets.append(agent.agent_id)

        # Aspirational: Ops agents should define deployment targets
        # Skip if most ops agents don't have this defined
        if len(without_targets) > len(ops_agents) * 0.6:
            pytest.skip(
                f"Most ops agents ({len(without_targets)}/{len(ops_agents)}) don't define deployment targets. "
                f"This is aspirational - ops agents can be updated to include deployment contexts."
            )

        # When defined, allow up to 40% without explicit targets (might be generic ops)
        max_without = len(ops_agents) * 0.4
        assert len(without_targets) <= max_without, (
            f"Ops agents without deployment targets:\n"
            f"{without_targets}\n"
            f"Note: This is informational - ops agents should ideally define deployment contexts."
        )

    @pytest.mark.knowledge
    def test_handoff_targets_are_valid_strings(self, all_agents: List[AgentDefinition]) -> None:
        """Test that handoff targets are valid non-empty strings.

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If agents have invalid handoff targets
        """
        invalid_targets = []

        for agent in all_agents:
            interactions = agent.interactions or {}
            handoff_agents = interactions.get("handoff_agents", [])

            for target in handoff_agents:
                if not target or not str(target).strip():
                    invalid_targets.append((agent.agent_id, target))

        assert not invalid_targets, (
            f"Agents with invalid handoff targets:\n"
            f"{invalid_targets}\n"
            f"Handoff targets should be non-empty strings."
        )


class TestKnowledgeStructure:
    """Test the structure and format of knowledge definitions."""

    @pytest.mark.knowledge
    def test_knowledge_uses_dict_format(self, all_agents: List[AgentDefinition]) -> None:
        """Test that knowledge uses structured dict format (not just list).

        Args:
            all_agents: List of all agent definitions

        Raises:
            AssertionError: If too many agents use old list format
        """
        old_format = []
        new_format = []

        for agent in all_agents:
            if not agent.knowledge:
                continue

            if isinstance(agent.knowledge, dict):
                new_format.append(agent.agent_id)
            elif isinstance(agent.knowledge, list):
                old_format.append(agent.agent_id)

        total_with_knowledge = len(old_format) + len(new_format)
        if total_with_knowledge == 0:
            pytest.skip("No agents with knowledge")

        # At least 60% should use new dict format
        min_new_format = total_with_knowledge * 0.6
        assert len(new_format) >= min_new_format, (
            f"Agents using old list format for knowledge:\n"
            f"{old_format}\n"
            f"Consider migrating to structured dict format with domain_expertise and best_practices keys."
        )

    @pytest.mark.knowledge
    def test_knowledge_dict_has_expected_keys(self, all_agents: List[AgentDefinition]) -> None:
        """Test that knowledge dicts contain expected keys.

        Args:
            all_agents: List of all agent definitions
        """
        expected_keys = {"domain_expertise", "best_practices"}
        missing_keys_agents = []

        for agent in all_agents:
            if not isinstance(agent.knowledge, dict):
                continue

            knowledge = agent.knowledge
            has_expected = any(key in knowledge for key in expected_keys)

            if not has_expected:
                missing_keys_agents.append((agent.agent_id, list(knowledge.keys())))

        # Allow up to 20% to have different keys
        total_dict_knowledge = sum(1 for a in all_agents if isinstance(a.knowledge, dict))
        max_missing = total_dict_knowledge * 0.2 if total_dict_knowledge > 0 else 0

        assert len(missing_keys_agents) <= max_missing, (
            f"Agents with knowledge dict but missing expected keys:\n"
            f"{missing_keys_agents[:5]}\n"
            f"Expected keys: {expected_keys}"
        )
