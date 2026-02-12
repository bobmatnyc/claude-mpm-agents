"""
Deepeval synthetic tests for Visual Basic Engineer agent.
Tests behavioral consistency and VB coding skills without actual VB environment.
"""

import pytest
from deepeval import assert_test
from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


# Test 1: Type Safety Knowledge
def test_vb_engineer_understands_option_strict():
    """VB engineer should enforce Option Strict On for type safety"""
    test_case = LLMTestCase(
        input="How should I handle type conversions in VB.NET?",
        expected_output="Use Option Strict On and explicit type conversions with Integer.Parse() or CInt()",
        actual_output="Always enable Option Strict On to enforce type safety. Use explicit conversion functions like Integer.Parse(), Double.Parse(), or CStr() instead of implicit conversions.",
        context=["VB.NET best practices", "Type safety"],
    )

    relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [relevancy_metric])


# Test 2: Error Handling Pattern
def test_vb_engineer_recommends_try_catch():
    """VB engineer should prefer Try/Catch over On Error for VB.NET"""
    test_case = LLMTestCase(
        input="What's the best error handling approach for VB.NET?",
        expected_output="Use Try/Catch/Finally blocks with specific exception types, not On Error",
        actual_output="In VB.NET, use Try/Catch/Finally blocks with specific exception types (IOException, SqlException) rather than catching generic Exception. For VB6 legacy code, use On Error GoTo, but migrate to Try/Catch when possible.",
        context=["VB.NET error handling", "Exception types"],
    )

    correctness_metric = GEval(
        name="Error Handling Correctness",
        criteria="Evaluate if the response correctly recommends Try/Catch for VB.NET and explains specific exception handling",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7,
    )
    assert_test(test_case, [correctness_metric])


# Test 3: SQL Injection Prevention
def test_vb_engineer_enforces_parameterized_queries():
    """VB engineer should always recommend parameterized queries"""
    test_case = LLMTestCase(
        input="How do I query a database for a user by ID in VB.NET?",
        expected_output="Use parameterized queries with SqlCommand and AddWithValue to prevent SQL injection",
        actual_output="Always use parameterized queries: cmd.Parameters.AddWithValue('@Id', userId). Never use string concatenation like 'SELECT * FROM Users WHERE Id = ' & userId which creates SQL injection vulnerabilities.",
        context=["Database security", "SQL injection prevention"],
    )

    security_metric = GEval(
        name="Security Best Practice",
        criteria="Evaluate if the response emphasizes parameterized queries and warns against string concatenation",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.8,
    )
    assert_test(test_case, [security_metric])


# Test 4: Resource Cleanup Pattern
def test_vb_engineer_uses_using_statement():
    """VB engineer should recommend Using statement for IDisposable"""
    test_case = LLMTestCase(
        input="How should I manage database connections in VB.NET?",
        expected_output="Use Using statement to automatically dispose connections",
        actual_output="Always use Using statements for database connections and other IDisposable resources: 'Using conn As New SqlConnection(connString)'. This ensures proper disposal even if exceptions occur, preventing resource leaks.",
        context=["Resource management", "IDisposable pattern"],
    )

    correctness_metric = GEval(
        name="Resource Management",
        criteria="Evaluate if the response correctly recommends Using statement and explains automatic disposal benefits",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7,
    )
    assert_test(test_case, [correctness_metric])


# Test 5: COM Cleanup (VB6)
def test_vb_engineer_cleans_up_com_objects():
    """VB engineer should ensure COM object cleanup in VB6"""
    test_case = LLMTestCase(
        input="How do I use Excel automation in VB6?",
        expected_output="Create Excel object with CreateObject and release with Set xlApp = Nothing",
        actual_output="In VB6, use CreateObject('Excel.Application') for late binding. Always release COM objects with 'Set xlApp = Nothing' to prevent memory leaks. For early binding, add reference to Excel library and use proper cleanup in error handlers.",
        context=["VB6 COM", "Excel automation"],
    )

    com_cleanup_metric = GEval(
        name="COM Cleanup",
        criteria="Evaluate if the response includes proper COM object release with Set = Nothing",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7,
    )
    assert_test(test_case, [com_cleanup_metric])


# Test 6: Behavioral Consistency with Other Engineers
def test_vb_engineer_follows_testing_standards():
    """VB engineer should follow same testing principles as other language engineers"""
    test_case = LLMTestCase(
        input="How do I test my VB.NET business logic?",
        expected_output="Use unit testing framework like NUnit with Arrange-Act-Assert pattern and 80%+ coverage",
        actual_output="Use NUnit or xUnit for unit testing. Follow Arrange-Act-Assert pattern: set up test data, execute the method, verify results. Aim for 80%+ code coverage. Mock external dependencies with interfaces. Test edge cases and error conditions.",
        context=["Unit testing", "Test coverage"],
    )

    testing_metric = GEval(
        name="Testing Standards",
        criteria="Evaluate if testing approach matches standard engineering practices with AAA pattern and coverage targets",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.7,
    )
    assert_test(test_case, [testing_metric])


# Test 7: Code Quality Standards
def test_vb_engineer_avoids_on_error_resume_next():
    """VB engineer should warn against On Error Resume Next abuse"""
    test_case = LLMTestCase(
        input="Should I use On Error Resume Next in VB6?",
        expected_output="Avoid On Error Resume Next as it silently hides errors; use On Error GoTo with specific error handlers",
        actual_output="Avoid 'On Error Resume Next' - it hides all errors silently, making debugging nearly impossible. Use 'On Error GoTo ErrorHandler' with specific error handling logic. Check Err.Number after critical operations. In VB.NET, migrate to Try/Catch.",
        context=["VB6 error handling", "Code quality"],
    )

    quality_metric = GEval(
        name="Code Quality Warning",
        criteria="Evaluate if the response clearly warns against On Error Resume Next and provides better alternatives",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        threshold=0.8,
    )
    assert_test(test_case, [quality_metric])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
