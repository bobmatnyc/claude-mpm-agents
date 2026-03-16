"""Tests for agent-specific domain patterns.

This module validates that each agent contains patterns specific to its domain.
For example, python-engineer should mention pytest, typing, pydantic, etc.
"""

import re
from typing import Dict, List

import pytest

from tests.fixtures.agent_loader import CompiledAgent

# Define expected patterns for each agent type
# Each pattern list should contain regex patterns that should appear in the agent
AGENT_PATTERNS: Dict[str, List[str]] = {
    # Backend Engineer agents
    "python-engineer": [
        r"pytest|python|pip|pyproject|typing|pydantic",
        r"def |class |import ",
        r"async|asyncio",
        r"mypy|type hint",
    ],
    "typescript-engineer": [
        r"TypeScript|interface|type |generic|tsconfig",
        r"npm|yarn|pnpm",
        r"Promise|async/await",
    ],
    "rust-engineer": [
        r"Rust|cargo|ownership|borrow|lifetime|Result<",
        r"trait|impl|struct",
    ],
    "golang-engineer": [
        r"Go|goroutine|channel|defer|interface\{\}",
        r"package|import",
    ],
    "java-engineer": [
        r"Java|Spring|Maven|Gradle|@Autowired|interface",
        r"class|public|private",
    ],
    "ruby-engineer": [
        r"Ruby|Rails|Gem|ActiveRecord|RSpec",
        r"def |class |module",
    ],
    "php-engineer": [
        r"PHP|Laravel|Composer|Eloquent|Blade",
        r"class|namespace",
    ],
    "phoenix-engineer": [
        r"Phoenix|Elixir|LiveView|Ecto|GenServer",
        r"defmodule|def ",
    ],
    # Frontend Engineer agents
    "react-engineer": [
        r"React|useState|useEffect|component|JSX|props",
        r"hook|render",
    ],
    "nextjs-engineer": [
        r"Next\.js|getServerSideProps|App Router|Server Component",
        r"router|route",
    ],
    "svelte-engineer": [
        r"Svelte|runes|\$state|\$effect|SvelteKit",
        r"component|store",
    ],
    "dart-engineer": [
        r"Dart|Flutter|Widget|StatefulWidget|Bloc",
        r"class|void",
    ],
    "tauri-engineer": [
        r"Tauri|Rust|WebView|IPC|invoke",
        r"command|event",
    ],
    # QA agents
    "qa": [
        r"test|coverage|assert|mock|fixture",
        r"quality|validation",
    ],
    "api-qa": [
        r"API|endpoint|HTTP|request|response|status",
        r"REST|GraphQL",
    ],
    "web-qa": [
        r"Playwright|browser|DOM|screenshot|accessibility",
        r"e2e|integration",
    ],
    # Ops agents
    "ops": [
        r"deploy|infrastructure|container|CI/CD|monitor",
        r"docker|kubernetes",
    ],
    "local-ops": [
        r"localhost|PM2|docker|port|process",
        r"dev|development",
    ],
    "vercel-ops": [
        r"Vercel|serverless|edge|deployment",
        r"preview|production",
    ],
    "gcp-ops": [
        r"GCP|Google Cloud|IAM|OAuth|Cloud Run",
        r"project|service",
    ],
    "clerk-ops": [
        r"Clerk|auth|OAuth|middleware|session",
        r"user|authentication",
    ],
    "digitalocean-ops": [
        r"DigitalOcean|Droplet|Spaces|App Platform",
        r"deploy|infrastructure",
    ],
    # Research/Analysis
    "research": [
        r"research|analysis|investigate|pattern|finding",
        r"explore|discover",
    ],
    "code-analyzer": [
        r"analyze|pattern|architecture|complexity",
        r"metric|quality",
    ],
    # Security
    "security": [
        r"security|vulnerability|OWASP|authentication|encryption",
        r"threat|risk",
    ],
    # Documentation
    "documentation": [
        r"document|README|API doc|guide|specification",
        r"markdown|write",
    ],
    "ticketing": [
        r"ticket|issue|epic|sprint|backlog",
        r"Linear|Jira",
    ],
}


@pytest.mark.patterns
def test_agent_patterns_keys_match_compiled_agents(
    compiled_agents: Dict[str, CompiledAgent],
) -> None:
    """Verify AGENT_PATTERNS keys all correspond to real compiled agents."""
    stale_keys = [key for key in AGENT_PATTERNS if key not in compiled_agents]
    assert not stale_keys, (
        f"AGENT_PATTERNS has keys for non-existent agents: {stale_keys}\n"
        f"Available agents: {sorted(compiled_agents.keys())}"
    )


@pytest.mark.patterns
@pytest.mark.parametrize("agent_id,patterns", AGENT_PATTERNS.items())
def test_agent_has_domain_patterns(
    compiled_agents: Dict[str, CompiledAgent], agent_id: str, patterns: List[str]
) -> None:
    """Test each agent contains its expected domain-specific patterns.

    Args:
        compiled_agents: Dict of compiled agents
        agent_id: Agent identifier to test
        patterns: List of regex patterns that should appear in agent content

    Raises:
        pytest.skip: If agent not found in compiled agents
        AssertionError: If agent is missing required patterns
    """
    if agent_id not in compiled_agents:
        pytest.skip(f"Agent {agent_id} not found in compiled agents")

    agent = compiled_agents[agent_id]
    content = agent.compiled_content

    missing = []
    for pattern in patterns:
        if not re.search(pattern, content, re.IGNORECASE):
            missing.append(pattern)

    assert not missing, (
        f"{agent_id} missing expected domain patterns:\n"
        f"Missing patterns: {missing}\n"
        f"Expected all patterns to match agent's domain expertise."
    )


@pytest.mark.patterns
def test_engineer_agents_mention_testing_tools(
    compiled_agents: Dict[str, CompiledAgent],
) -> None:
    """Test that engineer agents mention testing tools relevant to their stack.

    Args:
        compiled_agents: Dict of compiled agents

    Raises:
        AssertionError: If too many engineer agents lack testing tool mentions
    """
    engineer_patterns = {
        "python-engineer": r"pytest|unittest|hypothesis",
        "typescript-engineer": r"jest|vitest|testing-library",
        "react-engineer": r"jest|vitest|testing-library|cypress",
        "rust-engineer": r"#\[test\]|cargo test",
        "golang-engineer": r"testing\.T|go test",
        "java-engineer": r"JUnit|TestNG|Mockito",
    }

    missing_testing = []
    for agent_id, pattern in engineer_patterns.items():
        if agent_id not in compiled_agents:
            continue

        agent = compiled_agents[agent_id]
        if not re.search(pattern, agent.compiled_content, re.IGNORECASE):
            missing_testing.append(agent_id)

    # Allow up to 20% to not explicitly mention testing
    max_missing = len(engineer_patterns) * 0.2
    assert len(missing_testing) <= max_missing, (
        f"Engineer agents without testing tool mentions: {missing_testing}\n"
        f"Expected engineers to mention testing frameworks relevant to their stack."
    )


@pytest.mark.patterns
def test_ops_agents_mention_deployment_platforms(
    compiled_agents: Dict[str, CompiledAgent],
) -> None:
    """Test that ops agents mention deployment platforms or tools.

    Args:
        compiled_agents: Dict of compiled agents

    Raises:
        AssertionError: If ops agents don't mention deployment tools
    """
    ops_pattern = r"deploy|docker|kubernetes|CI/CD|GitHub Actions|container|serverless"

    ops_agents = [
        agent_id for agent_id, agent in compiled_agents.items() if agent.agent_type == "ops"
    ]

    if not ops_agents:
        pytest.skip("No ops agents found")

    without_deployment = []
    for agent_id in ops_agents:
        agent = compiled_agents[agent_id]
        if not re.search(ops_pattern, agent.compiled_content, re.IGNORECASE):
            without_deployment.append(agent_id)

    # At least 80% should mention deployment
    max_without = len(ops_agents) * 0.2
    assert len(without_deployment) <= max_without, (
        f"Ops agents without deployment tool mentions: {without_deployment}\n"
        f"Expected ops agents to mention deployment platforms or CI/CD tools."
    )


@pytest.mark.patterns
def test_qa_agents_mention_quality_metrics(
    compiled_agents: Dict[str, CompiledAgent],
) -> None:
    """Test that QA agents mention quality metrics or testing concepts.

    Args:
        compiled_agents: Dict of compiled agents

    Raises:
        AssertionError: If QA agents don't mention quality concepts
    """
    qa_pattern = r"test|coverage|quality|assert|validation|bug|defect|regression"

    qa_agents = [
        agent_id for agent_id, agent in compiled_agents.items() if agent.agent_type == "qa"
    ]

    if not qa_agents:
        pytest.skip("No QA agents found")

    without_quality = []
    for agent_id in qa_agents:
        agent = compiled_agents[agent_id]
        if not re.search(qa_pattern, agent.compiled_content, re.IGNORECASE):
            without_quality.append(agent_id)

    assert not without_quality, (
        f"QA agents without quality/testing mentions: {without_quality}\n"
        f"Expected all QA agents to mention quality metrics or testing concepts."
    )


@pytest.mark.patterns
def test_agents_have_sufficient_content_length(
    compiled_agents: Dict[str, CompiledAgent],
) -> None:
    """Test that agents have sufficient content (not just stubs).

    Args:
        compiled_agents: Dict of compiled agents

    Raises:
        AssertionError: If too many agents have insufficient content
    """
    min_lines = 50  # Minimum lines for a valid agent
    short_agents = []

    for agent_id, agent in compiled_agents.items():
        if agent.total_lines < min_lines:
            short_agents.append((agent_id, agent.total_lines))

    # Allow up to 10% to be short (might be minimal agents)
    max_short = len(compiled_agents) * 0.1
    assert len(short_agents) <= max_short, (
        f"Agents with insufficient content (<{min_lines} lines): {short_agents}\n"
        f"Expected agents to have substantial content defining their expertise."
    )


@pytest.mark.patterns
def test_agents_define_their_identity(
    compiled_agents: Dict[str, CompiledAgent],
) -> None:
    """Test that agents define their role/identity in content.

    Args:
        compiled_agents: Dict of compiled agents

    Raises:
        AssertionError: If too many agents lack identity definition
    """
    # Patterns that indicate agent identity
    identity_patterns = [
        r"I am|I'm|specialist|expert|engineer|agent",
        r"my role|my expertise|my focus",
        r"when to use me|when to invoke",
    ]

    without_identity = []
    for agent_id, agent in compiled_agents.items():
        has_identity = any(
            re.search(pattern, agent.compiled_content, re.IGNORECASE)
            for pattern in identity_patterns
        )
        if not has_identity:
            without_identity.append(agent_id)

    # Allow up to 30% to not explicitly define identity
    max_without = len(compiled_agents) * 0.3
    assert len(without_identity) <= max_without, (
        f"Agents without clear identity: {without_identity[:10]}\n"
        f"Expected agents to define their role and expertise."
    )
