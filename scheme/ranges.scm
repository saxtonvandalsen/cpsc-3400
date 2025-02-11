; Ask the user for an integer as the max for a range of numbers
; Sum up total values of all numbers in the range
; recursively walk through this to sum up the number

(define (print_data)
    (display data) ;prints
    (display "\n")
)

; Understanding cdr and car below:
; (define l (1 2 3 4 5))
; (car l) -> 1
; (cdr l) -> (2 3 4 5)

; helpful for little programs
; (cdr (cdr l)) -> (3 4 5)

(define (sum-range range)
    ; base case, if length of range is zero
    ; returns zero if so
    (if (zero? (length range)) 0

    ; car is the head of the list (first element of the list)
    ; cdr is everything else other than the first item
    (+ (sum-range (cdr range)) (car range))
    )
)

;(cond (case 1)
;      (case 2)
;      (else)
;)

(define (sum-even-range range)
    (cond ((zero? (length range)) 0)
        ((zero? (modulo (car range) 2)) (+ (sum-even-range (cdr range)) (car range))
        (else (+ sum-even-range (cdr range)) 0))
    )
)

(define (sum-odd-range range)
    (cond ((zero? (length range)) 0)
        ((zero? (modulo (car range) 2)) (+ (sum-odd-range (cdr range)) 0))
        (else (+ sum-odd-range (cdr range)) 0)
    )
)

; function named "input" with parameter "prompt"
(define (input prompt)
    (display prompt)
    (read)
)

; function "num" equal to value of what input returns
(define num (input "Provide a number: "))

; iota parameters below:
; (iota count start stop)
; num is count, 1 is start
(define range (iota num 1))

(print (sum-range range))
(print (sum-even-range range))
(print (sum-odd-range range))