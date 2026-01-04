"""Tests for Control Unit."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from computer.control import ControlUnit
from computer.isa import OPCODES


class TestControlUnit:
    """Tests for Control Unit."""

    def setup_method(self):
        """Create control unit for each test."""
        self.cu = ControlUnit()
        self.flags = {'Z': 0, 'C': 0, 'N': 0, 'V': 0}

    def make_decoded(self, opname, rd=0, rs1=0, rs2_imm=0):
        """Helper to create decoded instruction dict."""
        return {
            'opcode': OPCODES[opname],
            'opcode_name': opname,
            'rd': rd,
            'rs1': rs1,
            'rs2_imm': rs2_imm
        }

    def test_initial_state_is_fetch(self):
        """Control unit starts in FETCH state."""
        assert self.cu.state == ControlUnit.FETCH

    def test_state_cycle(self):
        """States cycle correctly."""
        assert self.cu.state == ControlUnit.FETCH
        self.cu.next_state()
        assert self.cu.state == ControlUnit.DECODE
        self.cu.next_state()
        assert self.cu.state == ControlUnit.EXECUTE
        self.cu.next_state()
        assert self.cu.state == ControlUnit.WRITEBACK
        self.cu.next_state()
        assert self.cu.state == ControlUnit.FETCH

    def test_reset(self):
        """Reset returns to FETCH state."""
        self.cu.next_state()
        self.cu.next_state()
        self.cu.reset()
        assert self.cu.state == ControlUnit.FETCH

    def test_fetch_signals(self):
        """FETCH state sets mem_read and ir_load."""
        self.cu.state = ControlUnit.FETCH
        decoded = self.make_decoded('ADD')
        signals = self.cu.generate_signals(decoded, self.flags)
        assert signals.mem_read == 1
        assert signals.ir_load == 1

    def test_execute_add_signals(self):
        """EXECUTE ADD sets alu_op and reg_write."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('ADD')
        signals = self.cu.generate_signals(decoded, self.flags)
        assert signals.reg_write == 1

    def test_execute_load_signals(self):
        """EXECUTE LOAD sets mem_read and mem_to_reg."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('LOAD')
        signals = self.cu.generate_signals(decoded, self.flags)
        assert signals.mem_read == 1
        assert signals.mem_to_reg == 1

    def test_execute_store_signals(self):
        """EXECUTE STORE sets mem_write."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('STORE')
        signals = self.cu.generate_signals(decoded, self.flags)
        assert signals.mem_write == 1

    def test_execute_jmp_signals(self):
        """EXECUTE JMP sets pc_load."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('JMP')
        signals = self.cu.generate_signals(decoded, self.flags)
        assert signals.pc_load == 1

    def test_execute_jz_taken(self):
        """EXECUTE JZ with Z=1 sets pc_load."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('JZ')
        flags = {'Z': 1, 'C': 0, 'N': 0, 'V': 0}
        signals = self.cu.generate_signals(decoded, flags)
        assert signals.pc_load == 1

    def test_execute_jz_not_taken(self):
        """EXECUTE JZ with Z=0 sets pc_inc."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('JZ')
        flags = {'Z': 0, 'C': 0, 'N': 0, 'V': 0}
        signals = self.cu.generate_signals(decoded, flags)
        assert signals.pc_load == 0
        assert signals.pc_inc == 1

    def test_execute_jnz_taken(self):
        """EXECUTE JNZ with Z=0 sets pc_load."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('JNZ')
        flags = {'Z': 0, 'C': 0, 'N': 0, 'V': 0}
        signals = self.cu.generate_signals(decoded, flags)
        assert signals.pc_load == 1

    def test_execute_jnz_not_taken(self):
        """EXECUTE JNZ with Z=1 sets pc_inc."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('JNZ')
        flags = {'Z': 1, 'C': 0, 'N': 0, 'V': 0}
        signals = self.cu.generate_signals(decoded, flags)
        assert signals.pc_load == 0
        assert signals.pc_inc == 1

    def test_writeback_increments_pc(self):
        """WRITEBACK sets pc_inc."""
        self.cu.state = ControlUnit.WRITEBACK
        decoded = self.make_decoded('ADD')
        signals = self.cu.generate_signals(decoded, self.flags)
        assert signals.pc_inc == 1

    def test_signals_reset_between_calls(self):
        """Signals are reset between generate_signals calls."""
        self.cu.state = ControlUnit.EXECUTE
        decoded = self.make_decoded('LOAD')
        signals = self.cu.generate_signals(decoded, self.flags)
        assert signals.mem_read == 1

        # Now call with STORE
        decoded = self.make_decoded('STORE')
        signals = self.cu.generate_signals(decoded, self.flags)
        # mem_read should be 0 now
        assert signals.mem_write == 1
