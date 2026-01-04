"""Tests for RAM."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.memory import RAM


def int_to_bits(value: int, n: int = 8) -> list:
    """Convert integer to bit list (LSB first)."""
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int(bits: list) -> int:
    """Convert bit list to integer."""
    return sum(bit << i for i, bit in enumerate(bits))


class TestRAM:
    """Tests for RAM."""

    def test_initial_zero(self):
        """All memory starts at zero."""
        ram = RAM()
        for addr in [0, 1, 127, 128, 255]:
            addr_bits = int_to_bits(addr, 8)
            assert bits_to_int(ram.read(addr_bits)) == 0

    def test_write_read(self):
        """Write and read back value."""
        ram = RAM()
        addr = int_to_bits(0x10, 8)
        data = int_to_bits(42, 8)
        ram.write(addr, data, 1)
        assert bits_to_int(ram.read(addr)) == 42

    def test_write_disabled(self):
        """Write with enable=0 does nothing."""
        ram = RAM()
        addr = int_to_bits(0x10, 8)
        data = int_to_bits(42, 8)
        ram.write(addr, data, 0)  # Disabled
        assert bits_to_int(ram.read(addr)) == 0

    def test_multiple_addresses(self):
        """Different addresses are independent."""
        ram = RAM()
        # Write to different addresses
        ram.write(int_to_bits(0x00, 8), int_to_bits(10, 8), 1)
        ram.write(int_to_bits(0x10, 8), int_to_bits(20, 8), 1)
        ram.write(int_to_bits(0xFF, 8), int_to_bits(30, 8), 1)
        # Read back
        assert bits_to_int(ram.read(int_to_bits(0x00, 8))) == 10
        assert bits_to_int(ram.read(int_to_bits(0x10, 8))) == 20
        assert bits_to_int(ram.read(int_to_bits(0xFF, 8))) == 30
        # Others still zero
        assert bits_to_int(ram.read(int_to_bits(0x50, 8))) == 0

    def test_overwrite(self):
        """Overwriting a location changes its value."""
        ram = RAM()
        addr = int_to_bits(0x20, 8)
        ram.write(addr, int_to_bits(100, 8), 1)
        ram.write(addr, int_to_bits(200, 8), 1)
        assert bits_to_int(ram.read(addr)) == 200

    def test_edge_values(self):
        """Test 0 and 255 data values."""
        ram = RAM()
        addr1 = int_to_bits(0x10, 8)
        addr2 = int_to_bits(0x11, 8)
        ram.write(addr1, int_to_bits(0, 8), 1)
        ram.write(addr2, int_to_bits(255, 8), 1)
        assert bits_to_int(ram.read(addr1)) == 0
        assert bits_to_int(ram.read(addr2)) == 255

    def test_load_program(self):
        """Load program loads bytes sequentially."""
        ram = RAM()
        program = [
            int_to_bits(0x12, 8),
            int_to_bits(0x34, 8),
            int_to_bits(0x56, 8),
        ]
        ram.load_program(program, start_addr=0)
        assert bits_to_int(ram.read(int_to_bits(0, 8))) == 0x12
        assert bits_to_int(ram.read(int_to_bits(1, 8))) == 0x34
        assert bits_to_int(ram.read(int_to_bits(2, 8))) == 0x56

    def test_load_program_offset(self):
        """Load program at non-zero address."""
        ram = RAM()
        program = [
            int_to_bits(0xAB, 8),
            int_to_bits(0xCD, 8),
        ]
        ram.load_program(program, start_addr=0x10)
        assert bits_to_int(ram.read(int_to_bits(0x10, 8))) == 0xAB
        assert bits_to_int(ram.read(int_to_bits(0x11, 8))) == 0xCD
        assert bits_to_int(ram.read(int_to_bits(0x00, 8))) == 0  # Before

    def test_all_addresses(self):
        """Can write to all 256 addresses."""
        ram = RAM()
        # Write unique value to each address
        for i in range(256):
            addr = int_to_bits(i, 8)
            data = int_to_bits(i, 8)
            ram.write(addr, data, 1)
        # Verify
        for i in range(256):
            addr = int_to_bits(i, 8)
            assert bits_to_int(ram.read(addr)) == i

    def test_dump(self):
        """Dump produces hex output."""
        ram = RAM()
        ram.write(int_to_bits(0, 8), int_to_bits(0xAB, 8), 1)
        ram.write(int_to_bits(1, 8), int_to_bits(0xCD, 8), 1)
        dump = ram.dump(0, 2)
        assert "AB" in dump or "ab" in dump.lower()
        assert "CD" in dump or "cd" in dump.lower()
