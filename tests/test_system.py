"""Tests for Full System."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.system import Computer


class TestComputer:
    """Tests for Complete Computer System."""

    def setup_method(self):
        """Create computer for each test."""
        self.computer = Computer()

    def test_initial_state(self):
        """Computer starts in correct state."""
        state = self.computer.dump_state()
        assert state['halted'] == False
        for i in range(8):
            assert state['registers'][f'R{i}'] == 0

    def test_reset(self):
        """Reset clears state."""
        # Run a program first
        self.computer.load_program("NOP\nHALT")
        self.computer.run()
        # Reset
        self.computer.reset()
        state = self.computer.dump_state()
        assert state['halted'] == False

    def test_load_and_run_simple(self):
        """Can load and run simple program."""
        self.computer.load_program("HALT")
        result = self.computer.run()
        assert result['halted'] == True

    def test_add_two_numbers(self):
        """Add two numbers program works."""
        program = """
            LOAD R1, 0x10
            LOAD R2, 0x11
            ADD R0, R1, R2
            HALT
        """
        # We need to also load data
        self.computer.load_program(program)
        # Manually set memory values for data
        from computer import int_to_bits
        self.computer.cpu.datapath.memory.write(
            int_to_bits(0x10, 8), int_to_bits(5, 8), 1)
        self.computer.cpu.datapath.memory.write(
            int_to_bits(0x11, 8), int_to_bits(3, 8), 1)

        result = self.computer.run()
        assert result['registers']['R0'] == 8

    def test_loop_program(self):
        """Loop program executes correctly."""
        # Simple countdown: R0 = 3, decrement until zero
        program = """
            LOAD R0, counter
            LOAD R1, one
        loop:
            SUB R0, R0, R1
            JNZ loop
            HALT
        counter:
            .byte 3
        one:
            .byte 1
        """
        self.computer.load_program(program)
        result = self.computer.run()
        assert result['registers']['R0'] == 0
        assert result['halted'] == True

    def test_max_cycles_protection(self):
        """Max cycles prevents infinite loops."""
        # Program that never halts
        program = """
        loop:
            JMP loop
        """
        self.computer.load_program(program)
        result = self.computer.run(max_cycles=10)
        # Should have run 10 cycles without halting
        assert result['halted'] == False

    def test_dump_registers(self):
        """dump_registers returns formatted string."""
        result = self.computer.dump_registers()
        assert "R0:" in result
        assert "R7:" in result

    def test_dump_state(self):
        """dump_state returns complete state."""
        state = self.computer.dump_state()
        assert 'registers' in state
        assert 'halted' in state
        assert 'pc' in state
        assert 'flags' in state

    def test_multiple_programs(self):
        """Can load and run multiple programs sequentially."""
        # First program
        self.computer.load_program("NOP\nHALT")
        self.computer.run()
        assert self.computer.cpu.halted == True

        # Reset and run second program
        self.computer.reset()
        self.computer.load_program("NOP\nNOP\nHALT")
        result = self.computer.run()
        assert result['halted'] == True
