"""Test cases for CPU."""

from ..helpers import assert_eq, assert_true, assert_not_none


def get_tests() -> dict:
    """Return all test cases for CPU."""
    from computer.cpu import CPU

    return {
        # CPU initial state
        "CPU_initial_state": lambda: _test_cpu_initial(),
        # CPU fetch
        "CPU_fetch_returns_instruction": lambda: _test_cpu_fetch(),
        # CPU decode
        "CPU_decode_returns_dict": lambda: _test_cpu_decode(),
        # CPU execute
        "CPU_execute_runs": lambda: _test_cpu_execute(),
        # CPU step
        "CPU_step_works": lambda: _test_cpu_step(),
        # CPU run with halt
        "CPU_run_halts": lambda: _test_cpu_run_halts(),
        # CPU actually computes
        "CPU_add_computes_result": lambda: _test_cpu_add_computes(),
        "CPU_conditional_jump_loops": lambda: _test_cpu_jnz_loops(),
    }


def _load_program(cpu, instructions):
    """Write encoded 16-bit instructions into memory starting at address 0."""
    from ..helpers import int_to_bits

    for i, instr in enumerate(instructions):
        addr = i * 2
        cpu.datapath.memory.write(int_to_bits(addr, 8), instr[:8], 1)
        cpu.datapath.memory.write(int_to_bits(addr + 1, 8), instr[8:], 1)


def _set_register(cpu, reg, value):
    """Write an integer value into register R<reg>."""
    from ..helpers import int_to_bits

    cpu.datapath.reg_file.write(int_to_bits(reg, 3), int_to_bits(value, 8), 1, 1)


def _read_register(cpu, reg):
    """Read register R<reg> as an integer."""
    from ..helpers import bits_to_int, int_to_bits

    return bits_to_int(cpu.datapath.reg_file.read(int_to_bits(reg, 3)))


def _test_cpu_add_computes():
    """An ADD program must actually compute: R0 = R1 + R2.

    This is the end-to-end sanity check for the whole control/datapath
    integration - a CPU whose control unit asserts the wrong signals will
    halt cleanly but leave R0 unchanged.
    """
    from computer.cpu import CPU
    from computer.isa import encode_instruction

    cpu = CPU()
    _set_register(cpu, 1, 5)
    _set_register(cpu, 2, 3)
    _load_program(
        cpu,
        [
            encode_instruction("ADD", rd=0, rs1=1, rs2_imm=2),
            encode_instruction("HALT"),
        ],
    )
    cpu.run(max_cycles=10)
    assert_eq(cpu.halted, True, "CPU should halt after the HALT instruction")
    assert_eq(_read_register(cpu, 0), 8, "ADD R0, R1, R2 with R1=5, R2=3 must leave R0 = 8")


def _test_cpu_jnz_loops():
    """A JNZ countdown loop must execute the loop body the right number of times."""
    from computer.cpu import CPU
    from computer.isa import encode_instruction

    cpu = CPU()
    _set_register(cpu, 0, 3)  # counter
    _set_register(cpu, 1, 1)  # decrement constant
    _load_program(
        cpu,
        [
            encode_instruction("SUB", rd=0, rs1=0, rs2_imm=1),  # address 0: R0 -= R1
            encode_instruction("JNZ", rs2_imm=0),  # address 2: loop while R0 != 0
            encode_instruction("HALT"),  # address 4
        ],
    )
    cpu.run(max_cycles=50)
    assert_eq(cpu.halted, True, "CPU should halt once the counter reaches zero")
    assert_eq(_read_register(cpu, 0), 0, "The countdown loop must decrement R0 to exactly 0")


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
    """Test CPU execute handles a NOP without touching state, and HALT halts."""
    from computer.clock import ControlSignals
    from computer.cpu import CPU

    cpu = CPU()
    decoded = {"opcode": 0, "opcode_name": "NOP", "rd": 0, "rs1": 0, "rs2_imm": 0}
    cpu.execute(decoded, ControlSignals())  # NOP with quiet signals must not raise
    assert_eq(cpu.halted, False, "Executing NOP must not halt the CPU")
    decoded_halt = {"opcode": 15, "opcode_name": "HALT", "rd": 0, "rs1": 0, "rs2_imm": 0}
    cpu.execute(decoded_halt, ControlSignals())
    assert_eq(cpu.halted, True, "Executing HALT must set cpu.halted")


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
