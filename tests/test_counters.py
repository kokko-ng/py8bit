"""Tests for counters."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.counters import BinaryCounter8, ProgramCounter


def int_to_bits(value: int, n: int = 8) -> list:
    """Convert integer to bit list (LSB first)."""
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int(bits: list) -> int:
    """Convert bit list to integer."""
    return sum(bit << i for i, bit in enumerate(bits))


class TestBinaryCounter8:
    """Tests for 8-bit binary counter."""

    def test_initial_zero(self):
        """Counter starts at zero."""
        counter = BinaryCounter8()
        assert bits_to_int(counter.read()) == 0

    def test_count_up(self):
        """Counter increments on each clock."""
        counter = BinaryCounter8()
        for expected in range(1, 11):
            counter.clock(enable=1, reset=0)
            assert bits_to_int(counter.read()) == expected

    def test_hold_disabled(self):
        """Counter holds when disabled."""
        counter = BinaryCounter8()
        counter.clock(1, 0)  # Count to 1
        counter.clock(1, 0)  # Count to 2
        counter.clock(0, 0)  # Hold (disabled)
        assert bits_to_int(counter.read()) == 2
        counter.clock(0, 0)  # Still hold
        assert bits_to_int(counter.read()) == 2

    def test_reset(self):
        """Reset clears counter to zero."""
        counter = BinaryCounter8()
        for _ in range(5):
            counter.clock(1, 0)
        counter.clock(0, 1)  # Reset
        assert bits_to_int(counter.read()) == 0

    def test_reset_priority(self):
        """Reset takes priority over enable."""
        counter = BinaryCounter8()
        counter.clock(1, 0)  # Count to 1
        counter.clock(1, 1)  # Reset (even with enable=1)
        assert bits_to_int(counter.read()) == 0

    def test_overflow(self):
        """Counter wraps from 255 to 0."""
        counter = BinaryCounter8()
        counter.count = int_to_bits(255, 8)
        counter.clock(1, 0)  # Should wrap to 0
        assert bits_to_int(counter.read()) == 0


class TestProgramCounter:
    """Tests for Program Counter."""

    def test_initial_zero(self):
        """PC starts at zero."""
        pc = ProgramCounter()
        assert bits_to_int(pc.read()) == 0

    def test_increment(self):
        """PC increments."""
        pc = ProgramCounter()
        zero = [0] * 8
        for expected in range(1, 6):
            pc.clock(load=0, load_value=zero, increment=1, reset=0, clk=1)
            assert bits_to_int(pc.read()) == expected

    def test_load(self):
        """PC loads new value."""
        pc = ProgramCounter()
        addr = int_to_bits(0x20, 8)
        pc.clock(load=1, load_value=addr, increment=0, reset=0, clk=1)
        assert bits_to_int(pc.read()) == 0x20

    def test_reset(self):
        """PC resets to zero."""
        pc = ProgramCounter()
        # First increment
        zero = [0] * 8
        for _ in range(5):
            pc.clock(0, zero, 1, 0, 1)
        # Reset
        pc.clock(0, zero, 0, 1, 1)
        assert bits_to_int(pc.read()) == 0

    def test_reset_priority(self):
        """Reset takes priority over load and increment."""
        pc = ProgramCounter()
        zero = [0] * 8
        pc.clock(0, zero, 1, 0, 1)  # Count to 1
        addr = int_to_bits(0x50, 8)
        pc.clock(1, addr, 1, 1, 1)  # Reset wins
        assert bits_to_int(pc.read()) == 0

    def test_load_priority(self):
        """Load takes priority over increment."""
        pc = ProgramCounter()
        addr = int_to_bits(0x30, 8)
        pc.clock(load=1, load_value=addr, increment=1, reset=0, clk=1)
        assert bits_to_int(pc.read()) == 0x30

    def test_hold(self):
        """PC holds when no operation."""
        pc = ProgramCounter()
        zero = [0] * 8
        pc.clock(0, zero, 1, 0, 1)  # Count to 1
        pc.clock(0, zero, 0, 0, 1)  # Hold
        assert bits_to_int(pc.read()) == 1
        pc.clock(0, zero, 0, 0, 1)  # Hold
        assert bits_to_int(pc.read()) == 1

    def test_jump_and_continue(self):
        """PC can jump and continue from new address."""
        pc = ProgramCounter()
        zero = [0] * 8
        # Increment a few times
        for _ in range(3):
            pc.clock(0, zero, 1, 0, 1)
        assert bits_to_int(pc.read()) == 3
        # Jump to 0x10
        addr = int_to_bits(0x10, 8)
        pc.clock(1, addr, 0, 0, 1)
        assert bits_to_int(pc.read()) == 0x10
        # Continue from there
        pc.clock(0, zero, 1, 0, 1)
        assert bits_to_int(pc.read()) == 0x11
