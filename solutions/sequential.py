"""
Latches and Flip-Flops - Solution File
"""

from solutions.gates import AND, OR, NOT, NOR, NAND


class SRLatch:
    """SR (Set-Reset) Latch using NOR gates."""

    def __init__(self):
        self.q = 0
        self.q_bar = 1

    def __call__(self, s: int, r: int) -> int:
        # Cross-coupled NOR gates
        # Need to iterate to stabilize
        for _ in range(2):
            new_q = NOR(r, self.q_bar)
            new_q_bar = NOR(s, self.q)
            self.q = new_q
            self.q_bar = new_q_bar
        return self.q


class GatedSRLatch:
    """Gated SR Latch."""

    def __init__(self):
        self.sr_latch = SRLatch()

    def __call__(self, s: int, r: int, enable: int) -> int:
        gated_s = AND(s, enable)
        gated_r = AND(r, enable)
        return self.sr_latch(gated_s, gated_r)


class DLatch:
    """D (Data) Latch."""

    def __init__(self):
        self.q = 0

    def __call__(self, d: int, enable: int) -> int:
        if enable == 1:
            self.q = d
        return self.q


class DFlipFlop:
    """D Flip-Flop - edge-triggered."""

    def __init__(self):
        self.q = 0
        self._prev_clk = 0

    def clock(self, d: int, clk: int) -> int:
        # Detect rising edge
        if self._prev_clk == 0 and clk == 1:
            self.q = d
        self._prev_clk = clk
        return self.q

    def read(self) -> int:
        return self.q


class JKFlipFlop:
    """JK Flip-Flop."""

    def __init__(self):
        self.q = 0
        self._prev_clk = 0

    def clock(self, j: int, k: int, clk: int) -> int:
        # Detect rising edge
        if self._prev_clk == 0 and clk == 1:
            if j == 0 and k == 0:
                pass  # Hold
            elif j == 0 and k == 1:
                self.q = 0  # Reset
            elif j == 1 and k == 0:
                self.q = 1  # Set
            else:  # j == 1 and k == 1
                self.q = NOT(self.q)  # Toggle
        self._prev_clk = clk
        return self.q

    def read(self) -> int:
        return self.q


class TFlipFlop:
    """T (Toggle) Flip-Flop."""

    def __init__(self):
        self.jk = JKFlipFlop()

    def clock(self, t: int, clk: int) -> int:
        return self.jk.clock(t, t, clk)

    def read(self) -> int:
        return self.jk.read()
