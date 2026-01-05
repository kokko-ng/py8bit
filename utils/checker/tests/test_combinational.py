"""
Test cases for combinational circuits.
"""

from ..helpers import assert_eq


def get_tests() -> dict:
    """Return all test cases for combinational circuits."""
    from computer.combinational import (
        mux_2to1, mux_4to1, mux_8to1,
        demux_1to2, demux_1to4,
        decoder_2to4, encoder_4to2, encoder_8to3
    )

    return {
        # 2-to-1 MUX - all combinations
        "mux_2to1_sel0_a0_b0": lambda: assert_eq(mux_2to1(0, 0, 0), 0),
        "mux_2to1_sel0_a0_b1": lambda: assert_eq(mux_2to1(0, 1, 0), 0),
        "mux_2to1_sel0_a1_b0": lambda: assert_eq(mux_2to1(1, 0, 0), 1),
        "mux_2to1_sel0_a1_b1": lambda: assert_eq(mux_2to1(1, 1, 0), 1),
        "mux_2to1_sel1_a0_b0": lambda: assert_eq(mux_2to1(0, 0, 1), 0),
        "mux_2to1_sel1_a0_b1": lambda: assert_eq(mux_2to1(0, 1, 1), 1),
        "mux_2to1_sel1_a1_b0": lambda: assert_eq(mux_2to1(1, 0, 1), 0),
        "mux_2to1_sel1_a1_b1": lambda: assert_eq(mux_2to1(1, 1, 1), 1),

        # 4-to-1 MUX
        "mux_4to1_select_0": lambda: assert_eq(mux_4to1([1, 0, 0, 0], [0, 0]), 1),
        "mux_4to1_select_1": lambda: assert_eq(mux_4to1([0, 1, 0, 0], [1, 0]), 1),
        "mux_4to1_select_2": lambda: assert_eq(mux_4to1([0, 0, 1, 0], [0, 1]), 1),
        "mux_4to1_select_3": lambda: assert_eq(mux_4to1([0, 0, 0, 1], [1, 1]), 1),
        "mux_4to1_all_zeros": lambda: _test_mux_4to1_zeros(),
        "mux_4to1_all_ones": lambda: _test_mux_4to1_ones(),
        "mux_4to1_pattern": lambda: assert_eq(mux_4to1([1, 0, 1, 0], [0, 1]), 1),

        # 8-to-1 MUX
        "mux_8to1_select_0": lambda: assert_eq(mux_8to1([1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0]), 1),
        "mux_8to1_select_7": lambda: assert_eq(mux_8to1([0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1]), 1),
        "mux_8to1_all_selects": lambda: _test_mux_8to1_all(),

        # 1-to-2 DEMUX
        "demux_1to2_sel0_data0": lambda: assert_eq(demux_1to2(0, 0), (0, 0)),
        "demux_1to2_sel0_data1": lambda: assert_eq(demux_1to2(1, 0), (1, 0)),
        "demux_1to2_sel1_data0": lambda: assert_eq(demux_1to2(0, 1), (0, 0)),
        "demux_1to2_sel1_data1": lambda: assert_eq(demux_1to2(1, 1), (0, 1)),

        # 1-to-4 DEMUX
        "demux_1to4_route_0": lambda: assert_eq(demux_1to4(1, [0, 0]), [1, 0, 0, 0]),
        "demux_1to4_route_1": lambda: assert_eq(demux_1to4(1, [1, 0]), [0, 1, 0, 0]),
        "demux_1to4_route_2": lambda: assert_eq(demux_1to4(1, [0, 1]), [0, 0, 1, 0]),
        "demux_1to4_route_3": lambda: assert_eq(demux_1to4(1, [1, 1]), [0, 0, 0, 1]),
        "demux_1to4_data0_all_outputs": lambda: _test_demux_1to4_data0(),

        # 2-to-4 Decoder
        "decoder_2to4_00": lambda: assert_eq(decoder_2to4([0, 0]), [1, 0, 0, 0]),
        "decoder_2to4_01": lambda: assert_eq(decoder_2to4([1, 0]), [0, 1, 0, 0]),
        "decoder_2to4_10": lambda: assert_eq(decoder_2to4([0, 1]), [0, 0, 1, 0]),
        "decoder_2to4_11": lambda: assert_eq(decoder_2to4([1, 1]), [0, 0, 0, 1]),
        "decoder_2to4_one_hot": lambda: _test_decoder_2to4_one_hot(),

        # 3-to-8 Decoder
        "decoder_3to8_all_values": lambda: _test_decoder_3to8_all(),
        "decoder_3to8_one_hot": lambda: _test_decoder_3to8_one_hot(),

        # 4-to-2 Encoder
        "encoder_4to2_input_0": lambda: assert_eq(encoder_4to2([1, 0, 0, 0]), [0, 0]),
        "encoder_4to2_input_1": lambda: assert_eq(encoder_4to2([0, 1, 0, 0]), [1, 0]),
        "encoder_4to2_input_2": lambda: assert_eq(encoder_4to2([0, 0, 1, 0]), [0, 1]),
        "encoder_4to2_input_3": lambda: assert_eq(encoder_4to2([0, 0, 0, 1]), [1, 1]),
        "encoder_4to2_priority_1_over_0": lambda: assert_eq(encoder_4to2([1, 1, 0, 0]), [1, 0]),
        "encoder_4to2_priority_2_over_0_1": lambda: assert_eq(encoder_4to2([1, 1, 1, 0]), [0, 1]),
        "encoder_4to2_priority_all": lambda: assert_eq(encoder_4to2([1, 1, 1, 1]), [1, 1]),

        # 8-to-3 Encoder
        "encoder_8to3_all_inputs": lambda: _test_encoder_8to3_all(),
        "encoder_8to3_priority_all": lambda: assert_eq(encoder_8to3([1, 1, 1, 1, 1, 1, 1, 1]), [1, 1, 1]),
        "encoder_8to3_priority_first_4": lambda: assert_eq(encoder_8to3([1, 1, 1, 1, 0, 0, 0, 0]), [1, 1, 0]),
    }


def _test_mux_4to1_zeros():
    """Test 4-to-1 MUX with all zero inputs."""
    from computer.combinational import mux_4to1
    for sel in [[0, 0], [1, 0], [0, 1], [1, 1]]:
        assert_eq(mux_4to1([0, 0, 0, 0], sel), 0)


def _test_mux_4to1_ones():
    """Test 4-to-1 MUX with all one inputs."""
    from computer.combinational import mux_4to1
    for sel in [[0, 0], [1, 0], [0, 1], [1, 1]]:
        assert_eq(mux_4to1([1, 1, 1, 1], sel), 1)


def _test_mux_8to1_all():
    """Test 8-to-1 MUX for all select values."""
    from computer.combinational import mux_8to1
    for i in range(8):
        inputs = [0] * 8
        inputs[i] = 1
        sel = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
        assert_eq(mux_8to1(inputs, sel), 1)


def _test_demux_1to4_data0():
    """Test 1-to-4 DEMUX with data=0."""
    from computer.combinational import demux_1to4
    for s0 in [0, 1]:
        for s1 in [0, 1]:
            assert_eq(demux_1to4(0, [s0, s1]), [0, 0, 0, 0])


def _test_decoder_2to4_one_hot():
    """Test that 2-to-4 decoder outputs are one-hot."""
    from computer.combinational import decoder_2to4
    for s0 in [0, 1]:
        for s1 in [0, 1]:
            output = decoder_2to4([s0, s1])
            assert_eq(sum(output), 1)


def _test_decoder_3to8_all():
    """Test 3-to-8 decoder for all values."""
    from computer.combinational import decoder_3to8
    for i in range(8):
        sel = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
        output = decoder_3to8(sel)
        expected = [0] * 8
        expected[i] = 1
        assert_eq(output, expected)


def _test_decoder_3to8_one_hot():
    """Test that 3-to-8 decoder outputs are one-hot."""
    from computer.combinational import decoder_3to8
    for i in range(8):
        sel = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
        output = decoder_3to8(sel)
        assert_eq(sum(output), 1)


def _test_encoder_8to3_all():
    """Test 8-to-3 encoder for all single inputs."""
    from computer.combinational import encoder_8to3
    for i in range(8):
        inputs = [0] * 8
        inputs[i] = 1
        expected = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
        assert_eq(encoder_8to3(inputs), expected)
