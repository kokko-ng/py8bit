"""Control Unit - Solution File."""

from typing import Dict
from solutions.clock import ControlSignals


class ControlUnit:
    """CPU Control Unit.

    Generates control signals based on the decoded instruction.
    This is a simplified single-cycle design where all signals are
    generated for immediate execution.
    """

    FETCH = "FETCH"
    DECODE = "DECODE"
    EXECUTE = "EXECUTE"
    WRITEBACK = "WRITEBACK"

    def __init__(self):
        """Initialize control unit."""
        self.state = self.FETCH
        self.signals = ControlSignals()

    def generate_signals(self, decoded: Dict, flags: Dict) -> ControlSignals:
        """Generate control signals for the given instruction.

        In this single-cycle design, we generate all necessary signals
        for immediate execution based on the opcode.
        """
        self.signals.reset()
        opname = decoded.get("opcode_name", "NOP")

        if opname in ["ADD", "SUB", "AND", "OR", "XOR", "NOT", "SHL", "SHR"]:
            # ALU operation: read registers, perform op, write result
            alu_ops = {"ADD": 0, "SUB": 1, "AND": 2, "OR": 3, "XOR": 4, "NOT": 5, "SHL": 6, "SHR": 7}
            op = alu_ops.get(opname, 0)
            self.signals.alu_op = [(op >> i) & 1 for i in range(4)]
            self.signals.reg_write = 1

        elif opname == "LOAD":
            # Load from memory to register
            self.signals.mem_read = 1
            self.signals.mem_to_reg = 1
            self.signals.reg_write = 1

        elif opname == "STORE":
            # Store register to memory
            self.signals.mem_write = 1

        elif opname == "MOV":
            # Copy register to register
            self.signals.reg_write = 1

        elif opname == "JMP":
            # Unconditional jump
            self.signals.pc_load = 1

        elif opname == "JZ":
            # Jump if zero flag set
            if flags.get("Z", 0) == 1:
                self.signals.pc_load = 1

        elif opname == "JNZ":
            # Jump if zero flag not set
            if flags.get("Z", 0) == 0:
                self.signals.pc_load = 1

        # NOP and HALT don't need any signals

        return self.signals

    def next_state(self) -> str:
        """Advance to next state (for multi-cycle implementations)."""
        states = [self.FETCH, self.DECODE, self.EXECUTE, self.WRITEBACK]
        idx = states.index(self.state)
        self.state = states[(idx + 1) % len(states)]
        return self.state

    def reset(self) -> None:
        """Reset control unit state."""
        self.state = self.FETCH
        self.signals.reset()
