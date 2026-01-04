"""
Adders - Solution File

Complete implementations of all adder circuits.
"""

from typing import List, Tuple
from solutions.gates import AND, OR, XOR, NOT


def half_adder(a: int, b: int) -> Tuple[int, int]:
    """Half Adder - adds two single bits."""
    sum_bit = XOR(a, b)
    carry = AND(a, b)
    return (sum_bit, carry)


def full_adder(a: int, b: int, cin: int) -> Tuple[int, int]:
    """Full Adder - adds two single bits plus a carry input."""
    # First half adder: add a and b
    sum1, carry1 = half_adder(a, b)
    # Second half adder: add result with carry in
    sum2, carry2 = half_adder(sum1, cin)
    # Final carry is OR of both carries
    cout = OR(carry1, carry2)
    return (sum2, cout)


def ripple_carry_adder_8bit(a: List[int], b: List[int], cin: int = 0) -> Tuple[List[int], int]:
    """8-bit Ripple Carry Adder."""
    result = []
    carry = cin

    for i in range(8):
        sum_bit, carry = full_adder(a[i], b[i], carry)
        result.append(sum_bit)

    return (result, carry)


def subtractor_8bit(a: List[int], b: List[int]) -> Tuple[List[int], int, int]:
    """8-bit Subtractor using two's complement."""
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
    """Compute the two's complement of an 8-bit number."""
    # Invert all bits
    inverted = [NOT(bit) for bit in bits]
    # Add 1
    result, _ = ripple_carry_adder_8bit(inverted, [1, 0, 0, 0, 0, 0, 0, 0])
    return result
