"""Example of creating custom tests for agent compliance.

This file demonstrates how to:
1. Create custom DeepEval metrics
2. Write tests with mock responses
3. Test both compliant and non-compliant cases
"""

import re

import pytest
from deepeval import assert_test
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

from tests.fixtures.mock_responses import MockResponseGenerator


# Example 1: Custom Metric
class CodeQualityMetric(BaseMetric):
    """Custom metric to check code quality indicators in responses."""

    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold
        self.violations: list[str] = []

    @property
    def __name__(self) -> str:
        return "Code Quality"

    def measure(self, test_case: LLMTestCase) -> float:
        """Measure code quality indicators in response."""
        self.violations = []
        output = test_case.actual_output

        if not output:
            self.score = 0.0
            self.success = False
            self.reason = "Empty output"
            return self.score

        checks_passed = 0
        total_checks = 4

        # Check 1: Has type hints
        if re.search(r"(:\s*\w+|-> \w+)", output):
            checks_passed += 1
        else:
            self.violations.append("Missing type hints")

        # Check 2: Has error handling
        if re.search(r"(try:|except|raise|throw)", output, re.IGNORECASE):
            checks_passed += 1
        else:
            self.violations.append("No error handling")

        # Check 3: Has comments/docstrings
        if re.search(r'(""".*?"""|#.*)', output, re.DOTALL):
            checks_passed += 1
        else:
            self.violations.append("No comments or docstrings")

        # Check 4: Has tests mentioned
        if re.search(r"(test|assert|expect)", output, re.IGNORECASE):
            checks_passed += 1
        else:
            self.violations.append("No testing mentioned")

        self.score = checks_passed / total_checks
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"Code quality: {self.score:.1%}"
        else:
            self.reason = f"Quality issues: {', '.join(self.violations)}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return self.success


# Example 2: Test with Custom Metric
class TestCodeQualityExample:
    """Example tests using custom metric."""

    def test_high_quality_code_passes(self):
        """Test that high-quality code passes quality checks."""
        response_content = '''
## Implementation: User Service

```python
from typing import Optional

class UserService:
    """Service for managing user operations."""

    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User ID to fetch

        Returns:
            User object or None if not found

        Raises:
            DatabaseError: If database connection fails
        """
        try:
            user = await self.repository.get_by_id(user_id)
            return user
        except DatabaseError as e:
            logger.error("Failed to fetch user: %s", e)
            raise

# Tests:
# - test_get_user_returns_user()
# - test_get_user_not_found()
# - test_get_user_database_error()
```
'''

        test_case = LLMTestCase(
            input="Implement user service",
            actual_output=response_content,
        )

        metric = CodeQualityMetric(threshold=0.75)
        assert_test(test_case, [metric])

    def test_low_quality_code_fails(self):
        """Test that low-quality code fails quality checks."""
        response_content = """
Here's the code:

```python
def get_user(id):
    return db.query(id)
```

Done.
"""

        test_case = LLMTestCase(
            input="Get user",
            actual_output=response_content,
        )

        metric = CodeQualityMetric(threshold=0.75)
        try:
            assert_test(test_case, [metric])
            pytest.fail("Expected low quality code to fail")
        except AssertionError:
            # Expected to fail
            pass


# Example 3: Test with Mock Generator
class TestWithMockGenerator:
    """Example tests using mock response generator."""

    def test_engineer_response_quality(self, mock_generator: MockResponseGenerator):
        """Test that engineer response has quality code patterns."""
        response = mock_generator.generate_compliant_response(
            agent_type="engineer",
            task_type="implement_feature",
        )

        test_case = LLMTestCase(
            input="Implement authentication",
            actual_output=response.content,
        )

        metric = CodeQualityMetric(threshold=0.75)
        assert_test(test_case, [metric])


# Example 4: Parametrized Test
class TestParametrizedExample:
    """Example of parametrized tests for multiple scenarios."""

    @pytest.mark.parametrize(
        "agent_type,task_type",
        [
            ("engineer", "implement_feature"),
            ("engineer", "refactor_code"),
            ("qa", "test_plan"),
        ],
    )
    def test_all_responses_have_structure(
        self,
        mock_generator: MockResponseGenerator,
        agent_type: str,
        task_type: str,
    ):
        """Test that all response types have proper structure."""
        response = mock_generator.generate_compliant_response(
            agent_type=agent_type,
            task_type=task_type,
        )

        # Check for markdown headers
        assert re.search(r"^##+ .+", response.content, re.MULTILINE), (
            f"{agent_type}/{task_type} missing markdown headers"
        )


# Example 5: Test with Fixtures
class TestWithCustomFixture:
    """Example of creating and using custom fixtures."""

    @pytest.fixture
    def sample_engineer_response(self) -> str:
        """Fixture providing sample engineer response."""
        return """
## Implementation: API Endpoint

### Code

```typescript
interface CreateUserRequest {
  email: string;
  name: string;
}

async function createUser(
  req: CreateUserRequest
): Promise<User> {
  try {
    const user = await userRepository.create(req);
    return user;
  } catch (error) {
    logger.error('User creation failed', error);
    throw new ValidationError('Invalid user data');
  }
}
```

### Tests
- Unit tests for validation logic
- Integration tests for database
"""

    def test_with_fixture(self, sample_engineer_response: str):
        """Test using custom fixture."""
        test_case = LLMTestCase(
            input="Create user endpoint",
            actual_output=sample_engineer_response,
        )

        metric = CodeQualityMetric(threshold=0.75)
        assert_test(test_case, [metric])


# Run this file directly to see examples:
# pytest tests/examples/custom_test_example.py -v -s
