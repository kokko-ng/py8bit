#!/usr/bin/env python3
"""Copy reference solutions into src/computer/ (the working directory).

Use this to unblock yourself on a single module ("I'm stuck on the ALU but
want to keep going with registers") or to set up a fully-solved tree:

    python scripts/install_solutions.py alu          # install one solution
    python scripts/install_solutions.py alu memory   # install several
    python scripts/install_solutions.py --all        # install everything

This OVERWRITES your implementation of those modules. Your own code is
recoverable only if you committed it (git checkout -- src/computer restores
the last committed state).

Solution files import from the ``solutions`` package; this script rewrites
those imports to ``computer`` so the installed copies work in place.
"""

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOLUTIONS = REPO / "solutions"
STUBS = REPO / "src" / "computer"


def available_modules() -> list:
    """List installable module names."""
    return sorted(p.stem for p in SOLUTIONS.glob("*.py") if p.stem != "__init__")


def install(module: str) -> None:
    """Install one solution module into src/computer/."""
    source = (SOLUTIONS / f"{module}.py").read_text()
    source = source.replace("from solutions.", "from computer.")
    source = source.replace("from solutions import", "from computer import")
    (STUBS / f"{module}.py").write_text(source)
    print(f"installed solutions/{module}.py -> src/computer/{module}.py")


def main() -> int:
    """Install the requested solution modules."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("modules", nargs="*", help="module names to install (e.g. gates alu)")
    parser.add_argument("--all", action="store_true", help="install every solution module")
    args = parser.parse_args()

    modules = available_modules()
    if args.all:
        selected = modules
    elif args.modules:
        unknown = [m for m in args.modules if m not in modules]
        if unknown:
            print(f"error: unknown module(s): {', '.join(unknown)}")
            print(f"available: {', '.join(modules)}")
            return 1
        selected = args.modules
    else:
        parser.print_usage()
        print(f"available: {', '.join(modules)}")
        return 1

    for module in selected:
        install(module)
    print(f"\n{len(selected)} module(s) installed. To restore your own code: git checkout -- src/computer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
