"""Clock and Control Signals - Solution File."""


class Clock:
    """CPU Clock generator."""

    def __init__(self):
        """Initialize clock."""
        self.cycle = 0
        self.state = 0

    def tick(self) -> int:
        """Advance clock by one half-cycle."""
        self.state = 1 - self.state
        if self.state == 0:
            self.cycle += 1
        return self.cycle

    def reset(self) -> None:
        """Reset clock to initial state."""
        self.cycle = 0
        self.state = 0

    def get_state(self) -> int:
        """Get current clock state."""
        return self.state


class ControlSignals:
    """Container for all CPU control signals."""

    def __init__(self):
        """Initialize control signals to default values."""
        self.pc_load = 0
        self.pc_inc = 0
        self.pc_reset = 0
        self.mem_read = 0
        self.mem_write = 0
        self.reg_write = 0
        self.reg_read_a = 0
        self.reg_read_b = 0
        self.alu_op = [0, 0, 0, 0]
        self.ir_load = 0
        self.alu_src_b = 0
        self.reg_dst = 0
        self.mem_to_reg = 0

    def reset(self) -> None:
        """Reset all control signals to default values."""
        self.pc_load = 0
        self.pc_inc = 0
        self.pc_reset = 0
        self.mem_read = 0
        self.mem_write = 0
        self.reg_write = 0
        self.reg_read_a = 0
        self.reg_read_b = 0
        self.alu_op = [0, 0, 0, 0]
        self.ir_load = 0
        self.alu_src_b = 0
        self.reg_dst = 0
        self.mem_to_reg = 0

    def to_dict(self) -> dict:
        """Convert to dictionary for debugging."""
        return {
            "pc_load": self.pc_load,
            "pc_inc": self.pc_inc,
            "mem_read": self.mem_read,
            "mem_write": self.mem_write,
            "reg_write": self.reg_write,
            "alu_op": self.alu_op,
            "ir_load": self.ir_load,
        }
