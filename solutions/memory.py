"""Memory - RAM (Random Access Memory).

RAM allows reading and writing data at any address.
Our RAM has:
- 256 bytes (8-bit address space)
- 8-bit data width
"""


class RAM:
    """256-byte RAM with 8-bit addressing."""

    def __init__(self, size: int = 256):
        """Initialize RAM with given size."""
        self.size = size
        self.memory = [[0] * 8 for _ in range(size)]

    def _addr_to_index(self, address: list[int]) -> int:
        """Convert bit address to integer index."""
        return sum(bit << i for i, bit in enumerate(address))

    def read(self, address: list[int]) -> list[int]:
        """Read from memory.

        Args:
            address: 8-bit address (LSB at index 0)

        Returns:
            8-bit data at address
        """
        idx = self._addr_to_index(address)
        if 0 <= idx < self.size:
            return self.memory[idx].copy()
        return [0] * 8

    def write(self, address: list[int], data: list[int], enable: int) -> None:
        """Write to memory.

        Args:
            address: 8-bit address
            data: 8-bit data to write
            enable: Write enable (1 to write)
        """
        if enable == 1:
            idx = self._addr_to_index(address)
            if 0 <= idx < self.size:
                self.memory[idx] = data.copy()

    def load_program(self, program: list[list[int]], start_addr: int = 0) -> None:
        """Load a program into memory.

        Args:
            program: List of 8-bit values
            start_addr: Starting address
        """
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
