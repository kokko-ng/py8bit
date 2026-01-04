; Conditional Loop - Count Down
; Counts down from 10 to 0, storing each value in memory
;
; Demonstrates: loops, conditionals, memory writes

    LOAD R0, start    ; R0 = 10 (counter)
    LOAD R1, addr     ; R1 = starting memory address (0x20)
    LOAD R3, one      ; R3 = 1 (for decrementing)

loop:
    STORE R0, R1      ; Store current count at address
    ADD R1, R1, R3    ; Increment address pointer
    SUB R0, R0, R3    ; Decrement counter
    JNZ loop          ; Loop while counter != 0

    ; Store final 0
    STORE R0, R1
    HALT

start:
    .byte 10          ; Starting count value
addr:
    .byte 0x20        ; Starting address for output
one:
    .byte 1

; Output will be stored at addresses 0x20-0x2A:
; 0x20: 10
; 0x21: 9
; 0x22: 8
; ...
; 0x2A: 0
