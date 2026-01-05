"""
Assembler

Converts assembly language to machine code.
"""

from typing import List, Dict, Optional
from computer.isa import encode_instruction


class Assembler:
    """Two-pass assembler for our 8-bit CPU."""

    def __init__(self):
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
        self.symbol_table = {}
        self.errors = []
        self.data_bytes = {}
        parsed_lines = self.first_pass(source)
        return self.second_pass(parsed_lines)

    def first_pass(self, source: str) -> List[Dict]:
        """First pass: build symbol table and parse lines.

        Args:
            source: Assembly source code

        Returns:
            List of parsed line dictionaries
        """
        # TODO: Implement first pass
        parsed_lines = []
        address = 0

        for line_num, line in enumerate(source.split('\n'), 1):
            parsed = self.parse_line(line)
            if parsed is None:
                continue

            if parsed.get('label'):
                self.symbol_table[parsed['label']] = address

            if parsed.get('opcode'):
                parsed['address'] = address
                parsed['line_num'] = line_num
                parsed_lines.append(parsed)
                address += 2  # 16-bit instructions

            if parsed.get('directive') == '.org':
                address = parsed['value']
            elif parsed.get('directive') == '.byte':
                self.data_bytes[address] = parsed.get('value', 0)
                address += 1

        return parsed_lines

    def second_pass(self, parsed_lines: List[Dict]) -> List[List[int]]:
        """Second pass: generate machine code.

        Args:
            parsed_lines: Output from first pass

        Returns:
            List of 16-bit instructions
        """
        # TODO: Implement second pass
        machine_code = []

        for parsed in parsed_lines:
            opcode = parsed.get('opcode', 'NOP').upper()
            operands = parsed.get('operands', [])

            rd, rs1, rs2_imm = 0, 0, 0

            if opcode in ['ADD', 'SUB', 'AND', 'OR', 'XOR']:
                if len(operands) >= 3:
                    rd = self._parse_reg(operands[0])
                    rs1 = self._parse_reg(operands[1])
                    rs2_imm = self._parse_reg(operands[2])
            elif opcode in ['NOT', 'SHL', 'SHR', 'MOV']:
                if len(operands) >= 2:
                    rd = self._parse_reg(operands[0])
                    rs1 = self._parse_reg(operands[1])
            elif opcode in ['LOAD', 'STORE']:
                if len(operands) >= 2:
                    rd = self._parse_reg(operands[0])
                    rs2_imm = self._parse_value(operands[1])
            elif opcode in ['JMP', 'JZ', 'JNZ']:
                if len(operands) >= 1:
                    rs2_imm = self._parse_value(operands[0])

            instruction = encode_instruction(opcode, rd, rs1, rs2_imm)
            machine_code.append(instruction)

        return machine_code

    def parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single line of assembly.

        Args:
            line: Assembly line

        Returns:
            Dictionary with opcode, operands, label, or None for empty/comment
        """
        # TODO: Implement line parsing
        # Remove comments and strip whitespace
        line = line.split(';')[0].strip()
        if not line:
            return None

        result = {}

        # Check for label
        if ':' in line:
            parts = line.split(':', 1)
            result['label'] = parts[0].strip()
            line = parts[1].strip()
            if not line:
                return result

        # Check for directive
        if line.startswith('.'):
            parts = line.split(None, 1)
            result['directive'] = parts[0].lower()
            if len(parts) > 1:
                result['value'] = self._parse_value(parts[1])
            return result

        # Parse instruction
        parts = line.split(None, 1)
        result['opcode'] = parts[0].upper()
        if len(parts) > 1:
            result['operands'] = [op.strip() for op in parts[1].split(',')]

        return result

    def parse_operand(self, operand: str) -> tuple:
        """Parse an operand string.

        Args:
            operand: Operand string (e.g., 'R0', '0x10', 'label')

        Returns:
            Tuple of (type, value) where type is 'reg', 'imm', or 'label'
        """
        # TODO: Implement operand parsing
        operand = operand.strip()
        if operand.upper().startswith('R'):
            return ('reg', int(operand[1:]))
        elif operand in self.symbol_table:
            return ('label', self.symbol_table[operand])
        elif operand.startswith('0x') or operand.startswith('0X'):
            return ('imm', int(operand, 16))
        else:
            return ('imm', int(operand))

    def _parse_reg(self, operand: str) -> int:
        """Parse a register operand."""
        operand = operand.strip().upper()
        if operand.startswith('R'):
            return int(operand[1:])
        return 0

    def _parse_value(self, operand: str) -> int:
        """Parse an immediate value or label."""
        operand = operand.strip()
        if operand in self.symbol_table:
            return self.symbol_table[operand]
        if operand.startswith('0x') or operand.startswith('0X'):
            return int(operand, 16)
        return int(operand)
