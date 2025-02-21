; CPSC 3400-02 Languages & Computation
; Little Program 2
; Saxton Van Dalsen
; 2/21/2025

; Using the same output function that I created in lp1
; to produce the output but modified to print the sum of
; even numbers in Fibonacci sequence
(define (print_output)
    (display "Sum of Even Fibonacci Numbers: ") ; Prints the prompt
    
    ; Calls and prints function with specifically starting with first
    ; two terms 1 and 2, as stated in Problem, and setting sum argument to 0
    (display (sum-even-fibonacci 1 2 0))
    (display "\n") ; Print on a new line
)

; Need to define and implement a function to get the sum of
; all even integers in Fibonacci sequence recursively
; Using f0, f1, and sum as my parameters
(define (sum-even-fibonacci f0 f1 sum)
    ; Base case checking to make sure it stops before 1 billion
    ; specifically checking if current number (f1) is greater than or equal to 1 billion
    (cond ((>= f1 1000000000) sum)

        ; Checking if current number is even first, if so move to the recursive call
        ; where we update and move forward current number (f1) then adding it to the overall sum
        ((zero? (modulo f1 2)) (sum-even-fibonacci f1 (+ f0 f1) (+ sum f1)))

        ; If f1 is odd instead then recursive call without adding to sum
        ; and update f0 and f1 argument positions to the next Fibonacci number
        (else (sum-even-fibonacci f1 (+ f0 f1) sum))
    )
)

; Calling output function to print to the console
(print_output)