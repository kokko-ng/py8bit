"""Assembler.

Converts assembly language to machine code.
"""

from typing import Dict, List, Optional

from computer.isa import encode_instruction  # noqa: F401


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
        # TODO: Implement assembler
        pass

    def first_pass(self, source: str) -> List[Dict]:
        """First pass: build symbol table and parse lines.

        Args:
            source: Assembly source code

        Returns:
            List of parsed line dictionaries
        """
        # TODO: Implement first pass
        pass

    def second_pass(self, parsed_lines: List[Dict]) -> List[List[int]]:
        """Second pass: generate machine code.

        Args:
            parsed_lines: Output from first pass

        Returns:
            List of 16-bit instructions
        """
        # TODO: Implement second pass
        pass

    def parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single line of assembly.

        Args:
            line: Assembly line

        Returns:
            Dictionary with opcode, operands, label, or None for empty/comment
        """
        # TODO: Implement line parsing
        # Remove comments and strip whitespace
        pass

    def parse_operand(self, operand: str) -> tuple:
        """Parse an operand string.

        Args:
            operand: Operand string (e.g., 'R0', '0x10', 'label')

        Returns:
            Tuple of (type, value) where type is 'reg', 'imm', or 'label'
        """
        # TODO: Implement operand parsing
        pass

    def _parse_reg(self, operand: str) -> int:
        """Parse a register operand."""
        operand = operand.strip().upper()
        if operand.startswith("R"):
            return int(operand[1:])
        return 0

    def _parse_value(self, operand: str) -> int:
        """Parse an immediate value or label."""
        operand = operand.strip()
        if operand in self.symbol_table:
            return self.symbol_table[operand]
        if operand.startswith("0x") or operand.startswith("0X"):
            return int(operand, 16)
        return int(operand)
