# Sample Assembly Programs

This directory contains example assembly programs that demonstrate the capabilities of the 8-bit computer.

## Programs

### add_two_numbers.asm
The simplest program - loads two numbers from memory, adds them, and stores the result.

**Expected result:** R0 = 8 (5 + 3)

### multiply.asm
Demonstrates multiplication through repeated addition.

**Expected result:** R0 = 15 (5 × 3)

### fibonacci.asm
Calculates Fibonacci sequence values and stores them in memory.

### conditional_loop.asm
Shows conditional branching and loops with memory writes.

## Running Programs

These programs can be assembled and run once you've completed notebooks 15 (Assembler) and 16 (Full System).

From notebook 16 or a Python script:
```python
from computer.assembler import Assembler
from computer.system import Computer

# Load and assemble
assembler = Assembler()
with open('../programs/add_two_numbers.asm') as f:
    program = assembler.assemble(f.read())

# Run on computer
computer = Computer()
computer.load_machine_code(program)
computer.run()

# Check results
state = computer.dump_state()
print(f"Result in R0: {state['registers']['R0']}")
```

## Instruction Set Reference

See the main README.md for the complete instruction set table.
