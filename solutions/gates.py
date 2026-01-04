"""
Logic Gates - Solution File

This file contains the complete, working implementations of all logic gates.
Students can reference this if they get stuck.
"""


def NOT(a: int) -> int:
    """Logical NOT gate (inverter)."""
    return 1 if a == 0 else 0


def AND(a: int, b: int) -> int:
    """Logical AND gate."""
    return 1 if (a == 1 and b == 1) else 0


def OR(a: int, b: int) -> int:
    """Logical OR gate."""
    return 1 if (a == 1 or b == 1) else 0


def NAND(a: int, b: int) -> int:
    """Logical NAND gate (NOT-AND)."""
    return NOT(AND(a, b))


def NOR(a: int, b: int) -> int:
    """Logical NOR gate (NOT-OR)."""
    return NOT(OR(a, b))


def XOR(a: int, b: int) -> int:
    """Logical XOR gate (exclusive OR)."""
    return OR(AND(a, NOT(b)), AND(NOT(a), b))


def XNOR(a: int, b: int) -> int:
    """Logical XNOR gate (exclusive NOR)."""
    return NOT(XOR(a, b))
