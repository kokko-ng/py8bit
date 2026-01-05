"""
Test cases for sequential circuits.
"""

from ..helpers import assert_eq, assert_true


def get_tests() -> dict:
    """Return all test cases for sequential circuits."""
    from computer.sequential import SRLatch, GatedSRLatch, DLatch, DFlipFlop, JKFlipFlop, TFlipFlop

    return {
        # SR Latch
        "SRLatch_initial_state": lambda: assert_eq(SRLatch().q, 0),
        "SRLatch_set": lambda: _test_sr_set(),
        "SRLatch_reset": lambda: _test_sr_reset(),
        "SRLatch_hold_high": lambda: _test_sr_hold_high(),
        "SRLatch_hold_low": lambda: _test_sr_hold_low(),
        "SRLatch_sequence": lambda: _test_sr_sequence(),

        # Gated SR Latch
        "GatedSRLatch_disabled_ignores_set": lambda: assert_eq(GatedSRLatch()(1, 0, 0), 0),
        "GatedSRLatch_disabled_ignores_reset": lambda: _test_gated_sr_disabled_reset(),
        "GatedSRLatch_enabled_set": lambda: assert_eq(GatedSRLatch()(1, 0, 1), 1),
        "GatedSRLatch_enabled_reset": lambda: _test_gated_sr_enabled_reset(),

        # D Latch
        "DLatch_initial_state": lambda: assert_eq(DLatch().q, 0),
        "DLatch_transparent_high": lambda: assert_eq(DLatch()(1, 1), 1),
        "DLatch_transparent_low": lambda: _test_d_latch_transparent_low(),
        "DLatch_hold_when_disabled": lambda: _test_d_latch_hold(),
        "DLatch_sequence": lambda: _test_d_latch_sequence(),

        # D Flip-Flop
        "DFlipFlop_initial_state": lambda: assert_eq(DFlipFlop().read(), 0),
        "DFlipFlop_rising_edge_captures": lambda: _test_dff_rising_edge(),
        "DFlipFlop_ignores_falling_edge": lambda: _test_dff_falling_edge(),
        "DFlipFlop_holds_between_edges": lambda: _test_dff_holds(),
        "DFlipFlop_sequence": lambda: _test_dff_sequence(),

        # JK Flip-Flop
        "JKFlipFlop_initial_state": lambda: assert_eq(JKFlipFlop().read(), 0),
        "JKFlipFlop_set": lambda: _test_jk_set(),
        "JKFlipFlop_reset": lambda: _test_jk_reset(),
        "JKFlipFlop_hold": lambda: _test_jk_hold(),
        "JKFlipFlop_toggle": lambda: _test_jk_toggle(),
        "JKFlipFlop_toggle_sequence": lambda: _test_jk_toggle_sequence(),

        # T Flip-Flop
        "TFlipFlop_initial_state": lambda: assert_eq(TFlipFlop().read(), 0),
        "TFlipFlop_toggle_on": lambda: _test_t_toggle_on(),
        "TFlipFlop_hold_when_t0": lambda: _test_t_hold(),
        "TFlipFlop_counting_pattern": lambda: _test_t_counting(),
    }


# SR Latch tests
def _test_sr_set():
    """Test SR latch set."""
    from computer.sequential import SRLatch
    sr = SRLatch()
    result = sr(1, 0)
    assert_eq(result, 1)
    assert_eq(sr.q, 1)


def _test_sr_reset():
    """Test SR latch reset."""
    from computer.sequential import SRLatch
    sr = SRLatch()
    sr(1, 0)  # Set
    result = sr(0, 1)  # Reset
    assert_eq(result, 0)


def _test_sr_hold_high():
    """Test SR latch hold at 1."""
    from computer.sequential import SRLatch
    sr = SRLatch()
    sr(1, 0)  # Set to 1
    result = sr(0, 0)  # Hold
    assert_eq(result, 1)


def _test_sr_hold_low():
    """Test SR latch hold at 0."""
    from computer.sequential import SRLatch
    sr = SRLatch()
    sr(0, 1)  # Reset to 0
    result = sr(0, 0)  # Hold
    assert_eq(result, 0)


def _test_sr_sequence():
    """Test SR latch with sequence of operations."""
    from computer.sequential import SRLatch
    sr = SRLatch()
    assert_eq(sr(1, 0), 1)  # Set
    assert_eq(sr(0, 0), 1)  # Hold
    assert_eq(sr(0, 1), 0)  # Reset
    assert_eq(sr(0, 0), 0)  # Hold
    assert_eq(sr(1, 0), 1)  # Set again


# Gated SR Latch tests
def _test_gated_sr_disabled_reset():
    """Test gated SR latch ignores reset when disabled."""
    from computer.sequential import GatedSRLatch
    gated = GatedSRLatch()
    gated(1, 0, 1)  # Set first
    result = gated(0, 1, 0)  # Reset disabled
    assert_eq(result, 1)


def _test_gated_sr_enabled_reset():
    """Test gated SR latch reset when enabled."""
    from computer.sequential import GatedSRLatch
    gated = GatedSRLatch()
    gated(1, 0, 1)  # Set
    result = gated(0, 1, 1)  # Reset enabled
    assert_eq(result, 0)


# D Latch tests
def _test_d_latch_transparent_low():
    """Test D latch transparent with D=0."""
    from computer.sequential import DLatch
    d = DLatch()
    d(1, 1)  # Set to 1
    result = d(0, 1)  # Set to 0
    assert_eq(result, 0)


def _test_d_latch_hold():
    """Test D latch hold when disabled."""
    from computer.sequential import DLatch
    d = DLatch()
    d(1, 1)  # Set to 1
    result = d(0, 0)  # Try to change, but disabled
    assert_eq(result, 1)


def _test_d_latch_sequence():
    """Test D latch sequence."""
    from computer.sequential import DLatch
    d = DLatch()
    assert_eq(d(1, 1), 1)  # Transparent, D=1
    assert_eq(d(0, 0), 1)  # Hold
    assert_eq(d(0, 1), 0)  # Transparent, D=0
    assert_eq(d(1, 0), 0)  # Hold


# D Flip-Flop tests
def _test_dff_rising_edge():
    """Test D flip-flop captures on rising edge."""
    from computer.sequential import DFlipFlop
    dff = DFlipFlop()
    dff.clock(1, 0)  # D=1, CLK low
    assert_eq(dff.read(), 0)
    dff.clock(1, 1)  # Rising edge
    assert_eq(dff.read(), 1)


def _test_dff_falling_edge():
    """Test D flip-flop ignores falling edge."""
    from computer.sequential import DFlipFlop
    dff = DFlipFlop()
    dff.clock(1, 1)  # Rising edge, capture 1
    dff.clock(0, 0)  # Falling edge with D=0
    assert_eq(dff.read(), 1)


def _test_dff_holds():
    """Test D flip-flop holds between edges."""
    from computer.sequential import DFlipFlop
    dff = DFlipFlop()
    dff.clock(1, 0)
    dff.clock(1, 1)  # Capture 1
    dff.clock(0, 1)  # D changes while CLK high
    assert_eq(dff.read(), 1)
    dff.clock(0, 0)  # CLK goes low
    assert_eq(dff.read(), 1)


def _test_dff_sequence():
    """Test D flip-flop sequence."""
    from computer.sequential import DFlipFlop
    dff = DFlipFlop()
    # First rising edge
    dff.clock(1, 0)
    dff.clock(1, 1)
    assert_eq(dff.read(), 1)
    # Second rising edge
    dff.clock(0, 0)
    dff.clock(0, 1)
    assert_eq(dff.read(), 0)
    # Third rising edge
    dff.clock(1, 0)
    dff.clock(1, 1)
    assert_eq(dff.read(), 1)


# JK Flip-Flop tests
def _test_jk_set():
    """Test JK flip-flop set."""
    from computer.sequential import JKFlipFlop
    jk = JKFlipFlop()
    jk.clock(1, 0, 0)
    jk.clock(1, 0, 1)
    assert_eq(jk.read(), 1)


def _test_jk_reset():
    """Test JK flip-flop reset."""
    from computer.sequential import JKFlipFlop
    jk = JKFlipFlop()
    jk.clock(1, 0, 0)
    jk.clock(1, 0, 1)  # Set first
    jk.clock(0, 1, 0)
    jk.clock(0, 1, 1)  # Reset
    assert_eq(jk.read(), 0)


def _test_jk_hold():
    """Test JK flip-flop hold."""
    from computer.sequential import JKFlipFlop
    jk = JKFlipFlop()
    jk.clock(1, 0, 0)
    jk.clock(1, 0, 1)  # Set to 1
    jk.clock(0, 0, 0)
    jk.clock(0, 0, 1)  # Hold
    assert_eq(jk.read(), 1)


def _test_jk_toggle():
    """Test JK flip-flop toggle."""
    from computer.sequential import JKFlipFlop
    jk = JKFlipFlop()
    jk.clock(1, 1, 0)
    jk.clock(1, 1, 1)
    assert_eq(jk.read(), 1)
    jk.clock(1, 1, 0)
    jk.clock(1, 1, 1)
    assert_eq(jk.read(), 0)


def _test_jk_toggle_sequence():
    """Test JK flip-flop toggle sequence."""
    from computer.sequential import JKFlipFlop
    jk = JKFlipFlop()
    expected = [1, 0, 1, 0]
    for exp in expected:
        jk.clock(1, 1, 0)
        jk.clock(1, 1, 1)
        assert_eq(jk.read(), exp)


# T Flip-Flop tests
def _test_t_toggle_on():
    """Test T flip-flop toggle."""
    from computer.sequential import TFlipFlop
    t = TFlipFlop()
    t.clock(1, 0)
    t.clock(1, 1)
    assert_eq(t.read(), 1)
    t.clock(1, 0)
    t.clock(1, 1)
    assert_eq(t.read(), 0)


def _test_t_hold():
    """Test T flip-flop hold."""
    from computer.sequential import TFlipFlop
    t = TFlipFlop()
    t.clock(1, 0)
    t.clock(1, 1)  # Toggle to 1
    t.clock(0, 0)
    t.clock(0, 1)  # Hold
    assert_eq(t.read(), 1)
    t.clock(0, 0)
    t.clock(0, 1)  # Hold again
    assert_eq(t.read(), 1)


def _test_t_counting():
    """Test T flip-flop counting pattern."""
    from computer.sequential import TFlipFlop
    t = TFlipFlop()
    expected = [1, 0, 1, 0, 1, 0, 1, 0]
    for exp in expected:
        t.clock(1, 0)
        t.clock(1, 1)
        assert_eq(t.read(), exp)
