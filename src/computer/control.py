"""
Control Unit

The control unit generates control signals based on the current
instruction and CPU state. It implements the state machine for
the fetch-decode-execute cycle.
"""

from typing import Dict
from computer.clock import ControlSignals


class ControlUnit:
    """CPU Control Unit - generates control signals."""

    # CPU States
    FETCH = 'FETCH'
    DECODE = 'DECODE'
    EXECUTE = 'EXECUTE'
    MEMORY = 'MEMORY'
    WRITEBACK = 'WRITEBACK'

    def __init__(self):
        self.state = self.FETCH
        self.signals = ControlSignals()

    def generate_signals(self, decoded: Dict, flags: Dict) -> ControlSignals:
        """Generate control signals based on instruction and flags.

        Args:
            decoded: Decoded instruction fields
            flags: ALU flags (Z, C, N, V)

        Returns:
            Control signals for current state
        """
        # TODO: Implement control signal generation
        pass

    def next_state(self) -> str:
        """Advance to next state in the cycle.

        Returns:
            New state name
        """
        # TODO: Implement state machine
        pass

    def reset(self) -> None:
        """Reset control unit to initial state."""
        self.state = self.FETCH
        self.signals.reset()
