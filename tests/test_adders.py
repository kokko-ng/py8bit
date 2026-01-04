"""
Tests for Adders

Tests for half adder, full adder, 8-bit ripple carry adder, and subtractor.
"""

import pytest
from computer.adders import (
    half_adder, full_adder,
    ripple_carry_adder_8bit, subtractor_8bit, twos_complement
)
from tests.conftest import int_to_bits, bits_to_int


class TestHalfAdder:
    """Tests for the half adder."""

    def test_0_plus_0(self):
        """0 + 0 = 0 with no carry."""
        assert half_adder(0, 0) == (0, 0)

    def test_0_plus_1(self):
        """0 + 1 = 1 with no carry."""
        assert half_adder(0, 1) == (1, 0)

    def test_1_plus_0(self):
        """1 + 0 = 1 with no carry."""
        assert half_adder(1, 0) == (1, 0)

    def test_1_plus_1(self):
        """1 + 1 = 0 with carry 1."""
        assert half_adder(1, 1) == (0, 1)

    def test_returns_tuple(self):
        """Should return a tuple of (sum, carry)."""
        result = half_adder(1, 1)
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestFullAdder:
    """Tests for the full adder."""

    def test_all_zeros(self):
        """0 + 0 + 0 = 0."""
        assert full_adder(0, 0, 0) == (0, 0)

    def test_carry_in_only(self):
        """0 + 0 + 1 = 1."""
        assert full_adder(0, 0, 1) == (1, 0)

    def test_one_input(self):
        """1 + 0 + 0 = 1."""
        assert full_adder(1, 0, 0) == (1, 0)
        assert full_adder(0, 1, 0) == (1, 0)

    def test_two_inputs(self):
        """1 + 1 + 0 = 0 with carry."""
        assert full_adder(1, 1, 0) == (0, 1)

    def test_two_with_carry(self):
        """1 + 0 + 1 = 0 with carry."""
        assert full_adder(1, 0, 1) == (0, 1)
        assert full_adder(0, 1, 1) == (0, 1)

    def test_all_ones(self):
        """1 + 1 + 1 = 1 with carry."""
        assert full_adder(1, 1, 1) == (1, 1)

    def test_all_combinations(self, all_3bit_combinations):
        """Test all 8 input combinations."""
        expected = {
            (0, 0, 0): (0, 0),
            (0, 0, 1): (1, 0),
            (0, 1, 0): (1, 0),
            (0, 1, 1): (0, 1),
            (1, 0, 0): (1, 0),
            (1, 0, 1): (0, 1),
            (1, 1, 0): (0, 1),
            (1, 1, 1): (1, 1),
        }
        for a, b, c in all_3bit_combinations:
            assert full_adder(a, b, c) == expected[(a, b, c)]


class TestRippleCarryAdder:
    """Tests for the 8-bit ripple carry adder."""

    def test_zero_plus_zero(self, zero_byte):
        """0 + 0 = 0."""
        result, carry = ripple_carry_adder_8bit(zero_byte, zero_byte)
        assert result == [0] * 8
        assert carry == 0

    def test_one_plus_zero(self):
        """1 + 0 = 1."""
        a = int_to_bits(1, 8)
        b = int_to_bits(0, 8)
        result, carry = ripple_carry_adder_8bit(a, b)
        assert bits_to_int(result) == 1
        assert carry == 0

    def test_one_plus_one(self):
        """1 + 1 = 2."""
        a = int_to_bits(1, 8)
        b = int_to_bits(1, 8)
        result, carry = ripple_carry_adder_8bit(a, b)
        assert bits_to_int(result) == 2
        assert carry == 0

    def test_five_plus_three(self):
        """5 + 3 = 8."""
        a = int_to_bits(5, 8)
        b = int_to_bits(3, 8)
        result, carry = ripple_carry_adder_8bit(a, b)
        assert bits_to_int(result) == 8
        assert carry == 0

    def test_100_plus_55(self):
        """100 + 55 = 155."""
        a = int_to_bits(100, 8)
        b = int_to_bits(55, 8)
        result, carry = ripple_carry_adder_8bit(a, b)
        assert bits_to_int(result) == 155
        assert carry == 0

    def test_overflow(self):
        """255 + 1 = 0 with carry."""
        a = int_to_bits(255, 8)
        b = int_to_bits(1, 8)
        result, carry = ripple_carry_adder_8bit(a, b)
        assert bits_to_int(result) == 0
        assert carry == 1

    def test_max_plus_max(self):
        """255 + 255 = 254 with carry."""
        a = int_to_bits(255, 8)
        b = int_to_bits(255, 8)
        result, carry = ripple_carry_adder_8bit(a, b)
        assert bits_to_int(result) == 254
        assert carry == 1

    def test_with_carry_in(self):
        """5 + 3 + 1 = 9 when cin=1."""
        a = int_to_bits(5, 8)
        b = int_to_bits(3, 8)
        result, carry = ripple_carry_adder_8bit(a, b, cin=1)
        assert bits_to_int(result) == 9
        assert carry == 0

    def test_various_additions(self):
        """Test various addition combinations."""
        test_cases = [
            (0, 0, 0),
            (1, 1, 2),
            (10, 20, 30),
            (127, 1, 128),
            (128, 127, 255),
            (200, 55, 255),
        ]
        for x, y, expected in test_cases:
            a = int_to_bits(x, 8)
            b = int_to_bits(y, 8)
            result, carry = ripple_carry_adder_8bit(a, b)
            assert bits_to_int(result) == expected


class TestSubtractor:
    """Tests for the 8-bit subtractor."""

    def test_zero_minus_zero(self):
        """0 - 0 = 0."""
        a = int_to_bits(0, 8)
        b = int_to_bits(0, 8)
        result, borrow, _ = subtractor_8bit(a, b)
        assert bits_to_int(result) == 0
        assert borrow == 0

    def test_five_minus_three(self):
        """5 - 3 = 2."""
        a = int_to_bits(5, 8)
        b = int_to_bits(3, 8)
        result, borrow, _ = subtractor_8bit(a, b)
        assert bits_to_int(result) == 2
        assert borrow == 0

    def test_ten_minus_ten(self):
        """10 - 10 = 0."""
        a = int_to_bits(10, 8)
        b = int_to_bits(10, 8)
        result, borrow, _ = subtractor_8bit(a, b)
        assert bits_to_int(result) == 0
        assert borrow == 0

    def test_three_minus_five_unsigned_borrow(self):
        """3 - 5 = 254 (with borrow, unsigned)."""
        a = int_to_bits(3, 8)
        b = int_to_bits(5, 8)
        result, borrow, _ = subtractor_8bit(a, b)
        # In unsigned: 3 - 5 wraps to 254
        assert bits_to_int(result) == 254
        assert borrow == 1

    def test_100_minus_50(self):
        """100 - 50 = 50."""
        a = int_to_bits(100, 8)
        b = int_to_bits(50, 8)
        result, borrow, _ = subtractor_8bit(a, b)
        assert bits_to_int(result) == 50
        assert borrow == 0


class TestTwosComplement:
    """Tests for two's complement."""

    def test_zero(self):
        """Two's complement of 0 is 0."""
        bits = int_to_bits(0, 8)
        result = twos_complement(bits)
        assert bits_to_int(result) == 0

    def test_one(self):
        """Two's complement of 1 is 255 (-1 in signed)."""
        bits = int_to_bits(1, 8)
        result = twos_complement(bits)
        assert bits_to_int(result) == 255

    def test_five(self):
        """Two's complement of 5 is 251 (-5 in signed)."""
        bits = int_to_bits(5, 8)
        result = twos_complement(bits)
        assert bits_to_int(result) == 251

    def test_double_complement(self):
        """Two's complement of two's complement gives original."""
        for val in [1, 5, 10, 127]:
            bits = int_to_bits(val, 8)
            result = twos_complement(twos_complement(bits))
            assert bits_to_int(result) == val
