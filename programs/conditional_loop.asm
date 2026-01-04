; Conditional Loop - Count Down
; Counts down from 5 to 0, demonstrating loops and conditionals
;
; Note: Our ISA uses immediate addresses for STORE, not registers.
; This program demonstrates the countdown in registers.
;
; Registers:
;   R0 = counter (counts down from 5 to 0)
;   R1 = decrement constant (1)
;
; Expected: R0 = 0 when done, loop executes 5 times

    LOAD R0, start    ; R0 = 5 (counter)
    LOAD R1, one      ; R1 = 1 (for decrementing)

loop:
    SUB R0, R0, R1    ; Decrement counter
    JNZ loop          ; Loop while counter != 0

    ; Final result: R0 = 0
    STORE R0, 0x20    ; Store final value at fixed address
    HALT

start:
    .byte 5           ; Starting count value
one:
    .byte 1
