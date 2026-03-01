"""Tests for agent role boundary enforcement."""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from tests.fixtures.mock_responses import MockResponseGenerator
from tests.metrics.role_boundary import HandoffComplianceMetric, RoleBoundaryMetric


@pytest.mark.role_boundary
class TestEngineerRoleBoundaries:
    """Test engineer agents stay within role boundaries."""

    def test_engineer_stays_in_role(self, mock_generator: MockResponseGenerator):
        """Test that engineer response contains engineering activities."""
        response = mock_generator.generate_compliant_response(
            agent_type="engineer", task_type="implement_feature"
        )

        test_case = LLMTestCase(
            input="Implement user authentication",
            actual_output=response.content,
        )

        metric = RoleBoundaryMetric(agent_type="engineer", threshold=0.9)
        assert_test(test_case, [metric])

    def test_engineer_does_not_deploy(self):
        """Test that engineer does not cross into ops territory."""
        # Engineer trying to deploy
        response_content = """
## Deployment Complete

I've deployed the changes to production using:

```bash
kubectl apply -f deployment.yaml
docker push myapp:latest
```

The app is now live in production.
"""

        test_case = LLMTestCase(
            input="Deploy the feature",
            actual_output=response_content,
        )

        metric = RoleBoundaryMetric(agent_type="engineer", threshold=0.9)
        try:
            assert_test(test_case, [metric])
            pytest.fail("Expected engineer deployment to fail role boundary check")
        except AssertionError:
            # Expected to fail - engineer shouldn't deploy
            pass


@pytest.mark.role_boundary
class TestQARoleBoundaries:
    """Test QA agents stay within role boundaries."""

    def test_qa_stays_in_role(self, mock_generator: MockResponseGenerator):
        """Test that QA response contains testing activities."""
        response = mock_generator.generate_compliant_response(
            agent_type="qa", task_type="bug_report"
        )

        test_case = LLMTestCase(
            input="Report login validation bug",
            actual_output=response.content,
        )

        metric = RoleBoundaryMetric(agent_type="qa", threshold=0.9)
        assert_test(test_case, [metric])

    def test_qa_does_not_implement(self):
        """Test that QA does not cross into engineer territory."""
        # QA trying to implement fix
        response_content = r"""
## Bug Fix Implementation

I've implemented the fix for the validation bug:

```typescript
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

This refactors the validation logic to be more robust.
"""

        test_case = LLMTestCase(
            input="Fix the validation bug",
            actual_output=response_content,
        )

        metric = RoleBoundaryMetric(agent_type="qa", threshold=0.9)
        try:
            assert_test(test_case, [metric])
            pytest.fail("Expected QA implementation to fail role boundary check")
        except AssertionError:
            # Expected to fail - QA shouldn't implement
            pass


@pytest.mark.role_boundary
class TestHandoffCompliance:
    """Test proper handoff format between agents."""

    def test_proper_handoff_format(self):
        """Test that proper handoffs include all required sections."""
        handoff_content = """
## Work Completed

**Accomplished:**
- Implemented JWT authentication middleware with RS256 signing
- Added type-safe token validation with TypeScript guards
- Created integration tests for auth flow (90% coverage)
- Verified all tests passing in CI

**Handing off to Ops agent for deployment.**

**Remaining Tasks:**
- Deploy to staging environment
- Run smoke tests against staging endpoints
- Verify health checks and monitoring
- Update production environment variables

**Context:**
- Authentication uses RS256 signing algorithm (more secure than HS256)
- JWT_SECRET environment variable must be set in production
- Token expiry configured for 24 hours
- All dependencies updated to latest stable versions
- Priority: High - blocking user registration feature
"""

        test_case = LLMTestCase(
            input="Complete authentication implementation",
            actual_output=handoff_content,
        )

        metric = HandoffComplianceMetric(threshold=0.8)
        assert_test(test_case, [metric])

    def test_incomplete_handoff_detected(self):
        """Test that incomplete handoffs are detected."""
        incomplete_handoff = """
## Done

I finished the auth feature. Ops can deploy it now.
"""

        test_case = LLMTestCase(
            input="Complete feature",
            actual_output=incomplete_handoff,
        )

        metric = HandoffComplianceMetric(threshold=0.8)
        metric.measure(test_case)

        # Should fail due to missing accomplished/remaining tasks
        assert not metric.is_successful(), (
            f"Expected incomplete handoff to fail, got score: {metric.score}"
        )

    def test_non_handoff_scenario_passes(self):
        """Test that non-handoff responses don't trigger handoff checks."""
        regular_response = """
## Implementation Details

Here's the authentication middleware:

```typescript
const authMiddleware = (req, res, next) => {
  // Token validation logic
};
```
"""

        test_case = LLMTestCase(
            input="Show auth implementation",
            actual_output=regular_response,
        )

        # Should pass because it's not a handoff scenario
        metric = HandoffComplianceMetric(threshold=0.8)
        assert_test(test_case, [metric])
