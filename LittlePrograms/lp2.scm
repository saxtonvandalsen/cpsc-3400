; CPSC 3400-02 Languages & Computation
; Little Program 2
; Saxton Van Dalsen
; 2//2025

; Using the same output function that I created in lp1
; to produce the output and return value of the sum
; of even fibonacci numbers
(define (print_output)
    (display "Sum of Even Fibonacci Numbers: ") ; Prints the prompt
    
    ; Calls and prints function with specifically starting
    ; parameters 1 and 2 and sum argument is initialized as 0
    (display (sum-even-fibonacci 1 2 0))
    (display "\n") ; Print on a new line
)

; Need to define and implement a function to get the sum of
; all even integers in Fibonacci sequence recursively
; Using f0, f1, and sum as my parameters
(define (sum-even-fibonacci f0 f1 sum)
    ; Base case checking to make sure it stops before 1 billion
    (cond ((>= f1 1000000000) sum)

        ; Checking if current number is even first, if so add f1 to the sum and 
        ; make the recursive call. Then updating f0 and f1 to the next Fibonacci number
        ((zero? (modulo f1 2)) (sum-even-fibonacci f1 (+ f0 f1) (+ sum f1)))

        ; If not then move forward with recursion without adding to the sum
        (else (sum-even-fibonacci f1 (+ f0 f1) sum))
    )
)

; Calling the function to print the output to console
(print_output)