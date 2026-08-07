# Extensions: Where to Go After Notebook 16

You built a computer. Everything below makes it *more* of a computer. The challenges are roughly ordered by difficulty; each one says which layers you'll touch. There are no reference solutions for these - that's the point.

## Level 1: Write More Programs (no new hardware)

Warm up by programming the machine you already have. All of these fit in 256 bytes:

- **Maximum finder** - given values at `0x10`-`0x13`, leave the largest in R0. (You have no "compare" instruction - `SUB` + `JZ`/`JNZ` and some cleverness are enough.)
- **GCD** - Euclid's algorithm with repeated subtraction.
- **Memory copy** - copy N bytes from one address to another. You'll immediately feel the ISA's biggest limitation: `LOAD`/`STORE` take *fixed* addresses, so there's no way to index memory from a register. Write it as unrolled code, then read Level 3.
- **Triangle numbers** - compute 1+2+...+N; watch the carry flag when it overflows.

Run everything with `Computer.run(debug=True)` and read the trace. Debugging your own assembly with your own disassembler is the full-circle moment of this course.

## Level 2: Assembler Upgrades (software only)

The assembler is ordinary Python, so these need no new hardware:

- **Error messages with line numbers** - today, a bad register name silently becomes `R0`. Make `Assembler` collect errors (`self.errors` already exists) and report `line 7: unknown register 'R9'`.
- **Pseudo-instructions** - expand one source line into several real instructions in `first_pass`. Classic set:
  - `CLR Rd` → `XOR Rd, Rd, Rd`
  - `INC Rd` / `DEC Rd` → needs a register holding 1 - which leads straight to the calling-convention challenge below.
- **`.word` and `.string` directives** - multi-byte data. Decide on byte order and document it.
- **A memory annotator** - use `disassemble()` to print memory as code: every pair of bytes from 0 to the first `HALT`, one instruction per line. You've written two-thirds of a debugger.

## Level 3: Extend the ISA (the real design lesson)

Here's the catch: **all 16 opcodes are taken.** You cannot add an instruction without making room, and every way of making room is a real architecture trade-off:

1. **Steal encoding space.** `JMP`'s bits 11-8 are unused - they could select *sub-operations* (`JMP`, `JC`, `JV`, `CALL`...) turning opcode `1100` into a family. Cost: the decoder grows a second-level decode step.
2. **Retire an instruction.** Every ALU op earns its opcode - or does it? `MOV Rd, Rs` is exactly `OR Rd, Rs, Rs`; the assembler could expand it as a pseudo-instruction and free opcode `0011`. Decide what that costs (one extra register read per copy) and whether it's worth a free slot. Retiring `NOP` is tempting and wrong - find out why by single-stepping.
3. **Widen the instruction.** 24-bit instructions give you room forever and break *everything*: the fetch path, the PC increment, `load_machine_code`, the assembler. A great "feel the blast radius" exercise.

Good first additions once you've made room, in rising order of ambition:

- **`LOADI Rd, imm`** (load immediate) - today every constant must be planted in memory with `.byte`. This is the single most painful gap in the ISA; fixing it touches ISA → decoder → control → datapath → assembler → tests. Follow the checklist below.
- **`CMP Rs1, Rs2`** - the ALU has supported it since notebook 04 (`OP_CMP` sets flags, preserves A) and no instruction has ever used it. Wire it through.
- **`JC addr`** (jump if carry) - with `CMP`, this gives you real unsigned comparisons: `CMP a, b; JC a_less_than_b`.
- **Register-indirect `LOAD`/`STORE`** (`LOAD Rd, [Rs]`) - solves the memory-copy problem from Level 1 and is how real ISAs address arrays.

**The checklist for any new instruction** (this ordering keeps the checker useful at every step):

1. `solutions/isa.py` / `src/computer/isa.py`: opcode table, `encode_instruction`, `decode_instruction`, `disassemble`
2. `decoder.py`: field extraction for the new format (if any)
3. `control.py`: which signals does it assert?
4. `datapath.py`: any new routing (e.g. immediate → register file)
5. `assembler.py`: parse the new syntax
6. `utils/checker/tests/`: add tests *first*, watch them fail, make them pass
7. Write a program that needs the new instruction; add it to `programs/`

## Level 4: Bigger Machinery

- **A stack** - dedicate R7 as the stack pointer (a *convention*, no hardware needed). Implement `PUSH`/`POP` as pseudo-instructions... and discover you need register-indirect `STORE`/`LOAD` first (Level 3). Everything connects.
- **`CALL`/`RET`** - with a stack, subroutines are: push the return address, jump; pop, jump back. You'll need a way to get "the address after this instruction" - does that need hardware help? Design it.
- **Memory-mapped output** - declare address `0xFF` an output port: `STORE Rs, 0xFF` prints a character. One `if` in `RAM.write` (or better, a device hook in `Computer`), and suddenly your programs can talk. Hello, world.
- **Make the multi-cycle control real** - notebook 12's `next_state` machine is conceptual. Rebuild `CPU.step()` to call `generate_signals` once *per phase*, with the control unit asserting fetch signals in FETCH (`mem_read`, `ir_load`), execute signals in EXECUTE, and `pc_inc` in WRITEBACK. The tests in `utils/checker/tests/test_control.py` document the single-cycle contract - rewrite them to the multi-cycle one first.
- **De-cheat the simulation** - the README lists where plain Python stands in for hardware. Replace `RAM`'s Python list with a grid of your own D flip-flops plus your 3-to-8 decoders (256 bytes = 2,048 flip-flops; measure how much slower it runs - that's why simulators cheat). Replace the fetch path's Python `PC+1` with your ripple-carry adder.

## Level 5: Projects

- **A real debugger** - breakpoints (pause when PC hits an address), single-step, register/memory watch. `trace_step()` is your starting point.
- **A tiny compiler** - a language with variables and `while` loops, compiled to your assembly. Even 100 lines of Python compiling `a = a - 1` correctly will teach you more about compilers than a month of reading.
- **Fibonacci as fast as possible** - count cycles with the debug trace, then optimize: better code? A new instruction? This is computer architecture's whole job, in miniature.

---

*If you build something neat on top of this project, add a program to `programs/` and a test to `utils/checker/tests/test_programs.py` so it can never silently break.*
