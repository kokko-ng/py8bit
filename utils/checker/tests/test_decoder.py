"""Test cases for instruction decoder."""

from ..helpers import assert_eq, assert_true, bits_to_int, int_to_bits


def get_tests() -> dict:
    """Return all test cases for decoder."""
    from computer.decoder import InstructionDecoder

    return {
        # Decode instructions
        "Decoder_decode_NOP": lambda: _test_decode_nop(),
        "Decoder_decode_ADD": lambda: _test_decode_add(),
        "Decoder_decode_HALT": lambda: _test_decode_halt(),
        "Decoder_decode_JMP": lambda: _test_decode_jmp(),
        "Decoder_decode_LOAD": lambda: _test_decode_load(),
    }


def _test_decode_nop():
    """Test decoding NOP instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES

    decoder = InstructionDecoder()
    nop_instr = int_to_bits(OPCODES["NOP"] << 12, 16)
    decoded = decoder.decode(nop_instr)
    assert_true(decoded is not None, "decode() returned None")
    assert_eq(decoded["opcode"], OPCODES["NOP"])
    assert_eq(decoded["opcode_name"], "NOP")
    assert_eq(decoded["instruction_type"], "N")


def _test_decode_add():
    """Test decoding ADD instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES

    decoder = InstructionDecoder()
    # ADD rd=1, rs1=2, rs2=3
    instr = (OPCODES["ADD"] << 12) | (1 << 8) | (2 << 4) | 3
    add_instr = int_to_bits(instr, 16)
    decoded = decoder.decode(add_instr)
    assert_true(decoded is not None, "decode() returned None")
    assert_eq(decoded["opcode"], OPCODES["ADD"])
    assert_eq(decoded["opcode_name"], "ADD")
    assert_eq(decoded["instruction_type"], "R")
    assert_eq(decoded["rd"], 1)
    assert_eq(decoded["rs1"], 2)
    assert_eq(decoded["rs2_imm"], 3)
    assert_eq(bits_to_int(decoded["rd_bits"][:3]), 1)
    assert_eq(bits_to_int(decoded["rs1_bits"][:3]), 2)
    assert_eq(bits_to_int(decoded["rs2_bits"][:3]), 3)


def _test_decode_halt():
    """Test decoding HALT instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES

    decoder = InstructionDecoder()
    halt_instr = int_to_bits(OPCODES["HALT"] << 12, 16)
    decoded = decoder.decode(halt_instr)
    assert_true(decoded is not None, "decode() returned None")
    assert_eq(decoded["opcode"], OPCODES["HALT"])
    assert_eq(decoded["opcode_name"], "HALT")
    assert_eq(decoded["instruction_type"], "N")


def _test_decode_jmp():
    """Test decoding JMP instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES

    decoder = InstructionDecoder()
    # JMP to address 100
    instr = (OPCODES["JMP"] << 12) | 100
    jmp_instr = int_to_bits(instr, 16)
    decoded = decoder.decode(jmp_instr)
    assert_true(decoded is not None, "decode() returned None")
    assert_eq(decoded["opcode"], OPCODES["JMP"])
    assert_eq(decoded["opcode_name"], "JMP")
    assert_eq(decoded["instruction_type"], "J")
    assert_eq(decoded["rs2_imm"], 100)


def _test_decode_load():
    """Test decoding LOAD instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES

    decoder = InstructionDecoder()
    # LOAD rd=1, addr=50
    instr = (OPCODES["LOAD"] << 12) | (1 << 8) | 50
    load_instr = int_to_bits(instr, 16)
    decoded = decoder.decode(load_instr)
    assert_true(decoded is not None, "decode() returned None")
    assert_eq(decoded["opcode"], OPCODES["LOAD"])
    assert_eq(decoded["opcode_name"], "LOAD")
    assert_eq(decoded["instruction_type"], "I")
    assert_eq(decoded["rd"], 1)
    assert_eq(decoded["rs2_imm"], 50)
