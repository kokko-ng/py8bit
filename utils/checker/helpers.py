"""
Utility functions and assertion helpers for the checker.
"""


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


def assert_eq(actual, expected):
    """Assert that actual equals expected."""
    if actual != expected:
        raise AssertionError(f"Expected {expected}, got {actual}")


def assert_true(condition, message: str = "Condition is false"):
    """Assert that condition is true."""
    if not condition:
        raise AssertionError(message)


def assert_in(item, collection, message: str = None):
    """Assert that item is in collection."""
    if item not in collection:
        msg = message or f"Expected {item} to be in {collection}"
        raise AssertionError(msg)


def assert_isinstance(obj, expected_type, message: str = None):
    """Assert that obj is an instance of expected_type."""
    if not isinstance(obj, expected_type):
        msg = message or f"Expected instance of {expected_type}, got {type(obj)}"
        raise AssertionError(msg)


def assert_len(obj, expected_len: int, message: str = None):
    """Assert that obj has expected length."""
    if len(obj) != expected_len:
        msg = message or f"Expected length {expected_len}, got {len(obj)}"
        raise AssertionError(msg)
