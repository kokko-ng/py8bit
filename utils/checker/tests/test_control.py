"""Test cases for control unit.

The control unit uses a single-cycle design: ``generate_signals`` maps a
decoded instruction (plus the current flags) directly to the control signals
needed to execute it. The four-phase state machine (``next_state``) is a
conceptual model of how multi-cycle CPUs sequence their work.
"""

from ..helpers import assert_eq, assert_isinstance, assert_not_none
from ..runner import TestCases


def get_tests() -> TestCases:
    """Return all test cases for control unit."""
    from computer.control import ControlUnit  # noqa: F401  (fail fast on import errors)

    return {
        # Initial state
        "ControlUnit_initial_state": lambda: _test_control_initial(),
        # Per-instruction signal generation (single-cycle semantics)
        "ControlUnit_signals_ADD": lambda: _test_alu_signals("ADD", [0, 0, 0, 0]),
        "ControlUnit_signals_SUB": lambda: _test_alu_signals("SUB", [1, 0, 0, 0]),
        "ControlUnit_signals_AND": lambda: _test_alu_signals("AND", [0, 1, 0, 0]),
        "ControlUnit_signals_XOR": lambda: _test_alu_signals("XOR", [0, 0, 1, 0]),
        "ControlUnit_signals_LOAD": lambda: _test_load_signals(),
        "ControlUnit_signals_STORE": lambda: _test_store_signals(),
        "ControlUnit_signals_MOV": lambda: _test_mov_signals(),
        "ControlUnit_signals_JMP": lambda: _test_jmp_signals(),
        "ControlUnit_signals_JZ_taken": lambda: _test_cond_jump("JZ", z_flag=1, expect_jump=True),
        "ControlUnit_signals_JZ_not_taken": lambda: _test_cond_jump("JZ", z_flag=0, expect_jump=False),
        "ControlUnit_signals_JNZ_taken": lambda: _test_cond_jump("JNZ", z_flag=0, expect_jump=True),
        "ControlUnit_signals_JNZ_not_taken": lambda: _test_cond_jump("JNZ", z_flag=1, expect_jump=False),
        "ControlUnit_signals_NOP_quiet": lambda: _test_quiet_signals("NOP"),
        "ControlUnit_signals_HALT_quiet": lambda: _test_quiet_signals("HALT"),
        # Conceptual state machine
        "ControlUnit_next_state": lambda: _test_next_state(),
    }


def _decoded(opname, rd=0, rs1=1, rs2_imm=2):
    """Build a decoded-instruction dict like InstructionDecoder produces."""
    from computer.isa import OPCODES

    return {"opcode": OPCODES[opname], "opcode_name": opname, "rd": rd, "rs1": rs1, "rs2_imm": rs2_imm}


def _signals_for(opname, flags=None, **kwargs):
    """Run generate_signals for one instruction and validate the return type."""
    from computer.clock import ControlSignals
    from computer.control import ControlUnit

    cu = ControlUnit()
    result = cu.generate_signals(_decoded(opname, **kwargs), flags or {"Z": 0, "C": 0, "N": 0, "V": 0})
    assert_not_none(result, "ControlUnit.generate_signals() returned None - implement the method")
    assert_isinstance(result, ControlSignals, "generate_signals() should return a ControlSignals object")
    return result


def _test_control_initial():
    """Test control unit initial state."""
    from computer.control import ControlUnit

    cu = ControlUnit()
    assert_eq(cu.state, ControlUnit.FETCH, "A fresh ControlUnit should start in the FETCH state")


def _test_alu_signals(opname, expected_alu_op):
    """ALU instructions must select the right ALU operation and write the result."""
    signals = _signals_for(opname)
    assert_eq(signals.reg_write, 1, f"{opname} must assert reg_write to store the ALU result")
    assert_eq(signals.alu_op, expected_alu_op, f"{opname} must select the matching ALU operation (LSB-first bits)")
    assert_eq(signals.mem_write, 0, f"{opname} must not write memory")
    assert_eq(signals.pc_load, 0, f"{opname} must not load the PC")


def _test_load_signals():
    """LOAD reads memory into a register."""
    signals = _signals_for("LOAD", rd=1, rs2_imm=0x10)
    assert_eq(signals.mem_read, 1, "LOAD must assert mem_read")
    assert_eq(signals.mem_to_reg, 1, "LOAD must route memory data to the register file (mem_to_reg)")
    assert_eq(signals.reg_write, 1, "LOAD must assert reg_write")
    assert_eq(signals.mem_write, 0, "LOAD must not write memory")


def _test_store_signals():
    """STORE writes a register to memory."""
    signals = _signals_for("STORE", rd=1, rs2_imm=0x20)
    assert_eq(signals.mem_write, 1, "STORE must assert mem_write")
    assert_eq(signals.reg_write, 0, "STORE must not write the register file")


def _test_mov_signals():
    """MOV copies between registers."""
    signals = _signals_for("MOV", rd=1, rs1=2)
    assert_eq(signals.reg_write, 1, "MOV must assert reg_write")
    assert_eq(signals.mem_write, 0, "MOV must not write memory")
    assert_eq(signals.mem_read, 0, "MOV must not read memory")


def _test_jmp_signals():
    """JMP unconditionally loads the PC."""
    signals = _signals_for("JMP", rs2_imm=0x0C)
    assert_eq(signals.pc_load, 1, "JMP must assert pc_load")
    assert_eq(signals.reg_write, 0, "JMP must not write the register file")


def _test_cond_jump(opname, z_flag, expect_jump):
    """JZ/JNZ load the PC only when the Zero flag says so."""
    flags = {"Z": z_flag, "C": 0, "N": 0, "V": 0}
    signals = _signals_for(opname, flags=flags, rs2_imm=0x0C)
    expected = 1 if expect_jump else 0
    assert_eq(
        signals.pc_load,
        expected,
        f"{opname} with Z={z_flag} must {'take' if expect_jump else 'not take'} the jump (pc_load={expected})",
    )


def _test_quiet_signals(opname):
    """NOP and HALT assert no datapath signals."""
    signals = _signals_for(opname)
    assert_eq(signals.reg_write, 0, f"{opname} must not write registers")
    assert_eq(signals.mem_write, 0, f"{opname} must not write memory")
    assert_eq(signals.mem_read, 0, f"{opname} must not read memory")
    assert_eq(signals.pc_load, 0, f"{opname} must not load the PC")


def _test_next_state():
    """Test the conceptual four-phase state machine."""
    from computer.control import ControlUnit

    cu = ControlUnit()
    assert_eq(cu.state, ControlUnit.FETCH)
    assert_eq(cu.next_state(), ControlUnit.DECODE, "FETCH should advance to DECODE")
    assert_eq(cu.next_state(), ControlUnit.EXECUTE, "DECODE should advance to EXECUTE")
    assert_eq(cu.next_state(), ControlUnit.WRITEBACK, "EXECUTE should advance to WRITEBACK")
    assert_eq(cu.next_state(), ControlUnit.FETCH, "WRITEBACK should wrap around to FETCH")
