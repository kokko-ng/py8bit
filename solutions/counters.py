"""Counters - Sequential Counting Circuits.

Counters increment their value on each clock cycle.
Essential for the Program Counter in the CPU.
"""

from typing import List
from solutions.adders import ripple_carry_adder_8bit


class BinaryCounter8:
    """8-bit binary counter."""

    def __init__(self):
        """Initialize binary counter."""
        self.count = [0] * 8

    def clock(self, enable: int = 1, reset: int = 0, clk: int = 1) -> List[int]:
        """Increment counter on clock.

        Args:
            enable: Count enable (if 0, counter holds)
            reset: Synchronous reset (if 1, counter goes to 0)
            clk: Clock signal

        Returns:
            Current count value
        """
        if reset == 1:
            self.count = [0] * 8
        elif enable == 1:
            one = [1, 0, 0, 0, 0, 0, 0, 0]
            self.count, _ = ripple_carry_adder_8bit(self.count, one)
        return self.count.copy()

    def read(self) -> List[int]:
        """Read current counter value."""
        return self.count.copy()


class ProgramCounter:
    """Program Counter with load, increment, and reset.

    The PC holds the address of the next instruction.
    It can:
    - Increment by 1 (normal execution)
    - Load a new value (for jumps)
    - Reset to 0 (on startup)
    """

    def __init__(self):
        """Initialize program counter."""
        self.value = [0] * 8

    def clock(self, load: int, load_value: List[int], increment: int, reset: int, clk: int) -> List[int]:
        """Update PC on clock edge.

        Priority: reset > load > increment

        Args:
            load: If 1, load load_value into PC
            load_value: Value to load (for jumps)
            increment: If 1, increment PC by 1
            reset: If 1, reset PC to 0
            clk: Clock signal

        Returns:
            Current PC value
        """
        if reset == 1:
            self.value = [0] * 8
        elif load == 1:
            self.value = load_value.copy()
        elif increment == 1:
            one = [1, 0, 0, 0, 0, 0, 0, 0]
            self.value, _ = ripple_carry_adder_8bit(self.value, one)
        return self.value.copy()

    def read(self) -> List[int]:
        """Read current PC value."""
        return self.value.copy()
