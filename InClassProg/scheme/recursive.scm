; recursive scheme program in class - 02/24/2025

; bad way of doing factorial
; why its bad
(define (fac-bad n)
    (if (<= n 1) 1
        ; other recursive call to n - 1
        (* n (fac-bad (- n 1)))
    )
)

; recursive way that sums up to the nth Fibonacci term bad way
(define (fib-bad n)
    (if (< n 2) n
        (+ (fib-bad (- n 1)) (fib-bad (- n 2)))
    )
)

; tail recursive to sum up to nth Fibonacci term - good way
(define (fib-good n a b)
    (cond ((zero? n) a)
        ((= n 1) b)
        ((fib-good (- n 1) b (+ a b)))
    )
)

(define (sum-range-bad range)
    (if (zero? (length)) 0

    )
)

; non recursive tail call fcn
(define (sum-range-good range)
    (sum-range-iter range 0)
)

(dfine (sum-range-iter range acc)
    (if (zero? (length range)) acc
        (sum-range-iter (cdr range) (+ acc (car range)))
    )
)

; tail call recursion example
(define (fac-good n a)
    (if (<= n 1) a
        ; tail call because the parenthesis operations are step 1 then step 2
        ; then function call is last so its tail call recursion
        (fac-good (- n 1) (* n a))
    )
)

; notes from lecture class
; tail recursion, better way to do recursion
; tail call is a function in which where the last thing it does is call another function

; tail call function example
(define (print data)
    (display data)
    (display "\n")
)

(define num 10)
(define start 1)
(print (fib-good 5))