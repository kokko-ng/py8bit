"""Full System - Solution File."""

from typing import List, Dict
from solutions.cpu import CPU
from solutions.assembler import Assembler


class Computer:
    """Complete 8-bit computer system."""

    def __init__(self):
        """Initialize computer with CPU and assembler."""
        self.cpu = CPU()
        self.assembler = Assembler()

    def load_program(self, source: str) -> None:
        """Load and assemble a program from source code."""
        code = self.assembler.assemble(source)
        self.load_machine_code(code)
        # Also load data bytes from .byte directives
        for addr, value in self.assembler.data_bytes.items():
            addr_bits = [(addr >> i) & 1 for i in range(8)]
            value_bits = [(value >> i) & 1 for i in range(8)]
            self.cpu.datapath.memory.write(addr_bits, value_bits, 1)

    def load_machine_code(self, code: List[List[int]], start_addr: int = 0) -> None:
        """Load machine code into memory."""
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
        """Run the computer until HALT or max cycles."""
        cycles = 0
        while cycles < max_cycles:
            if debug:
                print(f"Cycle {cycles}: PC={self._format_bits(self.cpu.datapath.get_pc())}")
            if not self.cpu.step():
                break
            cycles += 1
        return self.dump_state()

    def reset(self) -> None:
        """Reset the computer to initial state."""
        self.cpu.reset()

    def dump_state(self) -> Dict:
        """Get current computer state."""
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

    def _bits_to_int(self, bits: List[int]) -> int:
        return sum(bit << i for i, bit in enumerate(bits))

    def _format_bits(self, bits: List[int]) -> str:
        val = self._bits_to_int(bits)
        return f"{val:3d} (0x{val:02X})"
