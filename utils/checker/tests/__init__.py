"""
Test modules for the 8-bit computer components.
"""

from .test_gates import get_tests as get_gates_tests
from .test_adders import get_tests as get_adders_tests
from .test_combinational import get_tests as get_combinational_tests
from .test_alu import get_tests as get_alu_tests
from .test_sequential import get_tests as get_sequential_tests
from .test_registers import get_tests as get_registers_tests
from .test_counters import get_tests as get_counters_tests
from .test_memory import get_tests as get_memory_tests
from .test_clock import get_tests as get_clock_tests
from .test_isa import get_tests as get_isa_tests
from .test_decoder import get_tests as get_decoder_tests
from .test_control import get_tests as get_control_tests
from .test_datapath import get_tests as get_datapath_tests
from .test_cpu import get_tests as get_cpu_tests
from .test_assembler import get_tests as get_assembler_tests
from .test_system import get_tests as get_system_tests

# Component to test function mapping
COMPONENT_TESTS = {
    'gates': get_gates_tests,
    'adders': get_adders_tests,
    'combinational': get_combinational_tests,
    'alu': get_alu_tests,
    'sequential': get_sequential_tests,
    'registers': get_registers_tests,
    'counters': get_counters_tests,
    'memory': get_memory_tests,
    'clock': get_clock_tests,
    'isa': get_isa_tests,
    'decoder': get_decoder_tests,
    'control': get_control_tests,
    'datapath': get_datapath_tests,
    'cpu': get_cpu_tests,
    'assembler': get_assembler_tests,
    'system': get_system_tests,
}

__all__ = ['COMPONENT_TESTS']
