"""Test cases for full system integration."""

from ..helpers import assert_true, assert_eq, bits_to_int


def get_tests() -> dict:
    """Return all test cases for system integration."""
    from computer.system import Computer

    return {
        # System creation
        "System_create": lambda: assert_true(Computer() is not None),
        # System components
        "System_has_cpu": lambda: assert_true(hasattr(Computer(), "cpu")),
        # System execution
        "System_run_add_program": lambda: _test_system_add_program(),
        "System_run_mov_program": lambda: _test_system_mov_program(),
        "System_run_memory_program": lambda: _test_system_memory_program(),
    }


def _test_system_add_program():
    """Test system runs ADD program correctly."""
    from computer.system import Computer

    comp = Computer()
    # Program: MOV R0, 5; MOV R1, 3; ADD R2, R0, R1; HALT
    # Encoded as bytes
    program = [
        0x30,
        0x05,  # MOV R0, #5 (opcode 0011, Rd=0, imm=5)
        0x31,
        0x03,  # MOV R1, #3 (opcode 0011, Rd=1, imm=3)
        0x42,
        0x01,  # ADD R2, R0, R1 (opcode 0100, Rd=2, Rs1=0, Rs2=1)
        0xF0,
        0x00,  # HALT
    ]
    comp.load_program(program)
    comp.run(max_cycles=100)
    # R2 should contain 8
    r2_addr = [0, 1, 0]  # Register 2
    r2_val = comp.cpu.datapath.reg_file.read(r2_addr)
    assert_eq(bits_to_int(r2_val), 8, "ADD program should compute 5 + 3 = 8 in R2")


def _test_system_mov_program():
    """Test system handles MOV instruction."""
    from computer.system import Computer

    comp = Computer()
    # Program: MOV R0, 42; HALT
    program = [
        0x30,
        0x2A,  # MOV R0, #42
        0xF0,
        0x00,  # HALT
    ]
    comp.load_program(program)
    comp.run(max_cycles=100)
    # R0 should contain 42
    r0_addr = [0, 0, 0]
    r0_val = comp.cpu.datapath.reg_file.read(r0_addr)
    assert_eq(bits_to_int(r0_val), 42, "MOV program should put 42 in R0")


def _test_system_memory_program():
    """Test system handles STORE and LOAD."""
    from computer.system import Computer

    comp = Computer()
    # Program: MOV R0, 99; STORE R0, 100; MOV R0, 0; LOAD R1, 100; HALT
    program = [
        0x30,
        0x63,  # MOV R0, #99
        0x20,
        0x64,  # STORE R0, 100
        0x30,
        0x00,  # MOV R0, #0 (clear R0)
        0x11,
        0x64,  # LOAD R1, 100
        0xF0,
        0x00,  # HALT
    ]
    comp.load_program(program)
    comp.run(max_cycles=100)
    # R1 should contain 99 (loaded from memory address 100)
    r1_addr = [1, 0, 0]
    r1_val = comp.cpu.datapath.reg_file.read(r1_addr)
    assert_eq(bits_to_int(r1_val), 99, "LOAD should retrieve 99 from memory")
