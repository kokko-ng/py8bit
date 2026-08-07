"""Test runner utilities for the checker."""


class TestResult:
    """Result of a single test."""

    def __init__(self, name: str, passed: bool, error: str | None = None, is_error: bool = False):
        """Initialize test result.

        Args:
            name: Test name
            passed: Whether the test passed
            error: Failure or exception message
            is_error: True when the test raised an unexpected exception
                (rather than a plain assertion failure)
        """
        self.name = name
        self.passed = passed
        self.error = error
        self.is_error = is_error

    def __repr__(self):
        """Return string representation."""
        status = "PASS" if self.passed else ("ERROR" if self.is_error else "FAIL")
        return f"TestResult({self.name}: {status})"


def run_test(name: str, test_fn) -> TestResult:
    """Run a single test function and return the result."""
    try:
        test_fn()
        return TestResult(name, True)
    except AssertionError as e:
        return TestResult(name, False, str(e) if str(e) else "Assertion failed")
    except Exception as e:
        return TestResult(name, False, f"{type(e).__name__}: {e}", is_error=True)


def run_tests(test_cases: dict, exercise: str | None = None) -> tuple:
    """Run a set of test cases and return (passed, failed, errors, results).

    Args:
        test_cases: Dict mapping test names to test functions
        exercise: Optional filter to run only tests containing this string

    Returns:
        Tuple of (passed_count, failed_count, error_count, results_list)
    """
    results = []
    passed = 0
    failed = 0
    errors = 0

    for name, test_fn in test_cases.items():
        # Filter by exercise name if specified
        if exercise and exercise.lower() not in name.lower():
            continue

        result = run_test(name, test_fn)
        results.append(result)

        if result.passed:
            passed += 1
        elif result.is_error:
            errors += 1
        else:
            failed += 1

    return passed, failed, errors, results


def display_results(
    component: str, exercise: str | None, passed: int, failed: int, errors: int, verbose: bool, results: list
):
    """Display test results in a user-friendly format."""
    title = f"Testing: {component}"
    if exercise:
        title += f" ({exercise})"

    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    if passed == 0 and failed == 0 and errors == 0:
        print("\nNo tests found matching the criteria.")
        return

    if failed == 0 and errors == 0:
        print(f"\nAll {passed} test(s) PASSED!")
        print("Great work! Your implementation is correct.")
        return

    print(f"\n{failed + errors} test(s) FAILED, {passed} test(s) passed")
    print("\n" + "-" * 50)
    print("FAILED TESTS:")
    print("-" * 50)
    for result in results:
        if result.passed:
            continue
        print(f"\n  TEST: {result.name}")
        if result.error:
            print(f"  {'RAISED' if result.is_error else 'ERROR'}: {result.error}")
        else:
            print("  ERROR: (no error message)")
    print("\n" + "-" * 50)

    if errors > 0:
        print("\nSome tests raised exceptions (marked RAISED above).")
        print("A TypeError or AttributeError about None usually means a function")
        print("it depends on isn't implemented yet or returns the wrong type.")
    if verbose:
        print("\nHints:")
        print("- Double-check your logic against the truth table or spec")
        print("- Make sure you're using the correct bit representation (0 and 1, LSB at index 0)")
        print("- Verify input/output types match the specification")
