"""Test cases for datapath."""

from ..helpers import assert_eq, assert_true, assert_not_none, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for datapath."""
    from computer.datapath import DataPath

    return {
        # DataPath initial state
        "DataPath_initial_pc": lambda: _test_datapath_initial_pc(),
        # DataPath PC operations
        "DataPath_set_pc": lambda: _test_datapath_set_pc(),
        "DataPath_increment_pc": lambda: _test_datapath_increment_pc(),
        # DataPath fetch
        "DataPath_fetch_instruction": lambda: _test_datapath_fetch(),
        # DataPath ALU
        "DataPath_alu_add": lambda: _test_datapath_alu_add(),
        # DataPath register operations
        "DataPath_write_read_register": lambda: _test_datapath_register(),
    }


def _test_datapath_initial_pc():
    """Test datapath initial PC is 0 and increment_pc works."""
    from computer.datapath import DataPath

    dp = DataPath()
    pc = dp.get_pc()
    assert_not_none(pc, "DataPath.get_pc() returned None")
    assert_eq(bits_to_int(pc), 0)
    # Also verify increment_pc works (increments by 2)
    dp.increment_pc()
    pc_after = dp.get_pc()
    assert_eq(bits_to_int(pc_after), 2, "increment_pc should increment PC by 2")


def _test_datapath_initial_flags():
    """Test datapath initial flags."""
    from computer.datapath import DataPath

    dp = DataPath()
    assert_true("Z" in dp.flags)
    assert_true("C" in dp.flags)
    assert_true("N" in dp.flags)


def _test_datapath_set_pc():
    """Test datapath set_pc method."""
    from computer.datapath import DataPath

    dp = DataPath()
    new_pc = int_to_bits(42, 8)
    dp.set_pc(new_pc)
    result = dp.get_pc()
    assert_not_none(result, "DataPath.get_pc() returned None after set_pc")
    assert_eq(bits_to_int(result), 42)


def _test_datapath_increment_pc():
    """Test datapath increment_pc method."""
    from computer.datapath import DataPath

    dp = DataPath()
    dp.increment_pc()
    result = dp.get_pc()
    assert_not_none(result, "DataPath.get_pc() returned None after increment_pc")
    assert_eq(bits_to_int(result), 2, "increment_pc should add 2 (instruction width)")


def _test_datapath_fetch():
    """Test datapath fetch_instruction method."""
    from computer.datapath import DataPath

    dp = DataPath()
    # Write a known instruction to memory at address 0
    test_val = 0xAB
    dp.memory.write(int_to_bits(0, 8), int_to_bits(test_val, 8), 1)
    dp.memory.write(int_to_bits(1, 8), int_to_bits(0xCD, 8), 1)
    result = dp.fetch_instruction()
    assert_not_none(result, "DataPath.fetch_instruction() returned None")
    assert_eq(len(result), 16, "fetch_instruction should return 16-bit instruction")


def _test_datapath_alu_add():
    """Test datapath ALU add operation."""
    from computer.datapath import DataPath
    from computer.alu import ALU

    dp = DataPath()
    a = int_to_bits(10, 8)
    b = int_to_bits(5, 8)
    output = dp.alu(a, b, ALU.OP_ADD)
    assert_not_none(output, "DataPath.alu() returned None")
    result, flags = output
    assert_eq(bits_to_int(result), 15)


def _test_datapath_register():
    """Test datapath register file operations."""
    from computer.datapath import DataPath

    dp = DataPath()
    # Write to register 1
    addr = [1, 0, 0]
    data = int_to_bits(77, 8)
    dp.reg_file.write(addr, data, 1, 0)
    dp.reg_file.write(addr, data, 1, 1)
    result = dp.reg_file.read(addr)
    assert_not_none(result, "RegisterFile.read() returned None")
    assert_eq(bits_to_int(result), 77)
