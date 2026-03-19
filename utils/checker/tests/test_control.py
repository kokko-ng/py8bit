"""Test cases for control unit."""

from ..helpers import assert_eq, assert_not_none


def get_tests() -> dict:
    """Return all test cases for control unit."""
    from computer.control import ControlUnit

    return {
        # Control signals
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
    from computer.clock import ControlSignals
    from computer.isa import OPCODES

    cu = ControlUnit()
    decoded = {"opcode": OPCODES["ADD"], "opcode_name": "ADD", "rd": 0, "rs1": 1, "rs2_imm": 2}
    flags = {"Z": 0, "C": 0, "N": 0, "V": 0}
    result = cu.generate_signals(decoded, flags)
    assert_not_none(result, "ControlUnit.generate_signals() returned None - implement the method")
    assert_eq(isinstance(result, ControlSignals), True, "generate_signals() should return a ControlSignals object")
    assert_eq(result.mem_read, 1, "FETCH should assert mem_read")
    assert_eq(result.ir_load, 1, "FETCH should assert ir_load")
    assert_eq(result.pc_inc, 0, "FETCH should not increment the PC yet")


def _test_next_state():
    """Test control unit state machine."""
    from computer.control import ControlUnit

    cu = ControlUnit()
    assert_eq(cu.state, ControlUnit.FETCH)
    assert_eq(cu.next_state(), ControlUnit.DECODE)
    assert_eq(cu.next_state(), ControlUnit.EXECUTE)
    assert_eq(cu.next_state(), ControlUnit.WRITEBACK)
    assert_eq(cu.next_state(), ControlUnit.FETCH)
