#!/usr/bin/env python3
"""Execute every notebook headlessly and report pass/fail.

Used by CI (with the reference solutions installed via
``scripts/install_solutions.py --all``) to prove that all 16 notebooks run
top to bottom against the current code. Requires nbclient, nbformat, and
ipykernel (see the ``dev`` extra in pyproject.toml).

Usage:
    python scripts/install_solutions.py --all
    python scripts/run_notebooks.py
"""

import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

REPO = Path(__file__).resolve().parent.parent
NOTEBOOKS = REPO / "notebooks"


def main() -> int:
    """Execute all notebooks; return 1 if any fails."""
    failed = []
    for path in sorted(NOTEBOOKS.glob("*.ipynb")):
        nb = nbformat.read(path, as_version=4)
        client = NotebookClient(
            nb,
            timeout=300,
            kernel_name="python3",
            resources={"metadata": {"path": str(NOTEBOOKS)}},
        )
        try:
            client.execute()
            print(f"PASS {path.name}")
        except Exception as exc:
            print(f"FAIL {path.name}: {str(exc)[:800]}")
            failed.append(path.name)

    if failed:
        print(f"\n{len(failed)} notebook(s) failed: {', '.join(failed)}")
        return 1
    print("\nAll notebooks executed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
