"""
Logic Gates - The Foundation of Digital Circuits

This module contains the fundamental logic gates that form the building blocks
of all digital circuits. Every component in our 8-bit computer will ultimately
be built from these basic gates.

Bit Representation:
- Inputs and outputs are integers: 0 or 1
- 0 represents LOW/False
- 1 represents HIGH/True

Your Task:
Complete the implementation of each gate function below.
"""


def NOT(a: int) -> int:
    """Logical NOT gate (inverter).

    Returns the opposite of the input.

    Truth Table:
        A | OUT
        --|----
        0 |  1
        1 |  0

    Args:
        a: Input bit (0 or 1)

    Returns:
        Inverted bit (0 or 1)
    """
    # TODO: Implement NOT gate
    return 1 if a == 0 else 0


def AND(a: int, b: int) -> int:
    """Logical AND gate.

    Returns 1 only if both inputs are 1.

    Truth Table:
        A | B | OUT
        --|---|----
        0 | 0 |  0
        0 | 1 |  0
        1 | 0 |  0
        1 | 1 |  1

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement AND gate
    return 1 if a == 1 and b == 1 else 0


def OR(a: int, b: int) -> int:
    """Logical OR gate.

    Returns 1 if at least one input is 1.

    Truth Table:
        A | B | OUT
        --|---|----
        0 | 0 |  0
        0 | 1 |  1
        1 | 0 |  1
        1 | 1 |  1

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement OR gate
    return 1 if a == 1 or b == 1 else 0


def NAND(a: int, b: int) -> int:
    """Logical NAND gate (NOT-AND).

    Returns 0 only if both inputs are 1.
    NAND is a universal gate - any other gate can be built from NAND gates.

    Truth Table:
        A | B | OUT
        --|---|----
        0 | 0 |  1
        0 | 1 |  1
        1 | 0 |  1
        1 | 1 |  0

    Hint: NAND = NOT(AND(a, b))

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement NAND gate using AND and NOT
    return NOT(AND(a, b))


def NOR(a: int, b: int) -> int:
    """Logical NOR gate (NOT-OR).

    Returns 1 only if both inputs are 0.
    NOR is also a universal gate.

    Truth Table:
        A | B | OUT
        --|---|----
        0 | 0 |  1
        0 | 1 |  0
        1 | 0 |  0
        1 | 1 |  0

    Hint: NOR = NOT(OR(a, b))

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement NOR gate using OR and NOT
    return NOT(OR(a, b))


def XOR(a: int, b: int) -> int:
    """Logical XOR gate (exclusive OR).

    Returns 1 if exactly one input is 1 (inputs are different).

    Truth Table:
        A | B | OUT
        --|---|----
        0 | 0 |  0
        0 | 1 |  1
        1 | 0 |  1
        1 | 1 |  0

    Hint: XOR can be built from AND, OR, and NOT gates.
          XOR(a, b) = OR(AND(a, NOT(b)), AND(NOT(a), b))

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement XOR gate
    return OR(AND(a, NOT(b)), AND(NOT(a), b))


def XNOR(a: int, b: int) -> int:
    """Logical XNOR gate (exclusive NOR).

    Returns 1 if both inputs are the same.

    Truth Table:
        A | B | OUT
        --|---|----
        0 | 0 |  1
        0 | 1 |  0
        1 | 0 |  0
        1 | 1 |  1

    Hint: XNOR = NOT(XOR(a, b))

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement XNOR gate using XOR and NOT
    return NOT(XOR(a, b))
