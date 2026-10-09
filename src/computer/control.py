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

# NOTE: Generated from solutions/control.py by scripts/generate_stubs.py.
# Write your implementations in the '# TODO' bodies below.
# (Maintainers: edit the solution file, not this one, then regenerate.)

from typing import Any

from computer.clock import ControlSignals


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

    def __init__(self) -> None:
        """Initialize control unit."""
        self.state = self.FETCH
        self.signals = ControlSignals()

    def generate_signals(self, decoded: dict[str, Any], flags: dict[str, int]) -> ControlSignals:
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
        # TODO: Implement control signal generation
        ...

    def next_state(self) -> str:
        """Advance the conceptual state machine by one phase.

        Cycle through FETCH -> DECODE -> EXECUTE -> WRITEBACK -> FETCH.
        Update ``self.state`` and return the new state.

        Returns:
            New state name
        """
        # TODO: Implement the conceptual state machine
        ...

    def reset(self) -> None:
        """Reset control unit to initial state."""
        self.state = self.FETCH
        self.signals.reset()
