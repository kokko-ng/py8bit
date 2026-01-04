"""
Clock and Control Signals

The clock coordinates all CPU operations. Control signals
direct data flow through the CPU.
"""


class Clock:
    """CPU Clock generator."""

    def __init__(self):
        self.cycle = 0
        self.state = 0  # 0 = low, 1 = high

    def tick(self) -> int:
        """Advance clock by one half-cycle.

        Returns:
            Current cycle number
        """
        self.state = 1 - self.state
        if self.state == 0:  # Completed a full cycle
            self.cycle += 1
        return self.cycle

    def reset(self) -> None:
        """Reset clock to initial state."""
        self.cycle = 0
        self.state = 0

    def get_state(self) -> int:
        """Get current clock state (0 or 1)."""
        return self.state


class ControlSignals:
    """Container for all CPU control signals."""

    def __init__(self):
        # Program counter controls
        self.pc_load = 0      # Load PC with new value
        self.pc_inc = 0       # Increment PC
        self.pc_reset = 0     # Reset PC to 0

        # Memory controls
        self.mem_read = 0     # Read from memory
        self.mem_write = 0    # Write to memory

        # Register file controls
        self.reg_write = 0    # Write to register
        self.reg_read_a = 0   # Read register for A operand
        self.reg_read_b = 0   # Read register for B operand

        # ALU controls
        self.alu_op = [0, 0, 0, 0]  # ALU operation code

        # Instruction register
        self.ir_load = 0      # Load instruction register

        # Data path controls
        self.alu_src_b = 0    # 0=register, 1=immediate
        self.reg_dst = 0      # Register destination select
        self.mem_to_reg = 0   # 0=ALU result, 1=memory data

    def reset(self) -> None:
        """Reset all control signals to 0."""
        self.__init__()

    def to_dict(self) -> dict:
        """Convert to dictionary for debugging."""
        return {
            'pc_load': self.pc_load,
            'pc_inc': self.pc_inc,
            'mem_read': self.mem_read,
            'mem_write': self.mem_write,
            'reg_write': self.reg_write,
            'alu_op': self.alu_op,
            'ir_load': self.ir_load,
        }
