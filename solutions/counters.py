"""Counters - Solution File."""

from typing import List
from solutions.adders import ripple_carry_adder_8bit


class BinaryCounter8:
    """8-bit binary counter."""

    def __init__(self):
        """Initialize binary counter."""
        self.count = [0] * 8

    def clock(self, enable: int = 1, reset: int = 0, clk: int = 1) -> List[int]:
        """Increment counter on clock edge."""
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
    """Program Counter with load, increment, and reset."""

    def __init__(self):
        """Initialize program counter."""
        self.value = [0] * 8

    def clock(self, load: int, load_value: List[int], increment: int, reset: int, clk: int) -> List[int]:
        """Update PC on clock edge."""
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
