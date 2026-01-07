"""Test cases for clock."""

from ..helpers import assert_eq, assert_true


def get_tests() -> dict:
    """Return all test cases for clock."""
    from computer.clock import Clock

    return {
        # Clock creation
        "Clock_create": lambda: assert_true(Clock() is not None),
        "Clock_has_state": lambda: assert_true(hasattr(Clock(), "state")),
        "Clock_has_tick": lambda: assert_true(hasattr(Clock(), "tick")),
        "Clock_initial_state": lambda: assert_eq(Clock().state, 0),
        # Clock tick
        "Clock_tick_goes_high": lambda: _test_clock_tick_high(),
        "Clock_tick_alternates": lambda: _test_clock_alternates(),
        "Clock_tick_sequence_8": lambda: _test_clock_sequence(8),
        "Clock_tick_sequence_16": lambda: _test_clock_sequence(16),
        # Clock rising/falling edge
        "Clock_rising_edge": lambda: _test_clock_rising_edge(),
        "Clock_falling_edge": lambda: _test_clock_falling_edge(),
    }


def _test_clock_tick_high():
    """Test clock tick goes to 1."""
    from computer.clock import Clock

    clock = Clock()
    clock.tick()
    assert_eq(clock.state, 1)


def _test_clock_alternates():
    """Test clock alternates between 0 and 1."""
    from computer.clock import Clock

    clock = Clock()
    states = []
    for _ in range(4):
        clock.tick()
        states.append(clock.state)
    assert_eq(states, [1, 0, 1, 0])


def _test_clock_sequence(count):
    """Test clock for longer sequence."""
    from computer.clock import Clock

    clock = Clock()
    expected = [(i + 1) % 2 for i in range(count)]
    for exp in expected:
        clock.tick()
        assert_eq(clock.state, exp)


def _test_clock_rising_edge():
    """Test detecting rising edge."""
    from computer.clock import Clock

    clock = Clock()
    prev = clock.state
    clock.tick()
    curr = clock.state
    rising = (prev == 0) and (curr == 1)
    assert_true(rising)


def _test_clock_falling_edge():
    """Test detecting falling edge."""
    from computer.clock import Clock

    clock = Clock()
    clock.tick()  # Go high
    prev = clock.state
    clock.tick()  # Go low
    curr = clock.state
    falling = (prev == 1) and (curr == 0)
    assert_true(falling)
