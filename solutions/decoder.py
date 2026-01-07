"""Instruction Decoder - Solution File."""

from typing import List, Dict
from solutions.isa import OPCODE_NAMES, bits_to_int_n


class InstructionDecoder:
    """Decodes instructions into control signals."""

    def decode(self, instruction: List[int]) -> Dict:
        """Decode an instruction into control signals."""
        val = bits_to_int_n(instruction)
        opcode = (val >> 12) & 0xF
        opcode_name = OPCODE_NAMES.get(opcode, "UNKNOWN")
        rd = (val >> 8) & 0xF

        # Different formats for different instruction types
        if opcode_name in ["LOAD", "STORE", "JMP", "JZ", "JNZ"]:
            # I-type or J-type: 8-bit immediate in low byte
            rs1 = 0
            rs2_imm = val & 0xFF
        else:
            # R-type
            rs1 = (val >> 4) & 0xF
            rs2_imm = val & 0xF

        return {
            "opcode": opcode,
            "opcode_name": opcode_name,
            "rd": rd,
            "rs1": rs1,
            "rs2_imm": rs2_imm,
            "instruction_type": self.get_instruction_type(opcode),
            "rd_bits": [(rd >> i) & 1 for i in range(3)],
            "rs1_bits": [(rs1 >> i) & 1 for i in range(3)],
            "rs2_bits": [(rs2_imm >> i) & 1 for i in range(8)],  # 8 bits for addresses
        }

    def get_instruction_type(self, opcode: int) -> str:
        """Get instruction type from opcode."""
        if opcode == 0 or opcode == 15:  # NOP, HALT
            return "N"
        elif opcode in [1, 2]:  # LOAD, STORE
            return "I"
        elif opcode in [12, 13, 14]:  # JMP, JZ, JNZ
            return "J"
        else:  # ALU operations, MOV, NOT, SHL, SHR
            return "R"
