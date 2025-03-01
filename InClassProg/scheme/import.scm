; load is import + execute. It will invoke the print in library.scm
(load "library.scm")

(define (print data)
    (display "From import.scm")
    (newline)
    (display data)
    (newline)
)

; overrides here, check this later
; (load "library.scm")

(print test)