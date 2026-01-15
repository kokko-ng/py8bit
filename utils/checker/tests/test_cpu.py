"""Test cases for CPU."""

from ..helpers import assert_eq, assert_true, assert_not_none


def get_tests() -> dict:
    """Return all test cases for CPU."""
    from computer.cpu import CPU

    return {
        # CPU creation
        "CPU_create": lambda: assert_true(CPU() is not None),
        # CPU methods
        "CPU_has_step": lambda: assert_true(hasattr(CPU(), "step")),
        "CPU_has_run": lambda: assert_true(hasattr(CPU(), "run")),
        # CPU state
        "CPU_initial_state": lambda: _test_cpu_initial(),
        # CPU fetch
        "CPU_fetch_returns_instruction": lambda: _test_cpu_fetch(),
        # CPU decode
        "CPU_decode_returns_dict": lambda: _test_cpu_decode(),
        # CPU execute
        "CPU_execute_works": lambda: _test_cpu_execute(),
        # CPU step
        "CPU_step_works": lambda: _test_cpu_step(),
        # CPU run with halt
        "CPU_run_halts": lambda: _test_cpu_run_halts(),
    }


def _test_cpu_initial():
    """Test CPU initial state."""
    from computer.cpu import CPU

    cpu = CPU()
    assert_eq(cpu.halted, False)


def _test_cpu_fetch():
    """Test CPU fetch returns instruction."""
    from computer.cpu import CPU

    cpu = CPU()
    result = cpu.fetch()
    assert_not_none(result, "CPU.fetch() returned None - implement the method")


def _test_cpu_decode():
    """Test CPU decode returns decoded instruction."""
    from computer.cpu import CPU

    cpu = CPU()
    instruction = [0] * 16  # NOP
    result = cpu.decode(instruction)
    assert_not_none(result, "CPU.decode() returned None - implement the method")
    assert_true(isinstance(result, dict), "CPU.decode() should return a dict")


def _test_cpu_execute():
    """Test CPU execute works."""
    from computer.cpu import CPU

    cpu = CPU()
    decoded = {"opcode": 0, "rd": 0, "rs1": 0, "rs2": 0, "immediate": 0, "address": 0}
    # Execute should not raise an error and should handle the instruction
    cpu.execute(decoded)
    # If we get here without exception, the method is implemented
    assert_true(True)


def _test_cpu_step():
    """Test CPU step executes one instruction cycle."""
    from computer.cpu import CPU

    cpu = CPU()
    # Step should perform fetch-decode-execute
    cpu.step()
    # Verify PC was incremented (should be 2 after one instruction)
    from ..helpers import bits_to_int

    pc_val = bits_to_int(cpu.datapath.get_pc())
    assert_eq(pc_val, 2, "CPU.step() should increment PC by 2 (instruction width)")


def _test_cpu_run_halts():
    """Test CPU run method stops on HALT instruction."""
    from computer.cpu import CPU
    from ..helpers import int_to_bits

    cpu = CPU()
    # Load HALT instruction (opcode 1111 = 15) at address 0
    halt_instr = int_to_bits(0xF000, 16)  # HALT opcode in upper 4 bits
    cpu.datapath.memory.write(int_to_bits(0, 8), halt_instr[:8], 1)
    cpu.datapath.memory.write(int_to_bits(1, 8), halt_instr[8:], 1)
    cpu.run(max_cycles=10)
    assert_eq(cpu.halted, True, "CPU should be halted after HALT instruction")
