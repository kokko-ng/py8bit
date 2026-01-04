"""
Pytest configuration and shared fixtures for the 8-bit computer test suite.
"""

import sys
from pathlib import Path

import pytest

# Add src to path so we can import computer modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))
sys.path.insert(0, str(project_root))


@pytest.fixture
def all_bit_pairs():
    """Generate all possible pairs of single bits: (0,0), (0,1), (1,0), (1,1)."""
    return [(0, 0), (0, 1), (1, 0), (1, 1)]


@pytest.fixture
def all_bits():
    """Generate all single bit values: 0, 1."""
    return [0, 1]


@pytest.fixture
def all_3bit_combinations():
    """Generate all 8 combinations of 3 bits."""
    return [(a, b, c) for a in [0, 1] for b in [0, 1] for c in [0, 1]]


@pytest.fixture
def zero_byte():
    """An 8-bit zero value."""
    return [0, 0, 0, 0, 0, 0, 0, 0]


@pytest.fixture
def one_byte():
    """An 8-bit value representing 1."""
    return [1, 0, 0, 0, 0, 0, 0, 0]


@pytest.fixture
def max_byte():
    """An 8-bit value representing 255 (all ones)."""
    return [1, 1, 1, 1, 1, 1, 1, 1]


@pytest.fixture
def sample_bytes():
    """A collection of useful 8-bit test values."""
    return {
        'zero': [0, 0, 0, 0, 0, 0, 0, 0],      # 0
        'one': [1, 0, 0, 0, 0, 0, 0, 0],       # 1
        'two': [0, 1, 0, 0, 0, 0, 0, 0],       # 2
        'five': [1, 0, 1, 0, 0, 0, 0, 0],      # 5
        'ten': [0, 1, 0, 1, 0, 0, 0, 0],       # 10
        'half': [0, 0, 0, 0, 0, 0, 0, 1],      # 128
        'max': [1, 1, 1, 1, 1, 1, 1, 1],       # 255
        'neg_one': [1, 1, 1, 1, 1, 1, 1, 1],   # -1 (two's complement)
        'neg_two': [0, 1, 1, 1, 1, 1, 1, 1],   # -2 (two's complement)
    }


def int_to_bits(value: int, num_bits: int = 8) -> list:
    """Convert an integer to a list of bits (LSB at index 0)."""
    if value < 0:
        value = (1 << num_bits) + value
    value = value & ((1 << num_bits) - 1)
    return [(value >> i) & 1 for i in range(num_bits)]


def bits_to_int(bits: list, signed: bool = False) -> int:
    """Convert a list of bits (LSB at index 0) to an integer."""
    result = sum(bit << i for i, bit in enumerate(bits))
    if signed and len(bits) > 0 and bits[-1] == 1:
        result -= (1 << len(bits))
    return result
