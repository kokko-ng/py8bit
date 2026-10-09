"""Latches and Flip-Flops - Sequential Logic Building Blocks.

Unlike combinational circuits, sequential circuits have memory - they can
store state. Latches and flip-flops are the fundamental memory elements.

Components:
- SR Latch: Set-Reset latch (level-sensitive)
- D Latch: Data latch (level-sensitive)
- D Flip-Flop: Edge-triggered data storage
- JK Flip-Flop: Versatile edge-triggered element
"""

from solutions.gates import AND, NOR, NOT


class SRLatch:
    """SR (Set-Reset) Latch using NOR gates.

    The SR latch is the simplest memory element. It has two inputs:
    - S (Set): Makes Q=1
    - R (Reset): Makes Q=0

    Invalid state: S=1 and R=1 simultaneously
    """

    def __init__(self) -> None:
        """Initialize SR latch with default state."""
        self.q = 0
        self.q_bar = 1

    def __call__(self, s: int, r: int) -> int:
        """Update latch state and return Q.

        Args:
            s: Set input
            r: Reset input

        Returns:
            Current Q output
        """
        # Cross-coupled NOR gates
        # Need to iterate to stabilize
        for _ in range(2):
            new_q = NOR(r, self.q_bar)
            new_q_bar = NOR(s, self.q)
            self.q = new_q
            self.q_bar = new_q_bar
        return self.q


class GatedSRLatch:
    """Gated SR Latch - SR latch with enable signal."""

    def __init__(self) -> None:
        """Initialize gated SR latch."""
        self.sr_latch = SRLatch()

    def __call__(self, s: int, r: int, enable: int) -> int:
        """Update latch when enabled.

        Args:
            s: Set input
            r: Reset input
            enable: Gate/enable signal

        Returns:
            Current Q output
        """
        gated_s = AND(s, enable)
        gated_r = AND(r, enable)
        return self.sr_latch(gated_s, gated_r)


class DLatch:
    """D (Data) Latch - stores a single bit when enabled.

    The D latch captures the input when enable is high.
    When enable is low, it holds its previous value.
    """

    def __init__(self) -> None:
        """Initialize D latch."""
        self.q = 0

    def __call__(self, d: int, enable: int) -> int:
        """Update latch.

        Args:
            d: Data input
            enable: Enable signal (level-sensitive)

        Returns:
            Current Q output
        """
        if enable == 1:
            self.q = d
        return self.q


class DFlipFlop:
    """D Flip-Flop - edge-triggered storage element.

    Unlike the D latch, the D flip-flop only samples the input
    on the rising edge of the clock.
    """

    def __init__(self) -> None:
        """Initialize D flip-flop."""
        self.q = 0
        self._prev_clk = 0

    def clock(self, d: int, clk: int) -> int:
        """Update flip-flop on clock edge.

        Args:
            d: Data input
            clk: Clock signal

        Returns:
            Current Q output
        """
        # Detect rising edge
        if self._prev_clk == 0 and clk == 1:
            self.q = d
        self._prev_clk = clk
        return self.q

    def read(self) -> int:
        """Read current Q value."""
        return self.q


class JKFlipFlop:
    """JK Flip-Flop - versatile edge-triggered element.

    J=0, K=0: Hold (no change)
    J=0, K=1: Reset (Q=0)
    J=1, K=0: Set (Q=1)
    J=1, K=1: Toggle (Q = NOT Q)
    """

    def __init__(self) -> None:
        """Initialize JK flip-flop."""
        self.q = 0
        self._prev_clk = 0

    def clock(self, j: int, k: int, clk: int) -> int:
        """Update flip-flop on clock edge.

        Args:
            j: J input
            k: K input
            clk: Clock signal

        Returns:
            Current Q output
        """
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
        """Read current Q value."""
        return self.q


class TFlipFlop:
    """T (Toggle) Flip-Flop - toggles on each clock when T=1."""

    def __init__(self) -> None:
        """Initialize T flip-flop."""
        self.jk = JKFlipFlop()

    def clock(self, t: int, clk: int) -> int:
        """Update flip-flop on clock edge.

        Args:
            t: Toggle input (when 1, Q toggles on clock edge)
            clk: Clock signal

        Returns:
            Current Q output
        """
        return self.jk.clock(t, t, clk)

    def read(self) -> int:
        """Read current Q value."""
        return self.jk.read()
