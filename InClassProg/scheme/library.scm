(define (print data)
    (display "From library.scm:")
    (newline)
    (display data)
    (newline)
)

(define (input prompt)
    (display prompt)
    (read)
)

(load "test.scm")
(print test)

; (define test "TEST")