"""
Test cases for logic gates.
"""

from ..helpers import assert_eq, assert_true, assert_isinstance


def get_tests() -> dict:
    """Return all test cases for gates."""
    from computer.gates import NOT, AND, OR, NAND, NOR, XOR, XNOR

    return {
        # NOT gate - complete truth table
        "NOT_0_returns_1": lambda: assert_eq(NOT(0), 1),
        "NOT_1_returns_0": lambda: assert_eq(NOT(1), 0),
        "NOT_returns_int_for_0": lambda: assert_isinstance(NOT(0), int),
        "NOT_returns_int_for_1": lambda: assert_isinstance(NOT(1), int),
        "NOT_double_negation_0": lambda: assert_eq(NOT(NOT(0)), 0),
        "NOT_double_negation_1": lambda: assert_eq(NOT(NOT(1)), 1),

        # AND gate - complete truth table
        "AND_0_0_returns_0": lambda: assert_eq(AND(0, 0), 0),
        "AND_0_1_returns_0": lambda: assert_eq(AND(0, 1), 0),
        "AND_1_0_returns_0": lambda: assert_eq(AND(1, 0), 0),
        "AND_1_1_returns_1": lambda: assert_eq(AND(1, 1), 1),
        "AND_returns_int": lambda: assert_isinstance(AND(0, 0), int),
        "AND_commutative": lambda: assert_eq(AND(0, 1), AND(1, 0)),
        "AND_identity_1": lambda: assert_eq(AND(1, 1), 1),
        "AND_annihilator_0": lambda: assert_eq(AND(0, 1), 0),

        # OR gate - complete truth table
        "OR_0_0_returns_0": lambda: assert_eq(OR(0, 0), 0),
        "OR_0_1_returns_1": lambda: assert_eq(OR(0, 1), 1),
        "OR_1_0_returns_1": lambda: assert_eq(OR(1, 0), 1),
        "OR_1_1_returns_1": lambda: assert_eq(OR(1, 1), 1),
        "OR_returns_int": lambda: assert_isinstance(OR(0, 0), int),
        "OR_commutative": lambda: assert_eq(OR(0, 1), OR(1, 0)),
        "OR_identity_0": lambda: assert_eq(OR(0, 0), 0),
        "OR_annihilator_1": lambda: assert_eq(OR(1, 0), 1),

        # NAND gate - complete truth table
        "NAND_0_0_returns_1": lambda: assert_eq(NAND(0, 0), 1),
        "NAND_0_1_returns_1": lambda: assert_eq(NAND(0, 1), 1),
        "NAND_1_0_returns_1": lambda: assert_eq(NAND(1, 0), 1),
        "NAND_1_1_returns_0": lambda: assert_eq(NAND(1, 1), 0),
        "NAND_returns_int": lambda: assert_isinstance(NAND(0, 0), int),
        "NAND_commutative": lambda: assert_eq(NAND(0, 1), NAND(1, 0)),
        "NAND_is_not_and": lambda: assert_eq(NAND(1, 1), NOT(AND(1, 1))),

        # NOR gate - complete truth table
        "NOR_0_0_returns_1": lambda: assert_eq(NOR(0, 0), 1),
        "NOR_0_1_returns_0": lambda: assert_eq(NOR(0, 1), 0),
        "NOR_1_0_returns_0": lambda: assert_eq(NOR(1, 0), 0),
        "NOR_1_1_returns_0": lambda: assert_eq(NOR(1, 1), 0),
        "NOR_returns_int": lambda: assert_isinstance(NOR(0, 0), int),
        "NOR_commutative": lambda: assert_eq(NOR(0, 1), NOR(1, 0)),
        "NOR_is_not_or": lambda: assert_eq(NOR(0, 1), NOT(OR(0, 1))),

        # XOR gate - complete truth table
        "XOR_0_0_returns_0": lambda: assert_eq(XOR(0, 0), 0),
        "XOR_0_1_returns_1": lambda: assert_eq(XOR(0, 1), 1),
        "XOR_1_0_returns_1": lambda: assert_eq(XOR(1, 0), 1),
        "XOR_1_1_returns_0": lambda: assert_eq(XOR(1, 1), 0),
        "XOR_returns_int": lambda: assert_isinstance(XOR(0, 0), int),
        "XOR_commutative": lambda: assert_eq(XOR(0, 1), XOR(1, 0)),
        "XOR_self_inverse": lambda: assert_eq(XOR(1, 1), 0),
        "XOR_identity_0": lambda: assert_eq(XOR(1, 0), 1),

        # XNOR gate - complete truth table
        "XNOR_0_0_returns_1": lambda: assert_eq(XNOR(0, 0), 1),
        "XNOR_0_1_returns_0": lambda: assert_eq(XNOR(0, 1), 0),
        "XNOR_1_0_returns_0": lambda: assert_eq(XNOR(1, 0), 0),
        "XNOR_1_1_returns_1": lambda: assert_eq(XNOR(1, 1), 1),
        "XNOR_returns_int": lambda: assert_isinstance(XNOR(0, 0), int),
        "XNOR_commutative": lambda: assert_eq(XNOR(0, 1), XNOR(1, 0)),
        "XNOR_is_not_xor": lambda: assert_eq(XNOR(0, 1), NOT(XOR(0, 1))),

        # De Morgan's Laws
        "DeMorgan_NAND": lambda: _test_demorgan_nand(),
        "DeMorgan_NOR": lambda: _test_demorgan_nor(),
    }


def _test_demorgan_nand():
    """Test De Morgan's law: NAND(a,b) = OR(NOT(a), NOT(b))"""
    from computer.gates import NOT, AND, OR, NAND
    for a in [0, 1]:
        for b in [0, 1]:
            assert_eq(NAND(a, b), OR(NOT(a), NOT(b)))


def _test_demorgan_nor():
    """Test De Morgan's law: NOR(a,b) = AND(NOT(a), NOT(b))"""
    from computer.gates import NOT, AND, NOR
    for a in [0, 1]:
        for b in [0, 1]:
            assert_eq(NOR(a, b), AND(NOT(a), NOT(b)))
