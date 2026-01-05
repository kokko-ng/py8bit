"""
Assembler

Converts assembly language to machine code.
"""

from typing import List, Dict, Optional


class Assembler:
    """Two-pass assembler for our 8-bit CPU."""

    def __init__(self):
        self.symbol_table: Dict[str, int] = {}
        self.errors: List[str] = []

    def assemble(self, source: str) -> List[List[int]]:
        """Assemble source code to machine code.

        Args:
            source: Assembly source code

        Returns:
            List of 16-bit instructions (each as list of bits)
        """
        # TODO: Implement assembler
        ...

    def first_pass(self, source: str) -> List[Dict]:
        """First pass: build symbol table and parse lines.

        Args:
            source: Assembly source code

        Returns:
            List of parsed line dictionaries
        """
        # TODO: Implement first pass
        ...

    def second_pass(self, parsed_lines: List[Dict]) -> List[List[int]]:
        """Second pass: generate machine code.

        Args:
            parsed_lines: Output from first pass

        Returns:
            List of 16-bit instructions
        """
        # TODO: Implement second pass
        ...

    def parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single line of assembly.

        Args:
            line: Assembly line

        Returns:
            Dictionary with opcode, operands, label, or None for empty/comment
        """
        # TODO: Implement line parsing
        ...

    def parse_operand(self, operand: str) -> tuple:
        """Parse an operand string.

        Args:
            operand: Operand string (e.g., 'R0', '0x10', 'label')

        Returns:
            Tuple of (type, value) where type is 'reg', 'imm', or 'label'
        """
        # TODO: Implement operand parsing
        ...
