"""
Instruction Set Architecture (ISA)

Defines the instruction format and opcodes for our 8-bit CPU.

Instruction Format (16 bits):
- Bits 15-12: Opcode (4 bits)
- Bits 11-8:  Rd (destination register)
- Bits 7-4:   Rs1 (source register 1)
- Bits 3-0:   Rs2/Imm (source register 2 or immediate)
"""

from typing import List, Dict


# Opcode definitions
OPCODES = {
    'NOP':   0b0000,
    'LOAD':  0b0001,
    'STORE': 0b0010,
    'MOV':   0b0011,
    'ADD':   0b0100,
    'SUB':   0b0101,
    'AND':   0b0110,
    'OR':    0b0111,
    'XOR':   0b1000,
    'NOT':   0b1001,
    'SHL':   0b1010,
    'SHR':   0b1011,
    'JMP':   0b1100,
    'JZ':    0b1101,
    'JNZ':   0b1110,
    'HALT':  0b1111,
}

# Reverse lookup
OPCODE_NAMES = {v: k for k, v in OPCODES.items()}


def encode_instruction(opcode: str, rd: int = 0, rs1: int = 0, rs2_imm: int = 0) -> List[int]:
    """Encode an instruction into 16 bits.

    Args:
        opcode: Instruction name (e.g., 'ADD')
        rd: Destination register (0-7)
        rs1: Source register 1 (0-7)
        rs2_imm: Source register 2 or immediate (0-15)

    Returns:
        16-bit instruction as list of bits (LSB at index 0)
    """
    # TODO: Implement instruction encoding
    pass


def decode_instruction(instruction: List[int]) -> Dict:
    """Decode a 16-bit instruction.

    Args:
        instruction: 16-bit instruction (LSB at index 0)

    Returns:
        Dictionary with opcode, rd, rs1, rs2_imm fields
    """
    # TODO: Implement instruction decoding
    pass


def int_to_bits_n(value: int, n: int) -> List[int]:
    """Convert integer to n-bit list (LSB first)."""
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int_n(bits: List[int]) -> int:
    """Convert bit list to integer."""
    return sum(bit << i for i, bit in enumerate(bits))
