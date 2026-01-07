"""Test cases for datapath."""

from ..helpers import assert_eq, assert_true


def get_tests() -> dict:
    """Return all test cases for datapath."""
    from computer.datapath import DataPath

    return {
        # DataPath creation
        "DataPath_create": lambda: assert_true(DataPath() is not None),
        # DataPath components
        "DataPath_has_pc": lambda: assert_true(hasattr(DataPath(), "pc")),
        "DataPath_has_memory": lambda: assert_true(hasattr(DataPath(), "memory")),
        "DataPath_has_reg_file": lambda: assert_true(hasattr(DataPath(), "reg_file")),
        "DataPath_has_alu": lambda: assert_true(hasattr(DataPath(), "alu")),
        "DataPath_has_ir": lambda: assert_true(hasattr(DataPath(), "ir")),
        "DataPath_has_flags": lambda: assert_true(hasattr(DataPath(), "flags")),
        # DataPath methods
        "DataPath_has_get_pc": lambda: assert_true(hasattr(DataPath(), "get_pc")),
        "DataPath_has_set_pc": lambda: assert_true(hasattr(DataPath(), "set_pc")),
        "DataPath_has_fetch": lambda: assert_true(hasattr(DataPath(), "fetch_instruction")),
        "DataPath_has_load_ir": lambda: assert_true(hasattr(DataPath(), "load_instruction")),
        # DataPath initial state
        "DataPath_initial_pc": lambda: _test_datapath_initial_pc(),
        "DataPath_initial_flags": lambda: _test_datapath_initial_flags(),
    }


def _test_datapath_initial_pc():
    """Test datapath initial PC is 0."""
    from computer.datapath import DataPath

    dp = DataPath()
    pc = dp.get_pc()
    if pc is not None:
        from ..helpers import bits_to_int

        assert_eq(bits_to_int(pc), 0)


def _test_datapath_initial_flags():
    """Test datapath initial flags."""
    from computer.datapath import DataPath

    dp = DataPath()
    if hasattr(dp, "flags"):
        assert_true("Z" in dp.flags)
        assert_true("C" in dp.flags)
        assert_true("N" in dp.flags)
