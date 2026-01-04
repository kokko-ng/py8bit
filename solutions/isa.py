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
    op = OPCODES.get(opcode.upper(), 0)
    instruction = (
        (rs2_imm & 0xF) |
        ((rs1 & 0xF) << 4) |
        ((rd & 0xF) << 8) |
        ((op & 0xF) << 12)
    )
    return int_to_bits_n(instruction, 16)


def decode_instruction(instruction: List[int]) -> Dict:
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
    }
