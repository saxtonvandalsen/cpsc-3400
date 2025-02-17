; CPSC 3400-02 Languages & Computation
; Little Program 1
; Saxton Van Dalsen
; 2/15/2025

; I need a function to display the output
; and specifically make sure its on a new line
(define (print_output)
    (display "Sum of multiples of 3 or 5: ") ; Prints the prompt
    (display (sum-multiples-3-or-5 range)) ; Prints the return value of the function
    (display "\n") ; Print on a new line
)

; After getting the range of numbers needed below, I need to 
; define a function to recursively go through the range
; and sum up the multiples of 3 and 5.
; I realized I needed to split up the two recursive checks for
; divisibility by 3 or 5 into separate cond branches to handle each case
(define (sum-multiples-3-or-5 range)
    ; Base case using zero? to check if length of range is zero
    (cond ((zero? (length range)) 0)
        
        ; Checking if value is divisible by 3, if so then add to sum
        ((zero? (modulo (car range) 3)) (+ (car range) (sum-multiples-3-or-5 (cdr range))))
        
        ; Checking if value is divisible by 5, if so then add to sum
        ((zero? (modulo (car range) 5)) (+ (car range) (sum-multiples-3-or-5 (cdr range))))
        
        ; Else case ignore numbers that are not divisible by 3 or 5, move forward
        (else (sum-multiples-3-or-5 (cdr range)))
    )
)

; Using iota with specifically declared parameters
; that we learned in class to define the range of integers
; from 1 to 29,999 inclusive
; Defining num to 29999 for use
(define num 29999)
(define range (iota num 1))

; Calling the function to print the output to console
(print_output)