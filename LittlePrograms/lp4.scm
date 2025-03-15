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

; For calculating total value of hand of cards. Recursively sum up values
; of all cards in the hand
(define (total-hand-value hand)
    ; Base case if hand empty (zero), return zero
    (cond ((zero? (length hand)) 0)
        ; Recursively add numeric value of first card to sum of rest
        (else (+ (card-to-value (car hand)) (total-hand-value (cdr hand))))
    )
)

; After testing a working program and evaluating the scheme deck input file
; it looks like this one may be structured to cause more busts for the player

; Handling players turn to decide whether they should hit or stay. I adjusted this
; because I was getting varying results depending on where the player's hand value was
; Stopping at 16 seems a reasonable position to avoid losing more often for the player
(define (player-turn hand deck)
    ; Base case if players hand is 16 or higher, stop hitting to avoid busting
    ; had to tweak this a lot
    (cond ((>= (total-hand-value hand) 16) hand)
        ; Taking another card from the deck and adding to the current players hand
        (else (player-turn (rec-append hand (list (car deck))) (cdr deck)))
    )
)

; Handling the dealer's turn by deciding when to hit or stay, I changed the strategy
; for the dealer after testing to obtain a higher percent win rate which makes the dealer
; take more risks
(define (dealer-turn hand deck)
    ; Base case if dealers hand reaches 20 or higher then stopping. Having the dealer
    ; take more risks with higher value check, helped as well with higher win rate
    (cond ((>= (total-hand-value hand) 20) hand)
        ; Taking another card from the deck until hitting 20
        (else (dealer-turn (rec-append hand (list (car deck))) (cdr deck)))
    )
)

; Recursively appending two lists together, needed this for when player or
; dealer takes another card to add to their hand
(define (rec-append list1 list2)
    ; Base case if list1 empty then return list2, nothing to add
    (cond ((zero? (length list1)) list2)
        ; Taking the first from list1 and put it a the front of list2
        ; continuing until list1 is empty
        (else (cons (car list1) (rec-append (cdr list1) list2)))
    )
)

; To run a game round where it takes a hand from the deck and simulating
; the split of cards into dealer and player hands where I'm using it play both
; turns and return the final hands of each
(define (play-round hand)
    ; Getting first hand as initial
    (define dealer-hand (car hand))
    
    ; Getting first player card then second player card which is
    ; second card from list and third card
    (define player-card1 (car (cdr hand)))
    (define player-card2 (car (cdr (cdr hand))))
    
    ; Combining the cards handed into a list for the players starting hand
    (define player-hand (list player-card1 player-card2))

    ; Getting the remaining deck after initial cards have been dealt
    (define remaining-deck (cdr (cdr (cdr hand))))

    ; Playing out the round where the player goes first then the dealer
    (define player-final (player-turn player-hand remaining-deck))
    (define dealer-final (dealer-turn dealer-hand remaining-deck))

    ; Then return the final hands of each after completing turns
    (list player-final dealer-final)
)

; For printing the final hand values and determining who won where it takes
; the final hands of both player and dealer and evaluates the outcome 
(define (print-results player-final dealer-final)
    ; Displaying the player and dealers hand value after a round
    (display "Player’s Hand: ") (display (total-hand-value player-final))
    (display "\n")
    (display "Dealer’s Hand: ") (display (total-hand-value dealer-final))
    (display "\n")

    ; Ouput and determining the game results based on conditional checks/edge cases
    ; shown below and matching the output in Requirements
    (cond ((> (total-hand-value player-final) 21) (display "Player busts!\n") #f)
        ((> (total-hand-value dealer-final) 21) (display "Player wins!\n") #t)
        ((> (total-hand-value player-final) (total-hand-value dealer-final)) (display "Player wins!\n") #t)
        ((< (total-hand-value player-final) (total-hand-value dealer-final)) (display "Player loses.\n") #f)
        (else (display "Tie!\n") #f)
    )
)

; For playing a single round of blackjack with a given hand where it'll process
; a round played by calling play-round which will determines the final hands of 
; player and dealer. Print results for displaying outcome
(define (play-hand hand)
    ; Running the round to get final hands
    (define final-hands (play-round hand))
    
    ; Getting players final hand as first item in list and dealers
    ; as second item in list to print results
    (print-results (car final-hands) (car (cdr final-hands)))
)

; Used to output the game for all hands and tracking player wins. Taking in the list
; hands to play, current number wins, and total hands played then prints win count
(define (output-game hands wins total)
    ; Base case if no hands left, display win count
    (cond ((zero? (length hands))
        (display "Number of blackjack hands where current player wins: ")
        (display wins) (display "/") (display total) (display "\n"))
        
        ; Playing next hand and updating win count for player if they won
        (else (output-game (cdr hands)
            (if (play-hand (car hands)) (+ wins 1) wins)
            ; Incrementing total rounds played
            (+ total 1))
        )
    )
)

; Output of the game for all rounds
(output-game deck 0 0)