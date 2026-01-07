"""Adders - Arithmetic Building Blocks.

This module contains adder circuits that perform binary addition.
These are fundamental building blocks for the ALU.

Components:
- Half Adder: Adds two 1-bit numbers
- Full Adder: Adds two 1-bit numbers with carry input
- Ripple Carry Adder: Adds two 8-bit numbers
- Subtractor: Subtracts using two's complement

Bit representation: Lists with LSB at index 0.
"""

from typing import List, Tuple


def half_adder(a: int, b: int) -> Tuple[int, int]:
    """Half Adder - adds two single bits.

    A half adder computes the sum and carry of two single-bit inputs.
    It cannot handle a carry input, which is why it's called "half".

    Truth Table:
        A | B | Sum | Carry
        --|---|-----|------
        0 | 0 |  0  |   0
        0 | 1 |  1  |   0
        1 | 0 |  1  |   0
        1 | 1 |  0  |   1

    Args:
        a: First input bit
        b: Second input bit

    Returns:
        Tuple of (sum, carry)

    Hint:
        Sum = XOR(a, b)
        Carry = AND(a, b)
    """
    # TODO: Implement half adder
    pass


def full_adder(a: int, b: int, cin: int) -> Tuple[int, int]:
    """Full Adder - adds two single bits plus a carry input.

    A full adder handles three inputs: two bits to add and a carry from
    a previous addition. This allows chaining adders for multi-bit addition.

    Truth Table:
        A | B | Cin | Sum | Cout
        --|---|-----|-----|-----
        0 | 0 |  0  |  0  |  0
        0 | 0 |  1  |  1  |  0
        0 | 1 |  0  |  1  |  0
        0 | 1 |  1  |  0  |  1
        1 | 0 |  0  |  1  |  0
        1 | 0 |  1  |  0  |  1
        1 | 1 |  0  |  0  |  1
        1 | 1 |  1  |  1  |  1

    Args:
        a: First input bit
        b: Second input bit
        cin: Carry input bit

    Returns:
        Tuple of (sum, carry_out)

    Hint:
        Use two half adders!
        First half adder: adds a and b
        Second half adder: adds the result with cin
        Final carry = OR of the two carries
    """
    # TODO: Implement full adder using two half adders
    pass


def ripple_carry_adder_8bit(a: List[int], b: List[int], cin: int = 0) -> Tuple[List[int], int]:
    """8-bit Ripple Carry Adder.

    Adds two 8-bit numbers using a chain of full adders.
    The carry "ripples" from the LSB to the MSB.

    Args:
        a: First 8-bit number (list of 8 bits, LSB at index 0)
        b: Second 8-bit number (list of 8 bits, LSB at index 0)
        cin: Initial carry input (default 0)

    Returns:
        Tuple of (8-bit sum, carry_out)

    Example:
        5 + 3 = 8
        a = [1,0,1,0,0,0,0,0] (5 in binary, LSB first)
        b = [1,1,0,0,0,0,0,0] (3 in binary, LSB first)
        result = [0,0,0,1,0,0,0,0] (8 in binary, LSB first)
    """
    # TODO: Implement 8-bit ripple carry adder
    pass


def subtractor_8bit(a: List[int], b: List[int]) -> Tuple[List[int], int, int]:
    """8-bit Subtractor using two's complement.

    Computes a - b using the identity: a - b = a + (~b) + 1

    Two's complement subtraction:
    1. Invert all bits of b (one's complement)
    2. Add 1 (making it two's complement)
    3. Add to a

    Args:
        a: Minuend (8-bit number, LSB at index 0)
        b: Subtrahend (8-bit number, LSB at index 0)

    Returns:
        Tuple of (8-bit difference, borrow, overflow)
        - borrow: 1 if b > a (unsigned)
        - overflow: 1 if signed overflow occurred

    Note on overflow:
        Signed overflow occurs when adding two positive numbers gives negative,
        or adding two negative numbers gives positive.
    """
    # TODO: Implement 8-bit subtractor
    pass


def twos_complement(bits: List[int]) -> List[int]:
    """Compute the two's complement of an 8-bit number.

    Two's complement = NOT(bits) + 1

    Args:
        bits: 8-bit number (LSB at index 0)

    Returns:
        Two's complement (8-bit, LSB at index 0)
    """
    # TODO: Implement two's complement
    pass
