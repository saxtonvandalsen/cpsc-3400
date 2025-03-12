; In class programming before little program 4
; Assume value of Aces are 1 in Little Program 4

(define (sum-cards cards)
    ; (print cards)
    (if (zero? (length cards)) 0
        (+ (sum-cards (cdr cards)) (card-to-value (car cards)))
    )
)

; Convert two character string representing a card to its numerical value
; Three functions to make this work
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

(define (print data)
    (display data)
    (display "\n")
)

(define cards (list "9C" "AS" "AH" "TS" "AD" "8D" "7D" "QC" "JD" "KD" "AS"))
(print (sum-cards cards))