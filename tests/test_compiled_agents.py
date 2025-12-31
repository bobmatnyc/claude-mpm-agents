"""Tests for compiled agent instruction validation.

This module tests fully compiled agents (agent + all BASE-AGENT.md inheritance)
to verify that required instructions are present after compilation.
"""

import pytest
from pathlib import Path

from tests.fixtures.agent_loader import CompiledAgentLoader
from tests.fixtures.instruction_extractor import InstructionExtractor


@pytest.mark.compiled
class TestBaseAgentInheritance:
    """Test that agents properly inherit from BASE-AGENT.md files."""

    @pytest.fixture
    def compiled_loader(self, agents_dir: Path) -> CompiledAgentLoader:
        """Create compiled agent loader."""
        return CompiledAgentLoader(agents_dir)

    @pytest.fixture
    def compiled_agents(self, compiled_loader: CompiledAgentLoader) -> dict:
        """Load all compiled agents."""
        return compiled_loader.compile_all_agents()

    def test_all_agents_have_root_base_agent(self, compiled_agents: dict):
        """Verify all compiled agents include root BASE-AGENT.md content."""
        for agent_id, agent in compiled_agents.items():
            assert any(
                "BASE-AGENT.md" in str(b["relative"]) for b in agent.base_agents
            ), f"{agent_id} missing root BASE-AGENT.md inheritance"

    def test_engineer_agents_have_engineer_base(self, compiled_agents: dict):
        """Verify engineer agents include engineer/BASE-AGENT.md."""
        engineer_agents = {k: v for k, v in compiled_agents.items() if v.agent_type == "engineer"}

        for agent_id, agent in engineer_agents.items():
            has_engineer_base = any(
                "engineer/BASE-AGENT.md" in str(b["relative"]) for b in agent.base_agents
            )
            assert has_engineer_base, f"{agent_id} missing engineer/BASE-AGENT.md"

    def test_qa_agents_have_qa_base(self, compiled_agents: dict):
        """Verify QA agents include qa/BASE-AGENT.md."""
        qa_agents = {k: v for k, v in compiled_agents.items() if v.agent_type == "qa"}

        for agent_id, agent in qa_agents.items():
            has_qa_base = any("qa/BASE-AGENT.md" in str(b["relative"]) for b in agent.base_agents)
            assert has_qa_base, f"{agent_id} missing qa/BASE-AGENT.md"

    def test_ops_agents_have_ops_base(self, compiled_agents: dict):
        """Verify ops agents in ops/ directory include ops/BASE-AGENT.md."""
        ops_agents = {
            k: v
            for k, v in compiled_agents.items()
            if v.agent_type == "ops" and "ops/" in str(v.path)
        }

        for agent_id, agent in ops_agents.items():
            has_ops_base = any("ops/BASE-AGENT.md" in str(b["relative"]) for b in agent.base_agents)
            assert has_ops_base, f"{agent_id} missing ops/BASE-AGENT.md"

    def test_inheritance_chain_order(self, compiled_agents: dict):
        """Verify inheritance chain is in correct order (root first)."""
        for agent_id, agent in compiled_agents.items():
            if len(agent.inheritance_chain) > 1:
                # Root BASE-AGENT.md should come before category-specific ones
                chain = agent.inheritance_chain
                root_index = next(
                    (i for i, path in enumerate(chain) if path == "BASE-AGENT.md"), -1
                )
                if root_index >= 0:
                    # All other BASE-AGENT.md files should come after root
                    for i, path in enumerate(chain):
                        if i < root_index and "BASE-AGENT.md" in path:
                            pytest.fail(f"{agent_id} has incorrect inheritance order: {chain}")


@pytest.mark.compiled
class TestCompiledAgentInstructions:
    """Test that compiled agents contain required instructions."""

    @pytest.fixture
    def compiled_loader(self, agents_dir: Path) -> CompiledAgentLoader:
        """Create compiled agent loader."""
        return CompiledAgentLoader(agents_dir)

    @pytest.fixture
    def compiled_agents(self, compiled_loader: CompiledAgentLoader) -> dict:
        """Load all compiled agents."""
        return compiled_loader.compile_all_agents()

    # Root BASE-AGENT.md instructions (should be in ALL agents)

    def test_all_agents_have_git_workflow(self, compiled_agents: dict):
        """All agents must have Git Workflow instructions."""
        for agent_id, agent in compiled_agents.items():
            assert agent.has_instruction(
                r"Git Workflow"
            ), f"{agent_id} missing Git Workflow section"

    def test_all_agents_have_conventional_commits(self, compiled_agents: dict):
        """All agents must have conventional commits instructions."""
        for agent_id, agent in compiled_agents.items():
            assert agent.has_instruction(
                r"(feat|fix|docs|refactor|perf|test|chore)"
            ), f"{agent_id} missing conventional commits examples"

    def test_all_agents_have_output_format(self, compiled_agents: dict):
        """All agents must have Output Format instructions."""
        for agent_id, agent in compiled_agents.items():
            assert agent.has_instruction(
                r"Output Format"
            ), f"{agent_id} missing Output Format section"

    def test_all_agents_have_handoff_protocol(self, compiled_agents: dict):
        """All agents must have Handoff Protocol instructions."""
        for agent_id, agent in compiled_agents.items():
            assert agent.has_instruction(r"Handoff"), f"{agent_id} missing Handoff Protocol section"

    def test_all_agents_have_search_before_implement(self, compiled_agents: dict):
        """All agents should have search-before-implement instructions."""
        for agent_id, agent in compiled_agents.items():
            assert agent.has_instruction(
                r"Search Before|search.*existing|grep"
            ), f"{agent_id} missing search-before-implement instructions"

    def test_all_agents_have_quality_standards(self, compiled_agents: dict):
        """All agents should have quality standards."""
        for agent_id, agent in compiled_agents.items():
            assert agent.has_instruction(
                r"Quality|quality standards|best practices"
            ), f"{agent_id} missing quality standards"

    # Engineer-specific instructions

    def test_engineer_agents_have_type_safety(self, compiled_agents: dict):
        """Engineer agents must have type safety instructions."""
        engineers = {k: v for k, v in compiled_agents.items() if v.agent_type == "engineer"}

        for agent_id, agent in engineers.items():
            assert agent.has_instruction(
                r"type.?safe|type coverage|100%.*type"
            ), f"{agent_id} missing type safety instructions"

    def test_engineer_agents_have_testing_requirements(self, compiled_agents: dict):
        """Engineer agents must have testing requirements."""
        engineers = {k: v for k, v in compiled_agents.items() if v.agent_type == "engineer"}

        for agent_id, agent in engineers.items():
            assert agent.has_instruction(
                r"test|coverage|90%"
            ), f"{agent_id} missing testing requirements"

    def test_engineer_agents_have_architecture_guidance(self, compiled_agents: dict):
        """Engineer agents should have architecture guidance."""
        engineers = {k: v for k, v in compiled_agents.items() if v.agent_type == "engineer"}

        for agent_id, agent in engineers.items():
            assert agent.has_instruction(
                r"SOLID|architecture|design pattern"
            ), f"{agent_id} missing architecture guidance"

    # QA-specific instructions

    def test_qa_agents_have_coverage_standards(self, compiled_agents: dict):
        """QA agents must have coverage standards."""
        qa_agents = {k: v for k, v in compiled_agents.items() if v.agent_type == "qa"}

        for agent_id, agent in qa_agents.items():
            assert agent.has_instruction(r"coverage|test"), f"{agent_id} missing coverage standards"

    def test_qa_agents_have_bug_report_format(self, compiled_agents: dict):
        """QA agents should have bug report format instructions."""
        qa_agents = {k: v for k, v in compiled_agents.items() if v.agent_type == "qa"}

        for agent_id, agent in qa_agents.items():
            assert agent.has_instruction(
                r"steps to reproduce|expected.*actual"
            ), f"{agent_id} missing bug report format"

    # Ops-specific instructions

    def test_ops_agents_have_deployment_verification(self, compiled_agents: dict):
        """Ops agents must have deployment verification instructions."""
        ops_agents = {k: v for k, v in compiled_agents.items() if v.agent_type == "ops"}

        for agent_id, agent in ops_agents.items():
            assert agent.has_instruction(
                r"verif|health.?check|deployment"
            ), f"{agent_id} missing deployment verification"

    def test_ops_agents_have_rollback_guidance(self, compiled_agents: dict):
        """Ops agents in ops/ directory should have rollback/recovery guidance."""
        # Only check ops agents in the ops/ directory (deployment-focused)
        ops_agents = {
            k: v
            for k, v in compiled_agents.items()
            if v.agent_type == "ops" and "ops/" in str(v.path)
        }

        for agent_id, agent in ops_agents.items():
            assert agent.has_instruction(
                r"rollback|revert|recovery"
            ), f"{agent_id} missing rollback guidance"


@pytest.mark.base_agent
class TestBaseAgentFiles:
    """Test BASE-AGENT.md files directly."""

    @pytest.fixture
    def base_agent_files(self, agents_dir: Path) -> list[Path]:
        """Find all BASE-AGENT.md files."""
        return list(agents_dir.rglob("BASE-AGENT.md"))

    def test_base_agent_files_exist(self, base_agent_files: list[Path]):
        """Verify BASE-AGENT.md files exist."""
        assert len(base_agent_files) > 0, "No BASE-AGENT.md files found"

    def test_root_base_agent_exists(self, agents_dir: Path):
        """Root BASE-AGENT.md must exist."""
        root_base = agents_dir / "BASE-AGENT.md"
        assert root_base.exists(), "Root BASE-AGENT.md not found"

    def test_root_base_agent_has_required_sections(self, agents_dir: Path):
        """Root BASE-AGENT.md must have required sections."""
        root_base = agents_dir / "BASE-AGENT.md"
        content = root_base.read_text(encoding="utf-8")

        required_sections = [
            "Git Workflow",
            "Output Format",
            "Handoff Protocol",
        ]

        for section in required_sections:
            assert section in content, f"Root BASE-AGENT.md missing '{section}' section"

    def test_category_base_agents_have_category_content(
        self, base_agent_files: list[Path], agents_dir: Path
    ):
        """Category BASE-AGENT.md files should have category-specific content."""
        category_bases = [f for f in base_agent_files if f.parent != agents_dir]

        for base_file in category_bases:
            content = base_file.read_text(encoding="utf-8")

            # Each category should have some specific content
            assert len(content) > 100, f"{base_file} has insufficient content"

    def test_base_agent_files_are_valid_markdown(self, base_agent_files: list[Path]):
        """BASE-AGENT.md files should be valid markdown."""
        for base_file in base_agent_files:
            content = base_file.read_text(encoding="utf-8")

            # Basic markdown validation
            assert len(content) > 0, f"{base_file} is empty"

            # Should have at least one heading
            assert "#" in content, f"{base_file} has no markdown headings"


@pytest.mark.base_agent
class TestInstructionExtraction:
    """Test instruction extraction from BASE-AGENT.md files."""

    @pytest.fixture
    def extractor(self, agents_dir: Path) -> InstructionExtractor:
        """Create instruction extractor."""
        return InstructionExtractor(agents_dir.parent)

    def test_root_rules_extracted(self, extractor: InstructionExtractor):
        """Verify rules are extracted from root BASE-AGENT.md."""
        rules = extractor.extract_root_rules()
        assert len(rules) > 0, "No rules extracted from root BASE-AGENT.md"

    def test_category_rules_extracted(self, extractor: InstructionExtractor):
        """Verify rules are extracted from category BASE-AGENT.md files."""
        # Test engineer rules
        engineer_rules = extractor.extract_category_rules("engineer")
        assert len(engineer_rules) > 0, "No engineer rules extracted"

        # Test QA rules
        qa_rules = extractor.extract_category_rules("qa")
        assert len(qa_rules) > 0, "No QA rules extracted"

    def test_git_workflow_rule_exists(self, extractor: InstructionExtractor):
        """Verify git workflow rule is extracted."""
        rules = extractor.extract_root_rules()
        git_rules = [r for r in rules if "git" in r.rule_id.lower()]
        assert len(git_rules) > 0, "No git workflow rules extracted"

    def test_extracted_rules_have_patterns(self, extractor: InstructionExtractor):
        """Verify extracted rules have patterns."""
        rules = extractor.extract_root_rules()

        for rule in rules:
            assert (
                len(rule.positive_patterns) > 0 or len(rule.negative_patterns) > 0
            ), f"Rule {rule.rule_id} has no patterns"


@pytest.mark.compiled
class TestCompilationCorrectness:
    """Test that agent compilation works correctly."""

    @pytest.fixture
    def compiled_loader(self, agents_dir: Path) -> CompiledAgentLoader:
        """Create compiled agent loader."""
        return CompiledAgentLoader(agents_dir)

    def test_agent_body_preserved(self, compiled_loader: CompiledAgentLoader, agents_dir: Path):
        """Verify agent-specific content is preserved in compilation."""
        # Find a sample agent
        sample_agents = list(agents_dir.rglob("*.md"))
        sample_agents = [a for a in sample_agents if a.name != "BASE-AGENT.md"]

        if sample_agents:
            sample_agent = sample_agents[0]
            compiled = compiled_loader.compile_agent(sample_agent)

            # Agent body should be in compiled content
            assert (
                compiled.agent_body in compiled.compiled_content
            ), "Agent body not preserved in compilation"

    def test_base_content_appended(self, compiled_loader: CompiledAgentLoader, agents_dir: Path):
        """Verify BASE-AGENT.md content is appended to compiled agent."""
        # Find a sample agent
        sample_agents = list(agents_dir.rglob("*.md"))
        sample_agents = [a for a in sample_agents if a.name != "BASE-AGENT.md"]

        if sample_agents:
            sample_agent = sample_agents[0]
            compiled = compiled_loader.compile_agent(sample_agent)

            # Should have base agent content
            assert len(compiled.base_agents) > 0, "No base agents found"

            # Check that base content is present (using marker text instead of exact match)
            # The content might be slightly different due to whitespace normalization
            for base in compiled.base_agents:
                # Look for unique markers from the base content
                base_content_stripped = base["content"].strip()
                if base_content_stripped:
                    # Extract first non-empty line as marker
                    lines = [line for line in base_content_stripped.split("\n") if line.strip()]
                    if lines:
                        # Check if any distinctive line from base is in compiled
                        marker = lines[0][:50]  # First 50 chars of first line
                        assert (
                            marker in compiled.compiled_content
                        ), f"Base content from {base['relative']} not found in compiled agent (marker: {marker[:30]}...)"

    def test_frontmatter_extracted(self, compiled_loader: CompiledAgentLoader, agents_dir: Path):
        """Verify frontmatter is correctly extracted."""
        # Find a sample agent
        sample_agents = list(agents_dir.rglob("*.md"))
        sample_agents = [a for a in sample_agents if a.name != "BASE-AGENT.md"]

        if sample_agents:
            sample_agent = sample_agents[0]
            compiled = compiled_loader.compile_agent(sample_agent)

            # Should have frontmatter (most agents do)
            if compiled.frontmatter:
                assert isinstance(compiled.frontmatter, dict)
                assert "name" in compiled.frontmatter or "agent_id" in compiled.frontmatter

    def test_compiled_content_larger_than_agent_body(
        self, compiled_loader: CompiledAgentLoader, agents_dir: Path
    ):
        """Compiled content should be larger than agent body alone."""
        # Find a sample agent
        sample_agents = list(agents_dir.rglob("*.md"))
        sample_agents = [a for a in sample_agents if a.name != "BASE-AGENT.md"]

        if sample_agents:
            sample_agent = sample_agents[0]
            compiled = compiled_loader.compile_agent(sample_agent)

            # Compiled should be larger if there are BASE-AGENT.md files
            if len(compiled.base_agents) > 0:
                assert len(compiled.compiled_content) > len(
                    compiled.agent_body
                ), "Compiled content should be larger than agent body"
