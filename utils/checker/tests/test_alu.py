"""
Test cases for ALU.
"""

from ..helpers import assert_eq, assert_true, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for ALU."""
    from computer.alu import ALU

    def make_alu():
        return ALU()

    return {
        # ADD operations
        "ALU_add_0_0": lambda: _test_alu_op(make_alu(), 0, 0, ALU.OP_ADD, 0, {'Z': 1}),
        "ALU_add_1_0": lambda: _test_alu_op(make_alu(), 1, 0, ALU.OP_ADD, 1, {'Z': 0}),
        "ALU_add_0_1": lambda: _test_alu_op(make_alu(), 0, 1, ALU.OP_ADD, 1, {'Z': 0}),
        "ALU_add_1_1": lambda: _test_alu_op(make_alu(), 1, 1, ALU.OP_ADD, 2, {'Z': 0}),
        "ALU_add_5_3": lambda: _test_alu_op(make_alu(), 5, 3, ALU.OP_ADD, 8, {'Z': 0, 'C': 0}),
        "ALU_add_100_55": lambda: _test_alu_op(make_alu(), 100, 55, ALU.OP_ADD, 155, {'C': 0}),
        "ALU_add_overflow_255_1": lambda: _test_alu_op(make_alu(), 255, 1, ALU.OP_ADD, 0, {'C': 1, 'Z': 1}),
        "ALU_add_overflow_200_100": lambda: _test_alu_op(make_alu(), 200, 100, ALU.OP_ADD, 44, {'C': 1}),

        # SUB operations
        "ALU_sub_0_0": lambda: _test_alu_op(make_alu(), 0, 0, ALU.OP_SUB, 0, {'Z': 1}),
        "ALU_sub_5_3": lambda: _test_alu_op(make_alu(), 5, 3, ALU.OP_SUB, 2, {'Z': 0}),
        "ALU_sub_5_5": lambda: _test_alu_op(make_alu(), 5, 5, ALU.OP_SUB, 0, {'Z': 1}),
        "ALU_sub_100_50": lambda: _test_alu_op(make_alu(), 100, 50, ALU.OP_SUB, 50, {'Z': 0}),
        "ALU_sub_3_5_borrow": lambda: _test_alu_sub_borrow(make_alu()),

        # AND operations
        "ALU_and_0x00_0x00": lambda: _test_alu_op(make_alu(), 0x00, 0x00, ALU.OP_AND, 0x00, {'Z': 1}),
        "ALU_and_0xFF_0xFF": lambda: _test_alu_op(make_alu(), 0xFF, 0xFF, ALU.OP_AND, 0xFF, {}),
        "ALU_and_0xF0_0xAA": lambda: _test_alu_op(make_alu(), 0xF0, 0xAA, ALU.OP_AND, 0xA0, {}),
        "ALU_and_0x0F_0xF0": lambda: _test_alu_op(make_alu(), 0x0F, 0xF0, ALU.OP_AND, 0x00, {'Z': 1}),
        "ALU_and_0x55_0xAA": lambda: _test_alu_op(make_alu(), 0x55, 0xAA, ALU.OP_AND, 0x00, {'Z': 1}),

        # OR operations
        "ALU_or_0x00_0x00": lambda: _test_alu_op(make_alu(), 0x00, 0x00, ALU.OP_OR, 0x00, {'Z': 1}),
        "ALU_or_0xFF_0x00": lambda: _test_alu_op(make_alu(), 0xFF, 0x00, ALU.OP_OR, 0xFF, {}),
        "ALU_or_0xF0_0x0F": lambda: _test_alu_op(make_alu(), 0xF0, 0x0F, ALU.OP_OR, 0xFF, {}),
        "ALU_or_0x55_0xAA": lambda: _test_alu_op(make_alu(), 0x55, 0xAA, ALU.OP_OR, 0xFF, {}),

        # XOR operations
        "ALU_xor_0x00_0x00": lambda: _test_alu_op(make_alu(), 0x00, 0x00, ALU.OP_XOR, 0x00, {'Z': 1}),
        "ALU_xor_0xFF_0xFF": lambda: _test_alu_op(make_alu(), 0xFF, 0xFF, ALU.OP_XOR, 0x00, {'Z': 1}),
        "ALU_xor_0xF0_0xAA": lambda: _test_alu_op(make_alu(), 0xF0, 0xAA, ALU.OP_XOR, 0x5A, {}),
        "ALU_xor_0x55_0xAA": lambda: _test_alu_op(make_alu(), 0x55, 0xAA, ALU.OP_XOR, 0xFF, {}),

        # NOT operation
        "ALU_not_0x00": lambda: _test_alu_not(make_alu(), 0x00, 0xFF),
        "ALU_not_0xFF": lambda: _test_alu_not(make_alu(), 0xFF, 0x00),
        "ALU_not_0xF0": lambda: _test_alu_not(make_alu(), 0xF0, 0x0F),
        "ALU_not_0x55": lambda: _test_alu_not(make_alu(), 0x55, 0xAA),

        # Shift left
        "ALU_shl_0x01": lambda: _test_alu_op(make_alu(), 0x01, 0, ALU.OP_SHL, 0x02, {'C': 0}),
        "ALU_shl_0x05": lambda: _test_alu_op(make_alu(), 0x05, 0, ALU.OP_SHL, 0x0A, {'C': 0}),
        "ALU_shl_0x80_carry": lambda: _test_alu_op(make_alu(), 0x80, 0, ALU.OP_SHL, 0x00, {'C': 1, 'Z': 1}),
        "ALU_shl_0xFF_carry": lambda: _test_alu_op(make_alu(), 0xFF, 0, ALU.OP_SHL, 0xFE, {'C': 1}),

        # Shift right
        "ALU_shr_0x02": lambda: _test_alu_op(make_alu(), 0x02, 0, ALU.OP_SHR, 0x01, {'C': 0}),
        "ALU_shr_0x0A": lambda: _test_alu_op(make_alu(), 0x0A, 0, ALU.OP_SHR, 0x05, {'C': 0}),
        "ALU_shr_0x01_carry": lambda: _test_alu_op(make_alu(), 0x01, 0, ALU.OP_SHR, 0x00, {'C': 1, 'Z': 1}),
        "ALU_shr_0xFF_carry": lambda: _test_alu_op(make_alu(), 0xFF, 0, ALU.OP_SHR, 0x7F, {'C': 1}),

        # Zero flag
        "ALU_zero_flag_add": lambda: _test_alu_op(make_alu(), 0, 0, ALU.OP_ADD, 0, {'Z': 1}),
        "ALU_zero_flag_sub": lambda: _test_alu_op(make_alu(), 5, 5, ALU.OP_SUB, 0, {'Z': 1}),
        "ALU_zero_flag_and": lambda: _test_alu_op(make_alu(), 0x0F, 0xF0, ALU.OP_AND, 0, {'Z': 1}),

        # Negative flag
        "ALU_negative_flag_sub": lambda: _test_alu_negative_flag(make_alu()),
        "ALU_negative_flag_high_bit": lambda: _test_alu_op(make_alu(), 128, 0, ALU.OP_ADD, 128, {'N': 1}),

        # CMP operations
        "ALU_cmp_equal": lambda: _test_alu_cmp(make_alu(), 5, 5, {'Z': 1}),
        "ALU_cmp_greater": lambda: _test_alu_cmp(make_alu(), 10, 5, {'Z': 0, 'C': 0}),
        "ALU_cmp_less": lambda: _test_alu_cmp(make_alu(), 5, 10, {'Z': 0}),
        "ALU_cmp_preserves_a": lambda: _test_alu_cmp_preserves(make_alu()),
    }


def _test_alu_op(alu, a_val, b_val, op, expected_result, expected_flags):
    """Helper for ALU operation tests."""
    a = int_to_bits(a_val, 8)
    b = int_to_bits(b_val, 8)
    result, flags = alu(a, b, op)
    assert_eq(bits_to_int(result), expected_result)
    for flag, value in expected_flags.items():
        assert_eq(flags[flag], value, f"Flag {flag}")


def _test_alu_not(alu, a_val, expected):
    """Test ALU NOT operation."""
    from computer.alu import ALU
    a = int_to_bits(a_val, 8)
    b = [0] * 8
    result, _ = alu(a, b, ALU.OP_NOT)
    assert_eq(bits_to_int(result), expected)


def _test_alu_sub_borrow(alu):
    """Test ALU subtraction with borrow."""
    from computer.alu import ALU
    a = int_to_bits(3, 8)
    b = int_to_bits(5, 8)
    result, flags = alu(a, b, ALU.OP_SUB)
    assert_eq(bits_to_int(result), 254)  # -2 in unsigned


def _test_alu_negative_flag(alu):
    """Test ALU negative flag."""
    from computer.alu import ALU
    a = int_to_bits(0, 8)
    b = int_to_bits(1, 8)
    _, flags = alu(a, b, ALU.OP_SUB)
    assert_eq(flags['N'], 1)


def _test_alu_cmp(alu, a_val, b_val, expected_flags):
    """Test ALU CMP operation."""
    from computer.alu import ALU
    a = int_to_bits(a_val, 8)
    b = int_to_bits(b_val, 8)
    result, flags = alu(a, b, ALU.OP_CMP)
    assert_eq(bits_to_int(result), a_val)  # A is unchanged
    for flag, value in expected_flags.items():
        assert_eq(flags[flag], value)


def _test_alu_cmp_preserves(alu):
    """Test that CMP preserves A value."""
    from computer.alu import ALU
    for a_val in [0, 5, 127, 255]:
        a = int_to_bits(a_val, 8)
        b = int_to_bits(100, 8)
        result, _ = alu(a, b, ALU.OP_CMP)
        assert_eq(bits_to_int(result), a_val)
