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

from typing import ClassVar

from solutions.adders import ripple_carry_adder_8bit, subtractor_8bit
from solutions.gates import AND, NOT, OR, XOR


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
        result = [0] * 8
        carry = 0
        overflow = 0

        # Decode opcode (convert to integer for easier comparison)
        op_val = opcode[0] + opcode[1] * 2 + opcode[2] * 4 + opcode[3] * 8

        if op_val == 0:  # ADD
            result, carry = self._add(a, b)
            # Check for signed overflow
            overflow = AND(XOR(a[7], result[7]), AND(NOT(XOR(a[7], b[7])), 1))
        elif op_val == 1:  # SUB
            result, borrow, overflow = self._sub(a, b)
            carry = borrow
        elif op_val == 2:  # AND
            result = self._and(a, b)
        elif op_val == 3:  # OR
            result = self._or(a, b)
        elif op_val == 4:  # XOR
            result = self._xor(a, b)
        elif op_val == 5:  # NOT
            result = self._not(a)
        elif op_val == 6:  # SHL
            result, carry = self._shl(a)
        elif op_val == 7:  # SHR
            result, carry = self._shr(a)
        elif op_val == 8:  # CMP
            # Compare sets flags based on subtraction but returns A
            sub_result, carry, overflow = self._sub(a, b)
            result = a.copy()
            # Calculate flags based on the subtraction result, not the returned result
            flags = self._calculate_flags(sub_result, carry, overflow)
            return result, flags

        flags = self._calculate_flags(result, carry, overflow)
        return result, flags

    def _add(self, a: list[int], b: list[int]) -> tuple[list[int], int]:
        """Perform addition. Returns (result, carry)."""
        return ripple_carry_adder_8bit(a, b)

    def _sub(self, a: list[int], b: list[int]) -> tuple[list[int], int, int]:
        """Perform subtraction. Returns (result, borrow, overflow)."""
        return subtractor_8bit(a, b)

    def _and(self, a: list[int], b: list[int]) -> list[int]:
        """Perform bitwise AND."""
        return [AND(a[i], b[i]) for i in range(8)]

    def _or(self, a: list[int], b: list[int]) -> list[int]:
        """Perform bitwise OR."""
        return [OR(a[i], b[i]) for i in range(8)]

    def _xor(self, a: list[int], b: list[int]) -> list[int]:
        """Perform bitwise XOR."""
        return [XOR(a[i], b[i]) for i in range(8)]

    def _not(self, a: list[int]) -> list[int]:
        """Perform bitwise NOT."""
        return [NOT(a[i]) for i in range(8)]

    def _shl(self, a: list[int]) -> tuple[list[int], int]:
        """Shift left by 1. Returns (result, carry_out)."""
        carry = a[7]  # MSB becomes carry
        result = [0, *a[0:7]]  # Shift left, LSB becomes 0
        return result, carry

    def _shr(self, a: list[int]) -> tuple[list[int], int]:
        """Shift right by 1. Returns (result, carry_out)."""
        carry = a[0]  # LSB becomes carry
        result = [*a[1:8], 0]  # Shift right, MSB becomes 0
        return result, carry

    def _calculate_flags(self, result: list[int], carry: int, overflow: int) -> dict[str, int]:
        """Calculate status flags.

        Args:
            result: 8-bit result
            carry: Carry/borrow bit
            overflow: Overflow bit

        Returns:
            Dictionary with Z, C, N, V flags
        """
        # Zero flag: 1 if all bits are 0
        z = NOT(
            OR(
                OR(OR(result[0], result[1]), OR(result[2], result[3])),
                OR(OR(result[4], result[5]), OR(result[6], result[7])),
            )
        )

        return {
            "Z": z,
            "C": carry,
            "N": result[7],  # Negative = MSB
            "V": overflow,
        }
