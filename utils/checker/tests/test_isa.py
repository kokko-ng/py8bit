"""Test cases for ISA (Instruction Set Architecture)."""

from ..helpers import assert_eq, assert_len, assert_not_none, bits_to_int


def get_tests() -> dict:
    """Return all test cases for ISA."""
    from computer.isa import OPCODES

    return {
        # Encode instruction
        "ISA_encode_NOP": lambda: _test_encode("NOP"),
        "ISA_encode_ADD": lambda: _test_encode_rtype("ADD"),
        "ISA_encode_LOAD": lambda: _test_encode_itype("LOAD"),
        "ISA_encode_JMP": lambda: _test_encode_jtype("JMP"),
        # Decode instruction
        "ISA_decode_NOP": lambda: _test_decode_nop(),
        "ISA_encode_decode_roundtrip": lambda: _test_roundtrip(),
    }


def _test_unique_opcodes():
    """Test that all opcodes have unique values."""
    from computer.isa import OPCODES

    values = list(OPCODES.values())
    assert_eq(len(values), len(set(values)))


def _test_encode(opcode):
    """Test encoding an instruction."""
    from computer.isa import OPCODES, encode_instruction

    result = encode_instruction(opcode)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)
    assert_eq(bits_to_int(result[12:16]), OPCODES[opcode], "Opcode bits should be stored in bits 15-12")


def _test_encode_rtype(opcode):
    """Test encoding an R-type instruction."""
    from computer.isa import OPCODES, encode_instruction

    result = encode_instruction(opcode, rd=1, rs1=2, rs2_imm=3)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)
    assert_eq(bits_to_int(result[12:16]), OPCODES[opcode], "Opcode bits should match the instruction")
    assert_eq(bits_to_int(result[8:12]), 1, "Rd should be encoded in bits 11-8")
    assert_eq(bits_to_int(result[4:8]), 2, "Rs1 should be encoded in bits 7-4")
    assert_eq(bits_to_int(result[0:4]), 3, "Rs2 should be encoded in bits 3-0")


def _test_encode_itype(opcode):
    """Test encoding an I-type instruction."""
    from computer.isa import OPCODES, encode_instruction

    result = encode_instruction(opcode, rd=1, rs2_imm=100)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)
    assert_eq(bits_to_int(result[12:16]), OPCODES[opcode], "Opcode bits should match the instruction")
    assert_eq(bits_to_int(result[8:12]), 1, "Rd should be encoded in bits 11-8")
    assert_eq(bits_to_int(result[0:8]), 100, "Address/immediate should be encoded in bits 7-0")


def _test_encode_jtype(opcode):
    """Test encoding a J-type instruction."""
    from computer.isa import OPCODES, encode_instruction

    result = encode_instruction(opcode, rs2_imm=200)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)
    assert_eq(bits_to_int(result[12:16]), OPCODES[opcode], "Opcode bits should match the instruction")
    assert_eq(bits_to_int(result[0:8]), 200, "Jump target should be encoded in bits 7-0")


def _test_decode_nop():
    """Test decoding NOP instruction."""
    from computer.isa import OPCODES, decode_instruction, encode_instruction

    encoded = encode_instruction("NOP")
    assert_not_none(encoded, "encode_instruction() returned None")
    decoded = decode_instruction(encoded)
    assert_not_none(decoded, "decode_instruction() returned None")
    assert_eq(decoded["opcode"], OPCODES["NOP"])
    assert_eq(decoded["opcode_name"], "NOP")


def _test_roundtrip():
    """Test encode/decode roundtrip."""
    from computer.isa import encode_instruction, decode_instruction

    cases = [
        ("NOP", {}),
        ("ADD", {"rd": 1, "rs1": 2, "rs2_imm": 3}),
        ("LOAD", {"rd": 4, "rs2_imm": 99}),
        ("JMP", {"rs2_imm": 200}),
        ("HALT", {}),
    ]
    for opcode, kwargs in cases:
        encoded = encode_instruction(opcode, **kwargs)
        assert_not_none(encoded, f"encode_instruction({opcode}) returned None")
        decoded = decode_instruction(encoded)
        assert_not_none(decoded, f"decode_instruction() returned None for {opcode}")
        assert_eq(decoded["opcode_name"], opcode, "Opcode name should survive encode/decode roundtrip")
        for key, value in kwargs.items():
            assert_eq(decoded[key], value, f"{key} should survive encode/decode roundtrip")
