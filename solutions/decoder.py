"""
Instruction Decoder - Solution File
"""

from typing import List, Dict
from solutions.isa import OPCODE_NAMES, bits_to_int_n


class InstructionDecoder:
    """Decodes instructions into control signals."""

    def decode(self, instruction: List[int]) -> Dict:
        val = bits_to_int_n(instruction)
        opcode = (val >> 12) & 0xF
        rd = (val >> 8) & 0xF
        rs1 = (val >> 4) & 0xF
        rs2_imm = val & 0xF

        return {
            'opcode': opcode,
            'opcode_name': OPCODE_NAMES.get(opcode, 'UNKNOWN'),
            'rd': rd,
            'rs1': rs1,
            'rs2_imm': rs2_imm,
            'instruction_type': self.get_instruction_type(opcode),
            'rd_bits': [(rd >> i) & 1 for i in range(4)],
            'rs1_bits': [(rs1 >> i) & 1 for i in range(4)],
            'rs2_bits': [(rs2_imm >> i) & 1 for i in range(4)],
        }

    def get_instruction_type(self, opcode: int) -> str:
        if opcode == 0 or opcode == 15:  # NOP, HALT
            return 'N'
        elif opcode in [1, 2, 3]:  # LOAD, STORE, MOV
            return 'I'
        elif opcode in [12, 13, 14]:  # JMP, JZ, JNZ
            return 'J'
        else:  # ALU operations
            return 'R'
