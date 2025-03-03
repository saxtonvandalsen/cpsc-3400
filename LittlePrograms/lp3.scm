; CPSC 3400-02 Languages & Computation
; Little Program 3
; Saxton Van Dalsen
; 3/2/2025

; I noted from class that we would need bit wise operators for this program and read through the
; "Nim" hyperlink to wiki page from Problem section in handout to better understand the game.
; "Game play and illustration", "Winning positions", "Mathematical theory", and "Proof of the winning formula"
; sections on the wikipedia page helped. As well as the GNU Guile Reference Manual

; To hold the value of n <= 2^30, which is 1073741824
(define n-limit 1073741824)

; Using output function, same as other little programs
(define (print_output)
    (display "Number of Nim Heap Configurations Where Current Player Wins: ") ; Prints the prompt
    ; Starting at 1 (positive integers), ending at 2^30, and set initial count to 0
    (display (count-num-wins 1 n-limit 0))
    (display "\n") ; Print on a new line
)

; Using nim-sum naming standard from the "Mathematical theory" and other relevant sections. Using the bitwise XOR
; heap of size 3. I found section 6.6.2.13 Bitwise Operations from within the GNU Guile Reference Manual. I'm using
; Scheme procedure "logxor" with 3 heaps h1, h2, h3
(define (nim-sum h1 h2 h3)
    ; Computing the bitwise XOR on number of objects in the heap sizes, 
    ; which will set bits to 1 if there are odd number of inputs of 1s
    (logxor h1 h2 h3)
)

; nim-win function based on the Problem description and defined parameters for heap size 3
; to check if the current player wins or not. Evaluating the nim-sum return value
(define (nim-win h1 h2 h3)
    ; If nim-sum call is 0 then the current player loses, we return zero. If not return 1
    (if (= (nim-sum h1 h2 h3) 0) 0 1)
)


; After trial and error and noting the Problem requirements I separated functions to count number of times
; where the current player wins for (n, 2n, 3n) where n <= 2^30. Remember needing to use a 
; tail recursive callback function and using this function to get the count for output
(define (count-num-wins n limit count)
    ; Base case reached when limit is hit and will return the count
    (if (> n limit) count
        ; Tail recursive callback where I increment n by 1 each call then
        ; update the count by adding the result of nim-win (n, 2n, 3n)
        (count-num-wins (+ n 1) limit (+ count (nim-win n (* 2 n) (* 3 n))))
    )
)

; Calling output function to print to the console
(print_output)