"""Tests for registers."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.registers import Register8, RegisterFile


def int_to_bits(value: int, n: int = 8) -> list:
    """Convert integer to bit list (LSB first)."""
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int(bits: list) -> int:
    """Convert bit list to integer."""
    return sum(bit << i for i, bit in enumerate(bits))


class TestRegister8:
    """Tests for 8-bit register."""

    def test_initial_zero(self):
        """Register starts at zero."""
        reg = Register8()
        assert bits_to_int(reg.read()) == 0

    def test_write_value(self):
        """Writing a value stores it."""
        reg = Register8()
        data = int_to_bits(42, 8)
        reg.clock(data, 1, 0)  # CLK low
        reg.clock(data, 1, 1)  # Rising edge
        assert bits_to_int(reg.read()) == 42

    def test_write_disabled(self):
        """Writing with enable=0 does nothing."""
        reg = Register8()
        # First write 42
        data = int_to_bits(42, 8)
        reg.clock(data, 1, 0)
        reg.clock(data, 1, 1)
        # Try to write 100 with enable=0
        data = int_to_bits(100, 8)
        reg.clock(data, 0, 0)
        reg.clock(data, 0, 1)
        assert bits_to_int(reg.read()) == 42  # Still 42

    def test_overwrite(self):
        """Writing a new value overwrites old."""
        reg = Register8()
        # Write 10
        data = int_to_bits(10, 8)
        reg.clock(data, 1, 0)
        reg.clock(data, 1, 1)
        # Write 20
        data = int_to_bits(20, 8)
        reg.clock(data, 1, 0)
        reg.clock(data, 1, 1)
        assert bits_to_int(reg.read()) == 20

    def test_edge_values(self):
        """Test 0 and 255."""
        reg = Register8()
        # Write 0
        reg.clock(int_to_bits(0, 8), 1, 0)
        reg.clock(int_to_bits(0, 8), 1, 1)
        assert bits_to_int(reg.read()) == 0
        # Write 255
        reg.clock(int_to_bits(255, 8), 1, 0)
        reg.clock(int_to_bits(255, 8), 1, 1)
        assert bits_to_int(reg.read()) == 255


class TestRegisterFile:
    """Tests for register file."""

    def test_all_start_zero(self):
        """All registers start at zero."""
        rf = RegisterFile()
        for i in range(8):
            addr = int_to_bits(i, 3)
            assert bits_to_int(rf.read(addr)) == 0

    def test_write_read(self):
        """Write and read from register."""
        rf = RegisterFile()
        addr = int_to_bits(3, 3)  # R3
        data = int_to_bits(42, 8)
        rf.write(addr, data, 1, 0)
        rf.write(addr, data, 1, 1)
        assert bits_to_int(rf.read(addr)) == 42

    def test_independent_registers(self):
        """Registers are independent."""
        rf = RegisterFile()
        # Write 10 to R2
        rf.write(int_to_bits(2, 3), int_to_bits(10, 8), 1, 0)
        rf.write(int_to_bits(2, 3), int_to_bits(10, 8), 1, 1)
        # Write 20 to R5
        rf.write(int_to_bits(5, 3), int_to_bits(20, 8), 1, 0)
        rf.write(int_to_bits(5, 3), int_to_bits(20, 8), 1, 1)
        # Check both
        assert bits_to_int(rf.read(int_to_bits(2, 3))) == 10
        assert bits_to_int(rf.read(int_to_bits(5, 3))) == 20
        # Others still zero
        assert bits_to_int(rf.read(int_to_bits(0, 3))) == 0
        assert bits_to_int(rf.read(int_to_bits(7, 3))) == 0

    def test_read_two(self):
        """Read two registers simultaneously."""
        rf = RegisterFile()
        # Write values
        rf.write(int_to_bits(1, 3), int_to_bits(15, 8), 1, 0)
        rf.write(int_to_bits(1, 3), int_to_bits(15, 8), 1, 1)
        rf.write(int_to_bits(4, 3), int_to_bits(25, 8), 1, 0)
        rf.write(int_to_bits(4, 3), int_to_bits(25, 8), 1, 1)
        # Read both
        a, b = rf.read_two(int_to_bits(1, 3), int_to_bits(4, 3))
        assert bits_to_int(a) == 15
        assert bits_to_int(b) == 25

    def test_write_disabled(self):
        """Write with enable=0 does nothing."""
        rf = RegisterFile()
        addr = int_to_bits(3, 3)
        # Write 50
        rf.write(addr, int_to_bits(50, 8), 1, 0)
        rf.write(addr, int_to_bits(50, 8), 1, 1)
        # Try to write 100 disabled
        rf.write(addr, int_to_bits(100, 8), 0, 0)
        rf.write(addr, int_to_bits(100, 8), 0, 1)
        assert bits_to_int(rf.read(addr)) == 50

    def test_all_registers(self):
        """Write and read all 8 registers."""
        rf = RegisterFile()
        # Write i*10 to each register
        for i in range(8):
            addr = int_to_bits(i, 3)
            data = int_to_bits(i * 10, 8)
            rf.write(addr, data, 1, 0)
            rf.write(addr, data, 1, 1)
        # Read back
        for i in range(8):
            addr = int_to_bits(i, 3)
            assert bits_to_int(rf.read(addr)) == i * 10
