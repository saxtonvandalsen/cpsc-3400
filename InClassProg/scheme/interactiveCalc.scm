(define (print data)
    (display data)
    (display "\n")
)
# |
- last line is return value
- "op" on line 16 is a variable, doesn't need paranthesis
- also can comment with semi colon at beginning of line
| #

(define (input prompt)
    (display prompt)
    (read)
)

(define op (input "Prompt an operation: "))
(define x (input "Provie a number: "))
(define y (input "Provie a number: "))

(cond ((equal? op "+") (print + x y)))
    ((equal? op "-") (print (- x y)))
    ((equal? op "*") (print (* x y)))
    ((equal? op "/") (print (/ x y)))
    ((equal? op "%") (print (modulo x y)))
    (else (print "Invalid operation.")
)

;(print (+ x y))