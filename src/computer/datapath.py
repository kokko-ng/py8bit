"""Data Path.

The data path connects all CPU components:
- Program Counter
- Memory
- Register File
- ALU
- Instruction Register

It routes data between components based on control signals.
"""

from typing import List, Dict
from computer.counters import ProgramCounter
from computer.memory import RAM
from computer.registers import RegisterFile
from computer.alu import ALU
from computer.clock import ControlSignals


class DataPath:
    """CPU Data Path - connects all components."""

    def __init__(self):
        """Initialize data path components."""
        self.pc = ProgramCounter()
        self.memory = RAM()
        self.reg_file = RegisterFile()
        self.alu = ALU()
        self.ir = [0] * 16  # Instruction register (16-bit)
        self.flags = {"Z": 0, "C": 0, "N": 0, "V": 0}

    def execute_cycle(self, signals: ControlSignals, decoded: Dict) -> None:
        """Execute one clock cycle based on control signals.

        Args:
            signals: Control signals for this cycle
            decoded: Decoded instruction fields
        """
        # TODO: Implement data path execution
        ...

    def fetch_instruction(self) -> List[int]:
        """Fetch instruction at current PC.

        Returns:
            16-bit instruction
        """
        # TODO: Implement instruction fetch
        ...

    def load_instruction(self, instruction: List[int]) -> None:
        """Load instruction into IR."""
        self.ir = instruction.copy()

    def get_pc(self) -> List[int]:
        """Get current PC value."""
        return self.pc.read()

    def set_pc(self, value: List[int]) -> None:
        """Set PC value (for jumps)."""
        self.pc.clock(load=1, load_value=value, increment=0, reset=0, clk=1)
