"""Test cases for counters."""

from ..helpers import assert_eq, assert_true, assert_not_none, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for counters."""
    from computer.counters import BinaryCounter8, ProgramCounter

    return {
        # BinaryCounter8
        "BinaryCounter8_create": lambda: assert_true(BinaryCounter8() is not None),
        "BinaryCounter8_initial_state": lambda: assert_eq(BinaryCounter8().read(), [0] * 8),
        "BinaryCounter8_count_one": lambda: _test_counter8_count_one(),
        "BinaryCounter8_count_sequence": lambda: _test_counter8_sequence(),
        "BinaryCounter8_reset": lambda: _test_counter8_reset(),
        "BinaryCounter8_hold": lambda: _test_counter8_hold(),
        # ProgramCounter
        "ProgramCounter_create": lambda: assert_true(ProgramCounter() is not None),
        "ProgramCounter_initial_state": lambda: assert_eq(ProgramCounter().read(), [0] * 8),
        "ProgramCounter_increment": lambda: _test_pc_increment(),
        "ProgramCounter_increment_sequence": lambda: _test_pc_increment_sequence(),
        "ProgramCounter_load": lambda: _test_pc_load(),
        "ProgramCounter_reset": lambda: _test_pc_reset(),
        "ProgramCounter_priority": lambda: _test_pc_priority(),
    }


def _test_counter8_count_one():
    """Test 8-bit counter counting by one."""
    from computer.counters import BinaryCounter8

    counter = BinaryCounter8()
    counter.clock(1, 0, 1)
    result = counter.read()
    assert_not_none(result, "BinaryCounter8.read() returned None")
    assert_eq(bits_to_int(result), 1)


def _test_counter8_sequence():
    """Test 8-bit counter counting sequence."""
    from computer.counters import BinaryCounter8

    counter = BinaryCounter8()
    for expected in range(1, 10):
        counter.clock(1, 0, 1)
        result = counter.read()
        assert_not_none(result, "BinaryCounter8.read() returned None")
        assert_eq(bits_to_int(result), expected)


def _test_counter8_reset():
    """Test 8-bit counter reset."""
    from computer.counters import BinaryCounter8

    counter = BinaryCounter8()
    # Count up a bit
    for _ in range(5):
        counter.clock(1, 0, 1)
    # Verify counting worked before testing reset
    result = counter.read()
    assert_not_none(result, "BinaryCounter8.read() returned None")
    assert_eq(bits_to_int(result), 5, "Counter should be 5 before reset")
    # Reset
    counter.clock(0, 1, 1)
    result = counter.read()
    assert_eq(bits_to_int(result), 0, "Counter should be 0 after reset")


def _test_counter8_hold():
    """Test 8-bit counter hold."""
    from computer.counters import BinaryCounter8

    counter = BinaryCounter8()
    # Count to 5
    for _ in range(5):
        counter.clock(1, 0, 1)
    # Hold (enable=0)
    counter.clock(0, 0, 1)
    assert_eq(bits_to_int(counter.read()), 5)


def _test_pc_increment():
    """Test program counter increment."""
    from computer.counters import ProgramCounter

    pc = ProgramCounter()
    pc.clock(load=0, load_value=[0] * 8, increment=1, reset=0, clk=1)
    result = pc.read()
    assert_not_none(result, "ProgramCounter.read() returned None")
    assert_eq(bits_to_int(result), 1)


def _test_pc_increment_sequence():
    """Test program counter increment sequence."""
    from computer.counters import ProgramCounter

    pc = ProgramCounter()
    for expected in range(1, 10):
        pc.clock(load=0, load_value=[0] * 8, increment=1, reset=0, clk=1)
        result = pc.read()
        assert_not_none(result, "ProgramCounter.read() returned None")
        assert_eq(bits_to_int(result), expected)


def _test_pc_load():
    """Test program counter load."""
    from computer.counters import ProgramCounter

    pc = ProgramCounter()
    addr = int_to_bits(100, 8)
    pc.clock(load=1, load_value=addr, increment=0, reset=0, clk=1)
    result = pc.read()
    assert_not_none(result, "ProgramCounter.read() returned None")
    assert_eq(bits_to_int(result), 100)


def _test_pc_reset():
    """Test program counter reset."""
    from computer.counters import ProgramCounter

    pc = ProgramCounter()
    # Load a value first
    addr = int_to_bits(50, 8)
    pc.clock(load=1, load_value=addr, increment=0, reset=0, clk=1)
    # Verify load worked before testing reset
    result = pc.read()
    assert_not_none(result, "ProgramCounter.read() returned None")
    assert_eq(bits_to_int(result), 50, "PC should be 50 before reset")
    # Reset
    pc.clock(load=0, load_value=[0] * 8, increment=0, reset=1, clk=1)
    result = pc.read()
    assert_eq(bits_to_int(result), 0, "PC should be 0 after reset")


def _test_pc_priority():
    """Test program counter priority: reset > load > increment."""
    from computer.counters import ProgramCounter

    pc = ProgramCounter()
    # First, load a value to verify the PC can change
    addr = int_to_bits(50, 8)
    pc.clock(load=1, load_value=addr, increment=0, reset=0, clk=1)
    result = pc.read()
    assert_not_none(result, "ProgramCounter.read() returned None")
    assert_eq(bits_to_int(result), 50, "PC should be 50 after load")
    # Now test that reset takes priority over load
    new_addr = int_to_bits(100, 8)
    pc.clock(load=1, load_value=new_addr, increment=0, reset=1, clk=1)
    result = pc.read()
    assert_eq(bits_to_int(result), 0, "Reset should take priority over load")
