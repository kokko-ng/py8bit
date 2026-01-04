"""Tests for sequential circuits (latches and flip-flops)."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.sequential import SRLatch, GatedSRLatch, DLatch, DFlipFlop, JKFlipFlop, TFlipFlop


class TestSRLatch:
    """Tests for SR Latch."""

    def test_initial_state(self):
        """SR latch starts with Q=0."""
        sr = SRLatch()
        assert sr.q == 0

    def test_set(self):
        """S=1, R=0 sets Q to 1."""
        sr = SRLatch()
        result = sr(1, 0)
        assert result == 1
        assert sr.q == 1

    def test_reset(self):
        """S=0, R=1 resets Q to 0."""
        sr = SRLatch()
        sr(1, 0)  # First set
        result = sr(0, 1)  # Then reset
        assert result == 0
        assert sr.q == 0

    def test_hold_high(self):
        """S=0, R=0 holds Q at 1."""
        sr = SRLatch()
        sr(1, 0)  # Set
        result = sr(0, 0)  # Hold
        assert result == 1

    def test_hold_low(self):
        """S=0, R=0 holds Q at 0."""
        sr = SRLatch()
        sr(0, 1)  # Reset
        result = sr(0, 0)  # Hold
        assert result == 0

    def test_sequence(self):
        """Test a sequence of operations."""
        sr = SRLatch()
        assert sr(1, 0) == 1  # Set
        assert sr(0, 0) == 1  # Hold
        assert sr(0, 1) == 0  # Reset
        assert sr(0, 0) == 0  # Hold
        assert sr(1, 0) == 1  # Set again


class TestGatedSRLatch:
    """Tests for Gated SR Latch."""

    def test_disabled_ignores_set(self):
        """When enable=0, set is ignored."""
        gated = GatedSRLatch()
        result = gated(1, 0, 0)
        assert result == 0

    def test_enabled_set(self):
        """When enable=1, set works."""
        gated = GatedSRLatch()
        result = gated(1, 0, 1)
        assert result == 1

    def test_disabled_ignores_reset(self):
        """When enable=0, reset is ignored."""
        gated = GatedSRLatch()
        gated(1, 0, 1)  # Set first
        result = gated(0, 1, 0)  # Reset disabled
        assert result == 1  # Still 1

    def test_enabled_reset(self):
        """When enable=1, reset works."""
        gated = GatedSRLatch()
        gated(1, 0, 1)  # Set
        result = gated(0, 1, 1)  # Reset enabled
        assert result == 0


class TestDLatch:
    """Tests for D Latch."""

    def test_initial_state(self):
        """D latch starts with Q=0."""
        d = DLatch()
        assert d.q == 0

    def test_transparent_high(self):
        """Enable=1, D=1 makes Q=1."""
        d = DLatch()
        result = d(1, 1)
        assert result == 1

    def test_transparent_low(self):
        """Enable=1, D=0 makes Q=0."""
        d = DLatch()
        d(1, 1)  # Set to 1
        result = d(0, 1)  # Set to 0
        assert result == 0

    def test_hold_when_disabled(self):
        """Enable=0 holds previous value."""
        d = DLatch()
        d(1, 1)  # Set to 1
        result = d(0, 0)  # Try to set to 0, but disabled
        assert result == 1

    def test_sequence(self):
        """Test sequence of operations."""
        d = DLatch()
        assert d(1, 1) == 1  # Transparent, D=1
        assert d(0, 0) == 1  # Hold
        assert d(0, 1) == 0  # Transparent, D=0
        assert d(1, 0) == 0  # Hold


class TestDFlipFlop:
    """Tests for D Flip-Flop."""

    def test_initial_state(self):
        """D flip-flop starts with Q=0."""
        dff = DFlipFlop()
        assert dff.read() == 0

    def test_captures_on_rising_edge(self):
        """D is captured on rising edge (0->1)."""
        dff = DFlipFlop()
        dff.clock(1, 0)  # D=1, CLK low
        assert dff.read() == 0  # Not captured yet
        dff.clock(1, 1)  # Rising edge!
        assert dff.read() == 1  # Now captured

    def test_ignores_falling_edge(self):
        """D is not captured on falling edge."""
        dff = DFlipFlop()
        dff.clock(1, 1)  # Rising edge, capture 1
        dff.clock(0, 0)  # Falling edge with D=0
        assert dff.read() == 1  # Still 1

    def test_holds_between_edges(self):
        """Q holds between clock edges."""
        dff = DFlipFlop()
        dff.clock(1, 0)
        dff.clock(1, 1)  # Capture 1
        dff.clock(0, 1)  # D changes while CLK high
        assert dff.read() == 1  # Still holds
        dff.clock(0, 0)  # CLK goes low
        assert dff.read() == 1  # Still holds

    def test_sequence(self):
        """Test sequence with multiple edges."""
        dff = DFlipFlop()
        # First rising edge
        dff.clock(1, 0)
        dff.clock(1, 1)
        assert dff.read() == 1
        # Second rising edge
        dff.clock(0, 0)
        dff.clock(0, 1)
        assert dff.read() == 0
        # Third rising edge
        dff.clock(1, 0)
        dff.clock(1, 1)
        assert dff.read() == 1


class TestJKFlipFlop:
    """Tests for JK Flip-Flop."""

    def test_initial_state(self):
        """JK flip-flop starts with Q=0."""
        jk = JKFlipFlop()
        assert jk.read() == 0

    def test_set(self):
        """J=1, K=0 sets Q to 1."""
        jk = JKFlipFlop()
        jk.clock(1, 0, 0)
        jk.clock(1, 0, 1)
        assert jk.read() == 1

    def test_reset(self):
        """J=0, K=1 resets Q to 0."""
        jk = JKFlipFlop()
        jk.clock(1, 0, 0); jk.clock(1, 0, 1)  # Set first
        jk.clock(0, 1, 0); jk.clock(0, 1, 1)  # Reset
        assert jk.read() == 0

    def test_hold(self):
        """J=0, K=0 holds Q."""
        jk = JKFlipFlop()
        jk.clock(1, 0, 0); jk.clock(1, 0, 1)  # Set to 1
        jk.clock(0, 0, 0); jk.clock(0, 0, 1)  # Hold
        assert jk.read() == 1

    def test_toggle(self):
        """J=1, K=1 toggles Q."""
        jk = JKFlipFlop()
        assert jk.read() == 0
        jk.clock(1, 1, 0); jk.clock(1, 1, 1)  # Toggle 0->1
        assert jk.read() == 1
        jk.clock(1, 1, 0); jk.clock(1, 1, 1)  # Toggle 1->0
        assert jk.read() == 0
        jk.clock(1, 1, 0); jk.clock(1, 1, 1)  # Toggle 0->1
        assert jk.read() == 1


class TestTFlipFlop:
    """Tests for T Flip-Flop."""

    def test_initial_state(self):
        """T flip-flop starts with Q=0."""
        t = TFlipFlop()
        assert t.read() == 0

    def test_toggle(self):
        """T=1 toggles on each rising edge."""
        t = TFlipFlop()
        t.clock(1, 0); t.clock(1, 1)
        assert t.read() == 1
        t.clock(1, 0); t.clock(1, 1)
        assert t.read() == 0
        t.clock(1, 0); t.clock(1, 1)
        assert t.read() == 1

    def test_hold(self):
        """T=0 holds value."""
        t = TFlipFlop()
        t.clock(1, 0); t.clock(1, 1)  # Toggle to 1
        t.clock(0, 0); t.clock(0, 1)  # Hold
        assert t.read() == 1
        t.clock(0, 0); t.clock(0, 1)  # Hold again
        assert t.read() == 1

    def test_counting_pattern(self):
        """T flip-flop creates binary counting pattern."""
        t = TFlipFlop()
        expected = [1, 0, 1, 0, 1, 0, 1, 0]  # Alternating
        for exp in expected:
            t.clock(1, 0)
            t.clock(1, 1)
            assert t.read() == exp
