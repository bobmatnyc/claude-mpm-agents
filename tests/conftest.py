"""Pytest fixtures for agent testing."""

from pathlib import Path
from typing import Callable

import pytest

from tests.fixtures.agent_loader import (
    AgentDefinition,
    AgentLoader,
    CompiledAgent,
    CompiledAgentLoader,
)
from tests.fixtures.instruction_extractor import InstructionExtractor, TestableRule
from tests.fixtures.mock_responses import MockResponseGenerator


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get project root directory.

    Returns:
        Path to project root
    """
    # Assumes tests/ is in project root
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def agents_dir(project_root: Path) -> Path:
    """Get agents directory.

    Args:
        project_root: Project root path

    Returns:
        Path to agents directory
    """
    return project_root / "agents"


@pytest.fixture(scope="session")
def agent_loader(agents_dir: Path) -> AgentLoader:
    """Create agent loader instance.

    Args:
        agents_dir: Path to agents directory

    Returns:
        AgentLoader instance
    """
    return AgentLoader(agents_dir)


@pytest.fixture(scope="session")
def all_agents(agent_loader: AgentLoader) -> list[AgentDefinition]:
    """Load all agent definitions.

    Args:
        agent_loader: AgentLoader instance

    Returns:
        List of all agent definitions
    """
    return agent_loader.load_all_agents()


@pytest.fixture(scope="session")
def instruction_extractor(project_root: Path) -> InstructionExtractor:
    """Create instruction extractor instance.

    Args:
        project_root: Project root path

    Returns:
        InstructionExtractor instance
    """
    return InstructionExtractor(project_root)


@pytest.fixture(scope="session")
def root_base_rules(instruction_extractor: InstructionExtractor) -> list[TestableRule]:
    """Extract rules from root BASE-AGENT.md.

    Args:
        instruction_extractor: InstructionExtractor instance

    Returns:
        List of rules from root BASE-AGENT.md
    """
    return instruction_extractor.extract_root_rules()


@pytest.fixture(scope="session")
def category_rules(
    instruction_extractor: InstructionExtractor,
) -> Callable[[str], list[TestableRule]]:
    """Factory fixture for category-specific rules.

    Args:
        instruction_extractor: InstructionExtractor instance

    Returns:
        Function that returns rules for a given category
    """

    def _get_rules(category: str) -> list[TestableRule]:
        return instruction_extractor.extract_category_rules(category)

    return _get_rules


@pytest.fixture(scope="session")
def mock_generator() -> MockResponseGenerator:
    """Create mock response generator.

    Returns:
        MockResponseGenerator instance
    """
    return MockResponseGenerator()


# Agent type filter fixtures


@pytest.fixture(scope="session")
def engineer_agents(all_agents: list[AgentDefinition]) -> list[AgentDefinition]:
    """Get all engineer agents.

    Args:
        all_agents: List of all agents

    Returns:
        List of engineer agents
    """
    return [agent for agent in all_agents if agent.agent_type == "engineer"]


@pytest.fixture(scope="session")
def qa_agents(all_agents: list[AgentDefinition]) -> list[AgentDefinition]:
    """Get all QA agents.

    Args:
        all_agents: List of all agents

    Returns:
        List of QA agents
    """
    return [agent for agent in all_agents if agent.agent_type == "qa"]


@pytest.fixture(scope="session")
def ops_agents(all_agents: list[AgentDefinition]) -> list[AgentDefinition]:
    """Get all ops agents.

    Args:
        all_agents: List of all agents

    Returns:
        List of ops agents
    """
    return [agent for agent in all_agents if agent.agent_type == "ops"]


@pytest.fixture(scope="session")
def security_agents(all_agents: list[AgentDefinition]) -> list[AgentDefinition]:
    """Get all security agents.

    Args:
        all_agents: List of all agents

    Returns:
        List of security agents
    """
    return [agent for agent in all_agents if agent.agent_type == "security"]


@pytest.fixture(scope="session")
def research_agents(all_agents: list[AgentDefinition]) -> list[AgentDefinition]:
    """Get all research agents.

    Args:
        all_agents: List of all agents

    Returns:
        List of research agents
    """
    return [agent for agent in all_agents if agent.agent_type == "research"]


# Compiled agent fixtures


@pytest.fixture(scope="session")
def compiled_loader(agents_dir: Path) -> CompiledAgentLoader:
    """Create a CompiledAgentLoader instance.

    Args:
        agents_dir: Path to agents directory

    Returns:
        CompiledAgentLoader instance
    """
    return CompiledAgentLoader(agents_dir)


@pytest.fixture(scope="session")
def compiled_agents(compiled_loader: CompiledAgentLoader) -> dict[str, CompiledAgent]:
    """Load all compiled agents with BASE-AGENT.md inheritance.

    Args:
        compiled_loader: CompiledAgentLoader instance

    Returns:
        Dict mapping agent_id to CompiledAgent objects
    """
    return compiled_loader.compile_all_agents()


@pytest.fixture(scope="session")
def base_agent_files(agents_dir: Path) -> list[Path]:
    """Find all BASE-AGENT.md files.

    Args:
        agents_dir: Path to agents directory

    Returns:
        List of paths to BASE-AGENT.md files
    """
    return list(agents_dir.rglob("BASE-AGENT.md"))
