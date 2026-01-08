"""Instruction Decoder.

Decodes 16-bit instructions into their component fields
and instruction type.
"""

from typing import Dict, List

from computer.isa import OPCODE_NAMES, bits_to_int_n  # noqa: F401


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
        ...

    def get_instruction_type(self, opcode: int) -> str:
        """Determine instruction type from opcode.

        Types:
        - 'R': Register-register (ADD, SUB, AND, OR, XOR)
        - 'I': Immediate (LOAD, STORE, MOV)
        - 'J': Jump (JMP, JZ, JNZ)
        - 'N': No operands (NOP, HALT)
        """
        # TODO: Implement type detection
        ...
