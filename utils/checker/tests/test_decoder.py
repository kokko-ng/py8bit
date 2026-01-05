"""
Test cases for instruction decoder.
"""

from ..helpers import assert_eq, assert_true, int_to_bits, bits_to_int


def get_tests() -> dict:
    """Return all test cases for decoder."""
    from computer.decoder import InstructionDecoder

    return {
        # Decoder creation
        "Decoder_create": lambda: assert_true(InstructionDecoder() is not None),
        "Decoder_has_decode": lambda: assert_true(hasattr(InstructionDecoder(), 'decode')),

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
    nop_instr = int_to_bits(OPCODES['NOP'] << 12, 16)
    decoded = decoder.decode(nop_instr)
    assert_true(decoded is not None)


def _test_decode_add():
    """Test decoding ADD instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES
    decoder = InstructionDecoder()
    # ADD rd=1, rs1=2, rs2=3
    instr = (OPCODES['ADD'] << 12) | (1 << 8) | (2 << 4) | 3
    add_instr = int_to_bits(instr, 16)
    decoded = decoder.decode(add_instr)
    assert_true(decoded is not None)


def _test_decode_halt():
    """Test decoding HALT instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES
    decoder = InstructionDecoder()
    halt_instr = int_to_bits(OPCODES['HALT'] << 12, 16)
    decoded = decoder.decode(halt_instr)
    assert_true(decoded is not None)


def _test_decode_jmp():
    """Test decoding JMP instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES
    decoder = InstructionDecoder()
    # JMP to address 100
    instr = (OPCODES['JMP'] << 12) | 100
    jmp_instr = int_to_bits(instr, 16)
    decoded = decoder.decode(jmp_instr)
    assert_true(decoded is not None)


def _test_decode_load():
    """Test decoding LOAD instruction."""
    from computer.decoder import InstructionDecoder
    from computer.isa import OPCODES
    decoder = InstructionDecoder()
    # LOAD rd=1, addr=50
    instr = (OPCODES['LOAD'] << 12) | (1 << 8) | 50
    load_instr = int_to_bits(instr, 16)
    decoded = decoder.decode(load_instr)
    assert_true(decoded is not None)
