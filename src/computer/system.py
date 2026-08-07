"""Full System - Complete 8-bit Computer.

The complete computer system integrating:
- CPU
- Assembler
- Memory initialization
- I/O (simulated)
"""

# NOTE: Generated from solutions/system.py by scripts/generate_stubs.py.
# Write your implementations in the '# TODO' bodies below.
# (Maintainers: edit the solution file, not this one, then regenerate.)

from typing import List, Dict
from computer.cpu import CPU
from computer.assembler import Assembler
from computer.isa import disassemble


class Computer:
    """Complete 8-bit computer system."""

    def __init__(self):
        """Initialize computer with CPU and assembler."""
        self.cpu = CPU()
        self.assembler = Assembler()

    def load_program(self, source) -> None:
        """Load a program from source code or raw bytes.

        Args:
            source: Assembly source code (str) or raw bytes (List[int])
        """
        # TODO: Implement program loading (instructions AND the .byte data section)
        ...

    def load_machine_code(self, code: List[List[int]], start_addr: int = 0) -> None:
        """Load raw machine code into memory.

        Args:
            code: List of 16-bit instructions
            start_addr: Starting address
        """
        # TODO: Implement machine code loading
        ...

    def run(self, max_cycles: int = 1000, debug: bool = False) -> Dict:
        """Run the loaded program until HALT or max_cycles.

        Args:
            max_cycles: Maximum cycles to execute
            debug: If True, print the trace_step() line for each instruction
                (PC, disassembled instruction, register changes)

        Returns:
            Final system state (see dump_state)
        """
        # TODO: Implement run with optional debug tracing (see trace_step)
        ...

    def trace_step(self) -> str:
        """Execute one instruction and return a one-line trace of what it did.

        The trace shows the PC, the disassembled instruction, and every
        register that changed, e.g.::

            PC=0x04 | ADD R0, R1, R2     | R0: 0 -> 8 | Z=0 C=0

        This given helper powers ``run(debug=True)``.

        Returns:
            Trace line, or an empty string if the CPU is already halted
        """
        if self.cpu.halted:
            return ""
        pc = self._bits_to_int(self.cpu.datapath.get_pc())
        instruction = self.cpu.datapath.fetch_instruction()
        before = self._register_snapshot()
        self.cpu.step()
        after = self._register_snapshot()

        line = f"PC=0x{pc:02X} | {disassemble(instruction):<18}"
        changes = [f"{reg}: {before[reg]} -> {after[reg]}" for reg in before if before[reg] != after[reg]]
        if changes:
            line += " | " + ", ".join(changes)
        flags = self.cpu.datapath.flags
        line += f" | Z={flags['Z']} C={flags['C']}"
        return line

    def _register_snapshot(self) -> Dict[str, int]:
        """Read all eight registers as integers."""
        snapshot = {}
        for i in range(8):
            addr = [(i >> j) & 1 for j in range(3)]
            snapshot[f"R{i}"] = self._bits_to_int(self.cpu.datapath.reg_file.read(addr))
        return snapshot

    def reset(self) -> None:
        """Reset the computer to initial state."""
        self.cpu.reset()

    def dump_state(self) -> Dict:
        """Get complete system state for debugging.

        Returns:
            Dictionary with CPU state, register values, memory dump
        """
        # TODO: Implement the state dump
        ...

    def dump_registers(self) -> str:
        """Get formatted register dump."""
        # TODO: Implement the register dump
        ...

    def dump_memory(self, start: int = 0, end: int = 32) -> str:
        """Get formatted memory dump."""
        return self.cpu.datapath.memory.dump(start, end)

    def _bits_to_int(self, bits: List[int]) -> int:
        return sum(bit << i for i, bit in enumerate(bits))

    def _format_bits(self, bits: List[int]) -> str:
        val = self._bits_to_int(bits)
        return f"{val:3d} (0x{val:02X})"
