"""
CPU - Central Processing Unit

The CPU integrates all components and executes the fetch-decode-execute cycle.
"""

from typing import List, Dict, Optional
from computer.datapath import DataPath
from computer.control import ControlUnit
from computer.decoder import InstructionDecoder
from computer.clock import Clock


class CPU:
    """8-bit CPU - integrates datapath and control."""

    def __init__(self):
        self.datapath = DataPath()
        self.control = ControlUnit()
        self.decoder = InstructionDecoder()
        self.clock = Clock()
        self.halted = False
        self.current_instruction = None

    def reset(self) -> None:
        """Reset CPU to initial state."""
        self.datapath.pc.clock(load=0, load_value=[0]*8, increment=0, reset=1, clk=1)
        self.control.reset()
        self.halted = False
        self.current_instruction = None

    def fetch(self) -> List[int]:
        """Fetch instruction from memory.

        Returns:
            16-bit instruction
        """
        # TODO: Implement fetch
        ...

    def decode(self, instruction: List[int]) -> Dict:
        """Decode instruction.

        Args:
            instruction: 16-bit instruction

        Returns:
            Decoded instruction fields
        """
        # TODO: Implement decode
        ...

    def execute(self, decoded: Dict) -> None:
        """Execute instruction.

        Args:
            decoded: Decoded instruction fields
        """
        # TODO: Implement execute
        ...

    def step(self) -> bool:
        """Execute one complete instruction.

        Returns:
            True if CPU is still running, False if halted
        """
        # TODO: Implement single step
        ...

    def run(self, max_cycles: int = 1000) -> int:
        """Run until HALT or max cycles reached.

        Args:
            max_cycles: Maximum cycles to execute

        Returns:
            Number of cycles executed
        """
        # TODO: Implement run loop
        ...

    def get_state(self) -> Dict:
        """Get current CPU state for debugging."""
        return {
            'pc': self.datapath.get_pc(),
            'flags': self.datapath.flags.copy(),
            'halted': self.halted,
            'cycle': self.clock.cycle,
        }
