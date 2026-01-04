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

- Python 3.10+
- Jupyter Notebook

### Installation

```bash
# Clone or download the project
cd 8bit

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter notebook
```

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

1. Open notebooks in order (01, 02, 03...)
2. Read the theory and examples
3. Complete the exercises in each notebook
4. Copy your implementations to `src/computer/`
5. Run `check('component_name')` to validate
6. If stuck, reference the `solutions/` folder

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

## Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run tests for a specific component
pytest tests/test_gates.py -v
```

## License

MIT License - Feel free to use for education!

## Acknowledgments

Inspired by:
- "The Elements of Computing Systems" (Nand2Tetris)
- Ben Eater's 8-bit breadboard computer
- Classic computer architecture textbooks
