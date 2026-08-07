"""Assembler.

Converts assembly language to machine code.
"""

# NOTE: Generated from solutions/assembler.py by scripts/generate_stubs.py.
# Write your implementations in the '# TODO' bodies below.
# (Maintainers: edit the solution file, not this one, then regenerate.)

from typing import List, Dict, Optional
from computer.isa import encode_instruction


class Assembler:
    """Two-pass assembler for our 8-bit CPU."""

    def __init__(self):
        """Initialize assembler state."""
        self.symbol_table: Dict[str, int] = {}
        self.errors: List[str] = []
        self.data_bytes: Dict[int, int] = {}  # addr -> value

    def assemble(self, source: str) -> List[List[int]]:
        """Assemble source code to machine code.

        Args:
            source: Assembly source code

        Returns:
            List of 16-bit instructions (each as list of bits)
        """
        # TODO: Implement the two-pass assembler
        ...

    def first_pass(self, source: str) -> List[Dict]:
        """First pass: build symbol table and parse lines.

        Args:
            source: Assembly source code

        Returns:
            List of parsed line dictionaries
        """
        # TODO: Implement the first pass (labels and directives)
        ...

    def second_pass(self, parsed_lines: List[Dict]) -> List[List[int]]:
        """Second pass: generate machine code.

        Args:
            parsed_lines: Output from first pass

        Returns:
            List of 16-bit instructions
        """
        # TODO: Implement the second pass (machine code)
        ...

    def parse_line(self, line: str) -> Optional[Dict]:  # type: ignore[type-arg]
        """Parse a single line of assembly.

        Args:
            line: Assembly line

        Returns:
            Dictionary with opcode, operands, label, or None for empty/comment
        """
        # TODO: Implement line parsing
        ...

    def _parse_reg(self, operand: str) -> int:
        operand = operand.strip().upper()
        if operand.startswith("R"):
            return int(operand[1:])
        return 0

    def _parse_value(self, operand: str) -> int:
        operand = operand.strip()
        if operand in self.symbol_table:
            return self.symbol_table[operand]
        if operand.startswith("0x") or operand.startswith("0X"):
            return int(operand, 16)
        return int(operand)
