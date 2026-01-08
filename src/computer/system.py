"""Full System - Complete 8-bit Computer.

The complete computer system integrating:
- CPU
- Assembler
- Memory initialization
- I/O (simulated)
"""

from typing import List, Dict
from computer.cpu import CPU
from computer.assembler import Assembler


class Computer:
    """Complete 8-bit computer system."""

    def __init__(self):
        """Initialize computer with CPU and assembler."""
        self.cpu = CPU()
        self.assembler = Assembler()

    def load_program(self, source: str) -> None:
        """Assemble and load a program.

        Args:
            source: Assembly source code
        """
        # TODO: Implement program loading
        ...

    def load_machine_code(self, code: List[List[int]], start_addr: int = 0) -> None:
        """Load raw machine code into memory.

        Args:
            code: List of 16-bit instructions
            start_addr: Starting address
        """
        # TODO: Implement machine code loading
        # Convert 16-bit instructions to bytes and load
        ...

    def run(self, max_cycles: int = 1000, debug: bool = False) -> Dict:
        """Run the loaded program.

        Args:
            max_cycles: Maximum cycles to execute
            debug: If True, print state after each instruction

        Returns:
            Final CPU state
        """
        # TODO: Implement run with optional debug output
        ...

    def reset(self) -> None:
        """Reset the computer."""
        self.cpu.reset()

    def dump_state(self) -> Dict:
        """Get complete system state for debugging.

        Returns:
            Dictionary with CPU state, register values, memory dump
        """
        # TODO: Implement state dump
        ...

    def dump_registers(self) -> str:
        """Get formatted register dump."""
        # TODO: Implement register dump
        ...

    def dump_memory(self, start: int = 0, end: int = 32) -> str:
        """Get formatted memory dump."""
        return self.cpu.datapath.memory.dump(start, end)

    def _bits_to_int(self, bits: List[int]) -> int:
        """Convert bit list to integer."""
        return sum(bit << i for i, bit in enumerate(bits))

    def _format_bits(self, bits: List[int]) -> str:
        """Format bit list as decimal and hex."""
        val = self._bits_to_int(bits)
        return f"{val:3d} (0x{val:02X})"
