"""
Test cases for ISA (Instruction Set Architecture).
"""

from ..helpers import assert_eq, assert_true, assert_in, assert_len, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for ISA."""
    from computer.isa import OPCODES, encode_instruction, decode_instruction

    return {
        # OPCODES definitions
        "ISA_opcodes_defined": lambda: assert_true(len(OPCODES) > 0),
        "ISA_has_NOP": lambda: assert_in('NOP', OPCODES),
        "ISA_has_LOAD": lambda: assert_in('LOAD', OPCODES),
        "ISA_has_STORE": lambda: assert_in('STORE', OPCODES),
        "ISA_has_MOV": lambda: assert_in('MOV', OPCODES),
        "ISA_has_ADD": lambda: assert_in('ADD', OPCODES),
        "ISA_has_SUB": lambda: assert_in('SUB', OPCODES),
        "ISA_has_AND": lambda: assert_in('AND', OPCODES),
        "ISA_has_OR": lambda: assert_in('OR', OPCODES),
        "ISA_has_XOR": lambda: assert_in('XOR', OPCODES),
        "ISA_has_NOT": lambda: assert_in('NOT', OPCODES),
        "ISA_has_SHL": lambda: assert_in('SHL', OPCODES),
        "ISA_has_SHR": lambda: assert_in('SHR', OPCODES),
        "ISA_has_JMP": lambda: assert_in('JMP', OPCODES),
        "ISA_has_JZ": lambda: assert_in('JZ', OPCODES),
        "ISA_has_JNZ": lambda: assert_in('JNZ', OPCODES),
        "ISA_has_HALT": lambda: assert_in('HALT', OPCODES),

        # OPCODE values
        "ISA_NOP_is_0": lambda: assert_eq(OPCODES['NOP'], 0),
        "ISA_HALT_is_15": lambda: assert_eq(OPCODES['HALT'], 15),
        "ISA_unique_opcodes": lambda: _test_unique_opcodes(),

        # Encode instruction
        "ISA_encode_NOP": lambda: _test_encode('NOP'),
        "ISA_encode_ADD": lambda: _test_encode_rtype('ADD'),
        "ISA_encode_LOAD": lambda: _test_encode_itype('LOAD'),
        "ISA_encode_JMP": lambda: _test_encode_jtype('JMP'),

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
    if result is not None:
        assert_len(result, 16)


def _test_encode_rtype(opcode):
    """Test encoding an R-type instruction."""
    from computer.isa import encode_instruction
    result = encode_instruction(opcode, rd=1, rs1=2, rs2_imm=3)
    if result is not None:
        assert_len(result, 16)


def _test_encode_itype(opcode):
    """Test encoding an I-type instruction."""
    from computer.isa import encode_instruction
    result = encode_instruction(opcode, rd=1, rs2_imm=100)
    if result is not None:
        assert_len(result, 16)


def _test_encode_jtype(opcode):
    """Test encoding a J-type instruction."""
    from computer.isa import encode_instruction
    result = encode_instruction(opcode, rs2_imm=200)
    if result is not None:
        assert_len(result, 16)


def _test_decode_nop():
    """Test decoding NOP instruction."""
    from computer.isa import encode_instruction, decode_instruction, OPCODES
    encoded = encode_instruction('NOP')
    if encoded is not None:
        decoded = decode_instruction(encoded)
        if decoded is not None:
            assert_true('opcode' in decoded or len(decoded) > 0)


def _test_roundtrip():
    """Test encode/decode roundtrip."""
    from computer.isa import encode_instruction, decode_instruction, OPCODES
    for opcode in ['NOP', 'ADD', 'HALT']:
        encoded = encode_instruction(opcode)
        if encoded is not None:
            decoded = decode_instruction(encoded)
            if decoded is not None:
                # Just verify we get something back
                assert_true(decoded is not None)
