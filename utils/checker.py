"""
Test checker for 8-bit computer notebooks.

This is a backward-compatible wrapper that re-exports from the checker package.
For new code, import directly from utils.checker:

    from utils.checker import check, check_all
"""

from utils.checker import check, check_all, COMPONENT_TESTS

__all__ = ['check', 'check_all', 'COMPONENT_TESTS']
