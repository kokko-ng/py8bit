"""Tests for Assembler."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.assembler import Assembler
from computer.isa import OPCODES


def bits_to_int(bits: list) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


class TestAssembler:
    """Tests for Assembler."""

    def setup_method(self):
        """Create assembler for each test."""
        self.asm = Assembler()

    def test_assemble_nop(self):
        """Assemble NOP instruction."""
        code = self.asm.assemble("NOP")
        assert len(code) == 1
        val = bits_to_int(code[0])
        assert (val >> 12) == OPCODES['NOP']

    def test_assemble_halt(self):
        """Assemble HALT instruction."""
        code = self.asm.assemble("HALT")
        assert len(code) == 1
        val = bits_to_int(code[0])
        assert (val >> 12) == OPCODES['HALT']

    def test_assemble_add(self):
        """Assemble ADD with registers."""
        code = self.asm.assemble("ADD R0, R1, R2")
        assert len(code) == 1
        val = bits_to_int(code[0])
        assert (val >> 12) == OPCODES['ADD']
        assert ((val >> 8) & 0xF) == 0  # rd
        assert ((val >> 4) & 0xF) == 1  # rs1
        assert (val & 0xF) == 2          # rs2

    def test_assemble_load(self):
        """Assemble LOAD instruction."""
        code = self.asm.assemble("LOAD R3, 0x10")
        assert len(code) == 1
        val = bits_to_int(code[0])
        assert (val >> 12) == OPCODES['LOAD']
        assert ((val >> 8) & 0xF) == 3  # rd

    def test_assemble_jmp(self):
        """Assemble JMP instruction."""
        code = self.asm.assemble("JMP 0x08")
        assert len(code) == 1
        val = bits_to_int(code[0])
        assert (val >> 12) == OPCODES['JMP']
        assert (val & 0xF) == 8

    def test_ignore_comments(self):
        """Comments are ignored."""
        code = self.asm.assemble("; This is a comment\nNOP ; inline comment")
        assert len(code) == 1

    def test_ignore_empty_lines(self):
        """Empty lines are ignored."""
        code = self.asm.assemble("NOP\n\n\nHALT")
        assert len(code) == 2

    def test_label_recorded(self):
        """Labels are recorded in symbol table."""
        self.asm.assemble("start:\n    NOP\nend:\n    HALT")
        assert 'start' in self.asm.symbol_table
        assert 'end' in self.asm.symbol_table
        assert self.asm.symbol_table['start'] == 0
        assert self.asm.symbol_table['end'] == 2

    def test_label_resolution(self):
        """Labels can be used as operands."""
        code = self.asm.assemble("loop:\n    JMP loop")
        assert len(code) == 1
        val = bits_to_int(code[0])
        # JMP should jump to address 0 (where loop is)
        assert (val & 0xF) == 0

    def test_multiple_instructions(self):
        """Multiple instructions assembled."""
        source = """
            LOAD R1, 0x10
            LOAD R2, 0x11
            ADD R0, R1, R2
            HALT
        """
        code = self.asm.assemble(source)
        assert len(code) == 4

    def test_case_insensitive(self):
        """Mnemonics are case insensitive."""
        code1 = self.asm.assemble("ADD R0, R1, R2")
        code2 = self.asm.assemble("add r0, r1, r2")
        assert bits_to_int(code1[0]) == bits_to_int(code2[0])

    def test_hex_values(self):
        """Hex values with 0x prefix work."""
        code = self.asm.assemble("LOAD R0, 0x0F")
        val = bits_to_int(code[0])
        assert (val & 0xF) == 0x0F

    def test_decimal_values(self):
        """Decimal values work."""
        code = self.asm.assemble("LOAD R0, 5")
        val = bits_to_int(code[0])
        assert (val & 0xF) == 5
