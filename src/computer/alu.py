"""ALU - Arithmetic Logic Unit.

The ALU is the computational heart of the CPU. It performs arithmetic and
logical operations based on an opcode input.

Operations (4-bit opcode):
- 0000: ADD - Add A and B
- 0001: SUB - Subtract B from A
- 0010: AND - Bitwise AND
- 0011: OR  - Bitwise OR
- 0100: XOR - Bitwise XOR
- 0101: NOT - Bitwise NOT of A
- 0110: SHL - Shift A left by 1
- 0111: SHR - Shift A right by 1
- 1000: CMP - Compare (set flags only, result = A)

Flags:
- Z (Zero): Result is zero
- C (Carry): Carry/borrow occurred
- N (Negative): Result MSB is 1
- V (Overflow): Signed overflow occurred
"""

# NOTE: Generated from solutions/alu.py by scripts/generate_stubs.py.
# Write your implementations in the '# TODO' bodies below.
# (Maintainers: edit the solution file, not this one, then regenerate.)

from typing import ClassVar

from computer.adders import ripple_carry_adder_8bit, subtractor_8bit
from computer.gates import AND, NOT, OR, XOR


class ALU:
    """8-bit Arithmetic Logic Unit."""

    OP_ADD: ClassVar[list[int]] = [0, 0, 0, 0]
    OP_SUB: ClassVar[list[int]] = [1, 0, 0, 0]
    OP_AND: ClassVar[list[int]] = [0, 1, 0, 0]
    OP_OR: ClassVar[list[int]] = [1, 1, 0, 0]
    OP_XOR: ClassVar[list[int]] = [0, 0, 1, 0]
    OP_NOT: ClassVar[list[int]] = [1, 0, 1, 0]
    OP_SHL: ClassVar[list[int]] = [0, 1, 1, 0]
    OP_SHR: ClassVar[list[int]] = [1, 1, 1, 0]
    OP_CMP: ClassVar[list[int]] = [0, 0, 0, 1]

    def __call__(self, a: list[int], b: list[int], opcode: list[int]) -> tuple[list[int], dict[str, int]]:
        """Execute an ALU operation.

        Args:
            a: First operand (8 bits, LSB at index 0)
            b: Second operand (8 bits, LSB at index 0)
            opcode: 4-bit operation code (LSB at index 0)

        Returns:
            Tuple of (result, flags)
            - result: 8-bit result (LSB at index 0)
            - flags: Dictionary with keys 'Z', 'C', 'N', 'V'
        """
        # TODO: Implement the ALU: dispatch on opcode, compute result and flags
        ...

    def _add(self, a: list[int], b: list[int]) -> tuple[list[int], int]:
        """Perform addition. Returns (result, carry)."""
        # TODO: Implement using ripple_carry_adder_8bit
        ...

    def _sub(self, a: list[int], b: list[int]) -> tuple[list[int], int, int]:
        """Perform subtraction. Returns (result, borrow, overflow)."""
        # TODO: Implement using subtractor_8bit
        ...

    def _and(self, a: list[int], b: list[int]) -> list[int]:
        """Perform bitwise AND."""
        # TODO: Implement bitwise AND
        ...

    def _or(self, a: list[int], b: list[int]) -> list[int]:
        """Perform bitwise OR."""
        # TODO: Implement bitwise OR
        ...

    def _xor(self, a: list[int], b: list[int]) -> list[int]:
        """Perform bitwise XOR."""
        # TODO: Implement bitwise XOR
        ...

    def _not(self, a: list[int]) -> list[int]:
        """Perform bitwise NOT."""
        # TODO: Implement bitwise NOT
        ...

    def _shl(self, a: list[int]) -> tuple[list[int], int]:
        """Shift left by 1. Returns (result, carry_out)."""
        # TODO: Implement shift left (MSB becomes the carry)
        ...

    def _shr(self, a: list[int]) -> tuple[list[int], int]:
        """Shift right by 1. Returns (result, carry_out)."""
        # TODO: Implement shift right (LSB becomes the carry)
        ...

    def _calculate_flags(self, result: list[int], carry: int, overflow: int) -> dict[str, int]:
        """Calculate status flags.

        Args:
            result: 8-bit result
            carry: Carry/borrow bit
            overflow: Overflow bit

        Returns:
            Dictionary with Z, C, N, V flags
        """
        # TODO: Implement flag calculation (Z, C, N, V)
        ...
