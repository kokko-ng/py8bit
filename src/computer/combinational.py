"""Combinational Circuits - Data Routing and Selection.

This module contains combinational circuits built from logic gates.
These circuits perform data routing, selection, and encoding operations
that are essential for building more complex computer components.

Components in this module:
- Multiplexers (MUX): Select one of multiple inputs based on control signals
- Demultiplexers (DEMUX): Route one input to one of multiple outputs
- Decoders: Convert binary input to one-hot output
- Encoders: Convert one-hot input to binary output

All circuits use the gates from the gates module.
"""

from typing import List, Tuple

from computer.gates import AND, NOT, OR  # noqa: F401


def mux_2to1(a: int, b: int, sel: int) -> int:
    """2-to-1 Multiplexer.

    Selects between two inputs based on the select signal.
    - When sel=0, output is a
    - When sel=1, output is b

    Truth Table:
        sel | OUT
        ----|-----
         0  |  a
         1  |  b

    Args:
        a: First input (selected when sel=0)
        b: Second input (selected when sel=1)
        sel: Select signal (0 or 1)

    Returns:
        Selected input value
    """
    # TODO: Implement 2-to-1 MUX using AND, OR, NOT gates
    # Hint: OUT = OR(AND(a, NOT(sel)), AND(b, sel))
    ...


def mux_4to1(inputs: List[int], sel: List[int]) -> int:
    """4-to-1 Multiplexer.

    Selects one of four inputs based on two select signals.
    sel[0] is the LSB, sel[1] is the MSB.

    Selection:
        sel[1] | sel[0] | OUT
        -------|--------|-------
          0    |   0    | inputs[0]
          0    |   1    | inputs[1]
          1    |   0    | inputs[2]
          1    |   1    | inputs[3]

    Args:
        inputs: List of 4 input values
        sel: List of 2 select bits [sel0, sel1]

    Returns:
        Selected input value
    """
    # TODO: Implement 4-to-1 MUX using 2-to-1 MUXes
    # Hint: Use a tree of 2-to-1 muxes
    # First layer: select between pairs based on sel[0]
    ...


def mux_8to1(inputs: List[int], sel: List[int]) -> int:
    """8-to-1 Multiplexer.

    Selects one of eight inputs based on three select signals.
    sel[0] is the LSB.

    Args:
        inputs: List of 8 input values
        sel: List of 3 select bits [sel0, sel1, sel2]

    Returns:
        Selected input value
    """
    # TODO: Implement 8-to-1 MUX using 4-to-1 MUXes or 2-to-1 MUXes
    # First layer: use two 4-to-1 muxes on the lower and upper halves
    ...


def demux_1to2(data: int, sel: int) -> Tuple[int, int]:
    """1-to-2 Demultiplexer.

    Routes one input to one of two outputs based on the select signal.
    - When sel=0, output is (data, 0)
    - When sel=1, output is (0, data)

    Args:
        data: Input data bit
        sel: Select signal (0 or 1)

    Returns:
        Tuple of (out0, out1)
    """
    # TODO: Implement 1-to-2 DEMUX
    # Hint: out0 = AND(data, NOT(sel)), out1 = AND(data, sel)
    ...


def demux_1to4(data: int, sel: List[int]) -> List[int]:
    """1-to-4 Demultiplexer.

    Routes one input to one of four outputs based on two select signals.

    Args:
        data: Input data bit
        sel: List of 2 select bits [sel0, sel1]

    Returns:
        List of 4 output values [out0, out1, out2, out3]
    """
    # TODO: Implement 1-to-4 DEMUX
    # First demux into two lines based on sel[1]
    ...


def decoder_2to4(sel: List[int]) -> List[int]:
    """2-to-4 Decoder.

    Converts a 2-bit binary input to a 4-bit one-hot output.
    Exactly one output will be 1.

    Truth Table:
        sel[1] | sel[0] | out[3] out[2] out[1] out[0]
        -------|--------|---------------------------
          0    |   0    |   0      0      0      1
          0    |   1    |   0      0      1      0
          1    |   0    |   0      1      0      0
          1    |   1    |   1      0      0      0

    Args:
        sel: List of 2 input bits [sel0, sel1]

    Returns:
        List of 4 output bits (one-hot encoded)
    """
    # TODO: Implement 2-to-4 decoder
    # Each output is an AND of the appropriate select signals
    ...


def decoder_3to8(sel: List[int]) -> List[int]:
    """3-to-8 Decoder.

    Converts a 3-bit binary input to an 8-bit one-hot output.
    Exactly one output will be 1.

    Args:
        sel: List of 3 input bits [sel0, sel1, sel2]

    Returns:
        List of 8 output bits (one-hot encoded)
    """
    # TODO: Implement 3-to-8 decoder
    # Each output is an AND of the appropriate select signals
    ...


def encoder_4to2(inputs: List[int]) -> List[int]:
    """4-to-2 Priority Encoder.

    Encodes a 4-bit one-hot (or priority) input to a 2-bit binary output.
    If multiple inputs are high, the highest index wins (priority encoding).

    Examples:
        [1,0,0,0] -> [0,0] (index 0)
        [0,1,0,0] -> [1,0] (index 1)
        [0,0,1,0] -> [0,1] (index 2)
        [0,0,0,1] -> [1,1] (index 3)
        [1,1,0,0] -> [1,0] (index 1 wins over 0)
        [1,1,1,1] -> [1,1] (index 3 wins over all)

    Args:
        inputs: List of 4 input bits

    Returns:
        List of 2 output bits [out0, out1] representing the binary index
    """
    # TODO: Implement 4-to-2 priority encoder
    # Higher index takes precedence when multiple inputs are active
    # out1 = 1 when highest active index is 2 or 3
    # out0 = 1 when highest active index is 1 or 3
    ...


def encoder_8to3(inputs: List[int]) -> List[int]:
    """8-to-3 Priority Encoder.

    Encodes an 8-bit input to a 3-bit binary output.
    The output represents the index of the highest active input.

    Examples:
        Only inputs[5]=1 -> [1,0,1] (binary 5)
        All inputs active -> [1,1,1] (index 7 wins)

    Args:
        inputs: List of 8 input bits

    Returns:
        List of 3 output bits [out0, out1, out2]
    """
    # TODO: Implement 8-to-3 priority encoder
    # Higher index takes precedence when multiple inputs are active
    # out2 = 1 when highest active index is 4, 5, 6, or 7
    # out1 = 1 when highest active index is 2, 3, 6, or 7
    # out0 = 1 when highest active index is 1, 3, 5, or 7
    ...
