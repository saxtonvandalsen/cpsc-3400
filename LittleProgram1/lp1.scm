; CPSC 3400-02 Languages & Computation
; Little Program 1
; Saxton Van Dalsen
; 2/15/2025

; I need a function to display the output
; and specifically make sure its on a new line
(define (print_output)
    (display "") ; prints the prompt
    (display data) ; prints the output
    (display "\n") ; print on a new line
)

;


; Using iota with specifically declared parameters
; that we learned in class to define the range of integers
; from 1 to 29,999 inclusive
(define range (iota num 1 29999))