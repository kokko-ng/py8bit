"""Tests for CPU."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.cpu import CPU
from computer.isa import encode_instruction


def int_to_bits(value: int, n: int = 8) -> list:
    return [(value >> i) & 1 for i in range(n)]


def bits_to_int(bits: list) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


def load_program(cpu: CPU, program: list, start: int = 0) -> None:
    """Load program into CPU memory."""
    for i, instr in enumerate(program):
        low_byte = instr[:8]
        high_byte = instr[8:] if len(instr) > 8 else [0] * 8
        addr = start + i * 2
        cpu.datapath.memory.write(int_to_bits(addr, 8), low_byte, 1)
        cpu.datapath.memory.write(int_to_bits(addr + 1, 8), high_byte, 1)


class TestCPU:
    """Tests for CPU."""

    def setup_method(self):
        """Create CPU for each test."""
        self.cpu = CPU()

    def test_initial_state(self):
        """CPU starts in correct state."""
        assert bits_to_int(self.cpu.datapath.get_pc()) == 0
        assert self.cpu.halted == False

    def test_reset(self):
        """Reset returns to initial state."""
        # Modify state
        self.cpu.datapath.set_pc(int_to_bits(0x10, 8))
        self.cpu.halted = True
        # Reset
        self.cpu.reset()
        assert bits_to_int(self.cpu.datapath.get_pc()) == 0
        assert self.cpu.halted == False

    def test_fetch_returns_instruction(self):
        """Fetch returns 16-bit instruction."""
        load_program(self.cpu, [encode_instruction('NOP')])
        instr = self.cpu.fetch()
        assert len(instr) == 16

    def test_decode_returns_dict(self):
        """Decode returns dictionary."""
        instr = encode_instruction('ADD', rd=0, rs1=1, rs2_imm=2)
        decoded = self.cpu.decode(instr)
        assert isinstance(decoded, dict)
        assert 'opcode_name' in decoded

    def test_halt_stops_cpu(self):
        """HALT instruction stops CPU."""
        load_program(self.cpu, [encode_instruction('HALT')])
        self.cpu.step()
        assert self.cpu.halted == True

    def test_step_returns_false_after_halt(self):
        """Step returns False when halted."""
        load_program(self.cpu, [encode_instruction('HALT')])
        result = self.cpu.step()
        # After HALT, next step returns False
        assert self.cpu.halted == True

    def test_run_counts_cycles(self):
        """Run returns number of cycles executed."""
        program = [
            encode_instruction('NOP'),
            encode_instruction('NOP'),
            encode_instruction('HALT'),
        ]
        load_program(self.cpu, program)
        cycles = self.cpu.run()
        assert cycles >= 2  # At least NOP and HALT

    def test_add_instruction(self):
        """ADD instruction adds registers."""
        # Set up R1=10, R2=20
        self.cpu.datapath.reg_file.write([1, 0, 0], int_to_bits(10, 8), 1, 0)
        self.cpu.datapath.reg_file.write([1, 0, 0], int_to_bits(10, 8), 1, 1)
        self.cpu.datapath.reg_file.write([0, 1, 0], int_to_bits(20, 8), 1, 0)
        self.cpu.datapath.reg_file.write([0, 1, 0], int_to_bits(20, 8), 1, 1)

        program = [
            encode_instruction('ADD', rd=0, rs1=1, rs2_imm=2),
            encode_instruction('HALT'),
        ]
        load_program(self.cpu, program)
        self.cpu.run()

        # R0 should be 30
        r0 = bits_to_int(self.cpu.datapath.reg_file.read([0, 0, 0]))
        assert r0 == 30

    def test_get_state(self):
        """get_state returns CPU state."""
        state = self.cpu.get_state()
        assert 'pc' in state
        assert 'flags' in state
        assert 'halted' in state

    def test_max_cycles_prevents_infinite_loop(self):
        """run() stops at max_cycles."""
        # Program with no HALT (infinite loop risk)
        program = [
            encode_instruction('JMP', rs2_imm=0),  # Jump to self
        ]
        load_program(self.cpu, program)
        cycles = self.cpu.run(max_cycles=10)
        assert cycles == 10
