# Build an 8-Bit Computer from Scratch

An educational project that teaches computer architecture by building a complete 8-bit computer in Python, from logic gates to running assembly programs.

## Overview

This project consists of 16 Jupyter notebooks, each building one layer of a computer:

1. **Logic Gates** - AND, OR, NOT, NAND, NOR, XOR, XNOR
2. **Combinational Circuits** - Multiplexers, Demultiplexers, Encoders, Decoders
3. **Adders** - Half Adder, Full Adder, 8-bit Ripple Carry Adder
4. **ALU** - Arithmetic Logic Unit with 9 operations and status flags
5. **Latches & Flip-Flops** - SR, D, JK, T flip-flops
6. **Registers** - 8-bit registers and register file
7. **Counters** - Binary counter, Program Counter
8. **Memory** - 256-byte RAM
9. **Clock & Control Signals** - Timing and control
10. **ISA** - Instruction Set Architecture (16 instructions) + disassembler
11. **Instruction Decoder** - Decodes instructions
12. **Control Unit** - Generates control signals
13. **Data Path** - Connects all components
14. **CPU** - Fetch-Decode-Execute cycle
15. **Assembler** - Converts assembly to machine code
16. **Full System** - Complete computer with debug tracing

Done with all 16? [EXTENSIONS.md](EXTENSIONS.md) has a ladder of follow-on challenges.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Basic Python programming knowledge

### Installation

```bash
# Clone or download the project
cd py8bit

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
python -m pip install -r requirements.txt

# Start Jupyter Notebook
jupyter notebook
```

Open `notebooks/01_logic_gates.ipynb` and work through the notebooks in order.

## How the Course Works

Each notebook teaches the theory; your implementations live in the module files under `src/computer/`. The loop looks like this:

1. **Read** the notebook's explanation of a component.
2. **Implement** it in the matching file (the notebook links to it, e.g. `src/computer/gates.py`). Every function has a docstring spec and a `# TODO` marking where your code goes.
3. **Experiment** by running the notebook cells - they import your code, and the `%autoreload` magic in each setup cell picks up your saved edits automatically. No copying code between notebook and file.
4. **Validate** with the checker cell at the end of the notebook:

   ```python
   from utils.checker import check

   check("gates")  # test the whole module
   check("gates", "NAND")  # test one exercise
   check("gates", verbose=True)  # extra hints
   ```

### Tracking Progress

```python
from utils.checker import progress

progress()  # per-notebook [x]/[ ] table for the whole course
```

Or from the command line (great for a quick status check without Jupyter):

```bash
python -m utils.checker              # run every test, exit code 0/1
python -m utils.checker gates        # one component
python -m utils.checker --progress   # the progress table
```

### Stuck? The Solutions Policy

Reference solutions for every module live in `solutions/`. They're part of the repo on purpose - but you'll learn the most if you treat them as a last resort:

1. Re-read the docstring spec and the failing test's message first (the checker prints exactly what was expected).
2. Struggle for a while - that's where the learning is. 30 minutes is a reasonable budget.
3. Then peek at the *one* function you're stuck on, understand it, close the file, and write your own version.

If a module is blocking you and you want to keep moving, install its reference solution and come back later:

```bash
python scripts/install_solutions.py alu     # unblock one module
python scripts/install_solutions.py --all   # fully solved tree
git checkout -- src/computer                # restore your own committed code
```

## Project Structure

```
py8bit/
├── notebooks/           # 16 teaching notebooks (theory + experiments + validation)
├── src/computer/        # YOUR implementations - generated exercise stubs
├── solutions/           # Reference solutions (single source of truth)
├── programs/            # Sample assembly programs
├── scripts/             # generate_stubs.py, install_solutions.py
├── utils/checker/       # Test runner: check(), check_all(), progress()
└── requirements.txt
```

## Sample Programs

The `programs/` folder contains example assembly programs, all runnable in notebook 16:

- `add_two_numbers.asm` - Basic addition (R0 = 8)
- `multiply.asm` - Multiplication via repeated addition (R0 = 15)
- `fibonacci.asm` - Fibonacci sequence (R1 = 21)
- `conditional_loop.asm` - Count down with memory writes (R0 = 0)

See `programs/README.md` for how to load and run them - in short, always use `Computer.load_program(source)`, which loads both the instructions and the `.byte` data section. `Computer.run(debug=True)` prints a per-instruction trace (PC, disassembled instruction, register changes).

## Instruction Set

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| 0000 | NOP | No operation |
| 0001 | LOAD Rd, addr | Load from memory |
| 0010 | STORE Rs, addr | Store to memory |
| 0011 | MOV Rd, Rs | Copy register |
| 0100 | ADD Rd, Rs1, Rs2 | Add |
| 0101 | SUB Rd, Rs1, Rs2 | Subtract |
| 0110 | AND Rd, Rs1, Rs2 | Bitwise AND |
| 0111 | OR Rd, Rs1, Rs2 | Bitwise OR |
| 1000 | XOR Rd, Rs1, Rs2 | Bitwise XOR |
| 1001 | NOT Rd, Rs | Bitwise NOT |
| 1010 | SHL Rd, Rs | Shift left |
| 1011 | SHR Rd, Rs | Shift right |
| 1100 | JMP addr | Unconditional jump |
| 1101 | JZ addr | Jump if zero |
| 1110 | JNZ addr | Jump if not zero |
| 1111 | HALT | Stop execution |

Instruction formats (16 bits, opcode in bits 15-12):

```
R-type (ALU ops):   [opcode:4][rd:4][rs1:4][rs2:4]
I-type (LOAD/STORE):[opcode:4][rd:4][address:8]
J-type (jumps):     [opcode:4][unused:4][address:8]
```

## Conventions & Design Decisions

- **Bit representation**: integers (0 or 1), not booleans
- **LSB at index 0**: 8-bit values are lists with the least significant bit first - decimal 5 is `[1, 0, 1, 0, 0, 0, 0, 0]`. `int_to_bits` / `bits_to_int` convert; `bits_to_bin` prints MSB-first for humans
- **Instruction width**: 16 bits (2 bytes per instruction; the PC advances by 2)
- **Address space**: 256 bytes (8-bit addressing)
- **Registers**: 8 general-purpose registers (R0-R7)

### Where the Simulation Cheats

The point of this project is building logic from gates up - registers really are made of your D flip-flops, and the ALU really computes through your ripple-carry adder. In a few places we deliberately use plain Python instead, purely as plumbing: RAM stores bit-lists in a Python list rather than 2,048 flip-flops, the fetch path computes PC+1 with Python arithmetic, and the assembler/loader are ordinary Python programs (as real assemblers are). [EXTENSIONS.md](EXTENSIONS.md) lists "de-cheating" these as challenges.

## Learning Path

### Phase 1: Foundation (Notebooks 1-3)
Build the basic building blocks: gates, routing circuits, and arithmetic.

### Phase 2: State & Storage (Notebooks 4-8)
Add memory elements: flip-flops, registers, counters, and RAM.

### Phase 3: Control (Notebooks 9-12)
Design the instruction set and control logic.

### Phase 4: Integration (Notebooks 13-16)
Connect everything and run real programs!

## For Maintainers

The solution files are the single source of truth. The stubs in `src/computer/` are **generated**:

```bash
python scripts/generate_stubs.py           # regenerate stubs after editing solutions/
python scripts/generate_stubs.py --check   # CI freshness check
```

Install the git hooks once per clone:

```bash
pip install pre-commit
pre-commit install   # installs the pre-commit and commit-msg hooks
```

They run ruff, mypy (strict), the stub freshness check, gitleaks and file hygiene checks on every commit, and commitizen enforces [Conventional Commit](https://www.conventionalcommits.org/) messages (`feat: ...`, `fix: ...`, `docs: ...`).

CI (GitHub Actions) runs the same hooks on all files, checks every commit message, runs the full test suite against the solutions (including assembling and running every sample program), and executes all 16 notebooks headlessly.

## License

MIT License - Feel free to use for education!

## Acknowledgments

Inspired by:
- Sebastian Lague's videos on how computers work
- Ben Eater's series on creating an 8-bit computer from scratch
- Turing Complete for the gamified approach inspiration
