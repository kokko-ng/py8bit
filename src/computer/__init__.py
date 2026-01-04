"""
8-Bit Computer Components Library

This package contains all the building blocks for constructing an 8-bit computer
from scratch, starting with logic gates and building up to a complete CPU.

Bit Representation:
- Bits are represented as integers (0 or 1)
- 8-bit values are lists of 8 integers with LSB at index 0
- Example: decimal 5 = [1, 0, 1, 0, 0, 0, 0, 0] (binary 00000101, LSB first)
"""

from typing import List


def int_to_bits(value: int, num_bits: int = 8) -> List[int]:
    """Convert an integer to a list of bits (LSB at index 0).

    Args:
        value: Integer to convert (will be masked to fit num_bits)
        num_bits: Number of bits in the output list

    Returns:
        List of bits with LSB at index 0

    Example:
        >>> int_to_bits(5, 8)
        [1, 0, 1, 0, 0, 0, 0, 0]
    """
    # Handle negative numbers using two's complement
    if value < 0:
        value = (1 << num_bits) + value

    # Mask to ensure we only use num_bits
    value = value & ((1 << num_bits) - 1)

    return [(value >> i) & 1 for i in range(num_bits)]


def bits_to_int(bits: List[int], signed: bool = False) -> int:
    """Convert a list of bits (LSB at index 0) to an integer.

    Args:
        bits: List of bits with LSB at index 0
        signed: If True, interpret as two's complement signed integer

    Returns:
        Integer value

    Example:
        >>> bits_to_int([1, 0, 1, 0, 0, 0, 0, 0])
        5
    """
    result = sum(bit << i for i, bit in enumerate(bits))

    if signed and len(bits) > 0 and bits[-1] == 1:
        # Two's complement: subtract 2^n if MSB is 1
        result -= (1 << len(bits))

    return result


def bits_to_hex(bits: List[int]) -> str:
    """Convert a list of bits to a hexadecimal string.

    Args:
        bits: List of bits with LSB at index 0

    Returns:
        Hexadecimal string (e.g., '0x05')
    """
    value = bits_to_int(bits)
    num_hex_digits = (len(bits) + 3) // 4
    return f"0x{value:0{num_hex_digits}X}"


def bits_to_bin(bits: List[int]) -> str:
    """Convert a list of bits to a binary string (MSB first for readability).

    Args:
        bits: List of bits with LSB at index 0

    Returns:
        Binary string with MSB first (e.g., '00000101')
    """
    return ''.join(str(b) for b in reversed(bits))
