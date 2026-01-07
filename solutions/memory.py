"""Memory - Solution File."""

from typing import List


class RAM:
    """256-byte RAM with 8-bit addressing."""

    def __init__(self, size: int = 256):
        """Initialize RAM with given size."""
        self.size = size
        self.memory = [[0] * 8 for _ in range(size)]

    def _addr_to_index(self, address: List[int]) -> int:
        """Convert bit address to integer index."""
        return sum(bit << i for i, bit in enumerate(address))

    def read(self, address: List[int]) -> List[int]:
        """Read data from memory at address."""
        idx = self._addr_to_index(address)
        if 0 <= idx < self.size:
            return self.memory[idx].copy()
        return [0] * 8

    def write(self, address: List[int], data: List[int], enable: int) -> None:
        """Write data to memory at address when enabled."""
        if enable == 1:
            idx = self._addr_to_index(address)
            if 0 <= idx < self.size:
                self.memory[idx] = data.copy()

    def load_program(self, program: List[List[int]], start_addr: int = 0) -> None:
        """Load a program into memory."""
        for i, byte in enumerate(program):
            addr = start_addr + i
            if addr < self.size:
                self.memory[addr] = byte.copy()

    def dump(self, start: int = 0, end: int = 16) -> str:
        """Dump memory contents for debugging."""
        lines = []
        for addr in range(start, min(end, self.size)):
            val = sum(bit << i for i, bit in enumerate(self.memory[addr]))
            lines.append(f"{addr:02X}: {val:02X}")
        return "\n".join(lines)
