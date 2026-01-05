"""
ALU - Arithmetic Logic Unit

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

from typing import List, Tuple, Dict
from computer.gates import AND, OR, XOR, NOT
from computer.adders import ripple_carry_adder_8bit, subtractor_8bit
from computer.combinational import mux_8to1


class ALU:
    """8-bit Arithmetic Logic Unit."""

    # Opcode definitions
    OP_ADD = [0, 0, 0, 0]
    OP_SUB = [1, 0, 0, 0]
    OP_AND = [0, 1, 0, 0]
    OP_OR  = [1, 1, 0, 0]
    OP_XOR = [0, 0, 1, 0]
    OP_NOT = [1, 0, 1, 0]
    OP_SHL = [0, 1, 1, 0]
    OP_SHR = [1, 1, 1, 0]
    OP_CMP = [0, 0, 0, 1]

    def __call__(self, a: List[int], b: List[int], opcode: List[int]) -> Tuple[List[int], Dict[str, int]]:
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
        # TODO: Implement ALU
        # 1. Decode opcode and perform the operation
        # 2. Calculate flags based on the result
        # 3. Return (result, flags)
        ...

    def _add(self, a: List[int], b: List[int]) -> Tuple[List[int], int]:
        """Perform addition. Returns (result, carry)."""
        # TODO: Implement using ripple_carry_adder_8bit
        ...

    def _sub(self, a: List[int], b: List[int]) -> Tuple[List[int], int, int]:
        """Perform subtraction. Returns (result, borrow, overflow)."""
        # TODO: Implement using subtractor_8bit
        ...

    def _and(self, a: List[int], b: List[int]) -> List[int]:
        """Perform bitwise AND."""
        # TODO: Implement bitwise AND
        ...

    def _or(self, a: List[int], b: List[int]) -> List[int]:
        """Perform bitwise OR."""
        # TODO: Implement bitwise OR
        ...

    def _xor(self, a: List[int], b: List[int]) -> List[int]:
        """Perform bitwise XOR."""
        # TODO: Implement bitwise XOR
        ...

    def _not(self, a: List[int]) -> List[int]:
        """Perform bitwise NOT."""
        # TODO: Implement bitwise NOT
        ...

    def _shl(self, a: List[int]) -> Tuple[List[int], int]:
        """Shift left by 1. Returns (result, carry_out)."""
        # TODO: Implement shift left
        # The MSB becomes the carry, all bits shift left, LSB becomes 0
        ...

    def _shr(self, a: List[int]) -> Tuple[List[int], int]:
        """Shift right by 1. Returns (result, carry_out)."""
        # TODO: Implement shift right
        # The LSB becomes the carry, all bits shift right, MSB becomes 0
        ...

    def _calculate_flags(self, result: List[int], carry: int, overflow: int) -> Dict[str, int]:
        """Calculate status flags.

        Args:
            result: 8-bit result
            carry: Carry/borrow bit
            overflow: Overflow bit

        Returns:
            Dictionary with Z, C, N, V flags
        """
        # TODO: Implement flag calculation
        # Z: 1 if all result bits are 0
        # C: carry bit
        # N: MSB of result
        # V: overflow bit
        ...
