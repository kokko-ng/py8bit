"""
Registers - Multi-bit Storage Elements

Registers are groups of flip-flops that store multi-bit values.
They are fundamental for holding data in the CPU.

Components:
- Register8: 8-bit register
- RegisterFile: Collection of registers with addressing
"""

from typing import List
from computer.sequential import DFlipFlop


class Register8:
    """8-bit register built from D flip-flops."""

    def __init__(self):
        self.bits = [DFlipFlop() for _ in range(8)]

    def clock(self, data: List[int], enable: int, clk: int) -> List[int]:
        """Update register on clock edge when enabled.

        Args:
            data: 8-bit input data (LSB at index 0)
            enable: Write enable signal
            clk: Clock signal

        Returns:
            Current register value
        """
        # TODO: Implement 8-bit register
        # Only update bits if enable=1 on clock edge
        if enable == 1:
            for i in range(8):
                self.bits[i].clock(data[i], clk)
        return self.read()

    def read(self) -> List[int]:
        """Read current register value."""
        # TODO: Return current values of all flip-flops
        return [self.bits[i].read() for i in range(8)]


class RegisterFile:
    """Register file - collection of registers with addressing.

    Contains 8 registers addressable by 3-bit address.
    Supports simultaneous read of 2 registers and write of 1.
    """

    def __init__(self, num_registers: int = 8):
        self.registers = [Register8() for _ in range(num_registers)]
        self.num_registers = num_registers

    def _addr_to_index(self, addr: List[int]) -> int:
        """Convert bit address to integer index."""
        return sum(bit << i for i, bit in enumerate(addr))

    def read(self, addr: List[int]) -> List[int]:
        """Read from a register.

        Args:
            addr: 3-bit register address (LSB at index 0)

        Returns:
            8-bit register value
        """
        # TODO: Implement register read using address
        idx = self._addr_to_index(addr)
        if idx < self.num_registers:
            return self.registers[idx].read()
        return [0] * 8

    def write(self, addr: List[int], data: List[int], enable: int, clk: int) -> None:
        """Write to a register.

        Args:
            addr: 3-bit register address
            data: 8-bit data to write
            enable: Write enable signal
            clk: Clock signal
        """
        # TODO: Implement register write
        # Decode address and write to selected register
        if enable == 1:
            idx = self._addr_to_index(addr)
            if idx < self.num_registers:
                # Pulse clock: low then high for rising edge
                self.registers[idx].clock(data, 1, 0)  # Clock low
                self.registers[idx].clock(data, 1, 1)  # Clock high (rising edge)

    def read_two(self, addr1: List[int], addr2: List[int]) -> tuple:
        """Read from two registers simultaneously.

        Args:
            addr1: First register address
            addr2: Second register address

        Returns:
            Tuple of (value1, value2)
        """
        return (self.read(addr1), self.read(addr2))
