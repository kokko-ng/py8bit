"""Test cases for control unit."""

from ..helpers import assert_true, assert_eq, assert_not_none


def get_tests() -> dict:
    """Return all test cases for control unit."""
    from computer.control import ControlUnit

    return {
        # ControlUnit creation
        "ControlUnit_create": lambda: assert_true(ControlUnit() is not None),
        # Control signals
        "ControlUnit_initial_state": lambda: _test_control_initial(),
        "ControlUnit_generate_signals": lambda: _test_generate_signals(),
        "ControlUnit_next_state": lambda: _test_next_state(),
    }


def _test_control_initial():
    """Test control unit initial state."""
    from computer.control import ControlUnit

    cu = ControlUnit()
    assert_eq(cu.state, ControlUnit.FETCH)


def _test_generate_signals():
    """Test control unit generates control signals."""
    from computer.control import ControlUnit

    cu = ControlUnit()
    decoded = {"opcode": 0, "rd": 0, "rs1": 0, "rs2": 0}
    flags = {"Z": 0, "C": 0, "N": 0, "V": 0}
    result = cu.generate_signals(decoded, flags)
    assert_not_none(result, "ControlUnit.generate_signals() returned None - implement the method")


def _test_next_state():
    """Test control unit state machine."""
    from computer.control import ControlUnit

    cu = ControlUnit()
    assert_eq(cu.state, ControlUnit.FETCH)
    result = cu.next_state()
    assert_not_none(result, "ControlUnit.next_state() returned None - implement the method")
