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
from computer.system import Computer

computer = Computer()
with open("../programs/add_two_numbers.asm") as f:
    computer.load_program(f.read())  # assembles code AND loads the .byte data section
computer.run()

# Check results
state = computer.dump_state()
print(f"Result in R0: {state['registers']['R0']}")
```

> **Important:** always use `Computer.load_program(source)` for assembly source.
> Calling `Assembler.assemble()` yourself and passing the result to
> `load_machine_code()` loads only the instructions - the `.byte` data section
> would be silently skipped, and programs that read their operands from memory
> would compute all zeros.

## Instruction Set Reference

See the main README.md for the complete instruction set table.
