"""
Counters - Sequential Counting Circuits

Counters increment their value on each clock cycle.
Essential for the Program Counter in the CPU.
"""

from typing import List
from computer.adders import ripple_carry_adder_8bit


class BinaryCounter8:
    """8-bit binary counter."""

    def __init__(self):
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
        # TODO: Implement binary counter
        if reset == 1:
            self.count = [0] * 8
        elif enable == 1:
            one = [1] + [0] * 7
            self.count, _ = ripple_carry_adder_8bit(self.count, one)
        # If enable == 0, hold current value
        return self.count.copy()

    def read(self) -> List[int]:
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
        self.value = [0] * 8

    def clock(self, load: int, load_value: List[int],
              increment: int, reset: int, clk: int) -> List[int]:
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
        # TODO: Implement program counter
        # Priority: reset > load > increment
        if reset == 1:
            self.value = [0] * 8
        elif load == 1:
            self.value = load_value.copy()
        elif increment == 1:
            one = [1] + [0] * 7
            self.value, _ = ripple_carry_adder_8bit(self.value, one)
        # Otherwise hold
        return self.value.copy()

    def read(self) -> List[int]:
        return self.value.copy()
