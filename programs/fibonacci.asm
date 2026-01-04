; Fibonacci Sequence Generator
; Generates first 10 Fibonacci numbers in registers
;
; F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)
; Expected: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

    MOV R0, R0       ; R0 = 0 (F0)
    LOAD R1, one     ; R1 = 1 (F1)
    LOAD R2, count   ; R2 = counter (8 more iterations)

loop:
    ADD R3, R0, R1   ; R3 = F(n-2) + F(n-1)
    MOV R0, R1       ; Shift: R0 = old R1
    MOV R1, R3       ; Shift: R1 = new value
    SUB R2, R2, R1   ; Decrement counter (using R1 which is now >= 1)
    JNZ loop         ; Continue if counter != 0
    HALT

one:
    .byte 1
count:
    .byte 8
