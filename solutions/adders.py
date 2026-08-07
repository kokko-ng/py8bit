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
from solutions.gates import AND, OR, XOR, NOT


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
    """
    sum_bit = XOR(a, b)
    carry = AND(a, b)
    return (sum_bit, carry)


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
    """
    # First half adder: add a and b
    sum1, carry1 = half_adder(a, b)
    # Second half adder: add result with carry in
    sum2, carry2 = half_adder(sum1, cin)
    # Final carry is OR of both carries
    cout = OR(carry1, carry2)
    return (sum2, cout)


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
    result = []
    carry = cin

    for i in range(8):
        sum_bit, carry = full_adder(a[i], b[i], carry)
        result.append(sum_bit)

    return (result, carry)


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
    # Invert b
    b_inverted = [NOT(bit) for bit in b]

    # Add a + (~b) + 1
    result, carry = ripple_carry_adder_8bit(a, b_inverted, cin=1)

    # Borrow is inverted carry (no carry means we borrowed)
    borrow = NOT(carry)

    # Overflow detection for signed subtraction
    # Overflow if signs of a and -b are same, but result sign differs
    # -b has opposite sign of b (except for edge cases)
    # Simplified: overflow = (a[7] != b[7]) AND (a[7] != result[7])
    overflow = AND(XOR(a[7], b[7]), XOR(a[7], result[7]))

    return (result, borrow, overflow)


def twos_complement(bits: List[int]) -> List[int]:
    """Compute the two's complement of an 8-bit number.

    Two's complement = NOT(bits) + 1

    Args:
        bits: 8-bit number (LSB at index 0)

    Returns:
        Two's complement (8-bit, LSB at index 0)
    """
    # Invert all bits
    inverted = [NOT(bit) for bit in bits]
    # Add 1
    result, _ = ripple_carry_adder_8bit(inverted, [1, 0, 0, 0, 0, 0, 0, 0])
    return result
