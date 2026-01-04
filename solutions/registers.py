"""
Registers - Solution File
"""

from typing import List
from solutions.sequential import DFlipFlop


class Register8:
    """8-bit register built from D flip-flops."""

    def __init__(self):
        self.bits = [DFlipFlop() for _ in range(8)]

    def clock(self, data: List[int], enable: int, clk: int) -> List[int]:
        """Update register on clock edge when enabled."""
        if enable == 1:
            for i in range(8):
                self.bits[i].clock(data[i], clk)
        return self.read()

    def read(self) -> List[int]:
        """Read current register value."""
        return [self.bits[i].read() for i in range(8)]


class RegisterFile:
    """Register file - collection of registers with addressing."""

    def __init__(self, num_registers: int = 8):
        self.registers = [Register8() for _ in range(num_registers)]
        self.num_registers = num_registers

    def _addr_to_index(self, addr: List[int]) -> int:
        """Convert bit address to integer index."""
        return sum(bit << i for i, bit in enumerate(addr))

    def read(self, addr: List[int]) -> List[int]:
        """Read from a register."""
        idx = self._addr_to_index(addr)
        if idx < self.num_registers:
            return self.registers[idx].read()
        return [0] * 8

    def write(self, addr: List[int], data: List[int], enable: int, clk: int) -> None:
        """Write to a register.

        To ensure proper edge-triggered behavior, we pulse the clock
        by first setting it low, then high.
        """
        if enable == 1:
            idx = self._addr_to_index(addr)
            if idx < self.num_registers:
                # Pulse clock: low then high for rising edge
                self.registers[idx].clock(data, 1, 0)  # Clock low
                self.registers[idx].clock(data, 1, 1)  # Clock high (rising edge)

    def read_two(self, addr1: List[int], addr2: List[int]) -> tuple:
        """Read from two registers simultaneously."""
        return (self.read(addr1), self.read(addr2))
