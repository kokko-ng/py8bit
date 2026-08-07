"""Full System - Complete 8-bit Computer.

The complete computer system integrating:
- CPU
- Assembler
- Memory initialization
- I/O (simulated)
"""

from typing import List, Dict
from solutions.cpu import CPU
from solutions.assembler import Assembler
from solutions.isa import disassemble


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
        if isinstance(source, str):
            # Assembly source code
            code = self.assembler.assemble(source)
            self.load_machine_code(code)
            # Also load data bytes from .byte directives
            for addr, value in self.assembler.data_bytes.items():
                addr_bits = [(addr >> i) & 1 for i in range(8)]
                value_bits = [(value >> i) & 1 for i in range(8)]
                self.cpu.datapath.memory.write(addr_bits, value_bits, 1)
        else:
            # Raw bytes - load directly into memory
            for addr, byte_val in enumerate(source):
                addr_bits = [(addr >> i) & 1 for i in range(8)]
                value_bits = [(byte_val >> i) & 1 for i in range(8)]
                self.cpu.datapath.memory.write(addr_bits, value_bits, 1)

    def load_machine_code(self, code: List[List[int]], start_addr: int = 0) -> None:
        """Load raw machine code into memory.

        Args:
            code: List of 16-bit instructions
            start_addr: Starting address
        """
        # Convert 16-bit instructions to bytes and load
        for i, instruction in enumerate(code):
            addr = start_addr + i * 2
            # Split into two bytes
            low_byte = instruction[:8]
            high_byte = instruction[8:] if len(instruction) > 8 else [0] * 8
            addr_bits = [(addr >> j) & 1 for j in range(8)]
            self.cpu.datapath.memory.write(addr_bits, low_byte, 1)
            addr_bits = [((addr + 1) >> j) & 1 for j in range(8)]
            self.cpu.datapath.memory.write(addr_bits, high_byte, 1)

    def run(self, max_cycles: int = 1000, debug: bool = False) -> Dict:
        """Run the loaded program until HALT or max_cycles.

        Args:
            max_cycles: Maximum cycles to execute
            debug: If True, print the trace_step() line for each instruction
                (PC, disassembled instruction, register changes)

        Returns:
            Final system state (see dump_state)
        """
        cycles = 0
        while cycles < max_cycles and not self.cpu.halted:
            if debug:
                trace = self.trace_step()
                if trace:
                    print(trace)
            elif not self.cpu.step():
                break
            cycles += 1
        return self.dump_state()

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
        state = self.cpu.get_state()
        state["registers"] = {}
        for i in range(8):
            addr = [(i >> j) & 1 for j in range(3)]
            val = self.cpu.datapath.reg_file.read(addr)
            state["registers"][f"R{i}"] = self._bits_to_int(val)
        return state

    def dump_registers(self) -> str:
        """Get formatted register dump."""
        lines = []
        for i in range(8):
            addr = [(i >> j) & 1 for j in range(3)]
            val = self.cpu.datapath.reg_file.read(addr)
            lines.append(f"R{i}: {self._bits_to_int(val):3d} (0x{self._bits_to_int(val):02X})")
        return "\n".join(lines)

    def dump_memory(self, start: int = 0, end: int = 32) -> str:
        """Get formatted memory dump."""
        return self.cpu.datapath.memory.dump(start, end)

    def _bits_to_int(self, bits: List[int]) -> int:
        return sum(bit << i for i, bit in enumerate(bits))

    def _format_bits(self, bits: List[int]) -> str:
        val = self._bits_to_int(bits)
        return f"{val:3d} (0x{val:02X})"
