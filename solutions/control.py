"""
Control Unit - Solution File
"""

from typing import Dict
from solutions.clock import ControlSignals
from solutions.isa import OPCODES


class ControlUnit:
    """CPU Control Unit."""

    FETCH = 'FETCH'
    DECODE = 'DECODE'
    EXECUTE = 'EXECUTE'
    MEMORY = 'MEMORY'
    WRITEBACK = 'WRITEBACK'

    def __init__(self):
        self.state = self.FETCH
        self.signals = ControlSignals()

    def generate_signals(self, decoded: Dict, flags: Dict) -> ControlSignals:
        self.signals.reset()
        opcode = decoded.get('opcode', 0)
        opname = decoded.get('opcode_name', 'NOP')

        if self.state == self.FETCH:
            self.signals.mem_read = 1
            self.signals.ir_load = 1

        elif self.state == self.DECODE:
            pass  # No signals needed

        elif self.state == self.EXECUTE:
            if opname in ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'NOT', 'SHL', 'SHR']:
                # ALU operation
                alu_ops = {'ADD': 0, 'SUB': 1, 'AND': 2, 'OR': 3,
                          'XOR': 4, 'NOT': 5, 'SHL': 6, 'SHR': 7}
                op = alu_ops.get(opname, 0)
                self.signals.alu_op = [(op >> i) & 1 for i in range(4)]
                self.signals.reg_write = 1
            elif opname == 'LOAD':
                self.signals.mem_read = 1
                self.signals.mem_to_reg = 1
            elif opname == 'STORE':
                self.signals.mem_write = 1
            elif opname == 'MOV':
                self.signals.reg_write = 1
            elif opname == 'JMP':
                self.signals.pc_load = 1
            elif opname == 'JZ':
                if flags.get('Z', 0) == 1:
                    self.signals.pc_load = 1
                else:
                    self.signals.pc_inc = 1
            elif opname == 'JNZ':
                if flags.get('Z', 0) == 0:
                    self.signals.pc_load = 1
                else:
                    self.signals.pc_inc = 1

        elif self.state == self.WRITEBACK:
            self.signals.pc_inc = 1

        return self.signals

    def next_state(self) -> str:
        states = [self.FETCH, self.DECODE, self.EXECUTE, self.WRITEBACK]
        idx = states.index(self.state)
        self.state = states[(idx + 1) % len(states)]
        return self.state

    def reset(self) -> None:
        self.state = self.FETCH
        self.signals.reset()
