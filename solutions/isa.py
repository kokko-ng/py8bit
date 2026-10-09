"""Instruction Set Architecture (ISA).

Defines the instruction format and opcodes for our 8-bit CPU.

Instruction Formats (16 bits):

R-type (ALU operations like ADD, SUB, AND, OR, XOR):
- Bits 15-12: Opcode (4 bits)
- Bits 11-8:  Rd (destination register, 4 bits)
- Bits 7-4:   Rs1 (source register 1, 4 bits)
- Bits 3-0:   Rs2 (source register 2, 4 bits)

I-type (LOAD, STORE):
- Bits 15-12: Opcode (4 bits)
- Bits 11-8:  Rd/Rs (register, 4 bits)
- Bits 7-0:   Address (8 bits, allows 0-255)

J-type (JMP, JZ, JNZ):
- Bits 15-12: Opcode (4 bits)
- Bits 11-8:  Unused (4 bits)
- Bits 7-0:   Address (8 bits)

N-type (NOP, HALT, MOV, NOT, SHL, SHR):
- Bits 15-12: Opcode (4 bits)
- Bits 11-0:  Depends on instruction
"""

from typing import Any

OPCODES = {
    "NOP": 0b0000,
    "LOAD": 0b0001,
    "STORE": 0b0010,
    "MOV": 0b0011,
    "ADD": 0b0100,
    "SUB": 0b0101,
    "AND": 0b0110,
    "OR": 0b0111,
    "XOR": 0b1000,
    "NOT": 0b1001,
    "SHL": 0b1010,
    "SHR": 0b1011,
    "JMP": 0b1100,
    "JZ": 0b1101,
    "JNZ": 0b1110,
    "HALT": 0b1111,
}

OPCODE_NAMES = {v: k for k, v in OPCODES.items()}


def int_to_bits_n(value: int, n: int) -> list[int]:
    """Convert integer to n-bit list (LSB first)."""
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int_n(bits: list[int]) -> int:
    """Convert bit list to integer."""
    return sum(bit << i for i, bit in enumerate(bits))


def encode_instruction(opcode: str, rd: int = 0, rs1: int = 0, rs2_imm: int = 0) -> list[int]:
    """Encode an instruction into 16 bits.

    Args:
        opcode: Instruction name (e.g., 'ADD', 'LOAD', 'JMP')
        rd: Destination/source register (0-7)
        rs1: Source register 1 (0-7, for R-type instructions)
        rs2_imm: Source register 2 (0-7 for R-type) or address (0-255 for I/J-type)

    Returns:
        16-bit instruction as list of bits (LSB at index 0)

    Note:
        For LOAD/STORE/JMP/JZ/JNZ, rs2_imm is an 8-bit address (0-255).
        For R-type instructions (ADD, SUB, etc.), rs2_imm is a 4-bit register number.
    """
    op = OPCODES.get(opcode.upper(), 0)
    op_name = opcode.upper()

    if op_name in ["LOAD", "STORE"]:
        # I-type: 8-bit address in low byte
        instruction = (rs2_imm & 0xFF) | ((rd & 0xF) << 8) | ((op & 0xF) << 12)
    elif op_name in ["JMP", "JZ", "JNZ"]:
        # J-type: 8-bit address in low byte
        instruction = (rs2_imm & 0xFF) | ((op & 0xF) << 12)
    else:
        # R-type: standard format
        instruction = (rs2_imm & 0xF) | ((rs1 & 0xF) << 4) | ((rd & 0xF) << 8) | ((op & 0xF) << 12)
    return int_to_bits_n(instruction, 16)


def decode_instruction(instruction: list[int]) -> dict[str, Any]:
    """Decode a 16-bit instruction.

    Args:
        instruction: 16-bit instruction (LSB at index 0)

    Returns:
        Dictionary with opcode, rd, rs1, rs2_imm fields
    """
    val = bits_to_int_n(instruction)
    opcode = (val >> 12) & 0xF
    opcode_name = OPCODE_NAMES.get(opcode, "UNKNOWN")
    rd = (val >> 8) & 0xF

    if opcode_name in ["LOAD", "STORE", "JMP", "JZ", "JNZ"]:
        # I-type or J-type: 8-bit immediate
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
    }


def disassemble(instruction: list[int]) -> str:
    """Convert a 16-bit instruction back into assembly text.

    This is the inverse of the assembler's job. Examples:

    - ``ADD R0, R1, R2``   (R-type: three registers)
    - ``MOV R1, R2``       (two registers)
    - ``LOAD R1, 0x10``    (I-type: register and 8-bit address in hex)
    - ``JMP 0x0C``         (J-type: 8-bit target address in hex)
    - ``NOP`` / ``HALT``   (no operands)

    Args:
        instruction: 16-bit instruction (LSB at index 0)

    Returns:
        Assembly text for the instruction
    """
    decoded = decode_instruction(instruction)
    name: str = decoded["opcode_name"]
    rd = decoded["rd"]
    rs1 = decoded["rs1"]
    rs2_imm = decoded["rs2_imm"]

    if name in ("NOP", "HALT"):
        return name
    if name in ("LOAD", "STORE"):
        return f"{name} R{rd}, 0x{rs2_imm:02X}"
    if name in ("JMP", "JZ", "JNZ"):
        return f"{name} 0x{rs2_imm:02X}"
    if name in ("MOV", "NOT", "SHL", "SHR"):
        return f"{name} R{rd}, R{rs1}"
    # R-type ALU operations: ADD, SUB, AND, OR, XOR
    return f"{name} R{rd}, R{rs1}, R{rs2_imm}"
