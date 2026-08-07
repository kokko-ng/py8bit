"""Command-line entry point for the checker.

Usage:
    python -m utils.checker                    # run all tests (exit 0/1)
    python -m utils.checker gates              # check one component
    python -m utils.checker gates AND          # check one exercise
    python -m utils.checker gates -v           # verbose output
    python -m utils.checker --progress         # per-notebook progress table
"""

import argparse
import sys

from . import COMPONENT_TESTS, check, check_all, progress


def main() -> int:
    """Run the requested checks and return a process exit code."""
    parser = argparse.ArgumentParser(prog="python -m utils.checker", description=__doc__)
    parser.add_argument("component", nargs="?", help=f"component to check ({', '.join(COMPONENT_TESTS)})")
    parser.add_argument("exercise", nargs="?", help="only run tests whose name contains this string")
    parser.add_argument("-v", "--verbose", action="store_true", help="show extra hints on failure")
    parser.add_argument("--progress", action="store_true", help="show the per-notebook progress table")
    args = parser.parse_args()

    if args.progress:
        return 0 if progress() else 1
    if args.component:
        return 0 if check(args.component, args.exercise, verbose=args.verbose) else 1
    return 0 if check_all() else 1


if __name__ == "__main__":
    sys.exit(main())
