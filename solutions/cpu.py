"""CPU - Central Processing Unit.

The CPU integrates all components and executes the fetch-decode-execute cycle.
"""

from typing import List, Dict
from solutions.datapath import DataPath
from solutions.control import ControlUnit
from solutions.decoder import InstructionDecoder
from solutions.clock import Clock


class CPU:
    """8-bit CPU - integrates datapath and control."""

    def __init__(self):
        """Initialize CPU components."""
        self.datapath = DataPath()
        self.control = ControlUnit()
        self.decoder = InstructionDecoder()
        self.clock = Clock()
        self.halted = False
        self.current_instruction = None

    def reset(self) -> None:
        """Reset CPU to initial state."""
        self.datapath.pc.clock(load=0, load_value=[0] * 8, increment=0, reset=1, clk=1)
        self.control.reset()
        self.halted = False
        self.current_instruction = None

    def fetch(self) -> List[int]:
        """Fetch instruction from memory.

        Returns:
            16-bit instruction
        """
        return self.datapath.fetch_instruction()

    def decode(self, instruction: List[int]) -> Dict:
        """Decode instruction.

        Args:
            instruction: 16-bit instruction

        Returns:
            Decoded instruction fields
        """
        return self.decoder.decode(instruction)

    def execute(self, decoded: Dict, signals) -> None:
        """Execute instruction.

        Args:
            decoded: Decoded instruction fields
            signals: Control signals for this instruction
        """
        if decoded.get("opcode_name") == "HALT":
            self.halted = True
            return

        self.datapath.execute_cycle(signals, decoded)

    def step(self) -> bool:
        """Execute one complete instruction.

        Returns:
            True if CPU is still running, False if halted
        """
        if self.halted:
            return False

        # Fetch
        instruction = self.fetch()
        self.datapath.load_instruction(instruction)

        # Decode
        decoded = self.decode(instruction)
        self.current_instruction = decoded

        # Generate control signals
        signals = self.control.generate_signals(decoded, self.datapath.flags)

        # Execute
        self.execute(decoded, signals)

        # Increment PC by 2 (if not a jump that modified it, and not HALT)
        # 16-bit instructions take 2 bytes
        opname = decoded.get("opcode_name", "")
        if opname == "HALT":
            pass  # Don't increment on HALT
        elif opname == "JMP":
            pass  # JMP always loads PC, don't increment
        elif opname in ["JZ", "JNZ"]:
            # Conditional jump: check if jump was taken (pc_load was set)
            if not signals.pc_load:
                # Jump not taken, increment PC to next instruction
                self.datapath.pc.clock(load=0, load_value=[0] * 8, increment=1, reset=0, clk=1)
                self.datapath.pc.clock(load=0, load_value=[0] * 8, increment=1, reset=0, clk=1)
        else:
            # Normal instruction, increment PC
            self.datapath.pc.clock(load=0, load_value=[0] * 8, increment=1, reset=0, clk=1)
            self.datapath.pc.clock(load=0, load_value=[0] * 8, increment=1, reset=0, clk=1)

        self.clock.tick()
        return not self.halted

    def run(self, max_cycles: int = 1000) -> int:
        """Run until HALT or max cycles reached.

        Args:
            max_cycles: Maximum cycles to execute

        Returns:
            Number of cycles executed
        """
        cycles = 0
        while cycles < max_cycles and self.step():
            cycles += 1
        return cycles

    def get_state(self) -> Dict:
        """Get current CPU state for debugging."""
        return {
            "pc": self.datapath.get_pc(),
            "flags": self.datapath.flags.copy(),
            "halted": self.halted,
            "cycle": self.clock.cycle,
        }
