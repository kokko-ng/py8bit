"""
Tests for ALU
"""

import pytest
from computer.alu import ALU
from tests.conftest import int_to_bits, bits_to_int


@pytest.fixture
def alu():
    return ALU()


class TestALUAdd:
    """Tests for ALU ADD operation."""

    def test_add_zero(self, alu):
        """0 + 0 = 0."""
        a = int_to_bits(0, 8)
        b = int_to_bits(0, 8)
        result, flags = alu(a, b, ALU.OP_ADD)
        assert bits_to_int(result) == 0
        assert flags['Z'] == 1

    def test_add_simple(self, alu):
        """5 + 3 = 8."""
        a = int_to_bits(5, 8)
        b = int_to_bits(3, 8)
        result, flags = alu(a, b, ALU.OP_ADD)
        assert bits_to_int(result) == 8
        assert flags['Z'] == 0
        assert flags['C'] == 0

    def test_add_overflow(self, alu):
        """255 + 1 = 0 with carry."""
        a = int_to_bits(255, 8)
        b = int_to_bits(1, 8)
        result, flags = alu(a, b, ALU.OP_ADD)
        assert bits_to_int(result) == 0
        assert flags['C'] == 1


class TestALUSub:
    """Tests for ALU SUB operation."""

    def test_sub_simple(self, alu):
        """5 - 3 = 2."""
        a = int_to_bits(5, 8)
        b = int_to_bits(3, 8)
        result, flags = alu(a, b, ALU.OP_SUB)
        assert bits_to_int(result) == 2
        assert flags['Z'] == 0

    def test_sub_zero(self, alu):
        """5 - 5 = 0."""
        a = int_to_bits(5, 8)
        b = int_to_bits(5, 8)
        result, flags = alu(a, b, ALU.OP_SUB)
        assert bits_to_int(result) == 0
        assert flags['Z'] == 1


class TestALULogic:
    """Tests for ALU logical operations."""

    def test_and(self, alu):
        """AND operation."""
        a = int_to_bits(0b11110000, 8)
        b = int_to_bits(0b10101010, 8)
        result, _ = alu(a, b, ALU.OP_AND)
        assert bits_to_int(result) == 0b10100000

    def test_or(self, alu):
        """OR operation."""
        a = int_to_bits(0b11110000, 8)
        b = int_to_bits(0b00001111, 8)
        result, _ = alu(a, b, ALU.OP_OR)
        assert bits_to_int(result) == 0b11111111

    def test_xor(self, alu):
        """XOR operation."""
        a = int_to_bits(0b11110000, 8)
        b = int_to_bits(0b10101010, 8)
        result, _ = alu(a, b, ALU.OP_XOR)
        assert bits_to_int(result) == 0b01011010

    def test_not(self, alu):
        """NOT operation."""
        a = int_to_bits(0b11110000, 8)
        b = [0] * 8
        result, _ = alu(a, b, ALU.OP_NOT)
        assert bits_to_int(result) == 0b00001111


class TestALUShift:
    """Tests for ALU shift operations."""

    def test_shl(self, alu):
        """Shift left."""
        a = int_to_bits(0b00000101, 8)
        b = [0] * 8
        result, flags = alu(a, b, ALU.OP_SHL)
        assert bits_to_int(result) == 0b00001010
        assert flags['C'] == 0

    def test_shl_with_carry(self, alu):
        """Shift left with carry out."""
        a = int_to_bits(0b10000000, 8)
        b = [0] * 8
        result, flags = alu(a, b, ALU.OP_SHL)
        assert flags['C'] == 1

    def test_shr(self, alu):
        """Shift right."""
        a = int_to_bits(0b00001010, 8)
        b = [0] * 8
        result, flags = alu(a, b, ALU.OP_SHR)
        assert bits_to_int(result) == 0b00000101
        assert flags['C'] == 0


class TestALUFlags:
    """Tests for ALU flags."""

    def test_zero_flag(self, alu):
        """Zero flag set when result is 0."""
        a = int_to_bits(5, 8)
        b = int_to_bits(5, 8)
        _, flags = alu(a, b, ALU.OP_SUB)
        assert flags['Z'] == 1

    def test_negative_flag(self, alu):
        """Negative flag set when MSB is 1."""
        a = int_to_bits(0, 8)
        b = int_to_bits(1, 8)
        result, flags = alu(a, b, ALU.OP_SUB)
        assert flags['N'] == 1  # Result is 255 in unsigned, -1 in signed


class TestALUCompare:
    """Tests for ALU CMP operation."""

    def test_cmp_equal(self, alu):
        """CMP sets zero flag when equal."""
        a = int_to_bits(5, 8)
        b = int_to_bits(5, 8)
        result, flags = alu(a, b, ALU.OP_CMP)
        assert bits_to_int(result) == 5  # Result is unchanged A
        assert flags['Z'] == 1

    def test_cmp_greater(self, alu):
        """CMP with A > B."""
        a = int_to_bits(10, 8)
        b = int_to_bits(5, 8)
        result, flags = alu(a, b, ALU.OP_CMP)
        assert bits_to_int(result) == 10
        assert flags['Z'] == 0
        assert flags['C'] == 0  # No borrow means A >= B
