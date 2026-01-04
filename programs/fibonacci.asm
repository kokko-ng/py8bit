; Fibonacci Sequence Generator
; Computes Fibonacci numbers: F(n) = F(n-1) + F(n-2)
;
; Registers:
;   R0 = F(n-2), starts at 0
;   R1 = F(n-1), starts at 1
;   R2 = counter
;   R3 = decrement constant (1)
;   R4 = temp for F(n)
;
; Expected final R1: 21 (after 7 iterations: 0,1,1,2,3,5,8,13,21)

    LOAD R0, zero    ; R0 = 0 (F0)
    LOAD R1, one     ; R1 = 1 (F1)
    LOAD R2, count   ; R2 = 7 (iterations)
    LOAD R3, one     ; R3 = 1 (for decrementing)

loop:
    ADD R4, R0, R1   ; R4 = F(n) = F(n-2) + F(n-1)
    MOV R0, R1       ; Shift: R0 = old F(n-1)
    MOV R1, R4       ; Shift: R1 = new F(n)
    SUB R2, R2, R3   ; Decrement counter by 1
    JNZ loop         ; Continue if counter != 0
    HALT

zero:
    .byte 0
one:
    .byte 1
count:
    .byte 7
