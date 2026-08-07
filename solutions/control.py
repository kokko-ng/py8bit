"""Control Unit.

The control unit is the CPU's traffic director: given a decoded instruction
(and the current flags), it decides which control signals to assert so the
datapath executes that instruction.

Design note - single-cycle control:
    This CPU uses a *single-cycle* design. ``CPU.step()`` performs fetch and
    decode itself, then calls ``generate_signals`` exactly once per
    instruction. Your job here is to map each instruction to the signals its
    execution needs (for example, ADD needs ``reg_write`` and the right
    ``alu_op``). Real multi-cycle CPUs instead sequence through
    FETCH -> DECODE -> EXECUTE -> WRITEBACK states, asserting different
    signals in each phase; ``next_state`` models that sequencing as a
    conceptual exercise.
"""

from typing import Dict
from solutions.clock import ControlSignals


class ControlUnit:
    """CPU Control Unit - maps decoded instructions to control signals.

    This is a single-cycle design: ``CPU.step()`` performs fetch and decode
    itself and calls ``generate_signals`` exactly once per instruction, so
    all signals for that instruction's execution are asserted at once. The
    FETCH/DECODE/EXECUTE/WRITEBACK states model how a multi-cycle CPU would
    sequence its work; ``next_state`` walks that cycle as a conceptual
    exercise.
    """

    # Conceptual CPU phases (see next_state)
    FETCH = "FETCH"
    DECODE = "DECODE"
    EXECUTE = "EXECUTE"
    WRITEBACK = "WRITEBACK"

    def __init__(self):
        """Initialize control unit."""
        self.state = self.FETCH
        self.signals = ControlSignals()

    def generate_signals(self, decoded: Dict, flags: Dict) -> ControlSignals:
        """Generate the control signals needed to execute one instruction.

        Start from a clean slate (``self.signals.reset()``), then assert the
        signals this instruction needs:

        - ALU ops (ADD/SUB/AND/OR/XOR/NOT/SHL/SHR): select the operation via
          ``alu_op`` (4 bits, LSB-first, matching the ALU's OP_* constants)
          and assert ``reg_write`` so the result is stored.
        - LOAD: assert ``mem_read``, ``mem_to_reg``, and ``reg_write``.
        - STORE: assert ``mem_write``.
        - MOV: assert ``reg_write``.
        - JMP: assert ``pc_load``.
        - JZ / JNZ: assert ``pc_load`` only when the Zero flag allows the
          jump (JZ jumps when Z == 1, JNZ when Z == 0).
        - NOP / HALT: assert nothing.

        Args:
            decoded: Decoded instruction fields (from InstructionDecoder)
            flags: ALU flags {'Z': 0/1, 'C': 0/1, 'N': 0/1, 'V': 0/1}

        Returns:
            ControlSignals for this instruction
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
        """Advance the conceptual state machine by one phase.

        Cycle through FETCH -> DECODE -> EXECUTE -> WRITEBACK -> FETCH.
        Update ``self.state`` and return the new state.

        Returns:
            New state name
        """
        states = [self.FETCH, self.DECODE, self.EXECUTE, self.WRITEBACK]
        idx = states.index(self.state)
        self.state = states[(idx + 1) % len(states)]
        return self.state

    def reset(self) -> None:
        """Reset control unit to initial state."""
        self.state = self.FETCH
        self.signals.reset()
