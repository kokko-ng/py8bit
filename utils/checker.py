"""
Test checker for 8-bit computer notebooks.

This module provides a `check()` function that runs pytest tests for a component
and displays friendly pass/fail messages without revealing the actual test code.
"""

import subprocess
import sys
import re
from pathlib import Path


def check(component_name: str, exercise: str = None, verbose: bool = False) -> bool:
    """Run hidden tests for a component and display pass/fail results.

    Args:
        component_name: Name of the component to test (e.g., 'gates', 'adders')
        exercise: Optional specific exercise/function to test (e.g., 'AND', 'half_adder')
        verbose: If True, show more detailed output on failure

    Returns:
        True if all tests passed, False otherwise

    Example:
        >>> check('gates')  # Run all gate tests
        >>> check('gates', 'AND')  # Run only AND gate tests
    """
    # Find the project root (where tests/ directory is)
    project_root = _find_project_root()
    if project_root is None:
        print("Error: Could not find project root. Make sure you're in the 8bit project directory.")
        return False

    test_file = project_root / 'tests' / f'test_{component_name}.py'

    if not test_file.exists():
        print(f"Error: Test file not found for '{component_name}'")
        print(f"Expected: {test_file}")
        return False

    # Build pytest command
    cmd = [
        sys.executable, '-m', 'pytest',
        str(test_file),
        '--tb=no',  # Don't show tracebacks (hide test implementation)
        '-q',       # Quiet mode
    ]

    # If a specific exercise is requested, use -k to filter
    if exercise:
        cmd.extend(['-k', exercise])

    # Run pytest
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )

    # Parse the output
    output = result.stdout + result.stderr
    passed, failed, errors = _parse_pytest_output(output)

    # Display results
    _display_results(component_name, exercise, passed, failed, errors, verbose, output)

    return failed == 0 and errors == 0


def check_all() -> bool:
    """Run all tests for the entire project.

    Returns:
        True if all tests passed, False otherwise
    """
    project_root = _find_project_root()
    if project_root is None:
        print("Error: Could not find project root.")
        return False

    cmd = [
        sys.executable, '-m', 'pytest',
        str(project_root / 'tests'),
        '--tb=no',
        '-q',
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(project_root)
    )

    output = result.stdout + result.stderr
    passed, failed, errors = _parse_pytest_output(output)

    print("\n" + "=" * 50)
    print("FULL PROJECT TEST RESULTS")
    print("=" * 50)

    if failed == 0 and errors == 0:
        print(f"\nAll {passed} tests passed!")
        return True
    else:
        print(f"\nPassed: {passed}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")
        return False


def _find_project_root() -> Path:
    """Find the project root directory (containing pyproject.toml)."""
    current = Path.cwd()

    # Check current directory and parents
    for path in [current] + list(current.parents):
        if (path / 'pyproject.toml').exists() and (path / 'tests').exists():
            return path

    # Also check if we're in notebooks/
    if current.name == 'notebooks':
        parent = current.parent
        if (parent / 'pyproject.toml').exists():
            return parent

    return None


def _parse_pytest_output(output: str) -> tuple:
    """Parse pytest output to extract pass/fail counts.

    Returns:
        Tuple of (passed, failed, errors)
    """
    passed = 0
    failed = 0
    errors = 0

    # Look for the summary line like "5 passed" or "3 passed, 2 failed"
    summary_match = re.search(r'(\d+) passed', output)
    if summary_match:
        passed = int(summary_match.group(1))

    failed_match = re.search(r'(\d+) failed', output)
    if failed_match:
        failed = int(failed_match.group(1))

    error_match = re.search(r'(\d+) error', output)
    if error_match:
        errors = int(error_match.group(1))

    return passed, failed, errors


def _display_results(component: str, exercise: str, passed: int, failed: int,
                     errors: int, verbose: bool, raw_output: str):
    """Display test results in a user-friendly format."""
    title = f"Testing: {component}"
    if exercise:
        title += f" ({exercise})"

    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    if errors > 0:
        print(f"\nERROR: {errors} test(s) could not run")
        print("This usually means there's a syntax error or import issue.")
        if verbose:
            # Extract error messages without revealing test code
            _show_error_hints(raw_output)
        else:
            print("Run with verbose=True for more details.")
        return

    if failed == 0:
        print(f"\nAll {passed} test(s) PASSED!")
        print("Great work! Your implementation is correct.")
    else:
        print(f"\n{failed} test(s) FAILED, {passed} test(s) passed")
        print("\nHints:")
        print("- Double-check your logic against the truth table")
        print("- Make sure you're using the correct bit representation (0 and 1)")
        print("- Verify input/output types match the specification")

        if verbose:
            _show_failure_hints(raw_output)


def _show_error_hints(output: str):
    """Extract and show helpful error hints without revealing test code."""
    # Look for common error patterns
    if 'ImportError' in output or 'ModuleNotFoundError' in output:
        print("\nImport Error Detected:")
        print("- Make sure the component module exists in src/computer/")
        print("- Check that all required functions/classes are defined")

    if 'SyntaxError' in output:
        print("\nSyntax Error Detected:")
        print("- Check your code for typos or missing colons/parentheses")

    if 'NameError' in output:
        print("\nName Error Detected:")
        print("- A variable or function is being used before it's defined")

    if 'TypeError' in output:
        print("\nType Error Detected:")
        print("- Check that your function accepts the right number of arguments")
        print("- Make sure you're returning the correct type")


def _show_failure_hints(output: str):
    """Show hints for failed tests without revealing test implementation."""
    # Extract failed test names
    failed_tests = re.findall(r'FAILED.*?test_(\w+)', output)

    if failed_tests:
        print("\nFailed tests:")
        for test in set(failed_tests):
            print(f"  - {test}")
