; CPSC 3400-02 Languages & Computation
; Little Program 4
; Saxton Van Dalsen
; 3/16/2025

; Load deck.scm file
(load "deck.scm")

; Convert two character string representing a card to its numerical value
; Three functions to make this work, learned this in class
; 1. (substring str start-pos end-pos)
; 2. (string-ci=? str1 str2) --> #t, #f | ci means case insensitive; are two strings equivalent
; 3. (string->number str) --> numeric value
(define (card-to-value card)
    ; no recursion here
    (define rank (substring card 0 1))
    (cond ((string-ci=? rank "A") 1)
        ((string-ci=? rank "J") 10)
        ((string-ci=? rank "Q") 10)
        ((string-ci=? rank "K") 10)
        ((string-ci=? rank "T") 10)
    (else (string->number rank))
    )
)

(define (total-hand-value hand)
    (if (zero? hand)
        (+ (total-hand-value (car range)) (total-hand-value (cdr hand)))
    )
)

