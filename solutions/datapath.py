"""Data Path - Solution File."""

from typing import List, Dict
from solutions.counters import ProgramCounter
from solutions.memory import RAM
from solutions.registers import RegisterFile
from solutions.alu import ALU
from solutions.clock import ControlSignals


class DataPath:
    """CPU Data Path."""

    def __init__(self):
        """Initialize data path components."""
        self.pc = ProgramCounter()
        self.memory = RAM()
        self.reg_file = RegisterFile()
        self.alu = ALU()
        self.ir = [0] * 16
        self.flags = {"Z": 0, "C": 0, "N": 0, "V": 0}

    def execute_cycle(self, signals: ControlSignals, decoded: Dict) -> None:
        """Execute one clock cycle based on control signals."""
        # Get register addresses from decoded instruction
        rd = decoded.get("rd_bits", [0, 0, 0])[:3]
        rs1 = decoded.get("rs1_bits", [0, 0, 0])[:3]
        rs2 = decoded.get("rs2_bits", [0, 0, 0])[:3]
        opname = decoded.get("opcode_name", "NOP")

        # Get 8-bit address for memory/jump operations
        addr_bits = decoded.get("rs2_bits", [0] * 8)[:8]
        # Pad to 8 bits if needed
        while len(addr_bits) < 8:
            addr_bits.append(0)

        # Read registers
        a_val = self.reg_file.read(rs1)
        b_val = self.reg_file.read(rs2)

        if signals.mem_read and signals.mem_to_reg:
            # LOAD instruction - use full 8-bit address
            data = self.memory.read(addr_bits)
            self.reg_file.write(rd, data, 1, 1)

        elif signals.mem_write:
            # STORE instruction - use full 8-bit address
            data = self.reg_file.read(rd)
            self.memory.write(addr_bits, data, 1)

        elif signals.reg_write and not signals.mem_to_reg:
            # ALU operation or MOV
            if opname == "MOV":
                result = a_val
            else:
                result, self.flags = self.alu(a_val, b_val, signals.alu_op)
            self.reg_file.write(rd, result, 1, 1)

        # Handle PC
        if signals.pc_load:
            # Jump - use full 8-bit address
            self.pc.clock(load=1, load_value=addr_bits, increment=0, reset=0, clk=1)
        elif signals.pc_inc:
            self.pc.clock(load=0, load_value=[0] * 8, increment=1, reset=0, clk=1)

    def fetch_instruction(self) -> List[int]:
        """Fetch instruction at current PC."""
        pc_val = self.pc.read()
        # Fetch two bytes for 16-bit instruction
        low_byte = self.memory.read(pc_val)
        # Calculate PC+1 for high byte (proper increment with carry)
        pc_int = sum(bit << i for i, bit in enumerate(pc_val))
        pc_plus_int = (pc_int + 1) & 0xFF
        pc_plus = [(pc_plus_int >> i) & 1 for i in range(8)]
        high_byte = self.memory.read(pc_plus)
        return low_byte + high_byte

    def load_instruction(self, instruction: List[int]) -> None:
        """Load instruction into IR."""
        self.ir = instruction.copy()

    def get_pc(self) -> List[int]:
        """Get current PC value."""
        return self.pc.read()

    def set_pc(self, value: List[int]) -> None:
        """Set PC value for jumps."""
        self.pc.clock(load=1, load_value=value, increment=0, reset=0, clk=1)
