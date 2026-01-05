"""
Instruction Decoder

Decodes 16-bit instructions into their component fields
and instruction type.
"""

from typing import List, Dict
from computer.isa import OPCODE_NAMES
from computer import bits_to_int


class InstructionDecoder:
    """Decodes instructions into control signals."""

    def decode(self, instruction: List[int]) -> Dict:
        """Decode a 16-bit instruction.

        Args:
            instruction: 16-bit instruction (LSB at index 0)

        Returns:
            Dictionary with decoded fields
        """
        # TODO: Implement instruction decoding
        # Convert bits to integer
        val = bits_to_int(instruction)

        # Extract opcode (bits 15-12)
        opcode = (val >> 12) & 0xF
        opcode_name = OPCODE_NAMES.get(opcode, 'UNKNOWN')

        # Extract rd (bits 11-8)
        rd = (val >> 8) & 0xF

        # Different formats for different instruction types
        if opcode_name in ['LOAD', 'STORE', 'JMP', 'JZ', 'JNZ']:
            # I-type or J-type: 8-bit immediate/address in low byte
            rs1 = 0
            rs2_imm = val & 0xFF
        else:
            # R-type: rs1 in bits 7-4, rs2 in bits 3-0
            rs1 = (val >> 4) & 0xF
            rs2_imm = val & 0xF

        return {
            'opcode': opcode,
            'opcode_name': opcode_name,
            'rd': rd,
            'rs1': rs1,
            'rs2_imm': rs2_imm,
            'instruction_type': self.get_instruction_type(opcode),
            'rd_bits': [(rd >> i) & 1 for i in range(3)],
            'rs1_bits': [(rs1 >> i) & 1 for i in range(3)],
            'rs2_bits': [(rs2_imm >> i) & 1 for i in range(8)],
        }

    def get_instruction_type(self, opcode: int) -> str:
        """Determine instruction type from opcode.

        Types:
        - 'R': Register-register (ADD, SUB, AND, OR, XOR)
        - 'I': Immediate (LOAD, STORE, MOV)
        - 'J': Jump (JMP, JZ, JNZ)
        - 'N': No operands (NOP, HALT)
        """
        # TODO: Implement type detection
        if opcode == 0 or opcode == 15:  # NOP, HALT
            return 'N'
        elif opcode in [1, 2]:  # LOAD, STORE
            return 'I'
        elif opcode in [12, 13, 14]:  # JMP, JZ, JNZ
            return 'J'
        else:  # ALU operations, MOV, NOT, SHL, SHR
            return 'R'
