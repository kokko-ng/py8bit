"""Test cases for registers."""

from ..helpers import assert_eq, assert_true, assert_not_none, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for registers."""
    from computer.registers import Register8, RegisterFile

    return {
        # Register8
        "Register8_create": lambda: assert_true(Register8() is not None),
        "Register8_has_read": lambda: assert_true(hasattr(Register8(), "read")),
        "Register8_has_clock": lambda: assert_true(hasattr(Register8(), "clock")),
        "Register8_load_value": lambda: _test_register_load(),
        "Register8_hold_value": lambda: _test_register_hold(),
        "Register8_multiple_values": lambda: _test_register_multiple(),
        # RegisterFile
        "RegisterFile_create": lambda: assert_true(RegisterFile() is not None),
        "RegisterFile_has_read": lambda: assert_true(hasattr(RegisterFile(), "read")),
        "RegisterFile_has_write": lambda: assert_true(hasattr(RegisterFile(), "write")),
        "RegisterFile_write_read": lambda: _test_regfile_write_read(),
        "RegisterFile_multiple_registers": lambda: _test_regfile_multiple(),
        "RegisterFile_read_two": lambda: _test_regfile_read_two(),
    }


def _test_register_load():
    """Test register load."""
    from computer.registers import Register8

    reg = Register8()
    data = int_to_bits(42, 8)
    reg.clock(data, 1, 0)
    reg.clock(data, 1, 1)
    result = reg.read()
    assert_not_none(result, "Register8.read() returned None")
    assert_eq(bits_to_int(result), 42)


def _test_register_hold():
    """Test register hold."""
    from computer.registers import Register8

    reg = Register8()
    data = int_to_bits(42, 8)
    reg.clock(data, 1, 0)
    reg.clock(data, 1, 1)
    # Now try to change with load=0
    new_data = int_to_bits(99, 8)
    reg.clock(new_data, 0, 0)
    reg.clock(new_data, 0, 1)
    result = reg.read()
    assert_not_none(result, "Register8.read() returned None")
    assert_eq(bits_to_int(result), 42)


def _test_register_multiple():
    """Test register with multiple values."""
    from computer.registers import Register8

    reg = Register8()
    for val in [0, 42, 127, 255, 1]:
        data = int_to_bits(val, 8)
        reg.clock(data, 1, 0)
        reg.clock(data, 1, 1)
        result = reg.read()
        assert_not_none(result, "Register8.read() returned None")
        assert_eq(bits_to_int(result), val)


def _test_regfile_write_read():
    """Test register file write and read."""
    from computer.registers import RegisterFile

    rf = RegisterFile()
    addr = [1, 0, 0]  # Address 1
    data = int_to_bits(123, 8)
    rf.write(addr, data, 1, 0)
    rf.write(addr, data, 1, 1)
    result = rf.read(addr)
    assert_not_none(result, "RegisterFile.read() returned None")
    assert_eq(bits_to_int(result), 123)


def _test_regfile_multiple():
    """Test register file with multiple registers."""
    from computer.registers import RegisterFile

    rf = RegisterFile()
    # Write different values to different registers
    test_data = [(0, 10), (1, 20), (2, 30), (3, 40)]
    for reg_idx, val in test_data:
        addr = [reg_idx & 1, (reg_idx >> 1) & 1, (reg_idx >> 2) & 1]
        data = int_to_bits(val, 8)
        rf.write(addr, data, 1, 0)
        rf.write(addr, data, 1, 1)
    # Verify all values
    for reg_idx, val in test_data:
        addr = [reg_idx & 1, (reg_idx >> 1) & 1, (reg_idx >> 2) & 1]
        result = rf.read(addr)
        assert_not_none(result, "RegisterFile.read() returned None")
        assert_eq(bits_to_int(result), val)


def _test_regfile_read_two():
    """Test register file read_two method."""
    from computer.registers import RegisterFile

    rf = RegisterFile()
    if not hasattr(rf, "read_two"):
        return
    # Write to registers 0 and 1
    rf.write([0, 0, 0], int_to_bits(100, 8), 1, 0)
    rf.write([0, 0, 0], int_to_bits(100, 8), 1, 1)
    rf.write([1, 0, 0], int_to_bits(200, 8), 1, 0)
    rf.write([1, 0, 0], int_to_bits(200, 8), 1, 1)
    # Read both
    val1, val2 = rf.read_two([0, 0, 0], [1, 0, 0])
    assert_not_none(val1, "RegisterFile.read_two() returned None for first value")
    assert_not_none(val2, "RegisterFile.read_two() returned None for second value")
    assert_eq(bits_to_int(val1), 100)
    assert_eq(bits_to_int(val2), 200)
