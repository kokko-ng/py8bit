"""
Assembler - Solution File
"""

from typing import List, Dict, Optional, Tuple
import re
from solutions.isa import OPCODES, encode_instruction


class Assembler:
    """Two-pass assembler."""

    def __init__(self):
        self.symbol_table: Dict[str, int] = {}
        self.errors: List[str] = []
        self.data_bytes: Dict[int, int] = {}  # addr -> value

    def assemble(self, source: str) -> List[List[int]]:
        self.symbol_table = {}
        self.errors = []
        self.data_bytes = {}
        parsed_lines = self.first_pass(source)
        return self.second_pass(parsed_lines)

    def first_pass(self, source: str) -> List[Dict]:
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
                # Store the byte value at current address
                self.data_bytes[address] = parsed.get('value', 0)
                address += 1

        return parsed_lines

    def second_pass(self, parsed_lines: List[Dict]) -> List[List[int]]:
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

    def _parse_reg(self, operand: str) -> int:
        operand = operand.strip().upper()
        if operand.startswith('R'):
            return int(operand[1:])
        return 0

    def _parse_value(self, operand: str) -> int:
        operand = operand.strip()
        if operand in self.symbol_table:
            return self.symbol_table[operand]
        if operand.startswith('0x') or operand.startswith('0X'):
            return int(operand, 16)
        return int(operand)
