"""
ALU - Arithmetic Logic Unit - Solution File
"""

from typing import List, Tuple, Dict
from solutions.gates import AND, OR, XOR, NOT
from solutions.adders import ripple_carry_adder_8bit, subtractor_8bit


class ALU:
    """8-bit Arithmetic Logic Unit."""

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
        """Execute an ALU operation."""
        result = [0] * 8
        carry = 0
        overflow = 0

        # Decode opcode (convert to integer for easier comparison)
        op_val = opcode[0] + opcode[1]*2 + opcode[2]*4 + opcode[3]*8

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

    def _add(self, a: List[int], b: List[int]) -> Tuple[List[int], int]:
        """Perform addition."""
        return ripple_carry_adder_8bit(a, b)

    def _sub(self, a: List[int], b: List[int]) -> Tuple[List[int], int, int]:
        """Perform subtraction."""
        return subtractor_8bit(a, b)

    def _and(self, a: List[int], b: List[int]) -> List[int]:
        """Perform bitwise AND."""
        return [AND(a[i], b[i]) for i in range(8)]

    def _or(self, a: List[int], b: List[int]) -> List[int]:
        """Perform bitwise OR."""
        return [OR(a[i], b[i]) for i in range(8)]

    def _xor(self, a: List[int], b: List[int]) -> List[int]:
        """Perform bitwise XOR."""
        return [XOR(a[i], b[i]) for i in range(8)]

    def _not(self, a: List[int]) -> List[int]:
        """Perform bitwise NOT."""
        return [NOT(a[i]) for i in range(8)]

    def _shl(self, a: List[int]) -> Tuple[List[int], int]:
        """Shift left by 1."""
        carry = a[7]  # MSB becomes carry
        result = [0] + a[0:7]  # Shift left, LSB becomes 0
        return result, carry

    def _shr(self, a: List[int]) -> Tuple[List[int], int]:
        """Shift right by 1."""
        carry = a[0]  # LSB becomes carry
        result = a[1:8] + [0]  # Shift right, MSB becomes 0
        return result, carry

    def _calculate_flags(self, result: List[int], carry: int, overflow: int) -> Dict[str, int]:
        """Calculate status flags."""
        # Zero flag: 1 if all bits are 0
        z = NOT(OR(OR(OR(result[0], result[1]), OR(result[2], result[3])),
                   OR(OR(result[4], result[5]), OR(result[6], result[7]))))

        return {
            'Z': z,
            'C': carry,
            'N': result[7],  # Negative = MSB
            'V': overflow
        }
