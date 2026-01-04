; Add Two Numbers
; Adds 5 + 3 and stores result in R0
;
; Expected result: R0 = 8

    LOAD R1, 0x10    ; Load first number (5) from address 0x10
    LOAD R2, 0x11    ; Load second number (3) from address 0x11
    ADD R0, R1, R2   ; R0 = R1 + R2
    STORE R0, 0x12   ; Store result at address 0x12
    HALT

; Data section
.org 0x10
    .byte 5          ; First operand
    .byte 3          ; Second operand
