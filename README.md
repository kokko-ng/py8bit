# Build an 8-Bit Computer from Scratch

An educational project that teaches computer architecture by building a complete 8-bit computer in Python, from logic gates to running assembly programs.

## Overview

This project consists of 16 Jupyter notebooks, each building one layer of a computer:

1. **Logic Gates** - AND, OR, NOT, NAND, NOR, XOR, XNOR
2. **Combinational Circuits** - Multiplexers, Demultiplexers, Encoders, Decoders
3. **Adders** - Half Adder, Full Adder, 8-bit Ripple Carry Adder
4. **ALU** - Arithmetic Logic Unit with 9 operations
5. **Latches & Flip-Flops** - SR, D, JK, T flip-flops
6. **Registers** - 8-bit registers and register file
7. **Counters** - Binary counter, Program Counter
8. **Memory** - 256-byte RAM
9. **Clock & Control Signals** - Timing and control
10. **ISA** - Instruction Set Architecture (16 instructions)
11. **Instruction Decoder** - Decodes instructions
12. **Control Unit** - Generates control signals
13. **Data Path** - Connects all components
14. **CPU** - Fetch-Decode-Execute cycle
15. **Assembler** - Converts assembly to machine code
16. **Full System** - Complete computer

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Basic Python programming knowledge
- Understanding of binary (0s and 1s)

### Installation

```bash
# Clone or download the project
cd 8bit

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyter Notebook
jupyter notebook
```

This will open Jupyter in your browser. Navigate to the `notebooks/` folder and start with `01_logic_gates.ipynb`.

### Project Structure

```
8bit/
├── notebooks/           # 16 educational notebooks
├── src/computer/        # Student module stubs
├── solutions/           # Reference implementations
├── tests/               # Pytest validation tests
├── programs/            # Sample assembly programs
├── utils/               # Helper utilities
└── requirements.txt
```

## How to Use

### Step-by-Step Workflow

1. **Open notebooks in order** - Start with `01_logic_gates.ipynb`, then `02_combinational_circuits.ipynb`, etc.

2. **Read and learn** - Each notebook teaches you the theory with examples

3. **Complete exercises** - Write your code directly in the notebook cells

4. **Save to module** - Once your code works in the notebook, copy it to the corresponding file in `src/computer/`. For example:
   - From notebook: Copy your `AND()` function
   - To file: Paste into `src/computer/gates.py` (replacing the `...`)

5. **Validate** - Run the validation cell in the notebook:
   ```python
   from utils.checker import check
   check('gates')  # Tests your gates.py implementation
   ```

6. **Debug** - If tests fail, review the error messages and fix your code

7. **Get help if stuck** - Reference implementations are in the `solutions/` folder

## Checking Your Work

Each notebook includes a validation cell:

```python
from utils.checker import check
check('gates')  # Run tests for the gates module
```

This runs hidden tests that verify your implementation without revealing the test code.

## Sample Programs

The `programs/` folder contains example assembly programs:

- `add_two_numbers.asm` - Basic addition
- `fibonacci.asm` - Fibonacci sequence
- `multiply.asm` - Multiplication via repeated addition
- `conditional_loop.asm` - Count down with memory writes

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

## Design Decisions

- **Bit Representation**: Integers (0 or 1), not booleans
- **Byte Order**: LSB at index 0 (little-endian style)
- **Instruction Width**: 16 bits
- **Address Space**: 256 bytes (8-bit addressing)
- **Registers**: 8 general-purpose registers (R0-R7)

## Learning Path

### Phase 1: Foundation (Notebooks 1-3)
Build the basic building blocks: gates, routing circuits, and arithmetic.

### Phase 2: State & Storage (Notebooks 4-8)
Add memory elements: flip-flops, registers, counters, and RAM.

### Phase 3: Control (Notebooks 9-12)
Design the instruction set and control logic.

### Phase 4: Integration (Notebooks 13-16)
Connect everything and run real programs!

## Advanced: Running All Tests

The checker utility runs tests on individual components. If you want to test everything at once from the command line:

```bash
# Activate virtual environment
source .venv/bin/activate

# In a Python shell or script
python3 -c "from utils.checker import check_all; check_all()"
```

Alternatively, you can run pytest (though tests will fail for unimplemented components):

```bash
pytest
```

## License

MIT License - Feel free to use for education!

## Acknowledgments

Inspired by:
- "The Elements of Computing Systems" (Nand2Tetris)
- Ben Eater's 8-bit breadboard computer
- Classic computer architecture textbooks
