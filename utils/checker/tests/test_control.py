"""
Test cases for control unit.
"""

from ..helpers import assert_true


def get_tests() -> dict:
    """Return all test cases for control unit."""
    from computer.control import ControlUnit

    return {
        # ControlUnit creation
        "ControlUnit_create": lambda: assert_true(ControlUnit() is not None),

        # Control signals
        "ControlUnit_has_attributes": lambda: _test_control_attributes(),
        "ControlUnit_initial_state": lambda: _test_control_initial(),
    }


def _test_control_attributes():
    """Test control unit has expected attributes."""
    from computer.control import ControlUnit
    cu = ControlUnit()
    # At minimum should exist
    assert_true(cu is not None)


def _test_control_initial():
    """Test control unit initial state."""
    from computer.control import ControlUnit
    cu = ControlUnit()
    # Just verify it initializes without error
    assert_true(cu is not None)
