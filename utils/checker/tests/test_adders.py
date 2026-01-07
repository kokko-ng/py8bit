"""Test cases for adders."""

from ..helpers import assert_eq, assert_isinstance, assert_len, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for adders."""
    from computer.adders import half_adder, full_adder, twos_complement

    return {
        # Half adder - complete truth table
        "half_adder_0_0": lambda: assert_eq(half_adder(0, 0), (0, 0)),
        "half_adder_0_1": lambda: assert_eq(half_adder(0, 1), (1, 0)),
        "half_adder_1_0": lambda: assert_eq(half_adder(1, 0), (1, 0)),
        "half_adder_1_1": lambda: assert_eq(half_adder(1, 1), (0, 1)),
        "half_adder_returns_tuple": lambda: assert_isinstance(half_adder(0, 0), tuple),
        "half_adder_tuple_length": lambda: assert_len(half_adder(0, 0), 2),
        "half_adder_commutative": lambda: assert_eq(half_adder(0, 1), half_adder(1, 0)),
        # Full adder - complete truth table (all 8 combinations)
        "full_adder_0_0_0": lambda: assert_eq(full_adder(0, 0, 0), (0, 0)),
        "full_adder_0_0_1": lambda: assert_eq(full_adder(0, 0, 1), (1, 0)),
        "full_adder_0_1_0": lambda: assert_eq(full_adder(0, 1, 0), (1, 0)),
        "full_adder_0_1_1": lambda: assert_eq(full_adder(0, 1, 1), (0, 1)),
        "full_adder_1_0_0": lambda: assert_eq(full_adder(1, 0, 0), (1, 0)),
        "full_adder_1_0_1": lambda: assert_eq(full_adder(1, 0, 1), (0, 1)),
        "full_adder_1_1_0": lambda: assert_eq(full_adder(1, 1, 0), (0, 1)),
        "full_adder_1_1_1": lambda: assert_eq(full_adder(1, 1, 1), (1, 1)),
        "full_adder_returns_tuple": lambda: assert_isinstance(full_adder(0, 0, 0), tuple),
        "full_adder_tuple_length": lambda: assert_len(full_adder(0, 0, 0), 2),
        # Ripple carry adder - basic operations
        "ripple_adder_0_plus_0": lambda: _test_ripple_add(0, 0, 0, 0),
        "ripple_adder_1_plus_0": lambda: _test_ripple_add(1, 0, 1, 0),
        "ripple_adder_0_plus_1": lambda: _test_ripple_add(0, 1, 1, 0),
        "ripple_adder_1_plus_1": lambda: _test_ripple_add(1, 1, 2, 0),
        "ripple_adder_5_plus_3": lambda: _test_ripple_add(5, 3, 8, 0),
        "ripple_adder_10_plus_20": lambda: _test_ripple_add(10, 20, 30, 0),
        "ripple_adder_50_plus_50": lambda: _test_ripple_add(50, 50, 100, 0),
        "ripple_adder_100_plus_55": lambda: _test_ripple_add(100, 55, 155, 0),
        "ripple_adder_127_plus_1": lambda: _test_ripple_add(127, 1, 128, 0),
        "ripple_adder_128_plus_127": lambda: _test_ripple_add(128, 127, 255, 0),
        # Ripple carry adder - overflow cases
        "ripple_adder_255_plus_1_overflow": lambda: _test_ripple_add(255, 1, 0, 1),
        "ripple_adder_255_plus_255": lambda: _test_ripple_add(255, 255, 254, 1),
        "ripple_adder_200_plus_100": lambda: _test_ripple_add(200, 100, 44, 1),
        "ripple_adder_128_plus_128": lambda: _test_ripple_add(128, 128, 0, 1),
        # Ripple carry adder - commutative property
        "ripple_adder_commutative": lambda: _test_ripple_commutative(),
        # Subtractor - basic operations
        "subtractor_0_minus_0": lambda: _test_sub(0, 0, 0, 0),
        "subtractor_1_minus_0": lambda: _test_sub(1, 0, 1, 0),
        "subtractor_1_minus_1": lambda: _test_sub(1, 1, 0, 0),
        "subtractor_5_minus_3": lambda: _test_sub(5, 3, 2, 0),
        "subtractor_10_minus_5": lambda: _test_sub(10, 5, 5, 0),
        "subtractor_10_minus_10": lambda: _test_sub(10, 10, 0, 0),
        "subtractor_100_minus_50": lambda: _test_sub(100, 50, 50, 0),
        "subtractor_255_minus_1": lambda: _test_sub(255, 1, 254, 0),
        "subtractor_255_minus_255": lambda: _test_sub(255, 255, 0, 0),
        # Subtractor - borrow cases
        "subtractor_0_minus_1_borrow": lambda: _test_sub(0, 1, 255, 1),
        "subtractor_3_minus_5_borrow": lambda: _test_sub(3, 5, 254, 1),
        "subtractor_10_minus_20_borrow": lambda: _test_sub(10, 20, 246, 1),
        "subtractor_1_minus_255_borrow": lambda: _test_sub(1, 255, 2, 1),
        # Two's complement
        "twos_complement_0": lambda: assert_eq(bits_to_int(twos_complement(int_to_bits(0, 8))), 0),
        "twos_complement_1": lambda: assert_eq(bits_to_int(twos_complement(int_to_bits(1, 8))), 255),
        "twos_complement_2": lambda: assert_eq(bits_to_int(twos_complement(int_to_bits(2, 8))), 254),
        "twos_complement_5": lambda: assert_eq(bits_to_int(twos_complement(int_to_bits(5, 8))), 251),
        "twos_complement_127": lambda: assert_eq(bits_to_int(twos_complement(int_to_bits(127, 8))), 129),
        "twos_complement_128": lambda: assert_eq(bits_to_int(twos_complement(int_to_bits(128, 8))), 128),
        "twos_complement_double": lambda: _test_twos_complement_double(),
    }


def _test_ripple_add(a_val, b_val, expected_result, expected_carry):
    """Helper for ripple carry adder tests."""
    from computer.adders import ripple_carry_adder_8bit

    a = int_to_bits(a_val, 8)
    b = int_to_bits(b_val, 8)
    result, carry = ripple_carry_adder_8bit(a, b)
    assert_eq(bits_to_int(result), expected_result)
    assert_eq(carry, expected_carry)


def _test_ripple_commutative():
    """Test that addition is commutative."""
    from computer.adders import ripple_carry_adder_8bit

    for a_val, b_val in [(5, 10), (100, 50), (1, 254)]:
        a = int_to_bits(a_val, 8)
        b = int_to_bits(b_val, 8)
        result1, carry1 = ripple_carry_adder_8bit(a, b)
        result2, carry2 = ripple_carry_adder_8bit(b, a)
        assert_eq(bits_to_int(result1), bits_to_int(result2))
        assert_eq(carry1, carry2)


def _test_sub(a_val, b_val, expected_result, expected_borrow):
    """Helper for subtractor tests."""
    from computer.adders import subtractor_8bit

    a = int_to_bits(a_val, 8)
    b = int_to_bits(b_val, 8)
    result, borrow, _ = subtractor_8bit(a, b)
    assert_eq(bits_to_int(result), expected_result)
    assert_eq(borrow, expected_borrow)


def _test_twos_complement_double():
    """Test that double two's complement returns original."""
    from computer.adders import twos_complement

    for val in [1, 5, 10, 50, 127]:
        bits = int_to_bits(val, 8)
        result = twos_complement(twos_complement(bits))
        assert_eq(bits_to_int(result), val)
