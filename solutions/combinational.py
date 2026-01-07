"""Combinational Circuits - Solution File."""

from typing import List, Tuple

# Import gates from the solutions module for testing
from solutions.gates import AND, OR, NOT


def mux_2to1(a: int, b: int, sel: int) -> int:
    """2-to-1 Multiplexer."""
    return OR(AND(a, NOT(sel)), AND(b, sel))


def mux_4to1(inputs: List[int], sel: List[int]) -> int:
    """4-to-1 Multiplexer using tree of 2-to-1 muxes."""
    # First level: select between pairs
    mux01 = mux_2to1(inputs[0], inputs[1], sel[0])
    mux23 = mux_2to1(inputs[2], inputs[3], sel[0])
    # Second level: select between results
    return mux_2to1(mux01, mux23, sel[1])


def mux_8to1(inputs: List[int], sel: List[int]) -> int:
    """8-to-1 Multiplexer using tree of 4-to-1 muxes."""
    # First level: two 4-to-1 muxes
    mux_low = mux_4to1(inputs[0:4], sel[0:2])
    mux_high = mux_4to1(inputs[4:8], sel[0:2])
    # Second level: select between results
    return mux_2to1(mux_low, mux_high, sel[2])


def demux_1to2(data: int, sel: int) -> Tuple[int, int]:
    """1-to-2 Demultiplexer."""
    out0 = AND(data, NOT(sel))
    out1 = AND(data, sel)
    return (out0, out1)


def demux_1to4(data: int, sel: List[int]) -> List[int]:
    """1-to-4 Demultiplexer."""
    # Decode the select lines
    not_sel0 = NOT(sel[0])
    not_sel1 = NOT(sel[1])

    out0 = AND(AND(data, not_sel1), not_sel0)
    out1 = AND(AND(data, not_sel1), sel[0])
    out2 = AND(AND(data, sel[1]), not_sel0)
    out3 = AND(AND(data, sel[1]), sel[0])

    return [out0, out1, out2, out3]


def decoder_2to4(sel: List[int]) -> List[int]:
    """2-to-4 Decoder."""
    not_sel0 = NOT(sel[0])
    not_sel1 = NOT(sel[1])

    out0 = AND(not_sel1, not_sel0)
    out1 = AND(not_sel1, sel[0])
    out2 = AND(sel[1], not_sel0)
    out3 = AND(sel[1], sel[0])

    return [out0, out1, out2, out3]


def decoder_3to8(sel: List[int]) -> List[int]:
    """3-to-8 Decoder."""
    not_sel0 = NOT(sel[0])
    not_sel1 = NOT(sel[1])
    not_sel2 = NOT(sel[2])

    out0 = AND(AND(not_sel2, not_sel1), not_sel0)
    out1 = AND(AND(not_sel2, not_sel1), sel[0])
    out2 = AND(AND(not_sel2, sel[1]), not_sel0)
    out3 = AND(AND(not_sel2, sel[1]), sel[0])
    out4 = AND(AND(sel[2], not_sel1), not_sel0)
    out5 = AND(AND(sel[2], not_sel1), sel[0])
    out6 = AND(AND(sel[2], sel[1]), not_sel0)
    out7 = AND(AND(sel[2], sel[1]), sel[0])

    return [out0, out1, out2, out3, out4, out5, out6, out7]


def encoder_4to2(inputs: List[int]) -> List[int]:
    """4-to-2 Priority Encoder."""
    # Priority encoder: higher index takes precedence
    out1 = OR(inputs[2], inputs[3])
    # out0 is 1 when highest active is 1 or 3 (but 2 takes priority over 1)
    out0 = OR(inputs[3], AND(inputs[1], NOT(inputs[2])))
    return [out0, out1]


def encoder_8to3(inputs: List[int]) -> List[int]:
    """8-to-3 Priority Encoder."""
    # Priority encoder: higher index takes precedence
    any_upper = OR(OR(inputs[4], inputs[5]), OR(inputs[6], inputs[7]))

    # out2 is 1 when highest active is in 4-7
    out2 = any_upper

    # out1 is 1 when highest active has bit 1 set (2,3 in lower half; 6,7 in upper half)
    out1 = OR(OR(inputs[6], inputs[7]), AND(NOT(any_upper), OR(inputs[2], inputs[3])))

    # out0 is 1 when highest active has bit 0 set (1,3 in lower half; 5,7 in upper half)
    out0 = OR(OR(inputs[5], inputs[7]), AND(NOT(any_upper), OR(inputs[1], inputs[3])))

    return [out0, out1, out2]
