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

; After getting the range of numbers needed, I need to 
; define a function to recursively iterate through the range
; and sum up the multiples of 3 and 5
(define (sum-multiples-3-and-5 range)
    ; base case using zero? to check if length of range is zero
    (cond ((zero? (length range)) 0)
        
    )
)


; Using iota with specifically declared parameters
; that we learned in class to define the range of integers
; from 1 to 29,999 inclusive
; Defining num to 29999 for use
(define num 29999)
(define range (iota num 1))