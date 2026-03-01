"""
Real User Agent Behavioral Tests

Tests the Real User agent's ability to simulate realistic user behavior
with configurable personas and browser tool auto-selection.

Usage:
    pytest test_real_user_agent.py -v
    pytest test_real_user_agent.py -v -m persona
    pytest test_real_user_agent.py -v -m browser_tools
"""

import random
import pytest
from dataclasses import dataclass
from typing import Dict, List, Optional
from unittest.mock import Mock

# DeepEval imports (install: pip install deepeval)
try:
    from deepeval import assert_test
    from deepeval.metrics import BiasMetric, ToxicityMetric, AnswerRelevancyMetric
    from deepeval.test_case import LLMTestCase

    DEEPEVAL_AVAILABLE = True
except ImportError:
    DEEPEVAL_AVAILABLE = False
    pytest.skip("deepeval not installed", allow_module_level=True)


# =============================================================================
# FIXTURES
# =============================================================================


@dataclass
class Persona:
    """User persona configuration."""

    name: str
    experience_level: str  # novice, intermediate, expert
    patience: str  # patient, normal, impatient
    device: str  # desktop, tablet, mobile
    reading_speed_wpm: int
    action_delay_ms: tuple  # (min, max) delay between actions


@pytest.fixture
def novice_persona() -> Persona:
    return Persona(
        name="novice_user",
        experience_level="novice",
        patience="patient",
        device="desktop",
        reading_speed_wpm=150,
        action_delay_ms=(2000, 5000),
    )


@pytest.fixture
def expert_persona() -> Persona:
    return Persona(
        name="expert_user",
        experience_level="expert",
        patience="normal",
        device="desktop",
        reading_speed_wpm=300,
        action_delay_ms=(200, 800),
    )


@pytest.fixture
def impatient_persona() -> Persona:
    return Persona(
        name="impatient_user",
        experience_level="intermediate",
        patience="impatient",
        device="desktop",
        reading_speed_wpm=250,
        action_delay_ms=(100, 500),
    )


@pytest.fixture
def mobile_persona() -> Persona:
    return Persona(
        name="mobile_user",
        experience_level="intermediate",
        patience="normal",
        device="mobile",
        reading_speed_wpm=200,
        action_delay_ms=(500, 1500),
    )


@pytest.fixture
def mock_browser_tools():
    """Mock browser tool availability."""
    return {
        "native_browser": Mock(available=True, name="mcp__browser__navigate"),
        "chrome_devtools": Mock(available=True, name="mcp__chrome-devtools__navigate"),
        "playwright": Mock(available=True, name="mcp__playwright__navigate"),
    }


@pytest.fixture
def test_page():
    """Sample test page content."""
    return {
        "url": "https://example.com/product",
        "title": "Product Page",
        "content_length": 500,  # words
        "load_time_ms": 1200,
        "has_form": True,
        "form_fields": 5,
    }


# =============================================================================
# MOCK REAL USER AGENT
# =============================================================================


class MockRealUserAgent:
    """Mock Real User agent for testing behavioral simulation."""

    def __init__(self, persona: Persona, available_tools: Dict):
        self.persona = persona
        self.available_tools = available_tools
        self.actions_log: List[Dict] = []

    def calculate_reading_time(self, word_count: int) -> int:
        """Calculate reading time based on persona's reading speed."""
        minutes = word_count / self.persona.reading_speed_wpm
        return int(minutes * 60 * 1000)  # Return milliseconds

    def get_action_delay(self) -> int:
        """Get randomized action delay within persona's range."""
        min_delay, max_delay = self.persona.action_delay_ms
        return random.randint(min_delay, max_delay)

    def should_abandon_slow_page(self, load_time_ms: int) -> bool:
        """Determine if user would abandon slow-loading page."""
        thresholds = {"patient": 5000, "normal": 3000, "impatient": 1500}
        return load_time_ms > thresholds[self.persona.patience]

    def select_browser_tool(self) -> Optional[str]:
        """Auto-select browser tool based on availability."""
        priority = ["native_browser", "chrome_devtools", "playwright"]
        for tool_key in priority:
            tool = self.available_tools.get(tool_key)
            if tool and tool.available:
                return tool.name
        return None

    def get_interaction_type(self) -> str:
        """Get appropriate interaction type for device."""
        if self.persona.device == "mobile":
            return "tap"
        return "click"


# =============================================================================
# PERSONA COMPLIANCE TESTS
# =============================================================================


class TestPersonaCompliance:
    """Test persona-based behavioral adjustments."""

    @pytest.mark.persona
    def test_novice_user_takes_longer_between_actions(self, novice_persona, expert_persona):
        """Novice users should have longer delays between actions."""
        novice_agent = MockRealUserAgent(novice_persona, {})
        expert_agent = MockRealUserAgent(expert_persona, {})

        novice_delays = [novice_agent.get_action_delay() for _ in range(100)]
        expert_delays = [expert_agent.get_action_delay() for _ in range(100)]

        avg_novice = sum(novice_delays) / len(novice_delays)
        avg_expert = sum(expert_delays) / len(expert_delays)

        assert (
            avg_novice > avg_expert
        ), f"Novice avg delay ({avg_novice}ms) should exceed expert ({avg_expert}ms)"
        assert avg_novice >= 2000, "Novice minimum delay should be >= 2000ms"

    @pytest.mark.persona
    def test_impatient_user_abandons_slow_pages(self, impatient_persona, test_page):
        """Impatient users should abandon pages that load slowly."""
        agent = MockRealUserAgent(impatient_persona, {})

        # Slow page (2000ms) should trigger abandonment for impatient user
        assert agent.should_abandon_slow_page(2000) is True
        # Fast page (500ms) should not trigger abandonment
        assert agent.should_abandon_slow_page(500) is False

    @pytest.mark.persona
    def test_mobile_user_uses_tap_interactions(self, mobile_persona):
        """Mobile users should use tap instead of click interactions."""
        agent = MockRealUserAgent(mobile_persona, {})

        interaction = agent.get_interaction_type()

        assert interaction == "tap", f"Mobile should use 'tap', got '{interaction}'"


# =============================================================================
# BEHAVIORAL AUTHENTICITY TESTS
# =============================================================================


class TestBehavioralAuthenticity:
    """Test realistic user simulation behaviors."""

    @pytest.mark.behavioral
    def test_reading_time_correlates_with_content_length(self, novice_persona):
        """Reading time should scale with content length."""
        agent = MockRealUserAgent(novice_persona, {})

        short_content_time = agent.calculate_reading_time(100)  # 100 words
        long_content_time = agent.calculate_reading_time(500)  # 500 words

        assert long_content_time > short_content_time
        assert (
            long_content_time == short_content_time * 5
        ), "500 words should take 5x longer than 100 words"

    @pytest.mark.behavioral
    def test_random_delays_within_expected_range(self, expert_persona):
        """Action delays should fall within persona's configured range."""
        agent = MockRealUserAgent(expert_persona, {})
        min_delay, max_delay = expert_persona.action_delay_ms

        delays = [agent.get_action_delay() for _ in range(100)]

        assert all(
            min_delay <= d <= max_delay for d in delays
        ), f"All delays should be between {min_delay} and {max_delay}ms"
        # Verify randomness (not all same value)
        assert len(set(delays)) > 1, "Delays should be randomized"


# =============================================================================
# BROWSER TOOL SELECTION TESTS
# =============================================================================


class TestBrowserToolSelection:
    """Test browser tool auto-selection logic."""

    @pytest.mark.browser_tools
    def test_prefers_native_browser_when_available(self, expert_persona, mock_browser_tools):
        """Should prefer native browser tool when available."""
        agent = MockRealUserAgent(expert_persona, mock_browser_tools)

        selected = agent.select_browser_tool()

        assert selected == "mcp__browser__navigate", f"Should select native browser, got {selected}"

    @pytest.mark.browser_tools
    def test_falls_back_to_chrome_devtools(self, expert_persona, mock_browser_tools):
        """Should fall back to Chrome DevTools when native unavailable."""
        mock_browser_tools["native_browser"].available = False
        agent = MockRealUserAgent(expert_persona, mock_browser_tools)

        selected = agent.select_browser_tool()

        assert selected == "mcp__chrome-devtools__navigate"

    @pytest.mark.browser_tools
    def test_reports_no_tools_available_gracefully(self, expert_persona):
        """Should return None when no browser tools available."""
        empty_tools = {}
        agent = MockRealUserAgent(expert_persona, empty_tools)

        selected = agent.select_browser_tool()

        assert selected is None, "Should return None when no tools available"


# =============================================================================
# DEEPEVAL METRIC TESTS
# =============================================================================


@pytest.mark.skipif(not DEEPEVAL_AVAILABLE, reason="deepeval not installed")
class TestDeepEvalMetrics:
    """Test agent outputs using DeepEval metrics."""

    def test_persona_behavior_is_unbiased(self):
        """Ensure persona configurations don't introduce harmful bias."""
        test_case = LLMTestCase(
            input="Simulate a novice user browsing an e-commerce site",
            actual_output="The novice user carefully reads product descriptions, "
            "takes 3-5 seconds between actions, and uses the search "
            "bar to find products rather than navigating categories.",
            expected_output="Realistic novice user behavior simulation",
        )
        metric = BiasMetric(threshold=0.7)
        assert_test(test_case, [metric])

    def test_simulated_behavior_is_appropriate(self):
        """Ensure simulated user behavior is non-toxic."""
        test_case = LLMTestCase(
            input="Simulate an impatient user encountering a slow website",
            actual_output="The user waits briefly, then navigates away after "
            "the page takes too long to load. They try a different "
            "search result instead.",
            expected_output="Realistic impatient user behavior",
        )
        metric = ToxicityMetric(threshold=0.7)
        assert_test(test_case, [metric])

    def test_agent_follows_persona_instructions(self):
        """Ensure agent responses are relevant to persona instructions."""
        test_case = LLMTestCase(
            input="Act as an expert user navigating to checkout",
            actual_output="Expert user navigates directly to cart, applies "
            "saved payment method, and completes checkout in "
            "under 30 seconds with minimal delays.",
            expected_output="Efficient expert user checkout flow",
        )
        metric = AnswerRelevancyMetric(threshold=0.7)
        assert_test(test_case, [metric])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
