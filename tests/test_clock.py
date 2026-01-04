"""Tests for Clock and Control Signals."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.clock import Clock, ControlSignals


class TestClock:
    """Tests for Clock generator."""

    def test_initial_state(self):
        """Clock starts at cycle 0, state 0."""
        clk = Clock()
        assert clk.cycle == 0
        assert clk.get_state() == 0

    def test_tick_toggles_state(self):
        """Tick toggles state between 0 and 1."""
        clk = Clock()
        clk.tick()
        assert clk.get_state() == 1
        clk.tick()
        assert clk.get_state() == 0
        clk.tick()
        assert clk.get_state() == 1

    def test_cycle_increments_on_falling_edge(self):
        """Cycle increments on falling edge (1->0)."""
        clk = Clock()
        clk.tick()  # 0->1
        assert clk.cycle == 0
        clk.tick()  # 1->0 (falling edge)
        assert clk.cycle == 1
        clk.tick()  # 0->1
        assert clk.cycle == 1
        clk.tick()  # 1->0
        assert clk.cycle == 2

    def test_multiple_cycles(self):
        """Multiple complete cycles."""
        clk = Clock()
        for expected in range(1, 6):
            clk.tick()  # rising
            clk.tick()  # falling
            assert clk.cycle == expected

    def test_reset(self):
        """Reset returns to initial state."""
        clk = Clock()
        for _ in range(10):
            clk.tick()
        clk.reset()
        assert clk.cycle == 0
        assert clk.get_state() == 0


class TestControlSignals:
    """Tests for Control Signals container."""

    def test_initial_zero(self):
        """All signals start at zero."""
        sig = ControlSignals()
        assert sig.pc_load == 0
        assert sig.pc_inc == 0
        assert sig.mem_read == 0
        assert sig.mem_write == 0
        assert sig.reg_write == 0
        assert sig.alu_op == [0, 0, 0, 0]

    def test_set_signals(self):
        """Can set individual signals."""
        sig = ControlSignals()
        sig.pc_load = 1
        sig.mem_read = 1
        sig.alu_op = [1, 0, 1, 0]
        assert sig.pc_load == 1
        assert sig.mem_read == 1
        assert sig.alu_op == [1, 0, 1, 0]

    def test_reset(self):
        """Reset clears all signals."""
        sig = ControlSignals()
        sig.pc_load = 1
        sig.mem_write = 1
        sig.reg_write = 1
        sig.reset()
        assert sig.pc_load == 0
        assert sig.mem_write == 0
        assert sig.reg_write == 0

    def test_to_dict(self):
        """to_dict includes key signals."""
        sig = ControlSignals()
        sig.pc_inc = 1
        sig.reg_write = 1
        d = sig.to_dict()
        assert 'pc_inc' in d
        assert 'reg_write' in d
        assert d['pc_inc'] == 1
        assert d['reg_write'] == 1

    def test_multiple_signal_combinations(self):
        """Can set various signal combinations."""
        sig = ControlSignals()

        # FETCH signals
        sig.mem_read = 1
        sig.ir_load = 1
        assert sig.mem_read == 1
        assert sig.ir_load == 1

        sig.reset()

        # LOAD signals
        sig.mem_read = 1
        sig.mem_to_reg = 1
        sig.reg_write = 1
        sig.pc_inc = 1
        assert sig.mem_read == 1
        assert sig.mem_to_reg == 1
        assert sig.reg_write == 1
        assert sig.pc_inc == 1
