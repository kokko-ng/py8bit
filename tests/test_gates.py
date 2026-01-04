"""
Tests for Logic Gates

These tests verify the correctness of all logic gate implementations
by testing all possible input combinations.
"""

import pytest
from computer.gates import NOT, AND, OR, NAND, NOR, XOR, XNOR


class TestNOT:
    """Tests for the NOT gate."""

    def test_not_zero(self):
        """NOT(0) should return 1."""
        assert NOT(0) == 1

    def test_not_one(self):
        """NOT(1) should return 0."""
        assert NOT(1) == 0

    def test_not_returns_int(self):
        """NOT should return an integer."""
        assert isinstance(NOT(0), int)
        assert isinstance(NOT(1), int)


class TestAND:
    """Tests for the AND gate."""

    def test_and_0_0(self):
        """AND(0, 0) should return 0."""
        assert AND(0, 0) == 0

    def test_and_0_1(self):
        """AND(0, 1) should return 0."""
        assert AND(0, 1) == 0

    def test_and_1_0(self):
        """AND(1, 0) should return 0."""
        assert AND(1, 0) == 0

    def test_and_1_1(self):
        """AND(1, 1) should return 1."""
        assert AND(1, 1) == 1

    def test_and_returns_int(self):
        """AND should return an integer."""
        assert isinstance(AND(0, 0), int)

    def test_and_all_combinations(self, all_bit_pairs):
        """Test AND with all input combinations."""
        expected = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}
        for a, b in all_bit_pairs:
            assert AND(a, b) == expected[(a, b)]


class TestOR:
    """Tests for the OR gate."""

    def test_or_0_0(self):
        """OR(0, 0) should return 0."""
        assert OR(0, 0) == 0

    def test_or_0_1(self):
        """OR(0, 1) should return 1."""
        assert OR(0, 1) == 1

    def test_or_1_0(self):
        """OR(1, 0) should return 1."""
        assert OR(1, 0) == 1

    def test_or_1_1(self):
        """OR(1, 1) should return 1."""
        assert OR(1, 1) == 1

    def test_or_all_combinations(self, all_bit_pairs):
        """Test OR with all input combinations."""
        expected = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1}
        for a, b in all_bit_pairs:
            assert OR(a, b) == expected[(a, b)]


class TestNAND:
    """Tests for the NAND gate."""

    def test_nand_0_0(self):
        """NAND(0, 0) should return 1."""
        assert NAND(0, 0) == 1

    def test_nand_0_1(self):
        """NAND(0, 1) should return 1."""
        assert NAND(0, 1) == 1

    def test_nand_1_0(self):
        """NAND(1, 0) should return 1."""
        assert NAND(1, 0) == 1

    def test_nand_1_1(self):
        """NAND(1, 1) should return 0."""
        assert NAND(1, 1) == 0

    def test_nand_all_combinations(self, all_bit_pairs):
        """Test NAND with all input combinations."""
        expected = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0}
        for a, b in all_bit_pairs:
            assert NAND(a, b) == expected[(a, b)]


class TestNOR:
    """Tests for the NOR gate."""

    def test_nor_0_0(self):
        """NOR(0, 0) should return 1."""
        assert NOR(0, 0) == 1

    def test_nor_0_1(self):
        """NOR(0, 1) should return 0."""
        assert NOR(0, 1) == 0

    def test_nor_1_0(self):
        """NOR(1, 0) should return 0."""
        assert NOR(1, 0) == 0

    def test_nor_1_1(self):
        """NOR(1, 1) should return 0."""
        assert NOR(1, 1) == 0

    def test_nor_all_combinations(self, all_bit_pairs):
        """Test NOR with all input combinations."""
        expected = {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0}
        for a, b in all_bit_pairs:
            assert NOR(a, b) == expected[(a, b)]


class TestXOR:
    """Tests for the XOR gate."""

    def test_xor_0_0(self):
        """XOR(0, 0) should return 0."""
        assert XOR(0, 0) == 0

    def test_xor_0_1(self):
        """XOR(0, 1) should return 1."""
        assert XOR(0, 1) == 1

    def test_xor_1_0(self):
        """XOR(1, 0) should return 1."""
        assert XOR(1, 0) == 1

    def test_xor_1_1(self):
        """XOR(1, 1) should return 0."""
        assert XOR(1, 1) == 0

    def test_xor_all_combinations(self, all_bit_pairs):
        """Test XOR with all input combinations."""
        expected = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}
        for a, b in all_bit_pairs:
            assert XOR(a, b) == expected[(a, b)]


class TestXNOR:
    """Tests for the XNOR gate."""

    def test_xnor_0_0(self):
        """XNOR(0, 0) should return 1."""
        assert XNOR(0, 0) == 1

    def test_xnor_0_1(self):
        """XNOR(0, 1) should return 0."""
        assert XNOR(0, 1) == 0

    def test_xnor_1_0(self):
        """XNOR(1, 0) should return 0."""
        assert XNOR(1, 0) == 0

    def test_xnor_1_1(self):
        """XNOR(1, 1) should return 1."""
        assert XNOR(1, 1) == 1

    def test_xnor_all_combinations(self, all_bit_pairs):
        """Test XNOR with all input combinations."""
        expected = {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 1}
        for a, b in all_bit_pairs:
            assert XNOR(a, b) == expected[(a, b)]
