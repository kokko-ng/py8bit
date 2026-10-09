"""Instruction Decoder.

Decodes 16-bit instructions into their component fields
and instruction type.
"""

from typing import Any

from solutions.isa import OPCODE_NAMES, bits_to_int_n


class InstructionDecoder:
    """Decodes instructions into control signals."""

    def decode(self, instruction: list[int]) -> dict[str, Any]:
        """Decode a 16-bit instruction.

        Args:
            instruction: 16-bit instruction (LSB at index 0)

        Returns:
            Dictionary with decoded fields
        """
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
        """Determine instruction type from opcode.

        Types:
        - 'R': Register-register (ADD, SUB, AND, OR, XOR)
        - 'I': Immediate (LOAD, STORE, MOV)
        - 'J': Jump (JMP, JZ, JNZ)
        - 'N': No operands (NOP, HALT)
        """
        if opcode == 0 or opcode == 15:  # NOP, HALT
            return "N"
        if opcode in [1, 2]:  # LOAD, STORE
            return "I"
        if opcode in [12, 13, 14]:  # JMP, JZ, JNZ
            return "J"
        # ALU operations, MOV, NOT, SHL, SHR
        return "R"
