"""Tests for ISA (Instruction Set Architecture)."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.isa import OPCODES, OPCODE_NAMES, encode_instruction, decode_instruction


def bits_to_int(bits: list) -> int:
    """Convert bit list to integer."""
    return sum(bit << i for i, bit in enumerate(bits))


class TestOpcodes:
    """Tests for opcode definitions."""

    def test_all_opcodes_defined(self):
        """All 16 opcodes are defined."""
        expected = ['NOP', 'LOAD', 'STORE', 'MOV', 'ADD', 'SUB', 'AND', 'OR',
                   'XOR', 'NOT', 'SHL', 'SHR', 'JMP', 'JZ', 'JNZ', 'HALT']
        for name in expected:
            assert name in OPCODES

    def test_opcodes_unique(self):
        """All opcode values are unique."""
        values = list(OPCODES.values())
        assert len(values) == len(set(values))

    def test_opcodes_in_range(self):
        """All opcodes fit in 4 bits (0-15)."""
        for code in OPCODES.values():
            assert 0 <= code <= 15

    def test_reverse_lookup(self):
        """OPCODE_NAMES provides reverse lookup."""
        for name, code in OPCODES.items():
            assert OPCODE_NAMES[code] == name


class TestEncodeInstruction:
    """Tests for instruction encoding."""

    def test_encode_nop(self):
        """NOP encodes correctly."""
        instr = encode_instruction('NOP')
        val = bits_to_int(instr)
        assert (val >> 12) == OPCODES['NOP']

    def test_encode_halt(self):
        """HALT encodes correctly."""
        instr = encode_instruction('HALT')
        val = bits_to_int(instr)
        assert (val >> 12) == OPCODES['HALT']

    def test_encode_add(self):
        """ADD R0, R1, R2 encodes correctly."""
        instr = encode_instruction('ADD', rd=0, rs1=1, rs2_imm=2)
        val = bits_to_int(instr)
        assert (val >> 12) & 0xF == OPCODES['ADD']
        assert (val >> 8) & 0xF == 0   # rd
        assert (val >> 4) & 0xF == 1   # rs1
        assert val & 0xF == 2           # rs2

    def test_encode_load(self):
        """LOAD R3, 5 encodes correctly."""
        instr = encode_instruction('LOAD', rd=3, rs2_imm=5)
        val = bits_to_int(instr)
        assert (val >> 12) & 0xF == OPCODES['LOAD']
        assert (val >> 8) & 0xF == 3   # rd
        assert val & 0xF == 5           # address

    def test_encode_jmp(self):
        """JMP 0x0F encodes correctly."""
        instr = encode_instruction('JMP', rs2_imm=0x0F)
        val = bits_to_int(instr)
        assert (val >> 12) & 0xF == OPCODES['JMP']
        assert val & 0xF == 0x0F

    def test_encode_16_bits(self):
        """Instructions are 16 bits."""
        instr = encode_instruction('ADD', rd=7, rs1=7, rs2_imm=15)
        assert len(instr) == 16


class TestDecodeInstruction:
    """Tests for instruction decoding."""

    def test_decode_returns_dict(self):
        """Decode returns dictionary with required fields."""
        instr = encode_instruction('ADD', rd=0, rs1=1, rs2_imm=2)
        decoded = decode_instruction(instr)
        assert 'opcode' in decoded
        assert 'opcode_name' in decoded
        assert 'rd' in decoded
        assert 'rs1' in decoded
        assert 'rs2_imm' in decoded

    def test_decode_add(self):
        """Decode ADD instruction."""
        instr = encode_instruction('ADD', rd=3, rs1=4, rs2_imm=5)
        decoded = decode_instruction(instr)
        assert decoded['opcode'] == OPCODES['ADD']
        assert decoded['opcode_name'] == 'ADD'
        assert decoded['rd'] == 3
        assert decoded['rs1'] == 4
        assert decoded['rs2_imm'] == 5

    def test_decode_jmp(self):
        """Decode JMP instruction."""
        instr = encode_instruction('JMP', rs2_imm=10)
        decoded = decode_instruction(instr)
        assert decoded['opcode_name'] == 'JMP'
        assert decoded['rs2_imm'] == 10

    def test_encode_decode_roundtrip(self):
        """Encode then decode preserves information."""
        test_cases = [
            ('NOP', 0, 0, 0),
            ('ADD', 1, 2, 3),
            ('SUB', 7, 6, 5),
            ('LOAD', 4, 0, 12),
            ('JMP', 0, 0, 15),
            ('HALT', 0, 0, 0),
        ]
        for opname, rd, rs1, rs2 in test_cases:
            instr = encode_instruction(opname, rd=rd, rs1=rs1, rs2_imm=rs2)
            decoded = decode_instruction(instr)
            assert decoded['opcode_name'] == opname
            assert decoded['rd'] == rd
            assert decoded['rs1'] == rs1
            assert decoded['rs2_imm'] == rs2
