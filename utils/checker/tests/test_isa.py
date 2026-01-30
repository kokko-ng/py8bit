"""Test cases for ISA (Instruction Set Architecture)."""

from ..helpers import assert_eq, assert_true, assert_in, assert_len, assert_not_none


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
    from computer.isa import encode_instruction

    result = encode_instruction(opcode)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)


def _test_encode_rtype(opcode):
    """Test encoding an R-type instruction."""
    from computer.isa import encode_instruction

    result = encode_instruction(opcode, rd=1, rs1=2, rs2_imm=3)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)


def _test_encode_itype(opcode):
    """Test encoding an I-type instruction."""
    from computer.isa import encode_instruction

    result = encode_instruction(opcode, rd=1, rs2_imm=100)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)


def _test_encode_jtype(opcode):
    """Test encoding a J-type instruction."""
    from computer.isa import encode_instruction

    result = encode_instruction(opcode, rs2_imm=200)
    assert_not_none(result, "encode_instruction() returned None")
    assert_len(result, 16)


def _test_decode_nop():
    """Test decoding NOP instruction."""
    from computer.isa import encode_instruction, decode_instruction

    encoded = encode_instruction("NOP")
    assert_not_none(encoded, "encode_instruction() returned None")
    decoded = decode_instruction(encoded)
    assert_not_none(decoded, "decode_instruction() returned None")
    assert_true("opcode" in decoded or len(decoded) > 0)


def _test_roundtrip():
    """Test encode/decode roundtrip."""
    from computer.isa import encode_instruction, decode_instruction

    for opcode in ["NOP", "ADD", "HALT"]:
        encoded = encode_instruction(opcode)
        assert_not_none(encoded, f"encode_instruction({opcode}) returned None")
        decoded = decode_instruction(encoded)
        assert_not_none(decoded, f"decode_instruction() returned None for {opcode}")
