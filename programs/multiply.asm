; Multiplication via Repeated Addition
; Multiplies two numbers using repeated addition
;
; Algorithm: result = 0; while(b > 0) { result += a; b--; }
; Example: 5 * 3 = 15

    LOAD R1, num_a    ; R1 = first operand (5)
    LOAD R2, num_b    ; R2 = second operand (3)
    MOV R0, R0        ; R0 = 0 (result accumulator)
    LOAD R3, one      ; R3 = 1 (for decrementing)

loop:
    ADD R0, R0, R1    ; result += a
    SUB R2, R2, R3    ; b--
    JNZ loop          ; continue while b != 0

    STORE R0, result  ; Store final result
    HALT

num_a:
    .byte 5           ; First operand
num_b:
    .byte 3           ; Second operand
one:
    .byte 1
result:
    .byte 0           ; Result will be stored here
