"""Tests for Instruction Decoder."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.decoder import InstructionDecoder
from computer.isa import OPCODES, encode_instruction


class TestInstructionDecoder:
    """Tests for Instruction Decoder."""

    def setup_method(self):
        """Create decoder for each test."""
        self.decoder = InstructionDecoder()

    def test_decode_returns_dict(self):
        """Decode returns dictionary."""
        instr = encode_instruction('NOP')
        result = self.decoder.decode(instr)
        assert isinstance(result, dict)

    def test_decode_has_required_fields(self):
        """Decode returns all required fields."""
        instr = encode_instruction('ADD', rd=0, rs1=1, rs2_imm=2)
        result = self.decoder.decode(instr)
        assert 'opcode' in result
        assert 'opcode_name' in result
        assert 'rd' in result
        assert 'rs1' in result
        assert 'rs2_imm' in result
        assert 'instruction_type' in result

    def test_decode_add(self):
        """Decode ADD instruction correctly."""
        instr = encode_instruction('ADD', rd=3, rs1=4, rs2_imm=5)
        result = self.decoder.decode(instr)
        assert result['opcode'] == OPCODES['ADD']
        assert result['opcode_name'] == 'ADD'
        assert result['rd'] == 3
        assert result['rs1'] == 4
        assert result['rs2_imm'] == 5
        assert result['instruction_type'] == 'R'

    def test_decode_load(self):
        """Decode LOAD instruction correctly."""
        instr = encode_instruction('LOAD', rd=2, rs2_imm=10)
        result = self.decoder.decode(instr)
        assert result['opcode_name'] == 'LOAD'
        assert result['rd'] == 2
        assert result['rs2_imm'] == 10
        assert result['instruction_type'] == 'I'

    def test_decode_jmp(self):
        """Decode JMP instruction correctly."""
        instr = encode_instruction('JMP', rs2_imm=8)
        result = self.decoder.decode(instr)
        assert result['opcode_name'] == 'JMP'
        assert result['rs2_imm'] == 8
        assert result['instruction_type'] == 'J'

    def test_decode_halt(self):
        """Decode HALT instruction correctly."""
        instr = encode_instruction('HALT')
        result = self.decoder.decode(instr)
        assert result['opcode_name'] == 'HALT'
        assert result['instruction_type'] == 'N'

    def test_decode_nop(self):
        """Decode NOP instruction correctly."""
        instr = encode_instruction('NOP')
        result = self.decoder.decode(instr)
        assert result['opcode_name'] == 'NOP'
        assert result['instruction_type'] == 'N'

    def test_instruction_type_r(self):
        """R-type for ALU operations."""
        for op in ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'NOT', 'SHL', 'SHR']:
            instr = encode_instruction(op, rd=0, rs1=1, rs2_imm=2)
            result = self.decoder.decode(instr)
            assert result['instruction_type'] == 'R', f"Failed for {op}"

    def test_instruction_type_i(self):
        """I-type for memory operations."""
        for op in ['LOAD', 'STORE', 'MOV']:
            instr = encode_instruction(op, rd=0, rs1=1, rs2_imm=2)
            result = self.decoder.decode(instr)
            assert result['instruction_type'] == 'I', f"Failed for {op}"

    def test_instruction_type_j(self):
        """J-type for jumps."""
        for op in ['JMP', 'JZ', 'JNZ']:
            instr = encode_instruction(op, rs2_imm=5)
            result = self.decoder.decode(instr)
            assert result['instruction_type'] == 'J', f"Failed for {op}"

    def test_decode_has_bit_fields(self):
        """Decode includes bit field representations."""
        instr = encode_instruction('ADD', rd=7, rs1=6, rs2_imm=5)
        result = self.decoder.decode(instr)
        assert 'rd_bits' in result
        assert 'rs1_bits' in result
        assert 'rs2_bits' in result
        # Check bits represent correct values
        rd_val = sum(b << i for i, b in enumerate(result['rd_bits'][:4]))
        assert rd_val == 7
