"""Test checker for 8-bit computer notebooks.

This module provides a `check()` function that runs inline tests for a component
and displays friendly pass/fail messages without requiring pytest.

Usage:
    from utils.checker import check, check_all

    check('gates')              # Run all gate tests
    check('gates', 'AND')       # Run only AND gate tests
    check('gates', verbose=True) # Show detailed error messages
    check_all()                 # Run all tests for all components
"""

import sys
import traceback
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from .runner import run_tests, display_results
from .tests import COMPONENT_TESTS

__all__ = ["check", "check_all", "COMPONENT_TESTS"]


def check(component_name: str, exercise: str | None = None, verbose: bool = False) -> bool:
    """Run tests for a component and display pass/fail results.

    Args:
        component_name: Name of the component to test (e.g., 'gates', 'adders')
        exercise: Optional specific exercise/function to test (e.g., 'AND', 'half_adder')
        verbose: If True, show more detailed output on failure

    Returns:
        True if all tests passed, False otherwise

    Example:
        >>> check('gates')  # Run all gate tests
        >>> check('gates', 'AND')  # Run only AND gate tests
        >>> check('adders', 'half_adder', verbose=True)
    """
    if component_name not in COMPONENT_TESTS:
        print(f"Error: Unknown component '{component_name}'")
        print(f"Available components: {', '.join(COMPONENT_TESTS.keys())}")
        return False

    try:
        test_cases = COMPONENT_TESTS[component_name]()
    except ImportError as e:
        print(f"\nError importing {component_name}: {e}")
        print("Make sure the component module exists in src/computer/")
        return False
    except Exception as e:
        print(f"\nError loading tests for {component_name}: {e}")
        if verbose:
            traceback.print_exc()
        return False

    passed, failed, errors, results = run_tests(test_cases, exercise)
    display_results(component_name, exercise, passed, failed, errors, verbose, results)

    return failed == 0 and errors == 0


def check_all() -> bool:
    """Run all tests for the entire project.

    Returns:
        True if all tests passed, False otherwise
    """
    total_passed = 0
    total_failed = 0
    total_errors = 0
    failed_components = []

    print("\n" + "=" * 50)
    print("FULL PROJECT TEST RESULTS")
    print("=" * 50)

    for component_name, get_tests in COMPONENT_TESTS.items():
        try:
            test_cases = get_tests()
            passed, failed, errors, _ = run_tests(test_cases)
            total_passed += passed
            total_failed += failed
            total_errors += errors

            status = "PASS" if failed == 0 and errors == 0 else "FAIL"
            print(f"  {component_name}: {status} ({passed} passed, {failed} failed, {errors} errors)")

            if failed > 0 or errors > 0:
                failed_components.append(component_name)
        except Exception as e:
            print(f"  {component_name}: ERROR - {e}")
            total_errors += 1
            failed_components.append(component_name)

    print("\n" + "-" * 50)
    if total_failed == 0 and total_errors == 0:
        print(f"All {total_passed} tests passed!")
        return True
    else:
        print(f"Passed: {total_passed}")
        print(f"Failed: {total_failed}")
        print(f"Errors: {total_errors}")
        if failed_components:
            print(f"\nFailed components: {', '.join(failed_components)}")
        return False
