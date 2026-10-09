#!/usr/bin/env python3
"""Generate the student stub files in src/computer/ from solutions/.

The solution files are the single source of truth: docstrings, signatures,
class constants, and given helper code all live there. This script copies
each solution into src/computer/ and replaces the body of every *exercise*
function (listed in EXERCISES below) with a TODO comment and ``...``.

Usage:
    python scripts/generate_stubs.py            # rewrite src/computer/
    python scripts/generate_stubs.py --check    # verify stubs are up to date

Maintainers edit solutions/, then regenerate. CI runs --check so the stubs
can never drift from the solutions again.
"""

import argparse
import ast
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOLUTIONS = REPO / "solutions"
STUBS = REPO / "src" / "computer"

# module -> {qualified function name -> TODO hint shown in the stub body}
EXERCISES = {
    "gates": {
        "NOT": "Implement the NOT gate",
        "AND": "Implement the AND gate",
        "OR": "Implement the OR gate",
        "NAND": "Implement the NAND gate by composing AND and NOT",
        "NOR": "Implement the NOR gate by composing OR and NOT",
        "XOR": "Implement the XOR gate",
        "XNOR": "Implement the XNOR gate by composing XOR and NOT",
    },
    "combinational": {
        "mux_2to1": "Implement the 2-to-1 MUX using AND, OR, NOT gates",
        "mux_4to1": "Implement the 4-to-1 MUX using 2-to-1 MUXes",
        "mux_8to1": "Implement the 8-to-1 MUX",
        "demux_1to2": "Implement the 1-to-2 DEMUX",
        "demux_1to4": "Implement the 1-to-4 DEMUX",
        "decoder_2to4": "Implement the 2-to-4 decoder",
        "decoder_3to8": "Implement the 3-to-8 decoder",
        "encoder_4to2": "Implement the 4-to-2 priority encoder",
        "encoder_8to3": "Implement the 8-to-3 priority encoder",
    },
    "adders": {
        "half_adder": "Implement the half adder",
        "full_adder": "Implement the full adder using two half adders",
        "ripple_carry_adder_8bit": "Implement the 8-bit ripple carry adder",
        "subtractor_8bit": "Implement the 8-bit subtractor",
        "twos_complement": "Implement two's complement",
    },
    "alu": {
        "ALU.__call__": "Implement the ALU: dispatch on opcode, compute result and flags",
        "ALU._add": "Implement using ripple_carry_adder_8bit",
        "ALU._sub": "Implement using subtractor_8bit",
        "ALU._and": "Implement bitwise AND",
        "ALU._or": "Implement bitwise OR",
        "ALU._xor": "Implement bitwise XOR",
        "ALU._not": "Implement bitwise NOT",
        "ALU._shl": "Implement shift left (MSB becomes the carry)",
        "ALU._shr": "Implement shift right (LSB becomes the carry)",
        "ALU._calculate_flags": "Implement flag calculation (Z, C, N, V)",
    },
    "sequential": {
        "SRLatch.__call__": "Implement the SR latch using cross-coupled NOR gates",
        "GatedSRLatch.__call__": "Implement the gated SR latch",
        "DLatch.__call__": "Implement the D latch",
        "DFlipFlop.clock": "Implement the D flip-flop (edge-triggered)",
        "JKFlipFlop.clock": "Implement the JK flip-flop",
        "TFlipFlop.clock": "Implement using the JK flip-flop",
    },
    "registers": {
        "Register8.clock": "Implement the 8-bit register (one D flip-flop per bit)",
        "Register8.read": "Return the current values of all flip-flops",
        "RegisterFile.read": "Implement register read using the 3-bit address",
        "RegisterFile.write": "Implement register write",
    },
    "counters": {
        "BinaryCounter8.clock": "Implement the binary counter",
        "ProgramCounter.clock": "Implement the program counter",
    },
    "memory": {
        "RAM.read": "Implement memory read",
        "RAM.write": "Implement memory write (only when enable == 1)",
    },
    "clock": {
        "Clock.tick": "Implement the clock tick",
        "Clock.reset": "Implement the clock reset",
        "Clock.get_state": "Implement get_state",
        "ControlSignals.reset": "Reset every control signal to its default value",
        "ControlSignals.to_dict": "Implement to_dict for debugging",
    },
    "isa": {
        "encode_instruction": "Implement instruction encoding",
        "decode_instruction": "Implement instruction decoding",
        "disassemble": "Implement disassembly: turn 16 bits back into assembly text",
    },
    "decoder": {
        "InstructionDecoder.decode": "Implement instruction decoding",
        "InstructionDecoder.get_instruction_type": "Implement type detection",
    },
    "control": {
        "ControlUnit.generate_signals": "Implement control signal generation",
        "ControlUnit.next_state": "Implement the conceptual state machine",
    },
    "datapath": {
        "DataPath.execute_cycle": "Implement data path execution",
        "DataPath.fetch_instruction": "Implement instruction fetch",
        "DataPath.increment_pc": "Implement PC increment by 2",
    },
    "cpu": {
        "CPU.fetch": "Implement fetch",
        "CPU.decode": "Implement decode",
        "CPU.execute": "Implement execute",
        "CPU.step": "Implement a single fetch-decode-execute step",
        "CPU.run": "Implement the run loop",
    },
    "assembler": {
        "Assembler.assemble": "Implement the two-pass assembler",
        "Assembler.first_pass": "Implement the first pass (labels and directives)",
        "Assembler.second_pass": "Implement the second pass (machine code)",
        "Assembler.parse_line": "Implement line parsing",
    },
    "system": {
        "Computer.load_program": "Implement program loading (instructions AND the .byte data section)",
        "Computer.load_machine_code": "Implement machine code loading",
        "Computer.run": "Implement run with optional debug tracing (see trace_step)",
        "Computer.dump_state": "Implement the state dump",
        "Computer.dump_registers": "Implement the register dump",
    },
}

GENERATED_NOTE = (
    "# NOTE: Generated from solutions/{name} by scripts/generate_stubs.py.\n"
    "# Write your implementations in the '# TODO' bodies below.\n"
    "# (Maintainers: edit the solution file, not this one, then regenerate.)"
)


def find_functions(tree: ast.AST) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Map qualified name -> FunctionDef node."""
    found: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}

    def visit(node: ast.AST, prefix: str = "") -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found[prefix + child.name] = child
            elif isinstance(child, ast.ClassDef):
                visit(child, prefix + child.name + ".")

    visit(tree)
    return found


def module_docstring_end(tree: ast.Module) -> int:
    """Return the 1-based end line of the module docstring, or 0."""
    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        return tree.body[0].end_lineno or 0
    return 0


def stub_out(source: str, exercises: dict[str, str], note: str) -> str:
    """Replace exercise function bodies with TODO stubs and add the header note."""
    tree = ast.parse(source)
    lines = source.splitlines()
    functions = find_functions(tree)

    missing = [q for q in exercises if q not in functions]
    if missing:
        raise SystemExit(f"error: manifest entries not found in solution: {missing}")

    replacements = []
    for qualname, hint in exercises.items():
        node = functions[qualname]
        body = node.body
        # keep the docstring, replace everything after it
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            start = int(body[0].end_lineno or 0)  # 0-based index of first line after docstring
        else:
            start = body[0].lineno - 1
        indent = " " * body[0].col_offset
        replacements.append((start, int(node.end_lineno or 0), [f"{indent}# TODO: {hint}", f"{indent}..."]))

    for start, end, block in sorted(replacements, key=lambda r: -r[0]):
        lines[start:end] = block

    doc_end = module_docstring_end(tree)
    lines[doc_end:doc_end] = ["", *note.splitlines()]

    text = "\n".join(lines) + "\n"
    text = text.replace("from solutions.", "from computer.").replace("from solutions import", "from computer import")
    # collapse any triple blank lines the splices may have produced
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n", "\n\n\n")
    return text


def generate() -> dict[str, str]:
    """Return {relative path -> generated stub text} for all modules."""
    out = {}
    for sol_path in sorted(SOLUTIONS.glob("*.py")):
        name = sol_path.name
        exercises = EXERCISES.get(sol_path.stem, {})
        out[name] = stub_out(sol_path.read_text(), exercises, GENERATED_NOTE.format(name=name))
    return out


def main() -> int:
    """Generate stubs, or verify them with --check."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify stubs match the solutions without writing")
    args = parser.parse_args()

    generated = generate()
    stale = []
    for name, text in generated.items():
        target = STUBS / name
        if args.check:
            if not target.exists() or target.read_text() != text:
                stale.append(name)
        else:
            target.write_text(text)
            print(f"wrote src/computer/{name}")

    if args.check:
        if stale:
            print(f"error: stale stubs (run 'python scripts/generate_stubs.py'): {', '.join(stale)}")
            return 1
        print(f"all {len(generated)} stub files are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
