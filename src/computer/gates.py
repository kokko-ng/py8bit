"""Logic Gates - The Foundation of Digital Circuits.

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

# NOTE: Generated from solutions/gates.py by scripts/generate_stubs.py.
# Write your implementations in the '# TODO' bodies below.
# (Maintainers: edit the solution file, not this one, then regenerate.)


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
    # TODO: Implement the NOT gate
    ...


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
    # TODO: Implement the AND gate
    ...


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
    # TODO: Implement the OR gate
    ...


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

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement the NAND gate by composing AND and NOT
    ...


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

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement the NOR gate by composing OR and NOT
    ...


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

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement the XOR gate
    ...


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

    Args:
        a: First input bit (0 or 1)
        b: Second input bit (0 or 1)

    Returns:
        Result bit (0 or 1)
    """
    # TODO: Implement the XNOR gate by composing XOR and NOT
    ...
