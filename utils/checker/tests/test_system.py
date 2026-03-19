"""Test cases for full system integration."""

from ..helpers import assert_eq, assert_not_none, int_to_bits


def get_tests() -> dict:
    """Return all test cases for system integration."""
    from computer.system import Computer

    return {
        # System execution
        "System_run_add_program": lambda: _test_system_add_program(),
        "System_run_mov_program": lambda: _test_system_mov_program(),
        "System_run_memory_program": lambda: _test_system_memory_program(),
    }


def _test_system_add_program():
    """Test system runs ADD program correctly."""
    from computer.system import Computer

    comp = Computer()
    program = [
        int_to_bits(0x1064, 16),  # LOAD R0, 100
        int_to_bits(0x1165, 16),  # LOAD R1, 101
        int_to_bits(0x4201, 16),  # ADD R2, R0, R1
        int_to_bits(0xF000, 16),  # HALT
    ]
    data = [5, 3]

    comp.load_machine_code(program)
    for offset, value in enumerate(data, start=100):
        comp.cpu.datapath.memory.write(int_to_bits(offset, 8), int_to_bits(value, 8), 1)
    state = comp.run(max_cycles=100)
    assert_not_none(state, "Computer.run() returned None")
    assert_eq(state["registers"]["R2"], 8, "ADD program should compute 5 + 3 = 8 in R2")


def _test_system_mov_program():
    """Test system handles LOAD instruction."""
    from computer.system import Computer

    comp = Computer()
    program = [
        int_to_bits(0x1064, 16),  # LOAD R0, 100
        int_to_bits(0xF000, 16),  # HALT
    ]

    comp.load_machine_code(program)
    comp.cpu.datapath.memory.write(int_to_bits(100, 8), int_to_bits(42, 8), 1)
    state = comp.run(max_cycles=100)
    assert_not_none(state, "Computer.run() returned None")
    assert_eq(state["registers"]["R0"], 42, "LOAD program should put 42 in R0")


def _test_system_memory_program():
    """Test system handles STORE and LOAD."""
    from computer.system import Computer

    comp = Computer()
    program = [
        int_to_bits(0x10C8, 16),  # LOAD R0, 200
        int_to_bits(0x2064, 16),  # STORE R0, 100
        int_to_bits(0x1164, 16),  # LOAD R1, 100
        int_to_bits(0xF000, 16),  # HALT
    ]

    comp.load_machine_code(program)
    comp.cpu.datapath.memory.write(int_to_bits(200, 8), int_to_bits(99, 8), 1)
    state = comp.run(max_cycles=100)
    assert_not_none(state, "Computer.run() returned None")
    assert_eq(state["registers"]["R1"], 99, "LOAD should retrieve 99 from memory")
