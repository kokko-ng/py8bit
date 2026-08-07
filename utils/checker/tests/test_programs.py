"""End-to-end tests: assemble and run every sample program in programs/.

These are the ultimate integration tests - they exercise the assembler, the
loader (including the .byte data section), the control unit, the datapath,
and the CPU together, and assert the results each program's header documents.
"""

from pathlib import Path

from ..helpers import assert_eq, assert_not_none, bits_to_int, int_to_bits

PROGRAMS_DIR = Path(__file__).resolve().parents[3] / "programs"


def get_tests() -> dict:
    """Return all end-to-end program tests."""
    from computer.system import Computer  # noqa: F401  (fail fast on import errors)

    return {
        "Program_add_two_numbers": lambda: _test_add_two_numbers(),
        "Program_multiply": lambda: _test_multiply(),
        "Program_fibonacci": lambda: _test_fibonacci(),
        "Program_conditional_loop": lambda: _test_conditional_loop(),
    }


def _run_program(name: str, max_cycles: int = 1000):
    """Assemble and run programs/<name>.asm, returning (computer, final state)."""
    from computer.system import Computer

    source = (PROGRAMS_DIR / f"{name}.asm").read_text()
    comp = Computer()
    comp.load_program(source)
    state = comp.run(max_cycles=max_cycles)
    assert_not_none(state, "Computer.run() returned None")
    assert_eq(state["halted"], True, f"{name}.asm must reach HALT within {max_cycles} cycles")
    return comp, state


def _read_memory(comp, addr: int) -> int:
    """Read one byte of memory as an integer."""
    return bits_to_int(comp.cpu.datapath.memory.read(int_to_bits(addr, 8)))


def _test_add_two_numbers():
    """add_two_numbers.asm: 5 + 3 -> R0 = 8, stored at 0x12."""
    comp, state = _run_program("add_two_numbers")
    assert_eq(state["registers"]["R0"], 8, "add_two_numbers.asm documents R0 = 8 (5 + 3)")
    assert_eq(_read_memory(comp, 0x12), 8, "add_two_numbers.asm stores the result at address 0x12")


def _test_multiply():
    """multiply.asm: 5 * 3 via repeated addition -> R0 = 15."""
    comp, state = _run_program("multiply")
    assert_eq(state["registers"]["R0"], 15, "multiply.asm documents R0 = 15 (5 x 3)")


def _test_fibonacci():
    """fibonacci.asm: 7 iterations -> R1 = 21."""
    comp, state = _run_program("fibonacci")
    assert_eq(state["registers"]["R1"], 21, "fibonacci.asm documents R1 = 21 after 7 iterations")


def _test_conditional_loop():
    """conditional_loop.asm: countdown from 5 -> R0 = 0, stored at 0x20."""
    comp, state = _run_program("conditional_loop")
    assert_eq(state["registers"]["R0"], 0, "conditional_loop.asm counts R0 down to 0")
    assert_eq(_read_memory(comp, 0x20), 0, "conditional_loop.asm stores the final counter at address 0x20")
