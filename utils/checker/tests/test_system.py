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
    # Test basic ADD: preload values into registers via memory operations
    # Since this ISA doesn't have immediate MOV, use LOAD from memory
    # Program layout:
    #   0-1: LOAD R0, 100  (load value 5 from address 100)
    #   2-3: LOAD R1, 101  (load value 3 from address 101)
    #   4-5: ADD R2, R0, R1
    #   6-7: HALT
    # Data:
    #   100: 5
    #   101: 3
    program = [
        # LOAD R0, 100 (opcode=1, rd=0, addr=100) -> 0x1064 -> little-endian: [0x64, 0x10]
        0x64, 0x10,
        # LOAD R1, 101 (opcode=1, rd=1, addr=101) -> 0x1165 -> little-endian: [0x65, 0x11]
        0x65, 0x11,
        # ADD R2, R0, R1 (opcode=4, rd=2, rs1=0, rs2=1) -> 0x4201 -> little-endian: [0x01, 0x42]
        0x01, 0x42,
        # HALT (opcode=15) -> 0xF000 -> little-endian: [0x00, 0xF0]
        0x00, 0xF0,
    ]
    # Pad to address 100 and add data
    while len(program) < 100:
        program.append(0x00)
    program.append(5)   # address 100: value 5
    program.append(3)   # address 101: value 3

    comp.load_program(program)
    comp.run(max_cycles=100)
    # R2 should contain 8
    r2_addr = [0, 1, 0]  # Register 2
    r2_val = comp.cpu.datapath.reg_file.read(r2_addr)
    assert_eq(bits_to_int(r2_val), 8, "ADD program should compute 5 + 3 = 8 in R2")


def _test_system_mov_program():
    """Test system handles LOAD instruction."""
    from computer.system import Computer

    comp = Computer()
    # Program: LOAD R0, 100; HALT
    # (MOV is register-to-register only, so we use LOAD to test loading values)
    program = [
        # LOAD R0, 100 (opcode=1, rd=0, addr=100) -> 0x1064 -> little-endian: [0x64, 0x10]
        0x64, 0x10,
        # HALT (opcode=15) -> 0xF000 -> little-endian: [0x00, 0xF0]
        0x00, 0xF0,
    ]
    # Pad to address 100 and add data
    while len(program) < 100:
        program.append(0x00)
    program.append(42)  # address 100: value 42

    comp.load_program(program)
    comp.run(max_cycles=100)
    # R0 should contain 42
    r0_addr = [0, 0, 0]
    r0_val = comp.cpu.datapath.reg_file.read(r0_addr)
    assert_eq(bits_to_int(r0_val), 42, "LOAD program should put 42 in R0")


def _test_system_memory_program():
    """Test system handles STORE and LOAD."""
    from computer.system import Computer

    comp = Computer()
    # Program: LOAD R0, 200; STORE R0, 100; LOAD R1, 100; HALT
    # Store a value from one location to another, then load it back
    program = [
        # LOAD R0, 200 (opcode=1, rd=0, addr=200) -> 0x10C8 -> little-endian: [0xC8, 0x10]
        0xC8, 0x10,
        # STORE R0, 100 (opcode=2, rd=0, addr=100) -> 0x2064 -> little-endian: [0x64, 0x20]
        0x64, 0x20,
        # LOAD R1, 100 (opcode=1, rd=1, addr=100) -> 0x1164 -> little-endian: [0x64, 0x11]
        0x64, 0x11,
        # HALT (opcode=15) -> 0xF000 -> little-endian: [0x00, 0xF0]
        0x00, 0xF0,
    ]
    # Pad to address 200 and add data
    while len(program) < 200:
        program.append(0x00)
    program.append(99)  # address 200: value 99

    comp.load_program(program)
    comp.run(max_cycles=100)
    # R1 should contain 99 (loaded from memory address 100, which got 99 from address 200)
    r1_addr = [1, 0, 0]
    r1_val = comp.cpu.datapath.reg_file.read(r1_addr)
    assert_eq(bits_to_int(r1_val), 99, "LOAD should retrieve 99 from memory")
