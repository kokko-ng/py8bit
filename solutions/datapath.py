"""
Data Path - Solution File
"""

from typing import List, Dict
from solutions.counters import ProgramCounter
from solutions.memory import RAM
from solutions.registers import RegisterFile
from solutions.alu import ALU
from solutions.clock import ControlSignals


class DataPath:
    """CPU Data Path."""

    def __init__(self):
        self.pc = ProgramCounter()
        self.memory = RAM()
        self.reg_file = RegisterFile()
        self.alu = ALU()
        self.ir = [0] * 16
        self.flags = {'Z': 0, 'C': 0, 'N': 0, 'V': 0}

    def execute_cycle(self, signals: ControlSignals, decoded: Dict) -> None:
        # Get register addresses from decoded instruction
        rd = decoded.get('rd_bits', [0, 0, 0])[:3]
        rs1 = decoded.get('rs1_bits', [0, 0, 0])[:3]
        rs2 = decoded.get('rs2_bits', [0, 0, 0])[:3]
        opname = decoded.get('opcode_name', 'NOP')

        # Read registers
        a_val = self.reg_file.read(rs1)
        b_val = self.reg_file.read(rs2)

        if signals.mem_read and signals.mem_to_reg:
            # LOAD instruction
            addr = [0] * 8
            addr[:4] = decoded.get('rs2_bits', [0, 0, 0, 0])
            data = self.memory.read(addr)
            self.reg_file.write(rd, data, 1, 1)

        elif signals.mem_write:
            # STORE instruction
            addr = [0] * 8
            addr[:4] = decoded.get('rs2_bits', [0, 0, 0, 0])
            data = self.reg_file.read(rd)
            self.memory.write(addr, data, 1)

        elif signals.reg_write and not signals.mem_to_reg:
            # ALU operation or MOV
            if opname == 'MOV':
                result = a_val
            else:
                result, self.flags = self.alu(a_val, b_val, signals.alu_op)
            self.reg_file.write(rd, result, 1, 1)

        # Handle PC
        if signals.pc_load:
            # Jump - load address from instruction
            addr = [0] * 8
            addr[:4] = decoded.get('rs2_bits', [0, 0, 0, 0])
            self.pc.clock(load=1, load_value=addr, increment=0, reset=0, clk=1)
        elif signals.pc_inc:
            self.pc.clock(load=0, load_value=[0]*8, increment=1, reset=0, clk=1)

    def fetch_instruction(self) -> List[int]:
        pc_val = self.pc.read()
        # Fetch two bytes for 16-bit instruction
        low_byte = self.memory.read(pc_val)
        # Increment PC for high byte
        pc_plus = [(pc_val[i] if i > 0 else 1 - pc_val[0]) for i in range(8)]
        high_byte = self.memory.read(pc_plus)
        return low_byte + high_byte

    def load_instruction(self, instruction: List[int]) -> None:
        self.ir = instruction.copy()

    def get_pc(self) -> List[int]:
        return self.pc.read()

    def set_pc(self, value: List[int]) -> None:
        self.pc.clock(load=1, load_value=value, increment=0, reset=0, clk=1)
