"""Load and parse agent markdown files with YAML frontmatter."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml


@dataclass
class AgentDefinition:
    """Represents a parsed agent definition."""

    path: Path
    name: str
    description: str
    agent_id: str
    agent_type: str
    version: str
    skills: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    knowledge: list[str] = field(default_factory=list)
    interactions: dict[str, Any] = field(default_factory=dict)
    body_content: str = ""
    raw_frontmatter: dict[str, Any] = field(default_factory=dict)


@dataclass
class CompiledAgent:
    """A fully compiled agent with all BASE-AGENT.md inheritance."""

    path: Path
    frontmatter: dict[str, Any]
    agent_body: str
    base_agents: list[dict[str, Any]]  # List of {path, content, relative}
    compiled_content: str
    total_lines: int

    @property
    def agent_id(self) -> str:
        """Get agent ID from frontmatter or filename."""
        return self.frontmatter.get("agent_id", self.path.stem)

    @property
    def agent_type(self) -> str:
        """Get agent type from frontmatter."""
        return self.frontmatter.get("agent_type", "")

    @property
    def inheritance_chain(self) -> list[str]:
        """Return list of BASE-AGENT.md files in inheritance order."""
        return [str(b["relative"]) for b in self.base_agents]

    def has_instruction(self, pattern: str) -> bool:
        """Check if compiled agent contains instruction matching pattern.

        Args:
            pattern: Regex pattern to search for

        Returns:
            True if pattern found in compiled content
        """
        return bool(re.search(pattern, self.compiled_content, re.IGNORECASE | re.MULTILINE))

    def get_section(self, header: str) -> Optional[str]:
        """Extract a markdown section by header.

        Args:
            header: Section header text (without ##)

        Returns:
            Section content or None if not found
        """
        pattern = rf"^##\s+{re.escape(header)}\s*\n(.*?)(?=^##|\Z)"
        match = re.search(pattern, self.compiled_content, re.MULTILINE | re.DOTALL)
        return match.group(1).strip() if match else None


class AgentLoader:
    """Load agent definitions from markdown files."""

    # Regex to extract YAML frontmatter
    FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

    def __init__(self, agents_dir: Path):
        """Initialize loader with agents directory.

        Args:
            agents_dir: Path to directory containing agent markdown files
        """
        self.agents_dir = Path(agents_dir)

    def load_agent(self, path: Path) -> AgentDefinition:
        """Load a single agent definition from markdown file.

        Args:
            path: Path to agent markdown file

        Returns:
            AgentDefinition with parsed frontmatter and body

        Raises:
            ValueError: If frontmatter is missing or invalid
        """
        content = path.read_text(encoding="utf-8")

        # Extract frontmatter and body
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            raise ValueError(f"No frontmatter found in {path}")

        frontmatter_text = match.group(1)
        body_content = match.group(2).strip()

        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {path}: {e}")

        if not isinstance(frontmatter, dict):
            raise ValueError(f"Frontmatter must be a dict in {path}")

        # Extract required fields with defaults
        return AgentDefinition(
            path=path,
            name=frontmatter.get("name", ""),
            description=frontmatter.get("description", ""),
            agent_id=frontmatter.get("agent_id", ""),
            agent_type=frontmatter.get("agent_type", ""),
            version=frontmatter.get("version", ""),
            skills=frontmatter.get("skills", []),
            tags=frontmatter.get("tags", []),
            knowledge=frontmatter.get("knowledge", []),
            interactions=frontmatter.get("interactions", {}),
            body_content=body_content,
            raw_frontmatter=frontmatter,
        )

    def load_all_agents(self) -> list[AgentDefinition]:
        """Load all agent definitions from agents directory.

        Returns:
            List of AgentDefinition objects

        Raises:
            ValueError: If agents_dir does not exist
        """
        if not self.agents_dir.exists():
            raise ValueError(f"Agents directory not found: {self.agents_dir}")

        agents = []
        for agent_file in self.agents_dir.rglob("*.md"):
            # Skip BASE-AGENT.md files (they are templates, not agents)
            if agent_file.name.startswith("BASE-AGENT"):
                continue

            try:
                agent = self.load_agent(agent_file)
                agents.append(agent)
            except ValueError as e:
                # Log but continue - some files may not be valid agents
                print(f"Warning: Skipping {agent_file}: {e}")
                continue

        return agents

    def get_agents_by_type(self, agent_type: str) -> list[AgentDefinition]:
        """Get all agents of a specific type.

        Args:
            agent_type: Agent type to filter by (e.g., 'engineer', 'qa', 'ops')

        Returns:
            List of AgentDefinition objects matching the type
        """
        all_agents = self.load_all_agents()
        return [agent for agent in all_agents if agent.agent_type == agent_type]


class CompiledAgentLoader:
    """Load and compile agents with full BASE-AGENT.md inheritance."""

    # Regex to extract YAML frontmatter
    FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

    def __init__(self, agents_dir: Path):
        """Initialize loader with agents directory.

        Args:
            agents_dir: Path to directory containing agent markdown files
        """
        self.agents_dir = Path(agents_dir)
        self.root_dir = agents_dir.parent

    def find_base_agents(self, agent_path: Path) -> list[Path]:
        """Find all BASE-AGENT.md files from agent's directory up to agents root.

        Args:
            agent_path: Path to agent file

        Returns:
            List of BASE-AGENT.md paths in inheritance order (root first)
        """
        base_files = []
        current = agent_path.parent

        while current >= self.agents_dir:
            base_file = current / "BASE-AGENT.md"
            if base_file.exists():
                base_files.insert(0, base_file)
            current = current.parent

        return base_files

    def _extract_frontmatter(self, content: str) -> tuple[str, str]:
        """Extract YAML frontmatter from content.

        Args:
            content: Markdown content with frontmatter

        Returns:
            Tuple of (frontmatter, body)
        """
        match = self.FRONTMATTER_PATTERN.match(content)
        if match:
            return match.group(1), match.group(2)
        return "", content

    def compile_agent(self, agent_path: Path) -> CompiledAgent:
        """Compile agent with all inherited BASE-AGENT.md content.

        Args:
            agent_path: Path to agent markdown file

        Returns:
            CompiledAgent with all BASE-AGENT.md content merged

        Raises:
            FileNotFoundError: If agent file doesn't exist
            ValueError: If frontmatter is invalid
        """
        if not agent_path.exists():
            raise FileNotFoundError(f"Agent file not found: {agent_path}")

        # Read agent content
        agent_content = agent_path.read_text(encoding="utf-8")
        frontmatter_text, body = self._extract_frontmatter(agent_content)

        # Parse frontmatter
        frontmatter = {}
        if frontmatter_text:
            try:
                frontmatter = yaml.safe_load(frontmatter_text)
                if not isinstance(frontmatter, dict):
                    frontmatter = {}
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid YAML frontmatter in {agent_path}: {e}")

        # Find and read all BASE-AGENT.md files
        base_files = self.find_base_agents(agent_path)
        base_contents = []
        for base_path in base_files:
            base_content = base_path.read_text(encoding="utf-8")
            _, base_body = self._extract_frontmatter(base_content)
            base_contents.append(
                {
                    "path": base_path,
                    "content": base_body,
                    "relative": base_path.relative_to(self.agents_dir),
                }
            )

        # Combine: agent body + all BASE-AGENT content (root first)
        compiled_content = body.strip()
        for base in base_contents:
            compiled_content += f"\n\n---\n\n# Inherited from {base['relative']}\n\n"
            compiled_content += base["content"].strip()

        return CompiledAgent(
            path=agent_path,
            frontmatter=frontmatter,
            agent_body=body.strip(),
            base_agents=base_contents,
            compiled_content=compiled_content,
            total_lines=len(compiled_content.split("\n")),
        )

    def compile_all_agents(self) -> dict[str, CompiledAgent]:
        """Compile all agents with BASE-AGENT.md inheritance.

        Returns:
            Dict mapping agent_id to CompiledAgent objects
        """
        compiled = {}
        for agent_path in self.agents_dir.rglob("*.md"):
            if agent_path.name == "BASE-AGENT.md":
                continue
            try:
                agent = self.compile_agent(agent_path)
                agent_id = agent.frontmatter.get("agent_id", agent_path.stem)
                compiled[agent_id] = agent
            except Exception as e:
                print(f"Warning: Failed to compile {agent_path}: {e}")
        return compiled
