"""
ISA - Solution File
"""

from typing import List, Dict


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

OPCODE_NAMES = {v: k for k, v in OPCODES.items()}


def int_to_bits_n(value: int, n: int) -> List[int]:
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int_n(bits: List[int]) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


def encode_instruction(opcode: str, rd: int = 0, rs1: int = 0, rs2_imm: int = 0) -> List[int]:
    """Encode an instruction into 16 bits.

    Instruction formats:
    - R-type (ALU ops): opcode(4) + rd(4) + rs1(4) + rs2(4)
    - I-type (LOAD/STORE): opcode(4) + rd(4) + addr(8)
    - J-type (JMP/JZ/JNZ): opcode(4) + unused(4) + addr(8)
    """
    op = OPCODES.get(opcode.upper(), 0)
    op_name = opcode.upper()

    if op_name in ['LOAD', 'STORE']:
        # I-type: 8-bit address in low byte
        instruction = (
            (rs2_imm & 0xFF) |
            ((rd & 0xF) << 8) |
            ((op & 0xF) << 12)
        )
    elif op_name in ['JMP', 'JZ', 'JNZ']:
        # J-type: 8-bit address in low byte
        instruction = (
            (rs2_imm & 0xFF) |
            ((op & 0xF) << 12)
        )
    else:
        # R-type: standard format
        instruction = (
            (rs2_imm & 0xF) |
            ((rs1 & 0xF) << 4) |
            ((rd & 0xF) << 8) |
            ((op & 0xF) << 12)
        )
    return int_to_bits_n(instruction, 16)


def decode_instruction(instruction: List[int]) -> Dict:
    """Decode a 16-bit instruction."""
    val = bits_to_int_n(instruction)
    opcode = (val >> 12) & 0xF
    opcode_name = OPCODE_NAMES.get(opcode, 'UNKNOWN')
    rd = (val >> 8) & 0xF

    if opcode_name in ['LOAD', 'STORE', 'JMP', 'JZ', 'JNZ']:
        # I-type or J-type: 8-bit immediate
        rs1 = 0
        rs2_imm = val & 0xFF
    else:
        # R-type
        rs1 = (val >> 4) & 0xF
        rs2_imm = val & 0xF

    return {
        'opcode': opcode,
        'opcode_name': opcode_name,
        'rd': rd,
        'rs1': rs1,
        'rs2_imm': rs2_imm,
    }
