"""Tests for Data Path."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.datapath import DataPath
from computer.clock import ControlSignals


def int_to_bits(value: int, n: int = 8) -> list:
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int(bits: list) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


class TestDataPath:
    """Tests for Data Path."""

    def setup_method(self):
        """Create data path for each test."""
        self.dp = DataPath()

    def test_initial_pc_zero(self):
        """PC starts at zero."""
        assert bits_to_int(self.dp.get_pc()) == 0

    def test_initial_flags_zero(self):
        """Flags start at zero."""
        assert self.dp.flags == {'Z': 0, 'C': 0, 'N': 0, 'V': 0}

    def test_set_pc(self):
        """Can set PC to new value."""
        self.dp.set_pc(int_to_bits(0x10, 8))
        assert bits_to_int(self.dp.get_pc()) == 0x10

    def test_load_instruction(self):
        """Can load instruction into IR."""
        instr = int_to_bits(0x1234, 16)
        self.dp.load_instruction(instr)
        assert self.dp.ir == instr

    def test_register_file_accessible(self):
        """Can read/write register file."""
        addr = [1, 0, 0]  # R1
        data = int_to_bits(42, 8)
        self.dp.reg_file.write(addr, data, 1, 0)
        self.dp.reg_file.write(addr, data, 1, 1)
        assert bits_to_int(self.dp.reg_file.read(addr)) == 42

    def test_memory_accessible(self):
        """Can read/write memory."""
        addr = int_to_bits(0x10, 8)
        data = int_to_bits(100, 8)
        self.dp.memory.write(addr, data, 1)
        assert bits_to_int(self.dp.memory.read(addr)) == 100

    def test_alu_accessible(self):
        """Can use ALU."""
        a = int_to_bits(5, 8)
        b = int_to_bits(3, 8)
        op_add = [0, 0, 0, 0]
        result, flags = self.dp.alu(a, b, op_add)
        assert bits_to_int(result) == 8

    def test_fetch_instruction(self):
        """Can fetch instruction from memory."""
        # Load bytes at address 0
        self.dp.memory.write(int_to_bits(0, 8), int_to_bits(0x34, 8), 1)
        self.dp.memory.write(int_to_bits(1, 8), int_to_bits(0x12, 8), 1)
        instr = self.dp.fetch_instruction()
        # Should be 16 bits
        assert len(instr) == 16

    def test_execute_cycle_with_add(self):
        """Execute ADD stores result in register."""
        # Set up R1=10, R2=20
        addr_r1 = [1, 0, 0]
        addr_r2 = [0, 1, 0]
        self.dp.reg_file.write(addr_r1, int_to_bits(10, 8), 1, 0)
        self.dp.reg_file.write(addr_r1, int_to_bits(10, 8), 1, 1)
        self.dp.reg_file.write(addr_r2, int_to_bits(20, 8), 1, 0)
        self.dp.reg_file.write(addr_r2, int_to_bits(20, 8), 1, 1)

        # Execute ADD R0, R1, R2
        signals = ControlSignals()
        signals.reg_write = 1
        signals.alu_op = [0, 0, 0, 0]

        decoded = {
            'opcode_name': 'ADD',
            'rd': 0, 'rs1': 1, 'rs2_imm': 2,
            'rd_bits': [0, 0, 0],
            'rs1_bits': [1, 0, 0],
            'rs2_bits': [0, 1, 0],
        }

        self.dp.execute_cycle(signals, decoded)

        # R0 should be 30
        addr_r0 = [0, 0, 0]
        assert bits_to_int(self.dp.reg_file.read(addr_r0)) == 30

    def test_execute_cycle_updates_flags(self):
        """Execute cycle updates flags from ALU."""
        # Set up R1=0, R2=0
        addr_r1 = [1, 0, 0]
        addr_r2 = [0, 1, 0]
        self.dp.reg_file.write(addr_r1, int_to_bits(0, 8), 1, 0)
        self.dp.reg_file.write(addr_r1, int_to_bits(0, 8), 1, 1)
        self.dp.reg_file.write(addr_r2, int_to_bits(0, 8), 1, 0)
        self.dp.reg_file.write(addr_r2, int_to_bits(0, 8), 1, 1)

        signals = ControlSignals()
        signals.reg_write = 1
        signals.alu_op = [0, 0, 0, 0]

        decoded = {
            'opcode_name': 'ADD',
            'rd': 0, 'rs1': 1, 'rs2_imm': 2,
            'rd_bits': [0, 0, 0],
            'rs1_bits': [1, 0, 0],
            'rs2_bits': [0, 1, 0],
        }

        self.dp.execute_cycle(signals, decoded)

        # Result is 0, so Z flag should be set
        assert self.dp.flags['Z'] == 1
