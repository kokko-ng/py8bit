"""Utility functions and assertion helpers for the checker."""


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
        result -= 1 << len(bits)
    return result


def assert_eq(actual, expected, message: str | None = None):
    """Assert that actual equals expected.

    Note: If both values are None, this is treated as a failure since
    None typically indicates an unimplemented function.
    """
    if actual is None and expected is None:
        msg = "Both values are None (function may be unimplemented)"
        if message:
            msg = f"{message}\n           {msg}"
        raise AssertionError(msg)
    if actual != expected:
        details = f"Expected: {expected!r}\n           Actual: {actual!r}"
        if message:
            msg = f"{message}\n           {details}"
        else:
            msg = details
        raise AssertionError(msg)


def assert_true(condition, message: str | None = None):
    """Assert that condition is true."""
    if not condition:
        msg = message or "Condition evaluated to False (expected True)"
        raise AssertionError(msg)


def assert_in(item, collection, message: str | None = None):
    """Assert that item is in collection."""
    if item not in collection:
        details = f"Item {item!r} not found in collection\n           Collection: {collection!r}"
        if message:
            msg = f"{message}\n           {details}"
        else:
            msg = details
        raise AssertionError(msg)


def assert_not_none(obj, message: str | None = None):
    """Assert that obj is not None."""
    if obj is None:
        msg = message or "Value is None (function may be unimplemented)"
        raise AssertionError(msg)


def assert_isinstance(obj, expected_type, message: str | None = None):
    """Assert that obj is an instance of expected_type."""
    if not isinstance(obj, expected_type):
        type_name = expected_type.__name__ if hasattr(expected_type, "__name__") else expected_type
        details = f"Expected type: {type_name}\n           Actual type: {type(obj).__name__}\n           Value: {obj!r}"
        if message:
            msg = f"{message}\n           {details}"
        else:
            msg = details
        raise AssertionError(msg)


def assert_len(obj, expected_len: int, message: str | None = None):
    """Assert that obj has expected length."""
    actual_len = len(obj)
    if actual_len != expected_len:
        details = f"Expected length: {expected_len}\n           Actual length: {actual_len}\n           Value: {obj!r}"
        if message:
            msg = f"{message}\n           {details}"
        else:
            msg = details
        raise AssertionError(msg)
