"""
Tests for Combinational Circuits

These tests verify the correctness of multiplexers, demultiplexers,
decoders, and encoders.
"""

import pytest
from computer.combinational import (
    mux_2to1, mux_4to1, mux_8to1,
    demux_1to2, demux_1to4,
    decoder_2to4, decoder_3to8,
    encoder_4to2, encoder_8to3
)


class TestMux2to1:
    """Tests for the 2-to-1 multiplexer."""

    def test_sel_0_returns_a(self):
        """When sel=0, output should be a."""
        assert mux_2to1(0, 1, 0) == 0
        assert mux_2to1(1, 0, 0) == 1

    def test_sel_1_returns_b(self):
        """When sel=1, output should be b."""
        assert mux_2to1(0, 1, 1) == 1
        assert mux_2to1(1, 0, 1) == 0

    def test_all_combinations(self):
        """Test all input combinations."""
        # sel=0: output = a
        for a in [0, 1]:
            for b in [0, 1]:
                assert mux_2to1(a, b, 0) == a
        # sel=1: output = b
        for a in [0, 1]:
            for b in [0, 1]:
                assert mux_2to1(a, b, 1) == b


class TestMux4to1:
    """Tests for the 4-to-1 multiplexer."""

    def test_select_input_0(self):
        """sel=[0,0] should select inputs[0]."""
        assert mux_4to1([1, 0, 0, 0], [0, 0]) == 1
        assert mux_4to1([0, 1, 1, 1], [0, 0]) == 0

    def test_select_input_1(self):
        """sel=[1,0] should select inputs[1]."""
        assert mux_4to1([0, 1, 0, 0], [1, 0]) == 1
        assert mux_4to1([1, 0, 1, 1], [1, 0]) == 0

    def test_select_input_2(self):
        """sel=[0,1] should select inputs[2]."""
        assert mux_4to1([0, 0, 1, 0], [0, 1]) == 1
        assert mux_4to1([1, 1, 0, 1], [0, 1]) == 0

    def test_select_input_3(self):
        """sel=[1,1] should select inputs[3]."""
        assert mux_4to1([0, 0, 0, 1], [1, 1]) == 1
        assert mux_4to1([1, 1, 1, 0], [1, 1]) == 0

    def test_all_select_combinations(self):
        """Test all select combinations."""
        inputs = [1, 0, 1, 0]  # inputs[0]=1, [1]=0, [2]=1, [3]=0
        assert mux_4to1(inputs, [0, 0]) == 1  # select 0
        assert mux_4to1(inputs, [1, 0]) == 0  # select 1
        assert mux_4to1(inputs, [0, 1]) == 1  # select 2
        assert mux_4to1(inputs, [1, 1]) == 0  # select 3


class TestMux8to1:
    """Tests for the 8-to-1 multiplexer."""

    def test_select_each_input(self):
        """Test that each select value picks the correct input."""
        for i in range(8):
            inputs = [0] * 8
            inputs[i] = 1
            sel = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
            assert mux_8to1(inputs, sel) == 1

    def test_all_zeros_inputs(self):
        """All zero inputs should give zero output."""
        inputs = [0] * 8
        for i in range(8):
            sel = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
            assert mux_8to1(inputs, sel) == 0


class TestDemux1to2:
    """Tests for the 1-to-2 demultiplexer."""

    def test_sel_0_routes_to_out0(self):
        """sel=0 should route data to out0."""
        assert demux_1to2(1, 0) == (1, 0)
        assert demux_1to2(0, 0) == (0, 0)

    def test_sel_1_routes_to_out1(self):
        """sel=1 should route data to out1."""
        assert demux_1to2(1, 1) == (0, 1)
        assert demux_1to2(0, 1) == (0, 0)


class TestDemux1to4:
    """Tests for the 1-to-4 demultiplexer."""

    def test_route_to_each_output(self):
        """Data=1 should route to exactly one output based on sel."""
        assert demux_1to4(1, [0, 0]) == [1, 0, 0, 0]
        assert demux_1to4(1, [1, 0]) == [0, 1, 0, 0]
        assert demux_1to4(1, [0, 1]) == [0, 0, 1, 0]
        assert demux_1to4(1, [1, 1]) == [0, 0, 0, 1]

    def test_data_0_gives_all_zeros(self):
        """Data=0 should give all zero outputs."""
        for s0 in [0, 1]:
            for s1 in [0, 1]:
                assert demux_1to4(0, [s0, s1]) == [0, 0, 0, 0]


class TestDecoder2to4:
    """Tests for the 2-to-4 decoder."""

    def test_all_select_values(self):
        """Each select value should activate exactly one output."""
        assert decoder_2to4([0, 0]) == [1, 0, 0, 0]
        assert decoder_2to4([1, 0]) == [0, 1, 0, 0]
        assert decoder_2to4([0, 1]) == [0, 0, 1, 0]
        assert decoder_2to4([1, 1]) == [0, 0, 0, 1]

    def test_exactly_one_output_active(self):
        """Exactly one output should be 1 for any input."""
        for s0 in [0, 1]:
            for s1 in [0, 1]:
                output = decoder_2to4([s0, s1])
                assert sum(output) == 1


class TestDecoder3to8:
    """Tests for the 3-to-8 decoder."""

    def test_all_select_values(self):
        """Each select value should activate exactly one output."""
        for i in range(8):
            sel = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
            output = decoder_3to8(sel)
            expected = [0] * 8
            expected[i] = 1
            assert output == expected

    def test_exactly_one_output_active(self):
        """Exactly one output should be 1 for any input."""
        for i in range(8):
            sel = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
            output = decoder_3to8(sel)
            assert sum(output) == 1


class TestEncoder4to2:
    """Tests for the 4-to-2 priority encoder."""

    def test_single_input_active(self):
        """Single active input should encode to its index."""
        assert encoder_4to2([1, 0, 0, 0]) == [0, 0]  # index 0
        assert encoder_4to2([0, 1, 0, 0]) == [1, 0]  # index 1
        assert encoder_4to2([0, 0, 1, 0]) == [0, 1]  # index 2
        assert encoder_4to2([0, 0, 0, 1]) == [1, 1]  # index 3

    def test_priority_highest_wins(self):
        """When multiple inputs active, highest index wins."""
        assert encoder_4to2([1, 1, 0, 0]) == [1, 0]  # 1 wins over 0
        assert encoder_4to2([1, 0, 1, 0]) == [0, 1]  # 2 wins over 0
        assert encoder_4to2([1, 1, 1, 1]) == [1, 1]  # 3 wins over all


class TestEncoder8to3:
    """Tests for the 8-to-3 priority encoder."""

    def test_single_input_active(self):
        """Single active input should encode to its index."""
        for i in range(8):
            inputs = [0] * 8
            inputs[i] = 1
            expected = [(i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1]
            assert encoder_8to3(inputs) == expected

    def test_priority_highest_wins(self):
        """When multiple inputs active, highest index wins."""
        # All inputs active should give index 7
        assert encoder_8to3([1, 1, 1, 1, 1, 1, 1, 1]) == [1, 1, 1]
        # First 4 active should give index 3
        assert encoder_8to3([1, 1, 1, 1, 0, 0, 0, 0]) == [1, 1, 0]
