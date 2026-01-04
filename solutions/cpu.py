"""
CPU - Solution File
"""

from typing import List, Dict
from solutions.datapath import DataPath
from solutions.control import ControlUnit
from solutions.decoder import InstructionDecoder
from solutions.clock import Clock


class CPU:
    """8-bit CPU."""

    def __init__(self):
        self.datapath = DataPath()
        self.control = ControlUnit()
        self.decoder = InstructionDecoder()
        self.clock = Clock()
        self.halted = False
        self.current_instruction = None

    def reset(self) -> None:
        self.datapath.pc.clock(load=0, load_value=[0]*8, increment=0, reset=1, clk=1)
        self.control.reset()
        self.halted = False
        self.current_instruction = None

    def fetch(self) -> List[int]:
        return self.datapath.fetch_instruction()

    def decode(self, instruction: List[int]) -> Dict:
        return self.decoder.decode(instruction)

    def execute(self, decoded: Dict) -> None:
        if decoded.get('opcode_name') == 'HALT':
            self.halted = True
            return

        signals = self.control.generate_signals(decoded, self.datapath.flags)
        self.datapath.execute_cycle(signals, decoded)

    def step(self) -> bool:
        if self.halted:
            return False

        # Fetch
        instruction = self.fetch()
        self.datapath.load_instruction(instruction)

        # Decode
        decoded = self.decode(instruction)
        self.current_instruction = decoded

        # Execute
        self.execute(decoded)

        # Increment PC (if not a jump that already modified it)
        if decoded.get('opcode_name') not in ['JMP', 'JZ', 'JNZ', 'HALT']:
            self.datapath.pc.clock(load=0, load_value=[0]*8, increment=1, reset=0, clk=1)

        self.clock.tick()
        return not self.halted

    def run(self, max_cycles: int = 1000) -> int:
        cycles = 0
        while cycles < max_cycles and self.step():
            cycles += 1
        return cycles

    def get_state(self) -> Dict:
        return {
            'pc': self.datapath.get_pc(),
            'flags': self.datapath.flags.copy(),
            'halted': self.halted,
            'cycle': self.clock.cycle,
        }
