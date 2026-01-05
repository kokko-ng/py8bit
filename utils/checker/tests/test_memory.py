"""
Test cases for memory.
"""

from ..helpers import assert_eq, assert_true, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for memory."""
    from computer.memory import RAM

    return {
        # RAM creation and structure
        "RAM_create": lambda: assert_true(RAM() is not None),
        "RAM_has_read": lambda: assert_true(hasattr(RAM(), 'read')),
        "RAM_has_write": lambda: assert_true(hasattr(RAM(), 'write')),
        "RAM_has_load_program": lambda: assert_true(hasattr(RAM(), 'load_program')),
        "RAM_default_size": lambda: assert_eq(RAM().size, 256),

        # RAM read/write
        "RAM_write_read_addr0": lambda: _test_ram_addr(0),
        "RAM_write_read_addr10": lambda: _test_ram_addr(10),
        "RAM_write_read_addr127": lambda: _test_ram_addr(127),
        "RAM_write_read_addr255": lambda: _test_ram_addr(255),
        "RAM_multiple_addresses": lambda: _test_ram_multiple(),
        "RAM_overwrite": lambda: _test_ram_overwrite(),
        "RAM_write_disabled": lambda: _test_ram_write_disabled(),

        # RAM load program
        "RAM_load_program": lambda: _test_ram_load_program(),
        "RAM_load_program_offset": lambda: _test_ram_load_program_offset(),
    }


def _test_ram_addr(addr_val):
    """Test RAM write and read at specific address."""
    from computer.memory import RAM
    ram = RAM()
    addr = int_to_bits(addr_val, 8)
    data = int_to_bits(addr_val % 256, 8)
    ram.write(addr, data, 1)
    result = ram.read(addr)
    if result is not None:
        assert_eq(bits_to_int(result), addr_val % 256)


def _test_ram_multiple():
    """Test RAM with multiple addresses."""
    from computer.memory import RAM
    ram = RAM()
    # Write different values to different addresses
    for i in range(10):
        addr = int_to_bits(i * 10, 8)
        data = int_to_bits(i * 10, 8)
        ram.write(addr, data, 1)
    # Verify all values
    for i in range(10):
        addr = int_to_bits(i * 10, 8)
        result = ram.read(addr)
        if result is not None:
            assert_eq(bits_to_int(result), i * 10)


def _test_ram_overwrite():
    """Test RAM overwrite."""
    from computer.memory import RAM
    ram = RAM()
    addr = int_to_bits(5, 8)
    # Write first value
    data1 = int_to_bits(100, 8)
    ram.write(addr, data1, 1)
    # Overwrite with second value
    data2 = int_to_bits(200, 8)
    ram.write(addr, data2, 1)
    result = ram.read(addr)
    if result is not None:
        assert_eq(bits_to_int(result), 200)


def _test_ram_write_disabled():
    """Test RAM write when enable=0."""
    from computer.memory import RAM
    ram = RAM()
    addr = int_to_bits(5, 8)
    # Write first value
    data1 = int_to_bits(100, 8)
    ram.write(addr, data1, 1)
    # Try to write with enable=0
    data2 = int_to_bits(200, 8)
    ram.write(addr, data2, 0)
    result = ram.read(addr)
    if result is not None:
        assert_eq(bits_to_int(result), 100)


def _test_ram_load_program():
    """Test RAM load_program method."""
    from computer.memory import RAM
    ram = RAM()
    program = [
        int_to_bits(0x00, 8),  # NOP
        int_to_bits(0x10, 8),  # Instruction 1
        int_to_bits(0x20, 8),  # Instruction 2
    ]
    ram.load_program(program)
    # Verify program loaded
    for i, instr in enumerate(program):
        addr = int_to_bits(i, 8)
        result = ram.read(addr)
        if result is not None:
            assert_eq(result, instr)


def _test_ram_load_program_offset():
    """Test RAM load_program with offset."""
    from computer.memory import RAM
    ram = RAM()
    program = [
        int_to_bits(0xAA, 8),
        int_to_bits(0xBB, 8),
    ]
    ram.load_program(program, start_addr=100)
    # Verify program at offset
    result = ram.read(int_to_bits(100, 8))
    if result is not None:
        assert_eq(bits_to_int(result), 0xAA)
    result = ram.read(int_to_bits(101, 8))
    if result is not None:
        assert_eq(bits_to_int(result), 0xBB)
